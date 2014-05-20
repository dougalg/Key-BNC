##LL OR BNC##

This is a simple application to help researchers calculate Log Likelihood (LL) and Odds Ratio (OR) statistics against a word list from the BNC.

Downloads are available under the "build" directory. Currently only windows versions are available, but if you have Python installed, you can run the source code directly on any platform.

###Tokenization###

The tokenizer splits on spaces. For punctuation, the rules are:
- If it is followed by a space, the punctuation is separated from the word.
- Double-quotation marks are ignored
- If it is a right single quote or apostrophe, it is separated from the preceding word

    "You're fine!" is tokenized as: "You", "'re", "fine", "!"

###Word List###

The BNC word list is a CSV file and can be located in LL_OR_BNC/Data directory. It is encoded in UTF8 which may cause some characters to display incorrectly in MS Excel.
