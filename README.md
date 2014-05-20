##LL OR BNC##

This is a simple application to help researchers calculate Log Likelihood (LL) and Odds Ratio (OR) statistics against a word list from the BNC.

Downloads are available under the "build" directory. Currently only Windows versions are available, but if you have Python installed, you can run the source code directly on any platform.

###Use###

1. Download the appropriate version
2. Unzip the folder. Note that ALL contents of the folder are necessary, do not remove any of them. If you need to move the .exe file, move the entire folder together
3. Run the executable file from the folder by double-clicking it
4. Click the "load corpus" button to load a **folder** of **utf8 text files** (this means the files should be *.txt not .csv or .xml)
5. The program will create a word frequency list from your corpus and use it to calculate LL and OR against the BNC[1]. Results are sorted by frequency, but you can save the results as a CSV and sort them by other criteria using MS Excel, LibreOffice, or similar programs.

[1]: Note that the running time will depend on your corpus size. If your corpus is large, it may take some time to run the calculations, so please be patient. Results are displayed when complete.

###Tokenization###

The tokenizer splits on spaces, and converts upper case letters to lower. For punctuation, the rules are:

1. If it is followed by a space, the punctuation is separated from the word.
2. Double-quotation marks, parentheses, and braces are ignored
3. If it is a right single quote or apostrophe, it is separated from the preceding word

EG:

    "You're fine, fire-truck!" --> "You", "'re", "fine", ",", "fire-truck", "!"

###Word List###

The BNC word list is a CSV file and can be located in LL_OR_BNC/Data directory. It is encoded in UTF8 which may cause some characters to display incorrectly in MS Excel.
