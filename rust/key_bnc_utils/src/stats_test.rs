use crate::stats::{
	log_likelyhood,
	odds_ratio,
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
