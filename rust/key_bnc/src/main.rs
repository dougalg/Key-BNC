mod pre_tokenizer;

use pre_tokenizer::key_bnc_split::KeyBNCPreTokenizer;
use tokenizers::tokenizer::{Tokenizer, EncodeInput};
use tokenizers::models::wordlevel::WordLevelBuilder;
use std::collections::HashMap;

fn main() {
	let mut vocab = HashMap::new();
	vocab.insert("[UNK]".into(), 0);
	let wl = WordLevelBuilder::new()
		.vocab(vocab)
		.unk_token("[UNK]".into())
		.build();

	let mut tokenizer = Tokenizer::new(Box::new(wl));
	tokenizer.with_pre_tokenizer(Box::new(KeyBNCPreTokenizer::new()));

	match tokenizer.encode(EncodeInput::Single("Hey there!".into()), false) {
		Ok(encoding) => {
			println!("{:?}", encoding.get_tokens());
		},
		Err(e) => {
			println!("b {:?}", e);
		}
	}
}
