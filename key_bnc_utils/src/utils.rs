use unicase::UniCase;
use counter::Counter;


#[derive(Debug)]
enum WordType {
	String,
	Number,
}

const ADDITIONAL_VALID_NUMERIC_CHARS: [char; 3] = [ ':', ',', '.' ];
const STRING_WORD_BREAKS: [char; 10] = [ '“', '”', '‘', '’', '…', '"', '–', '•', '—', '′' ];

pub fn collect(results: Vec<String>) -> Counter<UniCase<String>> {
	results.into_iter()
		.map(UniCase::new)
		.collect::<Counter<_>>()
}

pub fn tokenize(normalized: &mut String) -> Vec<String> {
	let mut words = vec![];
	let mut word = Vec::with_capacity(1000);
	let mut current_word_type = WordType::String;
	let mut had_single_quote = false;

	normalized.chars().for_each(|curr_char| {
		let is_new_word = word.is_empty();
		had_single_quote = had_single_quote || curr_char == '\'';

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
			word.push(curr_char);
		}

		if should_end_word && !word.is_empty() {
			current_word_type = WordType::String;
			if had_single_quote {
				for w in clean_single_quotes(&word) {
					words.push(w);
				}
			}
			else {
				words.push(word.drain(0..).collect::<String>());
			}
			word.clear();
			had_single_quote = false;
		}
	});

	if !word.is_empty() {
		for w in clean_single_quotes(&word) {
			words.push(w);
		}
	}

	words
}

fn clean_single_quotes(orig_word: &[char]) -> Vec<String> {
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
