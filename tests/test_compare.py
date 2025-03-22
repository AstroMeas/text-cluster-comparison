import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add project root to system path to find modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import functions to test
from src.clustering.compare import compare_texts, filter_ordered_clusters


class TestOrderedClusters(unittest.TestCase):
    """Test cases for the filter_ordered_clusters function and related functionality."""
    
    def setUp(self):
        """Set up test data."""
        # Regular sequences
        self.a = ["word1", "word2", "word3", "word4", "word5", "word6"]
        
        # Sequences with out-of-order clusters
        self.b_disordered = ["other1", "word3", "word4", "other2", "word1", "word2"] 
        
        # DataFrame with out-of-order clusters
        self.disordered_clusters = pd.DataFrame({
            "start_a": [0, 2],       # word1-word2 and word3-word4
            "end_a": [2, 4],
            "start_b": [4, 1],       # Notice that word1-word2 appears AFTER word3-word4 in text B
            "end_b": [6, 3],
            "length": [2, 2],
            "differenz": [4, -1]
        })
        
        # DataFrame with ordered clusters
        self.ordered_clusters = pd.DataFrame({
            "start_a": [0, 2],       # word1-word2 and word3-word4
            "end_a": [2, 4],
            "start_b": [1, 3],       # Both clusters appear in same order
            "end_b": [3, 5],
            "length": [2, 2],
            "differenz": [1, 1]
        })
    
    def test_filter_ordered_clusters_with_ordered_input(self):
        """Test filter_ordered_clusters with already-ordered clusters."""
        result = filter_ordered_clusters(self.ordered_clusters)
        
        # Should return all clusters unchanged
        self.assertEqual(len(result), len(self.ordered_clusters))
        np.testing.assert_array_equal(result["start_a"].values, self.ordered_clusters["start_a"].values)
        np.testing.assert_array_equal(result["start_b"].values, self.ordered_clusters["start_b"].values)
    
    def test_filter_ordered_clusters_with_disordered_input(self):
        """Test filter_ordered_clusters with out-of-order clusters."""
        result = filter_ordered_clusters(self.disordered_clusters)
        
        # Should filter out clusters that break the ordering
        self.assertLess(len(result), len(self.disordered_clusters))
        # Specifically, it should pick either the first or second cluster, but not both
        self.assertEqual(len(result), 1)
    
    def test_filter_ordered_clusters_with_empty_input(self):
        """Test filter_ordered_clusters with empty input."""
        empty_df = pd.DataFrame()
        result = filter_ordered_clusters(empty_df)
        
        # Should return empty DataFrame
        self.assertTrue(result.empty)
    
    def test_filter_ordered_clusters_with_single_cluster(self):
        """Test filter_ordered_clusters with a single cluster."""
        single_cluster = pd.DataFrame({
            "start_a": [0],
            "end_a": [2],
            "start_b": [1],
            "end_b": [3],
            "length": [2],
            "differenz": [1]
        })
        
        result = filter_ordered_clusters(single_cluster)
        
        # Should return the single cluster unchanged
        self.assertEqual(len(result), 1)
        self.assertEqual(result["start_a"].iloc[0], single_cluster["start_a"].iloc[0])
        self.assertEqual(result["start_b"].iloc[0], single_cluster["start_b"].iloc[0])
    
    def test_compare_texts_with_order_enforcement(self):
        """Test compare_texts with order enforcement enabled."""
        result = compare_texts(self.a, self.b_disordered, self.disordered_clusters)
        
        # Should only include the cluster that maintains ordering
        self.assertEqual(sum(result["tag"] == "cluster"), 1)
    
    def test_compare_texts_without_order_enforcement(self):
        """Test compare_texts with order enforcement disabled."""
        result = compare_texts(self.a, self.b_disordered, self.disordered_clusters, enforce_order=False)
        
        # Should include both clusters, which will create a non-linear reading flow
        # But for some applications this might be desired
        self.assertEqual(sum(result["tag"] == "cluster"), 2)


if __name__ == "__main__":
    unittest.main()