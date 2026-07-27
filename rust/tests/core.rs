//! Tests for the demo crate.
//!
//! They exist mainly to prove the CI pipeline in this template works end to
//! end. Replace them along with `rust/src/`.

use std::collections::BTreeMap;

use docsforge::{compare, describe, normalize, summarize, trim, Error, Options};

#[test]
fn summarize_reports_mean_and_spread() {
    let options = Options {
        label: Some("demo".to_owned()),
        ..Options::default()
    };
    let report = summarize(&[3.0, 1.0, 4.0, 1.0, 5.0], &options).unwrap();

    assert_eq!(report.label.as_deref(), Some("demo"));
    assert!((report.mean - 2.8).abs() < 1e-12);
    assert!((report.spread - 4.0).abs() < f64::EPSILON);
    assert_eq!(report.n, 5);
}

#[test]
fn trimming_reduces_n() {
    let options = Options {
        trim: 0.2,
        ..Options::default()
    };

    assert_eq!(
        summarize(&[3.0, 1.0, 4.0, 1.0, 5.0], &options).unwrap().n,
        3
    );
}

#[test]
fn options_travel_with_the_result() {
    let options = Options {
        precision: 3,
        ..Options::default()
    };
    let report = summarize(&[1.0, 2.0], &options).unwrap();

    let expected = BTreeMap::from([("trim".to_owned(), 0.0), ("precision".to_owned(), 3.0)]);
    assert_eq!(report.options, expected);
}

#[test]
fn compare_preserves_insertion_order() {
    let series = [("a", &[1.0, 2.0, 3.0][..]), ("b", &[2.0, 4.0, 6.0][..])];
    let table = compare(&series, &Options::default()).unwrap();

    let labels: Vec<Option<&str>> = table.iter().map(|report| report.label.as_deref()).collect();
    assert_eq!(labels, [Some("a"), Some("b")]);

    let means: Vec<f64> = table.iter().map(|report| report.mean).collect();
    assert_eq!(means, [2.0, 4.0]);
}

#[test]
fn describe_returns_flat_rows() {
    let series = [("a", &[1.0, 2.0, 3.0][..])];
    let rows = describe(&compare(&series, &Options::default()).unwrap());

    let expected = BTreeMap::from([
        ("label".to_owned(), "a".to_owned()),
        ("mean".to_owned(), "2".to_owned()),
        ("spread".to_owned(), "2".to_owned()),
        ("n".to_owned(), "3".to_owned()),
    ]);
    assert_eq!(rows, [expected]);
}

#[test]
fn empty_input_raises() {
    assert_eq!(summarize(&[], &Options::default()), Err(Error::Empty));
}

#[test]
fn non_finite_input_raises() {
    assert_eq!(
        normalize(&[1.0, f64::INFINITY]),
        Err(Error::NotFinite(f64::INFINITY))
    );
}

#[test]
fn out_of_range_trim_raises() {
    for fraction in [-0.1, 0.5, 1.0] {
        assert_eq!(
            trim(&[1.0, 2.0, 3.0], fraction),
            Err(Error::InvalidTrim(fraction))
        );
    }
}
