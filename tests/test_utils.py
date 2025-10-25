"""
Unit tests for utility functions.
"""

import unittest
import pandas as pd
from src.utils import (
    get_specimen_id, extract_core_tcga_id,
    convert_counts_to_proportions, categorize_columns_train
)


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""
    
    def test_get_specimen_id(self):
        """Test specimen ID extraction."""
        full_id = "SBS::SA123456"
        result = get_specimen_id(full_id)
        self.assertEqual(result, "SA123456")
    
    def test_extract_core_tcga_id(self):
        """Test TCGA ID extraction."""
        full_id = "tcga-br-1234-01a-11d"
        result = extract_core_tcga_id(full_id)
        self.assertEqual(result, "tcga-br-1234")
        
        # Test with None
        result = extract_core_tcga_id("invalid-id")
        self.assertIsNone(result)
    
    def test_convert_counts_to_proportions(self):
        """Test count to proportion conversion."""
        df = pd.DataFrame({
            'A': [10, 20, 30],
            'B': [20, 30, 40],
            'C': [70, 50, 30]
        })
        
        result = convert_counts_to_proportions(df, ['A', 'B', 'C'])
        
        # Check that rows sum to 1
        row_sums = result[['A', 'B', 'C']].sum(axis=1)
        for s in row_sums:
            self.assertAlmostEqual(s, 1.0, places=5)
    
    def test_categorize_columns_train(self):
        """Test column categorization for training data."""
        df = pd.DataFrame({
            'CN1:het:1': [1, 2, 3],
            'A>C': [4, 5, 6],
            'DEL_1': [7, 8, 9],
            'INS_2': [10, 11, 12],
            'A_C_G_T': [13, 14, 15]
        })
        
        sbs_cols, dbs_cols, indel_cols = categorize_columns_train(df)
        
        # Check SBS columns
        self.assertIn('CN1:het:1', sbs_cols)
        self.assertIn('A>C', sbs_cols)
        
        # Check indel columns
        self.assertIn('DEL_1', indel_cols)
        self.assertIn('INS_2', indel_cols)


if __name__ == '__main__':
    unittest.main()

