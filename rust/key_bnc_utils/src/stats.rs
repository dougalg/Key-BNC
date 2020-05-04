pub fn log_likelyhood(target_freq: f64, target_corpus_size: f64, comparison_freq: f64, comparison_corpus_size: f64) -> f64 {
	let f1mil_1 = target_freq / target_corpus_size * 1_000_000.0;
	let f1mil_2 = comparison_freq / comparison_corpus_size * 1_000_000.0;

	let expected_freq_1 = target_corpus_size *
		(target_freq + comparison_freq) / (target_corpus_size + comparison_corpus_size);
	let expected_freq_2 = comparison_corpus_size *
		(target_freq + comparison_freq) / (target_corpus_size + comparison_corpus_size);

	let log1 = logdivision(target_freq, expected_freq_1);
	let log2 = logdivision(comparison_freq, expected_freq_2);

	let ll = 2.0 * ((target_freq * log1) + (comparison_freq * log2));

	if f1mil_1 < f1mil_2 {
		return -ll
	}

	ll
}

pub fn odds_ratio() -> f64 {
	123.0
}

pub fn dispersion() -> f64 {
	123.0
}

pub fn logdivision(target_freq: f64, expected_freq: f64) -> f64 {
	if expected_freq == 0.0 {
		return 0.0
	}
	let res = target_freq / expected_freq;
	res.ln()
}
