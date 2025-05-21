#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test suite for the ru_accent_poet package.
"""

import os
import re
import unittest
import tempfile
import tensorflow as tf
from ru_accent_poet import accent_line, write_file
from ru_accent_poet.rules import accent_line_rules
from ru_accent_poet.neuro import accent_neuro

# Suppress TensorFlow warnings for cleaner test output
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.get_logger().setLevel('ERROR')


class TestAccentLine(unittest.TestCase):
    """Test the accent_line function (combined approach)."""
    
    def test_basic_accentuation(self):
        """Test basic accentuation of simple phrases."""
        test_cases = [
            ("Мой дядя самых честных правил", 
             re.compile(r"Мой дя'дя са'мых че'стных пра'вил")),
            ("Когда не в шутку занемог", 
             re.compile(r"Когда' не в шу'тку занемо'г")),
            ("Он уважать себя заставил", 
             re.compile(r"Он уважа'ть себя' заста'вил")),
            ("И лучше выдумать не мог", 
             re.compile(r"И лу'чше вы'думать не мо[гк]'?")),
        ]
        
        for input_text, expected_pattern in test_cases:
            result = accent_line(input_text)
            self.assertRegex(result, expected_pattern, 
                f"Accentuation failed for '{input_text}', got '{result}'")
    
    def test_special_cases(self):
        """Test special cases: short words, 'ё', etc."""
        test_cases = [
            # Short word with one vowel - no accent needed
            ("Мой кот", re.compile(r"Мой ко'?т")),
            # Word with 'ё' - already has implicit stress
            ("Ещё мёд", re.compile(r"Ещё мёд")),
            # Short preposition - in non_str list
            ("Вышел изо льда", re.compile(r"Вы'шел изо льда")),
        ]
        
        for input_text, expected_pattern in test_cases:
            result = accent_line(input_text)
            self.assertRegex(result, expected_pattern, 
                f"Special case failed for '{input_text}', got '{result}'")
    
    def test_punctuation(self):
        """Test text with punctuation."""
        test_cases = [
            ("Привет, мир!", re.compile(r"Приве'т, мир!")),
            ("Жизнь — это сон.", re.compile(r"Жизнь — э'то сон.")),
            ("Чудная картина: как ты мне родна!", 
             re.compile(r"Чудна'я карти'на: как ты мне родна'!")),
        ]
        
        for input_text, expected_pattern in test_cases:
            result = accent_line(input_text)
            self.assertRegex(result, expected_pattern, 
                f"Punctuation test failed for '{input_text}', got '{result}'")
    
    def test_capitalization(self):
        """Test text with different capitalization."""
        test_cases = [
            ("РОССИЯ", re.compile(r"РОССИ'Я")),
            ("Москва", re.compile(r"Москва'")),
            ("санкт-ПЕТЕРБУРГ", re.compile(r"санкт-ПЕТЕРБУ'РГ")),
        ]
        
        for input_text, expected_pattern in test_cases:
            result = accent_line(input_text)
            self.assertRegex(result, expected_pattern, 
                f"Capitalization test failed for '{input_text}', got '{result}'")


class TestRulesAccentuation(unittest.TestCase):
    """Test the rules-based accentuation approach."""
    
    def test_dictionary_lookup(self):
        """Test dictionary-based accentuation using accent_line_rules."""
        test_cases = [
            # Common words that should be in the dictionary
            ("Россия", re.compile(r"Росси'я")),
            ("Москва", re.compile(r"Москва'")),
            # Words that may have multiple stresses in dictionary
            ("Правил", re.compile(r"Пра'ви'?л"))
        ]
        
        for input_text, expected_pattern in test_cases:
            result = accent_line_rules(input_text)
            self.assertRegex(result, expected_pattern, 
                f"Dictionary lookup failed for '{input_text}', got '{result}'")


class TestNeuroAccentuation(unittest.TestCase):
    """Test the neural network accentuation approach."""
    
    def test_neural_accentuation(self):
        """Test neural-based accentuation with PatchedAccent class."""
        # Simple tests to ensure neural accentuation produces a result with stress marks
        test_texts = [
            "Мой дядя самых честных правил",
            "Россия", 
            "Москва"
        ]
        
        for text in test_texts:
            # Use a temporary file to test accent_neuro which works on files
            with tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8', suffix='.txt', delete=False) as f:
                f.write(text)
                temp_filename = f.name
            
            try:
                # Run neural accentuation on the file
                accent_neuro([temp_filename])
                
                # Check if output file was created
                output_filename = re.sub(r'\.(?=[^.]+$)', '.nacc.', temp_filename)
                self.assertTrue(os.path.exists(output_filename), 
                    f"Output file {output_filename} was not created")
                
                # Check if it contains stress marks
                with open(output_filename, 'r', encoding='utf-8') as f:
                    result = f.read().strip()
                
                self.assertIn("'", result, 
                    f"Neural accentuation didn't add stress marks to '{text}', got '{result}'")
                
                # Clean up
                os.remove(output_filename)
            finally:
                os.remove(temp_filename)


class TestFileProcessing(unittest.TestCase):
    """Test file processing functions."""
    
    def test_write_file(self):
        """Test the write_file function for processing files."""
        test_texts = [
            "Мой дядя самых честных правил\nКогда не в шутку занемог",
            "Россия - священная наша держава",
            "Москва - столица России"
        ]
        
        for text in test_texts:
            # Create a temporary file for testing
            with tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8', suffix='.txt', delete=False) as f:
                f.write(text)
                temp_filename = f.name
            
            try:
                # Process the file
                write_file([temp_filename])
                
                # Check if output file was created
                output_filename = re.sub(r'\.(?=[^.]+$)', '.accented.', temp_filename)
                self.assertTrue(os.path.exists(output_filename), 
                    f"Output file {output_filename} was not created")
                
                # Check if it contains stress marks
                with open(output_filename, 'r', encoding='utf-8') as f:
                    result = f.read().strip()
                
                self.assertIn("'", result, 
                    f"File processing didn't add stress marks to '{text}', got '{result}'")
                
                # Clean up
                os.remove(output_filename)
            finally:
                os.remove(temp_filename)


if __name__ == '__main__':
    unittest.main()