#![feature(test)]
mod tokenizer;

use std::fs::{read_dir, DirEntry};
use std::io;
use std::path::Path;
use std::env;
use tokenizer::key_bnc_split::{tokenize, collect};
use std::fs::{read_to_string};

fn main() {
	let args: Vec<String> = env::args().collect();
	let root_dir = &args[1];
	println!("Reading {:#?}", root_dir);
	let dir = Path::new(root_dir);
	visit_dirs(dir, &process_file)
		.expect("fffuuuu");
}

fn process_file(entry: &DirEntry) {
	println!("Attempting to read {:#?}", entry.path());
	let mut contents = read_to_string(entry.path())
		.expect("Could not load contents.");

	match tokenize(&mut contents) {
		Ok(results) => {
			let cp = collect(&results);
			// println!("{:#?}", cp);
		},
		Err(e) => {
			// println!("b {:?}", e);
		}
	}
}

fn visit_dirs(dir: &Path, cb: &dyn Fn(&DirEntry)) -> io::Result<()> {
	if dir.is_dir() {
		for entry in read_dir(dir)? {
			let entry = entry?;
			let path = entry.path();
			if path.is_dir() {
				visit_dirs(&path, cb)?;
			} else {
				cb(&entry);
			}
		}
	}
	Ok(())
}
