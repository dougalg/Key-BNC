mod pdftotext;

extern crate serde_derive;
use std::collections::HashMap;
use serde_derive::{Serialize};
use wasm_bindgen::prelude::*;
use web_sys::FileReader;
use key_bnc_utils::utils::{tokenize, collect};
use key_bnc_utils::stats::{odds_ratio, log_likelihood, dispersion_normalized};
use unicase::UniCase;
use counter::Counter;
use csv::Reader;
use js_sys::Uint8Array;
use pdf::file::File;

// When the `wee_alloc` feature is enabled, use `wee_alloc` as the global
// allocator.
#[cfg(feature = "wee_alloc")]
#[global_allocator]
static ALLOC: wee_alloc::WeeAlloc = wee_alloc::WeeAlloc::INIT;

#[derive(Debug)]
pub struct CorpusPart {
	token_count: usize,
	word_counts: Counter<UniCase<String>>,
}

#[derive(Debug)]
#[derive(Serialize)]
pub struct WordStats {
	word: String,
	frequency: usize,
	frequency_bnc: usize,
	log_likelihood: f64,
	odds_ratio: f64,
	dispersion: f64,
}

#[wasm_bindgen]
#[derive(Default)]
pub struct KeyBnc {
	last_id: i32,
	has_loaded_bnc_data: bool,
	entries: HashMap<i32, CorpusPart>,
	bnc_counts: HashMap<UniCase<String>, usize>,
	total_num_tokens_in_bnc: usize,
	total_num_tokens_in_user_corpus: usize,
	user_corpus_words_counts: Counter<UniCase<String>>,
}

#[wasm_bindgen]
impl KeyBnc {
	pub fn new() -> KeyBnc {
		Default::default()
	}

	fn get_next_id(&mut self) -> i32 {
		self.last_id += 1;
		self.last_id
	}

	pub fn get_token_count(&mut self) -> usize {
		self.total_num_tokens_in_user_corpus
	}

	pub fn get_has_loaded_bnc_data(&mut self) -> bool {
		self.has_loaded_bnc_data
	}

	/**
	 * Add a text file to the corpus, as a JS FileReader
	 */
	pub fn add_entry(&mut self, file: FileReader) -> i32 {
		let contents = file.result()
			.expect("Could not read file");

		self.add_string(&mut contents.into_serde().unwrap())
	}

	/**
	 * Add a PDF to the corpus as a Uint8Array
	 */
	pub fn add_pdf(&mut self, file: Uint8Array) -> i32 {
		let mut t = String::new();
		read_pdf_file(file, &mut t);

		self.add_string(&mut t)
	}

	fn add_string(&mut self, text: &mut String) -> i32 {
		let file_id = self.get_next_id();
		let entry = process_file(tokenize(text));

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

	pub fn load_bnc_data(&mut self, bnc_raw_csv: String) {
		self.has_loaded_bnc_data = false;
		let bnc_counts = get_bnc_count(bnc_raw_csv);
		self.total_num_tokens_in_bnc = 0;

		for (_w, c) in bnc_counts.iter() {
			self.total_num_tokens_in_bnc += *c as usize;
		}
		self.bnc_counts = bnc_counts;
		self.has_loaded_bnc_data = true;
	}

	pub fn get_stats(&mut self) -> JsValue {
		// calculate percentages for each entry into a hashMap by entry id
		let entry_percentages: HashMap<&i32, f64> = self.entries.iter()
			.map(|(id, entry)| (id, entry.token_count as f64 / self.total_num_tokens_in_user_corpus as f64))
			.collect();
		let res: Vec<WordStats> = self.user_corpus_words_counts
			.iter()
			.map(|(word, count)| {
				let count_in_bnc = match self.bnc_counts.get(&word) {
					Some(val) => *val as f64,
					None => 0.0,
				};
				// [(part_percentage, part_freq)]
				let part_data: Vec<(f64, f64)> = self.entries.iter()
					.map(|(id, entry)| {
						let count_for_part = match entry.word_counts.get(&word) {
							Some(val) => *val as f64,
							None => 0.0,
						};
						(*entry_percentages.get(id).unwrap(), count_for_part)
					})
					.collect();
				WordStats {
					frequency: *count,
					frequency_bnc: count_in_bnc as usize,
					word: word.clone().into_inner(),
					log_likelihood: log_likelihood(*count as f64, self.total_num_tokens_in_user_corpus as f64, count_in_bnc as f64, self.total_num_tokens_in_bnc as f64),
					odds_ratio: odds_ratio(*count as f64, self.total_num_tokens_in_user_corpus as f64, count_in_bnc as f64, self.total_num_tokens_in_bnc as f64, 0.0),
					dispersion: dispersion_normalized(&part_data, *count as f64),
				}
			})
			.collect();
		JsValue::from_serde(&res).unwrap()
	}
}

fn process_file(tokens: Vec<String>) -> CorpusPart {
	let token_count = tokens.len();
	let counted_words = collect(tokens);

	CorpusPart {
		token_count,
		word_counts: counted_words,
	}
}

pub fn get_bnc_count(bnc_raw_csv: String) -> HashMap<UniCase<String>, usize> {
	// Create a CSV parser that reads data from stdin.
	let mut rdr = Reader::from_reader(bnc_raw_csv.as_bytes());
	// Loop over each record and convert it to a a HashMap
	rdr.records()
		.filter_map(|rec| rec.ok())
		.map(|rec| (UniCase::new(rec[2].parse::<String>().unwrap()), rec[1].parse::<usize>().unwrap()))
		.collect()
}

pub fn read_pdf_file(file: Uint8Array, text: &mut String) {
	// let mut text = "".to_owned();
	let file = File::from_data(file.to_vec()).expect("failed to read PDF");
	for (page_nr, page_result) in file.pages().enumerate() {
		let text_result = page_result.ok()
			.map(|page| {
				pdftotext::page_text(&page, &file).ok()
			})
			.flatten();
		if let Some(ok_text) = text_result {
			text.push_str(&ok_text);
		}
	}
}
