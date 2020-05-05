use std::f64::{INFINITY};
use crate::stats::{
	log_likelyhood,
	odds_ratio,
	dispersion_normalized,
	dispersion,
	logdivision,
};

#[test]
fn ll_1() {
	assert_eq!(log_likelyhood(1.0, 2.0, 3.0, 4.0), -0.131_334_069_034_738_88)
}

#[test]
fn ll_2() {
	assert_eq!(log_likelyhood(200.0, 80_000.0, 2_546.0, 10_000_000.0), 542.187_152_406_053_2)
}

#[test]
fn logdivision_1() {
	assert_eq!(logdivision(12.0, 4.0), 1.098_612_288_668_109_8);
}

#[test]
fn logdivision_2() {
	assert_eq!(logdivision(100.0, 0.0), 0.0);
}

#[test]
fn odds_ratio_1() {
	assert_eq!(odds_ratio(12.0, 24.0, 12.0, 24.0, 0.0), 1.0);
}

#[test]
fn odds_ratio_2() {
	assert_eq!(odds_ratio(100.0, 105.0, 12.0, 24.0, 0.0), 20.0);
}

#[test]
fn odds_ratio_3_division_by_zero_gives_infinity() {
	assert_eq!(odds_ratio(12.0, 12.0, 100.0, 1_000.0, 0.0), INFINITY);
}

#[test]
fn odds_ratio_4_zero_adjustment() {
	assert_eq!(odds_ratio(12.0, 12.0, 100.0, 1_000.0, 0.5), 224.004_975_124_378_12);
}

#[test]
fn odds_ratio_5() {
	let ten: f64 = 10.0;
	assert_eq!(odds_ratio(1.0, 10_000_000.0, ten.powi(-9), 1_000_000_000_000.0, 0.0), 100_000_010_000_000.98);
}

#[test]
fn dp_1() {
	let s_v = vec![
		(0.18, 1.0),
		(0.2, 2.0),
		(0.2, 3.0),
		(0.2, 4.0),
		(0.22, 5.0),
	];
	let f = 15.0;
	assert_eq!(dispersion(&s_v, f), 0.18);
}

#[test]
fn dispersion_normalized_1() {
	let s_v = vec![
		(0.18, 1.0),
		(0.2, 2.0),
		(0.2, 3.0),
		(0.2, 4.0),
		(0.22, 5.0),
	];
	let f = 15.0;
	assert_eq!(dispersion_normalized(&s_v, f), 0.219_512_195_121_951_2);
}

#[test]
fn dispersion_normalized_2() {
	let s_v = vec![
		(0.9, 9.0),
		(0.1, 1.0),
	];
	let f = 10.0;
	assert_eq!(dispersion_normalized(&s_v, f), 0.0);
}

#[test]
fn dispersion_normalized_3() {
	let s_v = vec![
		(0.9, 10.0),
		(0.1, 0.0),
	];
	let f = 10.0;
	assert_eq!(dispersion_normalized(&s_v, f), 0.111_111_111_111_111_1);
}

#[test]
fn dispersion_normalized_4() {
	let s_v = vec![
		(1.0, 10.0),
	];
	let f = 10.0;
	assert_eq!(dispersion_normalized(&s_v, f), 0.0);
}
