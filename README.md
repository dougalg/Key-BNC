## Key-BNC

This is a simple application to help researchers calculate Log Likelihood (LL) and Odds Ratio (OR) statistics against a word list from the BNC.

## Installation

Key-BNC is currently available as an online web-based application at https://key-bnc.tfiaa.com/. All future versions will
be distributed there. For historical reasons, the downloadable python versions are available below.

## Download

Versions of Key-BNC <= 1.2 are available to download:

1. [Windows 32-Bit](https://github.com/dougalg/Key-BNC/raw/master/build/Key-BNC-current-win32.zip) (v1.2)
2. [Windows 64-Bit](https://github.com/dougalg/Key-BNC/raw/master/build/Key-BNC-current-amd64.zip) (v1.2)
3. [Mac OSX 64-Bit](https://github.com/dougalg/Key-BNC/raw/master/build/Key-BNC-current-mac.zip) (v1.2)
4. [BNC Wordlist](https://github.com/dougalg/Key-BNC/blob/master/KEY_BNC/Data/BNC_wordlist.csv?raw=true)

### Tokenization

The tokenizer splits on spaces, and converts upper case letters to lower. For punctuation, the rules are:

1. If it is followed by a space, the punctuation is separated from the word.
2. Most punctuation counts as a word boundary (but is not included in words).
3. Numbers may contain: 0-9, commans, periods, and semi-colors (eg: 12:45, or 1,300.00).
4. Single quotes split a word in two and are attached to the second word.

EG:

    You're fine, fire-truck!
    you 're fine fire truck

    "'Tis", replied Aunt Helga.
    tis replied aunt helga

    Don't tell someone what they can or can't do
    don 't tell someone what they can or can 't do

    There are 100,000,000,000.00 words in the BNC.
    there are 100,000,000,000.00 words in the bnc


### Word List

The BNC word list is a CSV file and can be located in LL_OR_BNC/Data directory. It is encoded in UTF8 which may cause some characters to display incorrectly in MS Excel.
