# Key-BNC Frontend

## Setup

Requires `yarn`.

### Install

```
yarn install
```

### Build the WASM

You will need to build the rust wasm application first. See parent directory's README.md.


### Run locally

```
yarn serve
```

## Build 

```
yarn build --mode=production
```

*NOTE*: Sometimes this needs to be run twice in a row, after a `Parsing error: The keyword 'import' is reserved` error.

## Deploy

After building, deploy with `yarn deploy`. Requires a valid SSH key for the server.
