#![cfg_attr(test, feature(test))]

pub mod stats;
pub mod utils;

#[cfg(test)]
mod benches;

#[cfg(test)]
mod utils_test;

#[cfg(test)]
mod stats_test;
