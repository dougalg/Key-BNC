extern crate serde_derive;
extern crate console_error_panic_hook;
mod totext;
use wasm_bindgen::prelude::*;
use web_sys::FileReader;
use pdf::file::File;
use totext::page_text;
use js_sys::Uint8Array;
use std::panic;

#[wasm_bindgen]
extern "C" {
    // Use `js_namespace` here to bind `console.log(..)` instead of just
    // `log(..)`
    #[wasm_bindgen(js_namespace = console)]
    fn log(s: &str);

    // The `console.log` is quite polymorphic, so we can bind it with multiple
    // signatures. Note that we need to use `js_name` to ensure we always call
    // `log` in JS.
    #[wasm_bindgen(js_namespace = console, js_name = log)]
    fn log_vecU8(a: Vec<u8>);

    // Multiple arguments too!
    #[wasm_bindgen(js_namespace = console, js_name = log)]
    fn log_many(a: &str, b: &str);
}

#[wasm_bindgen]
#[derive(Default)]
#[derive(Debug)]
pub struct PdfToText {
	text: String,
}

#[wasm_bindgen]
impl PdfToText {
	pub fn new() -> PdfToText {
		panic::set_hook(Box::new(console_error_panic_hook::hook));
		Default::default()
	}

	pub fn read_file(&mut self, file: Uint8Array) -> JsValue {
		let file = File::from_data(file.to_vec()).expect("failed to read PDF");
		for (page_nr, page) in file.pages().enumerate() {
			if let Ok(page) = page {
				println!("=== PAGE {} ===\n", page_nr);
				if let Ok(text) = page_text(&page, &file) {
					self.text = text;
				} else {
					println!("ERROR");
				}
				println!();
			}
		}

		JsValue::from_serde(&self.text).unwrap()
	}
}
