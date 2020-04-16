extern crate test;

use crate::KeyBNCPreTokenizer;
use tokenizers::tokenizer::{NormalizedString, PreTokenizer};
use std::fs::{read_to_string};

#[cfg(test)]
mod tests {
    use super::*;
    use test::Bencher;

	fn it_lowercases_text(pt: &Box<KeyBNCPreTokenizer>, mut normalized: &mut NormalizedString) {
		match pt.pre_tokenize(&mut normalized) {
			Ok(_v) => {},
			Err(_e) => {
				unreachable!("The pre_tokenizer should not error out here.");
			}
		}
	}

	#[bench]
	fn bench_key_bnc(b: &mut Bencher) {
		let contents = read_to_string("/Users/dougal/Projects/Key-BNC/rust/key_bnc/sample_data/long.txt")
			.expect("Could not load contents.");
		let pt = Box::new(KeyBNCPreTokenizer::new());
		let mut normalized = NormalizedString::from(&contents);
		b.iter(|| it_lowercases_text(&pt, &mut normalized));
	}
}
