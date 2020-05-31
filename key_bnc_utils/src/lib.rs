#![cfg_attr(test, feature(test))]

pub mod utils;
pub mod stats;

#[cfg(test)]
mod benches;

#[cfg(test)]
mod utils_test;

#[cfg(test)]
mod stats_test;
