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

		if entry.file_type().is_file() {
			entries.push(process_file(&entry));
		}
	}

	let mut all_words_counts: Counter<UniCase<String>> = Counter::new();
	let mut total_num_tokens = 0;
	for entry in entries {
		total_num_tokens += entry.token_count;
		all_words_counts += entry.word_counts.clone();
	}

	let corpus = CorpusPart {
		token_count: total_num_tokens,
		word_counts: all_words_counts,
		percent_of_total: 1.0
	};
	// println!("{:#?}", corpus.word_counts);
	println!("{:#?}", corpus.token_count);
	println!("{:#?}", bnc_counts.len());
}

#[derive(Debug)]
pub struct CorpusPart {
	percent_of_total: f32,
	token_count: usize,
	word_counts: Counter<UniCase<String>>
}

fn process_file(entry: &DirEntry) -> CorpusPart {
	println!("Attempting to read {:#?}", entry.path());
	let mut contents = read_to_string(entry.path())
		.expect("Could not load contents.");

	let tokens = tokenize(&mut contents);
	let token_count = tokens.len();
	let counted_words = collect(tokens);

	CorpusPart {
		token_count,
		word_counts: counted_words,
		percent_of_total: 0.0
	}
}
