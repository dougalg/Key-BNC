extern crate serde_derive;
use std::collections::HashMap;
use serde_derive::{Serialize};
use wasm_bindgen::prelude::*;
use web_sys::FileReader;
use key_bnc_utils::utils::{tokenize, collect};
// use js_sys::Array;
// use unicase::UniCase;
use counter::Counter;

// When the `wee_alloc` feature is enabled, use `wee_alloc` as the global
// allocator.
#[cfg(feature = "wee_alloc")]
#[global_allocator]
static ALLOC: wee_alloc::WeeAlloc = wee_alloc::WeeAlloc::INIT;

// #[wasm_bindgen]
#[derive(Debug)]
#[derive(Serialize)]
pub struct CorpusPart {
	percent_of_total: f32,
	word_count: usize,
	word_counter: HashMap<String, usize>
}

// #[wasm_bindgen]
// impl CorpusPart {
// 	pub fn get_percent_of_total(&self) -> f32 {
// 		self.percent_of_total
// 	}

// 	pub fn get_word_count(&self) -> usize {
// 		self.word_count
// 	}

// 	pub fn get_word_counter(&self) -> Vec<(String, usize)> {
// 		self.word_counter
// 	}
// }

#[wasm_bindgen]
pub fn count_file(file: FileReader) -> JsValue {
	let contents = file.result()
		.expect("Could not read file");
	let tokens = tokenize(&mut contents.into_serde().unwrap());
	let word_count = tokens.len();
	let counted_words: HashMap<String, usize> = collect(tokens)
		.most_common()
		.into_iter()
		.map(|t| (t.0.into_inner(), t.1))
		.collect();

	JsValue::from_serde(&CorpusPart {
		word_count,
		percent_of_total: 0.0,
		word_counter: counted_words
	}).unwrap()
}
