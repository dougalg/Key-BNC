use indexed_db_futures::prelude::*;
use wasm_bindgen::prelude::*;

const DB_NAME: &str = "key_bnc";
const STORE_NAME: &str = "corpus_files";

pub async fn save_file_text(key: i32, text: String) -> Result<JsValue, JsValue> {
	// Open my_db v1
	let mut db_req: OpenDbRequest = IdbDatabase::open_u32(DB_NAME, 1)?;

	db_req.set_on_upgrade_needed(Some(|evt: &IdbVersionChangeEvent| -> Result<(), JsValue> {
		// Check if the object store exists; create it if it doesn't
		if let None = evt.db().object_store_names().find(|n| n == STORE_NAME) {
			evt.db().create_object_store(STORE_NAME)?;
		}
		Ok(())
	}));

	let db: IdbDatabase = db_req.into_future().await?;

	// Insert/overwrite a record
	let tx: IdbTransaction = db
		.transaction_on_one_with_mode(STORE_NAME, IdbTransactionMode::Readwrite)?;
	let store: IdbObjectStore = tx.object_store(STORE_NAME)?;

	store.put_key_val_owned(key, &JsValue::from(text))?;

	// IDBTransactions can have an Error or an Abort event; into_result() turns both into a
	// DOMException
	tx.await.into_result()?;

	Ok(JsValue::from(key))
}
