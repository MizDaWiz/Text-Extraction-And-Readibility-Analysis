# Text-Extraction-And-Readibility-Analysis

The text from the articles in each of the links in the Input sheet was extracted and stored in separate text files. Each file was then filtered for stop words<br/>
Following this, each article was tokenized into 3 kinds of sequences using word_tokenize, sent_tokenize and SyllableTokenizer from nltk's nltk.tokenize module[punkt had to be downloaded]
Using these tokens and few lists of positive and negative words, the following metrics for each article were calculated and stored in the output excel sheet:
For sentiment analysis-<br/>
1. Positive Score
2. Negative Score
3. Polarity Score
4. Subjectivity Score
For readibility analysis-<br/>
5. Percentage of Complex words(>2 syllables)
6. Fog Index
7. Average Words per sentence
8. Word Count
9. Personal Pronouns
10. Average word length
