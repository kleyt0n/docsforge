//! Small, composable helpers shared by the built-in summaries.
//!
//! These are public on purpose: anyone writing their own summary should be
//! able to reuse the parts that are easy to get subtly wrong, rather than
//! reimplementing them.

use std::collections::BTreeMap;

use crate::{Error, Report};

/// Validate a series into a vector of usable observations.
///
/// Validation happens once, at the public boundary, so that internal helpers
/// may assume valid input and errors point at the argument the caller passed.
///
/// # Errors
///
/// Returns [`Error::Empty`] if `values` is empty and [`Error::NotFinite`] if
/// a value is NaN or infinite.
///
/// # Examples
///
/// ```
/// use docsforge::normalize;
///
/// assert_eq!(normalize(&[3.0, 1.0, 4.0]), Ok(vec![3.0, 1.0, 4.0]));
/// ```
pub fn normalize(values: &[f64]) -> Result<Vec<f64>, Error> {
    if values.is_empty() {
        return Err(Error::Empty);
    }
    for &value in values {
        if !value.is_finite() {
            return Err(Error::NotFinite(value));
        }
    }
    Ok(values.to_vec())
}

/// Drop `fraction` of the observations from each tail.
///
/// Uses the standard convention: `k = floor(fraction * n)` values are removed
/// from each end of the sorted input.
///
/// # Errors
///
/// Returns [`Error::InvalidTrim`] if `fraction` is outside `[0, 0.5)`.
///
/// # Examples
///
/// ```
/// use docsforge::trim;
///
/// assert_eq!(trim(&[3.0, 1.0, 4.0, 1.0, 5.0], 0.2), Ok(vec![1.0, 3.0, 4.0]));
/// ```
pub fn trim(values: &[f64], fraction: f64) -> Result<Vec<f64>, Error> {
    if !(0.0..0.5).contains(&fraction) {
        return Err(Error::InvalidTrim(fraction));
    }
    if fraction == 0.0 {
        return Ok(values.to_vec());
    }

    let mut ordered = values.to_vec();
    ordered.sort_by(f64::total_cmp);
    let k = (fraction * ordered.len() as f64).floor() as usize;
    Ok(ordered[k..ordered.len() - k].to_vec())
}

/// Turn reports into printable rows.
///
/// # Examples
///
/// ```
/// use docsforge::{compare, describe, Options};
///
/// let series = [("a", &[1.0, 2.0, 3.0][..])];
/// let rows = describe(&compare(&series, &Options::default())?);
/// assert_eq!(rows[0]["label"], "a");
/// assert_eq!(rows[0]["n"], "3");
/// # Ok::<(), docsforge::Error>(())
/// ```
pub fn describe(reports: &[Report]) -> Vec<BTreeMap<String, String>> {
    reports.iter().map(Report::to_row).collect()
}
