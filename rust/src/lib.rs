//! Primary entry points and the uniform result type they all return.
//!
//! Every public entry point has the same shape — data in, [`Report`] out — so
//! that everything which consumes a result (serialization, comparison,
//! plotting) is written once and works for every summary.
//!
//! Lints for the crate live in the `[lints]` table of `Cargo.toml`, so
//! `cargo clippy` behaves the same here as it does in CI.

use std::collections::BTreeMap;
use std::error::Error as StdError;
use std::fmt;

pub mod utils;

pub use utils::{describe, normalize, trim};

/// Errors returned by the public entry points.
///
/// # Examples
///
/// ```
/// use docsforge::{summarize, Error, Options};
///
/// assert_eq!(summarize(&[], &Options::default()), Err(Error::Empty));
/// ```
#[derive(Debug, Clone, PartialEq)]
pub enum Error {
    /// The input contained no observations.
    Empty,
    /// An observation was not finite (NaN or infinite).
    NotFinite(f64),
    /// The trim fraction was outside `[0, 0.5)`.
    InvalidTrim(f64),
}

impl fmt::Display for Error {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Empty => write!(f, "expected at least one value; got 0"),
            Self::NotFinite(value) => write!(f, "values must be finite; got {value}"),
            Self::InvalidTrim(fraction) => {
                write!(f, "fraction must be in [0, 0.5); got {fraction}")
            }
        }
    }
}

impl StdError for Error {}

/// A summary of one series, carrying its own provenance.
///
/// A `Report` is immutable and self-describing: because `options` travels
/// with the numbers, a result read back from disk can always be traced to the
/// settings that produced it.
///
/// # Examples
///
/// ```
/// use std::collections::BTreeMap;
///
/// use docsforge::Report;
///
/// let report = Report {
///     label: Some("demo".to_owned()),
///     mean: 2.8,
///     spread: 4.0,
///     n: 5,
///     options: BTreeMap::new(),
/// };
/// assert_eq!(report.to_row()["label"], "demo");
/// ```
#[derive(Debug, Clone, PartialEq)]
pub struct Report {
    /// Human-readable name, propagated into comparison tables and plots.
    pub label: Option<String>,
    /// The central estimate.
    pub mean: f64,
    /// Dispersion of the input, measured as `max - min`.
    pub spread: f64,
    /// Number of observations actually used, *after* any trimming.
    pub n: usize,
    /// The normalized options this result was produced with.
    pub options: BTreeMap<String, f64>,
}

impl Report {
    /// Return a flat, string-keyed mapping of the reported figures.
    ///
    /// Keys `label`, `mean`, `spread`, and `n`. Suitable for a plain CSV
    /// writer or `format!`-based printing.
    ///
    /// # Examples
    ///
    /// ```
    /// use docsforge::{summarize, Options};
    ///
    /// let report = summarize(&[1.0, 2.0, 3.0], &Options::default())?;
    /// let row = report.to_row();
    /// assert_eq!(row["mean"], "2");
    /// assert_eq!(row["n"], "3");
    /// # Ok::<(), docsforge::Error>(())
    /// ```
    pub fn to_row(&self) -> BTreeMap<String, String> {
        BTreeMap::from([
            ("label".to_owned(), self.label.clone().unwrap_or_default()),
            ("mean".to_owned(), self.mean.to_string()),
            ("spread".to_owned(), self.spread.to_string()),
            ("n".to_owned(), self.n.to_string()),
        ])
    }
}

/// Options shared by [`summarize`] and [`compare`].
///
/// Passing one `Options` to [`compare`] is what makes the comparison fair —
/// it is not possible to accidentally trim one series and not another.
///
/// # Examples
///
/// ```
/// use docsforge::Options;
///
/// let options = Options { trim: 0.1, ..Options::default() };
/// assert_eq!(options.precision, 6);
/// ```
#[derive(Debug, Clone, PartialEq)]
pub struct Options {
    /// Name carried into tables and plots.
    pub label: Option<String>,
    /// Fraction dropped from *each* tail before averaging, in `[0, 0.5)`.
    pub trim: f64,
    /// Decimal places applied to the reported figures.
    pub precision: i32,
}

impl Default for Options {
    fn default() -> Self {
        Self {
            label: None,
            trim: 0.0,
            precision: 6,
        }
    }
}

/// Summarize one series.
///
/// # Errors
///
/// Returns [`Error::Empty`] if `values` is empty, [`Error::NotFinite`] if a
/// value is not finite, and [`Error::InvalidTrim`] if `options.trim` is
/// outside `[0, 0.5)`.
///
/// # Examples
///
/// ```
/// use docsforge::{summarize, Options};
///
/// let options = Options { label: Some("demo".to_owned()), ..Options::default() };
/// let report = summarize(&[3.0, 1.0, 4.0, 1.0, 5.0], &options)?;
/// assert!((report.mean - 2.8).abs() < 1e-12);
///
/// let trimmed = Options { trim: 0.2, ..Options::default() };
/// assert_eq!(summarize(&[3.0, 1.0, 4.0, 1.0, 5.0], &trimmed)?.n, 3);
/// # Ok::<(), docsforge::Error>(())
/// ```
pub fn summarize(values: &[f64], options: &Options) -> Result<Report, Error> {
    let observations = trim(&normalize(values)?, options.trim)?;

    let mean = observations.iter().sum::<f64>() / observations.len() as f64;
    let min = observations.iter().fold(f64::INFINITY, |a, &b| a.min(b));
    let max = observations
        .iter()
        .fold(f64::NEG_INFINITY, |a, &b| a.max(b));

    let provenance = BTreeMap::from([
        ("trim".to_owned(), options.trim),
        ("precision".to_owned(), f64::from(options.precision)),
    ]);

    Ok(Report {
        label: options.label.clone(),
        mean: round_to(mean, options.precision),
        spread: round_to(max - min, options.precision),
        n: observations.len(),
        options: provenance,
    })
}

/// Summarize several series under identical options.
///
/// Series are summarized in slice order, so the output is stable across runs
/// and safe to snapshot in a test.
///
/// # Errors
///
/// Returns the first [`Error`] produced by [`summarize`].
///
/// # Examples
///
/// ```
/// use docsforge::{compare, Options};
///
/// let series = [("a", &[1.0, 2.0, 3.0][..]), ("b", &[2.0, 4.0, 6.0][..])];
/// let table = compare(&series, &Options::default())?;
/// let means: Vec<f64> = table.iter().map(|report| report.mean).collect();
/// assert_eq!(means, [2.0, 4.0]);
/// # Ok::<(), docsforge::Error>(())
/// ```
pub fn compare(series: &[(&str, &[f64])], options: &Options) -> Result<Vec<Report>, Error> {
    series
        .iter()
        .map(|(label, values)| {
            summarize(
                values,
                &Options {
                    label: Some((*label).to_owned()),
                    ..options.clone()
                },
            )
        })
        .collect()
}

/// Round `value` to `precision` decimal places.
fn round_to(value: f64, precision: i32) -> f64 {
    let factor = 10f64.powi(precision);
    (value * factor).round() / factor
}
