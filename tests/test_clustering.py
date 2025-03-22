import unittest
import numpy as np
import pandas as pd
import sys
import os

# Add project root to system path to find modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import functions to test
from src.clustering.cluster_search import hash_strings, cluster_search, find_cluster


class TestHashStrings(unittest.TestCase):
    """Test cases for the hash_strings function."""
    
    def test_empty_list(self):
        """Test that an empty list produces an empty array."""
        result = hash_strings([])
        self.assertEqual(len(result), 0)
        self.assertIsInstance(result, np.ndarray)
    
    def test_single_string(self):
        """Test hashing a single string."""
        result = hash_strings(["test"])
        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], np.integer)
    
    def test_multiple_strings(self):
        """Test hashing multiple strings."""
        words = ["apple", "banana", "cherry"]
        result = hash_strings(words)
        self.assertEqual(len(result), len(words))
    
    def test_consistent_hashing(self):
        """Test that hashing the same string twice produces the same result."""
        word = "consistent"
        result1 = hash_strings([word])
        result2 = hash_strings([word])
        self.assertEqual(result1[0], result2[0])
    
    def test_different_strings_different_hashes(self):
        """Test that different strings have different hash values."""
        result = hash_strings(["apple", "orange"])
        # It's technically possible but extremely unlikely for two different strings 
        # to have the same hash
        self.assertNotEqual(result[0], result[1])
    
    def test_invalid_input_type(self):
        """Test that a TypeError is raised for non-list input."""
        with self.assertRaises(TypeError):
            hash_strings("not a list")
    
    def test_invalid_input_elements(self):
        """Test that a TypeError is raised for non-string elements."""
        with self.assertRaises(TypeError):
            hash_strings([1, 2, 3])
    
    def test_mixed_input_elements(self):
        """Test that a TypeError is raised for mixed element types."""
        with self.assertRaises(TypeError):
            hash_strings(["string", 123])


class TestClusterSearch(unittest.TestCase):
    """Test cases for the cluster_search function."""
    
    def test_identical_sequences(self):
        """Test with identical sequences."""
        sequence = np.array([1, 2, 3, 4, 5], dtype=np.int32)
        clusters, count = cluster_search(sequence, sequence, 3)
        
        # Should find one cluster with the entire sequence
        self.assertEqual(count, 1)
        self.assertEqual(clusters[0][0], 0)  # Start index in a
        self.assertEqual(clusters[0][1], 0)  # Start index in b
        self.assertEqual(clusters[0][2], 5)  # Length
    
    def test_partial_overlap(self):
        """Test with partially overlapping sequences."""
        a = np.array([1, 2, 3, 4, 5], dtype=np.int32)
        b = np.array([3, 4, 5, 6, 7], dtype=np.int32)
        
        # Should find one cluster with [3, 4, 5]
        clusters, count = cluster_search(a, b, 3)
        self.assertEqual(count, 1)
        self.assertEqual(clusters[0][0], 2)  # Start index in a (where 3 is)
        self.assertEqual(clusters[0][1], 0)  # Start index in b (where 3 is)
        self.assertEqual(clusters[0][2], 3)  # Length of the cluster
    
    def test_no_overlap(self):
        """Test with sequences that don't overlap."""
        a = np.array([1, 2, 3], dtype=np.int32)
        b = np.array([4, 5, 6], dtype=np.int32)
        
        # Should find no clusters
        clusters, count = cluster_search(a, b, 2)
        self.assertEqual(count, 0)
    
    def test_multiple_clusters(self):
        """Test finding multiple non-overlapping clusters."""
        a = np.array([1, 2, 3, 7, 8, 9], dtype=np.int32)
        b = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9], dtype=np.int32)
        
        # Should find two clusters
        clusters, count = cluster_search(a, b, 3)
        print(clusters)
        print(count)
        self.assertEqual(count, 2)
        
        # Sort clusters by start position for consistent testing
        sorted_clusters = sorted(clusters[:count], key=lambda x: x[0])
        
        # First cluster should be [1, 2, 3]
        self.assertEqual(sorted_clusters[0][0], 0)  # Start index in a
        self.assertEqual(sorted_clusters[0][1], 0)  # Start index in b
        self.assertEqual(sorted_clusters[0][2], 3)  # Length
        
        # Second cluster should be [7, 8, 9]
        self.assertEqual(sorted_clusters[1][0], 3)  # Start index in a
        self.assertEqual(sorted_clusters[1][1], 6)  # Start index in b
        self.assertEqual(sorted_clusters[1][2], 3)  # Length
    
    def test_minimum_length(self):
        """Test that clusters shorter than min_length are ignored."""
        a = np.array([1, 2, 3, 4, 5], dtype=np.int32)
        b = np.array([1, 2, 6, 7, 8], dtype=np.int32)
        
        # Should find one cluster of length 2
        clusters, count = cluster_search(a, b, 2)
        self.assertEqual(count, 1)
        self.assertEqual(clusters[0][2], 2)  # Length
        
        # Should find no clusters with min_length 3
        clusters, count = cluster_search(a, b, 3)
        self.assertEqual(count, 0)


class TestFindCluster(unittest.TestCase):
    """Test cases for the find_cluster function."""
    
    def test_basic_functionality(self):
        """Test the basic functionality with simple sequences."""
        a_seq = ["apple", "banana", "cherry", "date", "elderberry"]
        b_seq = ["apple", "banana", "fig", "grape", "honeydew"]
        
        result = find_cluster(a_seq, b_seq, min_length=2)
        
        # Should find one cluster with "apple", "banana"
        self.assertEqual(len(result), 1)
        self.assertEqual(result["length"].iloc[0], 2)
    
    def test_custom_names(self):
        """Test with custom sequence names."""
        a_seq = ["one", "two", "three"]
        b_seq = ["one", "two", "four"]
        
        result = find_cluster(a_seq, b_seq, min_length=2, a_name="sequence1", b_name="sequence2")
        
        # Check that custom names are used in column names
        self.assertIn("start_sequence1", result.columns)
        self.assertIn("end_sequence1", result.columns)
        self.assertIn("start_sequence2", result.columns)
        self.assertIn("end_sequence2", result.columns)
    
    def test_empty_sequences(self):
        """Test with empty sequences."""
        # Both sequences empty
        result = find_cluster([], [], min_length=1)
        self.assertEqual(len(result), 0)
        
        # One sequence empty
        result = find_cluster(["test"], [], min_length=1)
        self.assertEqual(len(result), 0)
    
    def test_no_clusters_found(self):
        """Test when no clusters meet the minimum length."""
        a_seq = ["one", "two", "three"]
        b_seq = ["four", "five", "six"]
        
        result = find_cluster(a_seq, b_seq, min_length=2)
        self.assertEqual(len(result), 0)
    
    def test_invalid_min_length(self):
        """Test with invalid minimum length."""
        with self.assertRaises(ValueError):
            find_cluster(["test"], ["test"], min_length=0)
    
    def test_invalid_sequence_types(self):
        """Test with invalid sequence types."""
        with self.assertRaises(TypeError):
            find_cluster("not a list", ["test"])
        
        with self.assertRaises(TypeError):
            find_cluster(["test"], "not a list")


if __name__ == "__main__":
    unittest.main()