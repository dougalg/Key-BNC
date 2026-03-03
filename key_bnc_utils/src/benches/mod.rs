extern crate test;

use crate::utils::{collect, tokenize};
use std::fs::read_to_string;

mod tests {
    use super::*;
    use test::Bencher;

    #[bench]
    fn bench_key_bnc_tokenization(b: &mut Bencher) {
        let path = format!("{}/sample_data/long.txt", env!("CARGO_MANIFEST_DIR"));
        let contents = read_to_string(path).expect("Could not load contents.");
        let mut normalized = String::from(&contents);
        b.iter(|| tokenize(&mut normalized));
    }

    #[bench]
    fn bench_key_bnc_collect(b: &mut Bencher) {
        let path = format!("{}/sample_data/long.txt", env!("CARGO_MANIFEST_DIR"));
        let contents = read_to_string(path).expect("Could not load contents.");
        let mut normalized = String::from(&contents);
        let v = tokenize(&mut normalized);
        b.iter(|| collect(v.clone()));
    }
}
