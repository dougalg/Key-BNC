# About

This is a web-based front-end for Key-BNC built on top of the key_bnc_utils package.

This application has two parts:
1. A rust data processor compiling to WASM
2. A vue.js front-end ([the README file in the www subfolder](./www/README.md))

## Installing

1. Install wasm-pack
2. Install dependencies: `cargo update`

## Building

1. First build the WASM
2. Then, build the web app

### WASM

```sh
wasm-pack build
```

### Web Application

See [the README file in the www subfolder](./www/README.md) for more details.
