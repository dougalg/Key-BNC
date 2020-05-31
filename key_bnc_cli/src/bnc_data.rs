extern crate csv;
use unicase::UniCase;
use std::collections::HashMap;
use std::path::Path;
use csv::Reader;

pub fn get_bnc_count() -> HashMap<UniCase<String>, u32> {
	// Create a CSV parser that reads data from stdin.
	let path_to_csv = Path::new("/Users/dougal/Projects/Key-BNC/rust/key_bnc_cli/BNC_wordlist.csv");
	let mut rdr = Reader::from_path(path_to_csv)
		.expect("Could not load BNC data file");
	// Loop over each record.
	rdr.records()
		.filter_map(|rec| rec.ok())
		.map(|rec| (UniCase::new(rec[2].parse::<String>().unwrap()), rec[1].parse::<u32>().unwrap()))
		.collect()
}
