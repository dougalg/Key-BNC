extern crate test;

use crate::KeyBNCPreTokenizer;
use tokenizers::tokenizer::{NormalizedString, PreTokenizer};

fn it_lowercases_text() {
	let pt = Box::new(KeyBNCPreTokenizer::new());
	let mut normalized = NormalizedString::from("uWu wHAt's this?");
	match pt.tokenize(&mut normalized) {
		Ok(v) => {
			assert_eq!(v.len(), 4);
			assert_eq!(v[0].0, "uwu");
			assert_eq!(v[1].0, "what");
			assert_eq!(v[2].0, "'s");
			assert_eq!(v[3].0, "this");
		},
		Err(_e) => {
			unreachable!("The tokenizer should not error out here.");
		}
	}
}

#[bench]
fn bench_key_bnc(b: &mut Bencher) {
	b.iter(|| it_lowercases_text());
}
