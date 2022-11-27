# GOKTU_NLP - TURKISH NLP PREPROCESSING TOOLBOX

> **Note**
> This toolbox is prepared for CMPE561 Natural Language Processing course given by Prof. Dr. Tunga Gungor in Boğaziçi University.

This Turkish NLP Preprocessing Toolbox have 5 functionalities:
- Tokenizer
    - Regex Based
    - Logistic Regression Based
- Sentence Splitter
    - Regex Based
    - Naive Bayesian Method Based
- Normalizer
- Stemmer
- Stopword Eliminator

## How to use toolbox?

### Tokenizer

```python
from nlp_preprocessing_toolbox.tokenizer import Tokenizer, TokenizerML

text = "..."

#for Regex Based tokenizer
tokenizer = Tokenizer()
tokenizer.setText(text)
tokenizer.run()
tokens = tokenizer.tokens

#for Logistic Regression based tokenizer
tokenizer = TokenizerML()
tokenizer.setText(text)
tokenizer.run()
tokens = tokenizer.tokens
```

### Sentence Splitter

```python
from nlp_preprocessing_toolbox.sentence_splitter import SentenceSplitter, SentenceSplitterML

text = "..."

#for Regex Based sentence splitter
sentSplit = SentenceSplitter()
sentSplit.setText(text)
sentSplit.run()
sentences = sentSplit.sentences

#for Naive Bayesian based sentence splitter
sentSplit = SentenceSplitterML()
sentSplit.setText(text)
sentSplit.run()
sentences = sentSplit.sentences
```

### Normalizer

```python
from nlp_preprocessing_toolbox.normalizer import Normalizer

words = [...] # a list of tokens

normalizer = Normalizer()
normalizer.setText(words)
normalized_tokens = normalizer.new_words
```

### Stemmer

```python
from nlp_preprocessing_toolbox.stemmer import Stemmer

words = [...] # a list of tokens

stemmer = Stemmer()
stemmer.setText(words)
stems = stemmer.stems
```

### Stopword Eliminator

```python
from nlp_preprocessing_toolbox.stopword_elimination import stopword_elimination

words = [...] # a list of tokens or stems

words = stopword_elimination(words)
```
