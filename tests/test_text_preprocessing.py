import unittest
from src.preprocessing.text_preprocessing import replace_chars, convert_to_list, cluster_preprocess

class TestTextPreprocessing(unittest.TestCase):
    """Test cases for text preprocessing functions."""
    
    def test_replace_chars(self):
        """Test the replace_chars function with various inputs."""
        # Test with no replacements
        self.assertEqual(replace_chars("Hello"), "Hello")
        
        # Test with single character replacement
        self.assertEqual(replace_chars("Hello", [('H', 'h')]), "hello")
        
        # Test with multiple character replacements
        self.assertEqual(replace_chars("Hello", [('H', 'h'), ('o', 'O')]), "hellO")
        
        # Test with empty string
        self.assertEqual(replace_chars("", [('a', 'b')]), "")
    
    def test_convert_to_list(self):
        """Test the convert_to_list function with various inputs."""
        # Test with default separators
        self.assertEqual(convert_to_list("Hello world"), ["Hello", "world"])
        
        # Test with custom separators
        self.assertEqual(convert_to_list("Hello-world", sep=['-']), ["Hello", "world"])
        
        # Test with multiple separators
        self.assertEqual(
            convert_to_list("Hello-world, test", sep=['-', ' ', ',']), 
            ["Hello", "world", "test"]
        )
        
        # Test with empty string
        self.assertEqual(convert_to_list(""), [])
    
    def test_cluster_preprocess(self):
        """Test the cluster_preprocess function with various inputs."""
        # Test with default parameters
        self.assertEqual(cluster_preprocess("Hello world"), ["Hello", "world"])
        
        # Test with custom separators and replacements
        self.assertEqual(
            cluster_preprocess("Hello-world", sep=['-'], chars_to_replace=[('H', 'h')]), 
            ["hello", "world"]
        )
        
        # Test with empty string
        self.assertEqual(cluster_preprocess(""), [])

if __name__ == '__main__':
    unittest.main()
