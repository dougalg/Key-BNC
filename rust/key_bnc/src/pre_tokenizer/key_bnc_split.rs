use tokenizers::tokenizer::{NormalizedString, Offsets, PreTokenizer, Result};

pub struct KeyBNCPreTokenizer {}

#[derive(Debug)]
enum WordType {
	String,
	Number,
}

impl KeyBNCPreTokenizer {
	pub fn new() -> Self {
		KeyBNCPreTokenizer {}
	}
}

const ADDITIONAL_VALID_NUMERIC_CHARS: [char; 3] = [ ':', ',', '.' ];
const STRING_WORD_BREAKS: [char; 10] = [ '“', '”', '‘', '’', '…', '"', '–', '•', '—', '′' ];

impl PreTokenizer for KeyBNCPreTokenizer {
	fn pre_tokenize(&self, normalized: &mut NormalizedString) -> Result<Vec<(String, Offsets)>> {
		let mut words = vec![];
		let mut word = Vec::with_capacity(1000);
		let mut current_word_type = WordType::String;

		normalized.get().chars().for_each(|curr_char| {
			let is_new_word = word.is_empty();
			if is_new_word && curr_char.is_digit(10) {
				current_word_type = WordType::Number;
			}

			let should_end_word = match current_word_type {
				WordType::String => curr_char.is_whitespace() || STRING_WORD_BREAKS.contains(&curr_char) || (curr_char != '\'' && curr_char.is_ascii_punctuation()),
				WordType::Number => !curr_char.is_digit(10) && !ADDITIONAL_VALID_NUMERIC_CHARS.contains(&curr_char),
			};

			let should_push_char = match current_word_type {
				WordType::String => (curr_char == '\'' && !is_new_word && !should_end_word) || !(curr_char.is_whitespace() || STRING_WORD_BREAKS.contains(&curr_char) || curr_char.is_ascii_punctuation()),
				WordType::Number => curr_char.is_digit(10) || ADDITIONAL_VALID_NUMERIC_CHARS.contains(&curr_char),
			};

			if should_push_char {
				for c in curr_char.to_lowercase() {
					word.push(c);
				}
			}

			if should_end_word && !word.is_empty() {
				current_word_type = WordType::String;
				for w in get_finalized_words(&word) {
					words.push((w, (0, 0)));
				}
				word.drain(0..);
			}
		});

		if !word.is_empty() {
			for w in get_finalized_words(&word) {
				words.push((w, (0, 0)));
			}
		}

		Ok(words)
	}
}

fn get_finalized_words(orig_word: &[char]) -> Vec<String> {
	let mut result = vec![];
	let mut word = Vec::with_capacity(1000);
	orig_word.iter().rev().for_each(|curr_char| {
		if result.is_empty() && word.is_empty() && (STRING_WORD_BREAKS.contains(&curr_char) || curr_char.is_ascii_punctuation()) {
			return;
		}
		word.push(curr_char);
		if curr_char == &'\'' && !word.is_empty() {
			word.reverse();
			result.push(word.drain(0..).collect::<String>());
		}
	});
	word.reverse();
	result.push(word.drain(0..).collect::<String>());
	result.reverse();
	result
}
