#![feature(test)]
mod pre_tokenizer;

use std::collections::HashMap;
use std::fs::{read_to_string, read_dir, DirEntry};
use std::io;
use std::path::Path;
use std::env;
use pre_tokenizer::key_bnc_split::KeyBNCPreTokenizer;
use tokenizers::tokenizer::{Tokenizer, EncodeInput};
use tokenizers::models::wordlevel::WordLevelBuilder;
use counter::Counter;

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
	let contents = read_to_string(entry.path())
		.expect("Could not load contents.");

	let mut vocab = HashMap::new();
	vocab.insert("[UNK]".into(), 0);
	let wl = WordLevelBuilder::new()
		.vocab(vocab)
		.unk_token("[UNK]".into())
		.build();

	let mut tokenizer = Tokenizer::new(Box::new(wl));
	tokenizer.with_pre_tokenizer(Box::new(KeyBNCPreTokenizer::new()));

	match tokenizer.encode(EncodeInput::Single(contents.to_lowercase()), false) {
		Ok(encoding) => {
			println!("{:#?}", encoding.get_tokens().iter().collect::<Counter<_>>());
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
