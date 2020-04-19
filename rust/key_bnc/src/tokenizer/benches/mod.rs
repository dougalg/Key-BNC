extern crate test;

use crate::KeyBNCPreTokenizer;
use std::fs::{read_to_string};

#[cfg(test)]
mod tests {
    use super::*;
    use test::Bencher;

	fn tokenize(pt: &KeyBNCPreTokenizer, mut normalized: &mut String) {
		match pt.tokenize(&mut normalized) {
			Ok(_v) => {},
			Err(_e) => {
				unreachable!("The tokenizer should not error out here.");
			}
		}
	}

	#[bench]
	fn bench_key_bnc_tokenization(b: &mut Bencher) {
		let contents = read_to_string("/home/dgraham/projects/Key-BNC/rust/key_bnc/sample_data/long.txt")
			.expect("Could not load contents.");
		let pt = KeyBNCPreTokenizer::new();
		let mut normalized = String::from(&contents);
		b.iter(|| tokenize(&pt, &mut normalized));
	}

	#[bench]
	fn bench_key_bnc_collect(b: &mut Bencher) {
		let contents = read_to_string("/home/dgraham/projects/Key-BNC/rust/key_bnc/sample_data/long.txt")
			.expect("Could not load contents.");
		let pt = KeyBNCPreTokenizer::new();
		let mut normalized = String::from(&contents);
		match pt.tokenize(&mut normalized) {
			Ok(v) => {
				b.iter(|| pt.collect(&v));
			},
			Err(_e) => {
				unreachable!("The tokenizer should not error out here.");
			}
		}
	}
}
