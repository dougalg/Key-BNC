use crate::KeyBNCPreTokenizer;
use tokenizers::tokenizer::{NormalizedString, PreTokenizer};

#[test]
fn it_splits_single_quotes_after_numbers() {
	let pt = Box::new(KeyBNCPreTokenizer::new());
	let mut normalized = NormalizedString::from("'adventure 2'adventure");
	match pt.pre_tokenize(&mut normalized) {
		Ok(v) => {
			assert_eq!(v.len(), 3);
			assert_eq!(v[0].0, "adventure");
			assert_eq!(v[1].0, "2");
			assert_eq!(v[2].0, "adventure");
		},
		Err(_e) => {
			unreachable!("The pre_tokenizer should not error out here.");
		}
	}
}

#[test]
fn it_keeps_single_quotes_inside_strings() {
	let pt = Box::new(KeyBNCPreTokenizer::new());
	let mut normalized = NormalizedString::from("you're fine, fire-truck!");
	match pt.pre_tokenize(&mut normalized) {
		Ok(v) => {
			assert_eq!(v.len(), 5);
			assert_eq!(v[0].0, "you");
			assert_eq!(v[1].0, "'re");
			assert_eq!(v[2].0, "fine");
			assert_eq!(v[3].0, "fire");
			assert_eq!(v[4].0, "truck");
		},
		Err(_e) => {
			unreachable!("The pre_tokenizer should not error out here.");
		}
	}
}
#[test]
fn it_keeps_single_quotes_at_the_end_of_strings() {
	let pt = Box::new(KeyBNCPreTokenizer::new());
	let mut normalized = NormalizedString::from("this is a 'quotation'.");
	match pt.pre_tokenize(&mut normalized) {
		Ok(v) => {
			assert_eq!(v.len(), 4);
			assert_eq!(v[0].0, "this");
			assert_eq!(v[1].0, "is");
			assert_eq!(v[2].0, "a");
			assert_eq!(v[3].0, "quotation");
		},
		Err(_e) => {
			unreachable!("The pre_tokenizer should not error out here.");
		}
	}
}

#[test]
fn it_removes_double_quotes_strings() {
	let pt = Box::new(KeyBNCPreTokenizer::new());
	let mut normalized = NormalizedString::from("so is \"this\".");
	match pt.pre_tokenize(&mut normalized) {
		Ok(v) => {
			assert_eq!(v.len(), 3);
			assert_eq!(v[0].0, "so");
			assert_eq!(v[1].0, "is");
			assert_eq!(v[2].0, "this");
		},
		Err(_e) => {
			unreachable!("The pre_tokenizer should not error out here.");
		}
	}
}

#[test]
fn it_keeps_numbers_together() {
	let pt = Box::new(KeyBNCPreTokenizer::new());
	let mut normalized = NormalizedString::from("there are 100,000,000,000.00 words in the bnc.");
	match pt.pre_tokenize(&mut normalized) {
		Ok(v) => {
			assert_eq!(v.len(), 7);
			assert_eq!(v[0].0, "there");
			assert_eq!(v[1].0, "are");
			assert_eq!(v[2].0, "100,000,000,000.00");
			assert_eq!(v[3].0, "words");
			assert_eq!(v[4].0, "in");
			assert_eq!(v[5].0, "the");
			assert_eq!(v[6].0, "bnc");
		},
		Err(_e) => {
			unreachable!("The pre_tokenizer should not error out here.");
		}
	}
}

#[test]
fn it_still_removes_punctuation() {
	let pt = Box::new(KeyBNCPreTokenizer::new());
	let mut normalized = NormalizedString::from("\"'tis!\" replied aunt helga.");
	match pt.pre_tokenize(&mut normalized) {
		Ok(v) => {
			assert_eq!(v.len(), 4);
			assert_eq!(v[0].0, "tis");
			assert_eq!(v[1].0, "replied");
			assert_eq!(v[2].0, "aunt");
			assert_eq!(v[3].0, "helga");
		},
		Err(_e) => {
			unreachable!("The pre_tokenizer should not error out here.");
		}
	}
}

#[test]
fn it_still_continues_to_remove_punctuation() {
	let pt = Box::new(KeyBNCPreTokenizer::new());
	let mut normalized = NormalizedString::from("don't tell someone what they can or can't do");
	match pt.pre_tokenize(&mut normalized) {
		Ok(v) => {
			assert_eq!(v.len(), 11);
			assert_eq!(v[0].0, "don");
			assert_eq!(v[1].0, "'t");
			assert_eq!(v[2].0, "tell");
			assert_eq!(v[3].0, "someone");
			assert_eq!(v[4].0, "what");
			assert_eq!(v[5].0, "they");
			assert_eq!(v[6].0, "can");
			assert_eq!(v[7].0, "or");
			assert_eq!(v[8].0, "can");
			assert_eq!(v[9].0, "'t");
			assert_eq!(v[10].0, "do");
		},
		Err(_e) => {
			unreachable!("The pre_tokenizer should not error out here.");
		}
	}
}
