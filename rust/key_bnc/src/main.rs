#![feature(test)]
mod pre_tokenizer;

use std::fs::{read_dir, DirEntry};
use std::io;
use std::path::Path;
use std::env;
use pre_tokenizer::key_bnc_split::KeyBNCPreTokenizer;
use counter::Counter;
use std::fs::{read_to_string};
use unicase::UniCase;

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

	let tokenizer = KeyBNCPreTokenizer::new();

	match tokenizer.pre_tokenize(&mut contents) {
		Ok(results) => {
			println!("{:#?}", results.iter()
				.map(|w| UniCase::new(w))
				.collect::<Counter<_>>());
		},
		Err(e) => {
			println!("b {:?}", e);
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
