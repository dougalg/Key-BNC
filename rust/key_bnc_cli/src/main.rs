mod bnc_data;

use key_bnc_utils::utils::{tokenize, collect};
use bnc_data::get_bnc_count;
use std::path::Path;
use std::env;
use std::fs::{read_to_string};
use walkdir::{WalkDir, DirEntry};
use unicase::UniCase;
use counter::Counter;


fn main() {
	let counter = 0;
	let bnc_counts = get_bnc_count();
	let args: Vec<String> = env::args().collect();
	let root_dir = &args[1];
	println!("Reading {:#?}", root_dir);
	let dir = Path::new(root_dir);
	let mut entries = vec![];

	for entry in WalkDir::new(dir)
		.follow_links(true)
		.into_iter()
		.filter_map(|e| e.ok()) {

		let id = counter + 1;

		if entry.file_type().is_file() {
			entries.push(process_file(&entry, id));
		}
	}

	let mut all_words_counts: Counter<UniCase<String>> = Counter::new();
	let mut total_num_tokens = 0;

	for entry in &entries {
		total_num_tokens += entry.token_count;
		all_words_counts += entry.word_counts.clone();
	}

	let results: Vec<WordStats> = all_words_counts
		.into_map()
		.into_iter()
		.map(|(word, count)| {
			WordStats {
				count,
				word,
				ll: 0.0,
				or: 0.0,
				dispersion: 0.0,
			}
		})
		.collect();

	println!("{:#?}", results);
	println!("{:#?}", total_num_tokens);
	println!("{:#?}", bnc_counts.len());
}

#[derive(Debug)]
pub struct CorpusPart {
	id: i32,
	name: String,
	percent_of_total: f32,
	token_count: usize,
	word_counts: Counter<UniCase<String>>,
}

#[derive(Debug)]
pub struct WordStats {
	word: UniCase<String>,
	count: usize,
	ll: f32,
	or: f32,
	dispersion: f32,
}

fn process_file(entry: &DirEntry, id: i32) -> CorpusPart {
	println!("Attempting to read {:#?}", entry.path());
	let mut contents = read_to_string(entry.path())
		.expect("Could not load contents.");

	let tokens = tokenize(&mut contents);
	let token_count = tokens.len();
	let counted_words = collect(tokens);

	CorpusPart {
		id,
		name: entry.file_name().to_str().unwrap_or(UNKNOWN_FILE).to_string(),
		token_count,
		word_counts: counted_words,
		percent_of_total: 0.0
	}
}

const UNKNOWN_FILE: &str = "Unknown File ";
