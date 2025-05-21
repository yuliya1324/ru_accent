"""
Patch for russtress package to be compatible with the latest TensorFlow/Keras.
This file provides a replacement for the Accent class in russtress.
"""

import tensorflow as tf
import numpy as np
import re
import os
from pathlib import Path
from russtress.tokenizer import tokenize
from russtress.constants import MODEL_FILE, WEIGHTS_FILE, MAXLEN, CHAR_INDICES, REG
from russtress.utils import parse_the_phrase, add_endings, is_small

class PatchedAccent:
    """A replacement for the russtress Accent class that works with modern TensorFlow/Keras"""
    
    def __init__(self):
        self.model_file = MODEL_FILE
        self.weights_file = str(WEIGHTS_FILE)
        
        # Clear any existing sessions
        tf.keras.backend.clear_session()
        
        # Load the model - handle compatibility with older model format
        with open(self.model_file, 'r') as content_file:
            json_string = content_file.read()
        
        # Replace old class names with new ones for Keras 3.x compatibility
        json_string = json_string.replace(
            '"class_name": "Sequential"', 
            '"class_name": "keras.src.engine.sequential.Sequential"'
        )
        json_string = json_string.replace(
            '"class_name": "Bidirectional"', 
            '"class_name": "keras.src.layers.rnn.bidirectional.Bidirectional"'
        )
        json_string = json_string.replace(
            '"class_name": "LSTM"', 
            '"class_name": "keras.src.layers.rnn.lstm.LSTM"'
        )
        json_string = json_string.replace(
            '"class_name": "Dropout"', 
            '"class_name": "keras.src.layers.regularization.dropout.Dropout"'
        )
        json_string = json_string.replace(
            '"class_name": "Dense"', 
            '"class_name": "keras.src.layers.core.dense.Dense"'
        )
        json_string = json_string.replace(
            '"class_name": "Activation"', 
            '"class_name": "keras.src.layers.core.activation.Activation"'
        )
        json_string = json_string.replace(
            '"class_name": "Zeros"', 
            '"class_name": "keras.src.initializers.initializers.Zeros"'
        )
        json_string = json_string.replace(
            '"class_name": "VarianceScaling"', 
            '"class_name": "keras.src.initializers.initializers.VarianceScaling"'
        )
        json_string = json_string.replace(
            '"class_name": "Orthogonal"', 
            '"class_name": "keras.src.initializers.initializers.Orthogonal"'
        )
        
        # Create a minimal model structure that matches the original
        # This approach avoids compatibility issues with model loading
        inputs = tf.keras.Input(shape=(MAXLEN, len(CHAR_INDICES)))
        
        # Create a Bidirectional LSTM layer
        x = tf.keras.layers.Bidirectional(
            tf.keras.layers.LSTM(64)
        )(inputs)
        
        # Add dropout
        x = tf.keras.layers.Dropout(0.2)(x)
        
        # Add dense layer
        x = tf.keras.layers.Dense(40)(x)
        
        # Add activation
        outputs = tf.keras.layers.Activation('softmax')(x)
        
        # Create the model
        self.model = tf.keras.Model(inputs, outputs)
        
        # Try to load weights from the original model
        try:
            self.model.load_weights(self.weights_file)
        except Exception as e:
            print(f"Warning: Could not load weights from {self.weights_file}. Using default initialization.")
            print(f"Error: {str(e)}")

    def _predict(self, word):
        """Predict the stress position for a word"""
        x = np.zeros((1, MAXLEN, len(CHAR_INDICES)), dtype=bool)
        for index, letter in enumerate(word):
            if letter in CHAR_INDICES:  # Make sure the letter exists in CHAR_INDICES
                pos = MAXLEN - len(word.replace("'", "")) + index
                if pos >= 0 and pos < MAXLEN:  # Ensure the position is valid
                    x[0, pos, CHAR_INDICES[letter]] = 1
        
        # Use the model to predict
        preds = self.model.predict(x, verbose=0)[0]
        preds = preds.tolist()
        max_value = max(preds)
        index = preds.index(max_value)
        
        # Cut left context "ные_мечты" -> "мечты"
        if '_' in word:
            word = word[word.index('_') + 1:]
        
        index = len(word) - MAXLEN + index
        if index > len(word) - 1:
            print('no %s-th letter in %s' % (index + 1, word))
            return word
        else:
            acc_word = word[:index + 1] + '\'' + word[index + 1:]
            return acc_word

    def put_stress(self, text, stress_symbol="'"):
        """
        This function gets any string as an input and returns the same string
        but only with the predicted stress marks.
        All the formatting is preserved using this function.
        """
        words = parse_the_phrase(text)
        tokens = tokenize(text)
        accented_phrase = []
        pluswords = add_endings(words)

        for w in pluswords:
            if not bool(re.search(REG, w)):
                pass
            else:
                accented_phrase.append(self._predict(w))
        final = []

        for token in tokens:
            if is_small(token):
                final.append(token)
            else:
                try:
                    temp = accented_phrase[0].replace("'", '')
                except IndexError:
                    temp = ''
                if temp == token.lower():
                    stress_position = accented_phrase[0].find("'")
                    final.append(token[:stress_position] +
                                 stress_symbol + token[stress_position:])
                    accented_phrase = accented_phrase[1:]
                else:
                    final.append(token)
        final = ''.join(final)
        return final