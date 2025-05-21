# ru_accent_poet Workflow Guide

This document provides a detailed explanation of how the Russian text accentuation process works in the ru_accent_poet package.

## Overview

The ru_accent_poet package uses a hybrid approach to add stress marks to Russian text, combining:
1. A dictionary/rules-based approach
2. A neural network approach

This hybrid method ensures high accuracy across a wide range of Russian words, including those that may not appear in dictionaries.

## Workflow Steps

### 1. Text Processing

When you call `accent_line()` with a line of Russian text, the following happens:

```python
from ru_accent_poet import accent_line
accented_text = accent_line("Мой дядя самых честных правил")
```

The function:
1. Splits the input text into individual words
2. Processes each word separately
3. Rejoins the words with their stress marks

### 2. Rules-Based Processing

For each word, the package first attempts to apply dictionary-based rules:

```python
words_rule = accent_line_rules(line).split()
```

The `accent_line_rules()` function:
1. Uses the dictionary files `accent.dic` and `accent1.dic` containing over 1 million Russian words with their correct stress marks
2. Looks up each word in the dictionary
3. Returns the word with stress marks if found
4. May return multiple stress marks per word (for words with alternative pronunciations)

### 3. Neural Network Processing

In parallel, the neural network model is applied to each word:

```python
words_nacc = accent.put_stress(line).split()
```

The neural approach:
1. Uses a Bidirectional LSTM model trained on Russian text
2. Predicts the most likely position for a stress mark
3. Always returns exactly one stress mark per word (if the word has vowels)

### 4. Decision Logic

For each word, the package decides which result to use based on specific criteria:

```python
if (len(re.findall("'", words_rule[j])) > 1) or \
   ("'" not in words_rule[j] and not re.findall('[ёЁ]', words_rule[j])) or \
   ("'" in words_rule[j] and re.findall('[ёЁ]', words_rule[j])):
    words[j] = words_nacc[j]  # Use neural network result
else:
    words[j] = words_rule[j]  # Use dictionary result
```

The neural network result is used when:
1. The dictionary returns multiple stress marks for a word
2. The dictionary doesn't provide any stress marks for a word
3. There's an inconsistency with the letter 'ё' (which already implies stress)

Otherwise, the dictionary result is used.

### 5. Special Cases

The package handles several special cases:
1. Words with a single vowel (no stress needed)
2. Words containing the letter 'ё' (already implies stress)
3. Short prepositions and particles like 'обо', 'изо', 'подо', 'нибудь'
4. Words not in the dictionary are handled by the neural network

## Command-Line Usage

The package can be used to process entire files:

```bash
python -m ru_accent_poet file1.txt file2.txt
```

This creates new files with `.accented.` added to the filename, containing the original text with stress marks added.

## Programmatic Usage

```python
# Process a single line
from ru_accent_poet import accent_line
result = accent_line("Мой дядя самых честных правил")
print(result)  # Outputs: "Мой дя'дя са'мых че'стных пра'вил"

# Process files
from ru_accent_poet import write_file
write_file(["file1.txt", "file2.txt"])

# Use only the neural network approach
from ru_accent_poet.neuro import accent_neuro
accent_neuro(["file1.txt"])  # Creates files with .nacc. extension

# Use only the dictionary approach
from ru_accent_poet.rules import accent_rules
accent_rules(["file1.txt"])  # Creates files with .acc. extension
```

## Technical Implementation

1. The dictionary approach uses a trie-based structure for efficient word lookup
2. The neural network is a Bidirectional LSTM model trained on a large corpus of Russian poetry
3. The TensorFlow/Keras implementation has been updated to work with modern versions (TensorFlow 2.15+ and Keras 3.x)
4. The package includes a custom patched version of the russtress Accent class for compatibility

## Error Handling and Edge Cases

The package handles several edge cases:
1. Words not in the dictionary
2. Foreign words in Cyrillic
3. Proper nouns and rare words
4. Words with multiple possible stress positions

By combining dictionary-based and neural approaches, the package provides robust accentuation even for difficult or ambiguous cases.

## Extending the Package

You can extend the package by:
1. Adding more words to the dictionary files
2. Retraining the neural model on specialized text
3. Modifying the decision logic to prefer one approach over the other

For most users, the default hybrid approach offers the best balance of accuracy and coverage.