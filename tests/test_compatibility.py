#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test suite to verify TensorFlow/Keras compatibility.
"""

import os
import unittest
import tensorflow as tf
from ru_accent_poet.patch_russtress import PatchedAccent

# Suppress TensorFlow warnings for cleaner test output
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.get_logger().setLevel('ERROR')


class TestTensorFlowCompatibility(unittest.TestCase):
    """Test TensorFlow and Keras compatibility."""
    
    def test_tensorflow_version(self):
        """Test that TensorFlow version is >= 2.15.0."""
        tf_version = tf.__version__
        major, minor = map(int, tf_version.split(".")[:2])
        
        self.assertTrue(
            (major > 2) or (major == 2 and minor >= 15),
            f"TensorFlow version {tf_version} is less than 2.15.0"
        )
    
    def test_keras_version(self):
        """Test that Keras version is >= 3.0.0."""
        keras_version = tf.keras.__version__
        major = int(keras_version.split(".")[0])
        
        self.assertTrue(
            major >= 3,
            f"Keras version {keras_version} is less than 3.0.0"
        )
    
    def test_patched_accent_initialization(self):
        """Test that PatchedAccent class can be initialized without errors."""
        try:
            patched_accent = PatchedAccent()
            self.assertIsNotNone(patched_accent, "PatchedAccent was not initialized properly")
            self.assertIsNotNone(patched_accent.model, "Neural model was not initialized properly")
        except Exception as e:
            self.fail(f"PatchedAccent initialization raised exception: {e}")
    
    def test_prediction_shape(self):
        """Test that model prediction produces expected output shape."""
        patched_accent = PatchedAccent()
        
        # Create a simple input (batch size 1, max length, char indices)
        from russtress.constants import MAXLEN, CHAR_INDICES
        import numpy as np
        
        # Create dummy input - a batch of one word
        x = np.zeros((1, MAXLEN, len(CHAR_INDICES)), dtype=bool)
        
        # The word "Москва"
        word = "москва"
        for index, letter in enumerate(word):
            if letter in CHAR_INDICES:
                pos = MAXLEN - len(word) + index
                if pos >= 0 and pos < MAXLEN:
                    x[0, pos, CHAR_INDICES[letter]] = 1
        
        # Run prediction
        prediction = patched_accent.model.predict(x, verbose=0)
        
        # Check output shape - should be (1, X) where X is the number of positions
        self.assertEqual(len(prediction.shape), 2, f"Prediction has wrong shape: {prediction.shape}")
        self.assertEqual(prediction.shape[0], 1, f"Batch dimension is not 1: {prediction.shape}")
    
    def test_predict_method(self):
        """Test that _predict method works correctly."""
        patched_accent = PatchedAccent()
        
        # Test with a simple word
        result = patched_accent._predict("москва")
        
        # Check that it added a stress mark
        self.assertIn("'", result, f"No stress mark was added to 'москва', got: {result}")
        
        # Check that only one stress mark was added
        stress_count = result.count("'")
        self.assertEqual(stress_count, 1, f"Expected 1 stress mark, got {stress_count} in: {result}")
    
    def test_put_stress_method(self):
        """Test that put_stress method works correctly."""
        patched_accent = PatchedAccent()
        
        # Test with a simple phrase
        result = patched_accent.put_stress("Москва река")
        
        # Check that it processed the text
        self.assertIsNotNone(result, "put_stress returned None")
        self.assertNotEqual(result, "", "put_stress returned empty string")
        
        # Check that it added stress marks
        self.assertIn("'", result, f"No stress marks were added to 'Москва река', got: {result}")


if __name__ == '__main__':
    unittest.main()