use std::f64::{INFINITY};

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

	if f64::is_nan(ll) {
		return 0.0
	}

	if f1mil_1 < f1mil_2 {
		return -ll
	}

	ll
}

pub fn odds_ratio(
	target_freq: f64,
	target_corpus_size: f64,
	comparison_freq: f64,
	comparison_corpus_size: f64,
	zero_adjustment: f64,
) -> f64 {
	let mut a = target_freq;
	let mut b = target_corpus_size - target_freq;
	let mut c = comparison_freq;
	let mut d = comparison_corpus_size - comparison_freq;

	if b == 0.0 || c == 0.0 || d == 0.0 {
		a += zero_adjustment;
		b += zero_adjustment;
		c += zero_adjustment;
		d += zero_adjustment;
	}

	if a == 0.0 || b == 0.0 || c == 0.0 || d == 0.0 {
		return INFINITY
	}
	(a/b)/(c/d)
}

pub fn logdivision(target_freq: f64, expected_freq: f64) -> f64 {
	if expected_freq == 0.0 {
		return 0.0
	}
	let res = target_freq / expected_freq;
	res.ln()
}

pub fn dispersion_normalized(s_v: &[(f64, f64)], f: f64) -> f64 {
	let min_s = s_v.iter()
		.map(|(s, _v)| s)
		.cloned()
		.fold(1.0, f64::min);

	if min_s >= 1.0 {
		return 0.0;
	}

	dispersion(s_v, f) / (1.0 - min_s)
}


pub fn dispersion(s_v: &[(f64, f64)], f: f64) -> f64 {
	let calculated_parts: f64 = s_v.iter()
		.map(|(s, v)| calculate_part_value(*s, *v, f))
		.sum();

	0.5 * calculated_parts
}

fn calculate_part_value(size_percentage: f64, frequency: f64, overall_frequency: f64) -> f64 {
	((frequency / overall_frequency) - size_percentage).abs()
}
