#![feature(test)]
mod tokenizer;

extern crate walkdir;

// use std::fs::{read_dir, DirEntry};
use std::io;
use std::path::Path;
use std::env;
use tokenizer::key_bnc_split::{tokenize, collect};
use std::fs::{read_to_string};
use unicase::UniCase;
use counter::Counter;
use walkdir::{WalkDir, DirEntry};

#[derive(Debug)]
struct Corpus<'a> {
	words: Counter<UniCase<&'a String>>,
	parts: Vec<CorpusPart>
}

#[derive(Debug)]
pub struct CorpusPart {
	percent_of_total: f32,
	word_count: usize,
	words: Counter<UniCase<String>>
}

fn main() {
	let args: Vec<String> = env::args().collect();
	let root_dir = &args[1];
	println!("Reading {:#?}", root_dir);
	let dir = Path::new(root_dir);

	// visit_dirs(dir, &process_file)
	// 	.expect("fffuuuu");

	for entry in WalkDir::new(dir)
		.follow_links(true)
		.into_iter()
		.filter_map(|e| e.ok()) {

		process_file(&entry);
	}
}

fn process_file(entry: &DirEntry) -> CorpusPart {
	println!("Attempting to read {:#?}", entry.path());
	let mut contents = read_to_string(entry.path())
		.expect("Could not load contents.");

	let tokens = tokenize(&mut contents);
	let word_count = tokens.len();
	let counted_words = collect(tokens);

	CorpusPart {
		word_count,
		words: counted_words,
		percent_of_total: 0.0
	}
}
