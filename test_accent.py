#!/usr/bin/env python
# Test script for ru_accent_poet with the latest TensorFlow/Keras

import os
import tensorflow as tf
from ru_accent_poet import accent_line
from ru_accent_poet.rules import accent_line_rules

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.get_logger().setLevel('ERROR')

def test_accent():
    print("TensorFlow version:", tf.__version__)
    print("Keras version:", tf.keras.__version__)
    
    sample_texts = [
        "Мой дядя самых честных правил",
        "Когда не в шутку занемог",
        "Он уважать себя заставил",
        "И лучше выдумать не мог"
    ]
    
    print("\nAccenting Russian text (combined approach):")
    print("-" * 40)
    
    for text in sample_texts:
        accented_text = accent_line(text)
        print(f"Original: {text}")
        print(f"Accented: {accented_text}")
        print()
    
    print("\nAccenting Russian text (rules-based only, using dictionaries):")
    print("-" * 60)
    
    for text in sample_texts:
        rules_accented_text = accent_line_rules(text)
        print(f"Original: {text}")
        print(f"Accented: {rules_accented_text}")
        print()
    
    print("Test completed successfully!")

if __name__ == "__main__":
    test_accent()