extern crate test;

use crate::{tokenize, collect};
use std::fs::{read_to_string};

#[cfg(test)]
mod tests {
    use super::*;
    use test::Bencher;

	#[bench]
	fn bench_key_bnc_tokenization(b: &mut Bencher) {
		let contents = read_to_string("/Users/dougal/Projects/Key-BNC/rust/key_bnc/sample_data/long.txt")
			.expect("Could not load contents.");
		let mut normalized = String::from(&contents);
		b.iter(|| tokenize(&mut normalized));
	}

	#[bench]
	fn bench_key_bnc_collect(b: &mut Bencher) {
		let contents = read_to_string("/Users/dougal/Projects/Key-BNC/rust/key_bnc/sample_data/long.txt")
			.expect("Could not load contents.");
		let mut normalized = String::from(&contents);
		match tokenize(&mut normalized) {
			Ok(v) => {
				b.iter(|| collect(&v));
			},
			Err(_e) => {
				unreachable!("The tokenizer should not error out here.");
			}
		}
	}
}
