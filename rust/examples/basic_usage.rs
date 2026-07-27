//! End-to-end example, run with `cargo run --example basic_usage`.
//!
//! Mirrors `examples/basic_usage.py` on the Python side, so the same story is
//! told in both languages.

use docsforge::{compare, describe, Options};

fn main() -> Result<(), docsforge::Error> {
    let series = [
        ("baseline", &[3.0, 1.0, 4.0, 1.0, 5.0, 9.0, 2.0, 6.0][..]),
        ("treatment", &[4.0, 2.0, 5.0, 2.0, 6.0, 9.0, 3.0, 7.0][..]),
    ];
    let options = Options {
        trim: 0.125,
        precision: 3,
        ..Options::default()
    };

    let table = compare(&series, &options)?;

    for row in describe(&table) {
        println!(
            "{:>10}  mean={:>6}  n={}",
            row["label"], row["mean"], row["n"]
        );
    }

    let best = table
        .iter()
        .max_by(|a, b| a.mean.total_cmp(&b.mean))
        .expect("compare() returns one report per series");
    println!(
        "\nhighest mean: {} ({})",
        best.label.as_deref().unwrap_or_default(),
        best.mean
    );

    Ok(())
}
