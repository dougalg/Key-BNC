extern crate serde_derive;
use std::collections::HashMap;
use serde_derive::{Serialize};
use wasm_bindgen::prelude::*;
use web_sys::FileReader;
use key_bnc_utils::utils::{tokenize, collect};
// use js_sys::Array;
use unicase::UniCase;
use counter::Counter;

// When the `wee_alloc` feature is enabled, use `wee_alloc` as the global
// allocator.
#[cfg(feature = "wee_alloc")]
#[global_allocator]
static ALLOC: wee_alloc::WeeAlloc = wee_alloc::WeeAlloc::INIT;

// // #[wasm_bindgen]
// #[derive(Debug)]
// #[derive(Serialize)]
// pub struct CorpusPart {
// 	percent_of_total: f32,
// 	word_count: usize,
// 	word_counter: HashMap<String, usize>
// }
// const UNKNOWN_FILE: &str = "Unknown File ";

// #[wasm_bindgen]
// pub fn count_file(file: FileReader) -> JsValue {
// 	let contents = file.result()
// 		.expect("Could not read file");
// 	let tokens = tokenize(&mut contents.into_serde().unwrap());
// 	let word_count = tokens.len();
// 	let counted_words: HashMap<String, usize> = collect(tokens)
// 		.most_common()
// 		.into_iter()
// 		.map(|t| (t.0.into_inner(), t.1))
// 		.collect();

// 	JsValue::from_serde(&CorpusPart {
// 		word_count,
// 		percent_of_total: 0.0,
// 		word_counter: counted_words
// 	}).unwrap()
// }

#[derive(Debug)]
pub struct CorpusPart {
	percent_of_total: f64,
	token_count: usize,
	word_counts: Counter<UniCase<String>>,
}

#[derive(Debug)]
pub struct WordStats {
	word: String,
	count: usize,
	log_likelyhood: f64,
	odds_ratio: f64,
	dispersion: f64,
}

#[wasm_bindgen]
pub struct KeyBnc {
	last_id: i32,
	entries: HashMap<i32, CorpusPart>,
	bnc_counts: HashMap<UniCase<String>, usize>,
	total_num_tokens_in_bnc: usize,
	total_num_tokens_in_user_corpus: usize,
	user_corpus_words_counts: Counter<UniCase<String>>,
}

#[wasm_bindgen]
impl KeyBnc {
	pub fn new() -> KeyBnc {
		KeyBnc {
			last_id: 0,
			entries: HashMap::new(),
			bnc_counts: HashMap::new(),
			total_num_tokens_in_bnc: 0,
			total_num_tokens_in_user_corpus: 0,
			user_corpus_words_counts: Counter::new(),
		}
	}

	fn get_next_id(&mut self) -> i32 {
		self.last_id += 1;
		self.last_id
	}

	pub fn get_token_count(&mut self) -> usize {
		self.total_num_tokens_in_user_corpus
	}

	pub fn add_entry(&mut self, file: FileReader) -> i32 {
		let contents = file.result()
			.expect("Could not read file");
		let tokens = tokenize(&mut contents.into_serde().unwrap());
		let file_id = self.get_next_id();
		let entry = process_file(tokens);

		// Update the struct
		self.total_num_tokens_in_user_corpus += entry.token_count;
		self.user_corpus_words_counts += entry.word_counts.clone();
		self.entries.insert(file_id.clone(), entry);

		file_id
	}

	pub fn remove_entry(&mut self, file_id: i32) {
		let entry = self.entries.get(&file_id)
			.expect("File does not exist");
		self.total_num_tokens_in_user_corpus -= entry.token_count;
		self.user_corpus_words_counts -= entry.word_counts.clone();
		self.entries.remove(&file_id);
	}

	// pub fn get_stats(&mut self) -> JsValue {

	// }
}

fn process_file(tokens: Vec<String>) -> CorpusPart {
	let token_count = tokens.len();
	let counted_words = collect(tokens);

	CorpusPart {
		token_count,
		word_counts: counted_words,
		percent_of_total: 0.0
	}
}
