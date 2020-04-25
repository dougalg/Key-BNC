use crate::utils::{tokenize};

#[test]
fn it_splits_single_quotes_after_numbers() {
	let mut normalized = String::from("'adventure 2'adventure");
	let v = tokenize(&mut normalized);
	assert_eq!(v.len(), 3);
	assert_eq!(v[0], "adventure");
	assert_eq!(v[1], "2");
	assert_eq!(v[2], "adventure");
}

#[test]
fn it_keeps_single_quotes_inside_strings() {
	let mut normalized = String::from("you're fine, fire-truck!");
	let v = tokenize(&mut normalized);
	assert_eq!(v.len(), 5);
	assert_eq!(v[0], "you");
	assert_eq!(v[1], "'re");
	assert_eq!(v[2], "fine");
	assert_eq!(v[3], "fire");
	assert_eq!(v[4], "truck");
}

#[test]
fn it_keeps_single_quotes_at_the_end_of_strings() {
	let mut normalized = String::from("this is a 'quotation'.");
	let v = tokenize(&mut normalized);
	assert_eq!(v.len(), 4);
	assert_eq!(v[0], "this");
	assert_eq!(v[1], "is");
	assert_eq!(v[2], "a");
	assert_eq!(v[3], "quotation");
}

#[test]
fn it_removes_double_quotes_strings() {
	let mut normalized = String::from("so is \"this\".");
	let v = tokenize(&mut normalized);
	assert_eq!(v.len(), 3);
	assert_eq!(v[0], "so");
	assert_eq!(v[1], "is");
	assert_eq!(v[2], "this");
}

#[test]
fn it_keeps_numbers_together() {
	let mut normalized = String::from("there are 100,000,000,0000 words in the bnc.");
	let v = tokenize(&mut normalized);
	assert_eq!(v.len(), 7);
	assert_eq!(v[0], "there");
	assert_eq!(v[1], "are");
	assert_eq!(v[2], "100,000,000,0000");
	assert_eq!(v[3], "words");
	assert_eq!(v[4], "in");
	assert_eq!(v[5], "the");
	assert_eq!(v[6], "bnc");
}

#[test]
fn it_still_removes_punctuation() {
	let mut normalized = String::from("\"'tis!\" replied aunt helga.");
	let v = tokenize(&mut normalized);
	assert_eq!(v.len(), 4);
	assert_eq!(v[0], "tis");
	assert_eq!(v[1], "replied");
	assert_eq!(v[2], "aunt");
	assert_eq!(v[3], "helga");
}

#[test]
fn it_still_continues_to_remove_punctuation() {
	let mut normalized = String::from("don't tell someone what they can or can't do");
	let v = tokenize(&mut normalized);
	assert_eq!(v.len(), 11);
	assert_eq!(v[0], "don");
	assert_eq!(v[1], "'t");
	assert_eq!(v[2], "tell");
	assert_eq!(v[3], "someone");
	assert_eq!(v[4], "what");
	assert_eq!(v[5], "they");
	assert_eq!(v[6], "can");
	assert_eq!(v[7], "or");
	assert_eq!(v[8], "can");
	assert_eq!(v[9], "'t");
	assert_eq!(v[10], "do");
}
