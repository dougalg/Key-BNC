use wasm_bindgen::prelude::*;
use key_bnc_utils::utils::{tokenize, collect};

use unicase::UniCase;
use counter::Counter;

// When the `wee_alloc` feature is enabled, use `wee_alloc` as the global
// allocator.
#[cfg(feature = "wee_alloc")]
#[global_allocator]
static ALLOC: wee_alloc::WeeAlloc = wee_alloc::WeeAlloc::INIT;

#[wasm_bindgen]
#[derive(Debug)]
pub struct CorpusPart {
	percent_of_total: f32,
	word_count: usize,
	words: Counter<UniCase<String>>
}

#[wasm_bindgen]
pub fn print_result(mut contents: String) -> CorpusPart {
	let tokens = tokenize(&mut contents);
	let word_count = tokens.len();
	let counted_words = collect(tokens);

	CorpusPart {
		word_count,
		words: counted_words,
		percent_of_total: 0.0
	}
}
