# About

This is a web-based front-end for Key-BNC built on top of the key_bnc_utils package.

This application has two parts:
1. A rust data processor compiling to WASM (located in `./key_bnc_wasm`)
2. A vue.js front-end (Here)

## Installing

1. Install rust, and rust toolchain
1. Install wasm-pack
1. Install JS dependencies: `yarn`
1. Build the wasm to generate the typescript typings: `yarn wasm`

## Development

The development script will automatically build the wasm and all web assets as well:

`yarn dev`

## Building

The wasm file and js/html/etc. will all be built as part of the vite build process:

`yarn build`

or

`yarn build --production`

### Build WASM Only

`yarn wasm`

## Deploy

After building, deploy with `yarn deploy`. Requires a valid SSH key for the server.
