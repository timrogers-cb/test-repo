"""
Tests for the Shiba Inu module.
"""

import unittest
from shiba_inu import ShibaInu, count_shiba_inus, get_oldest_shiba


class TestShibaInu(unittest.TestCase):
    """Test cases for the ShibaInu class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.shiba = ShibaInu("Hachi", age=5, color="red")
        self.puppy = ShibaInu("Yuki", age=0, color="cream")
        
    def test_init_with_all_parameters(self):
        """Test ShibaInu initialization with all parameters."""
        shiba = ShibaInu("Test", age=3, color="black and tan")
        self.assertEqual(shiba.name, "Test")
        self.assertEqual(shiba.age, 3)
        self.assertEqual(shiba.color, "black and tan")
        self.assertEqual(shiba.breed, "Shiba Inu")
        
    def test_init_with_minimal_parameters(self):
        """Test ShibaInu initialization with only required parameters."""
        shiba = ShibaInu("Minimal")
        self.assertEqual(shiba.name, "Minimal")
        self.assertIsNone(shiba.age)
        self.assertEqual(shiba.color, "red")
        self.assertEqual(shiba.breed, "Shiba Inu")
        
    def test_bark(self):
        """Test the bark method."""
        self.assertEqual(self.shiba.bark(), "Woof!")
        self.assertEqual(self.puppy.bark(), "Woof!")
        
    def test_get_info_with_age(self):
        """Test get_info method when age is provided."""
        expected = "Name: Hachi, Breed: Shiba Inu, Color: red, Age: 5 years"
        self.assertEqual(self.shiba.get_info(), expected)
        
    def test_get_info_without_age(self):
        """Test get_info method when age is not provided."""
        shiba_no_age = ShibaInu("Ageless", color="sesame")
        expected = "Name: Ageless, Breed: Shiba Inu, Color: sesame"
        self.assertEqual(shiba_no_age.get_info(), expected)
        
    def test_is_adult_true(self):
        """Test is_adult method returns True for adult dogs."""
        self.assertTrue(self.shiba.is_adult())
        
    def test_is_adult_false(self):
        """Test is_adult method returns False for young dogs."""
        self.assertFalse(self.puppy.is_adult())
        
    def test_is_adult_edge_case(self):
        """Test is_adult method at the boundary (2 years)."""
        adult_shiba = ShibaInu("Adult", age=2)
        self.assertTrue(adult_shiba.is_adult())
        
        young_shiba = ShibaInu("Young", age=1)
        self.assertFalse(young_shiba.is_adult())
        
    def test_is_adult_no_age(self):
        """Test is_adult method when age is not set."""
        shiba_no_age = ShibaInu("Unknown")
        self.assertIsNone(shiba_no_age.is_adult())
        
    def test_get_breed_characteristics(self):
        """Test the static method for breed characteristics."""
        characteristics = ShibaInu.get_breed_characteristics()
        
        self.assertIsInstance(characteristics, dict)
        self.assertEqual(characteristics["origin"], "Japan")
        self.assertEqual(characteristics["size"], "Small to medium")
        self.assertIn("Alert", characteristics["temperament"])
        self.assertIn("Independent", characteristics["temperament"])
        self.assertEqual(characteristics["life_span"], "13-16 years")
        self.assertIn("Red", characteristics["common_colors"])
        
    def test_create_puppy(self):
        """Test the class method for creating a puppy."""
        puppy = ShibaInu.create_puppy("Baby")
        self.assertEqual(puppy.name, "Baby")
        self.assertEqual(puppy.age, 0)
        self.assertEqual(puppy.color, "red")
        
        puppy_custom = ShibaInu.create_puppy("Custom", color="black and tan")
        self.assertEqual(puppy_custom.color, "black and tan")


class TestUtilityFunctions(unittest.TestCase):
    """Test cases for utility functions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.shiba1 = ShibaInu("Hachi", age=5)
        self.shiba2 = ShibaInu("Yuki", age=2)
        self.shiba3 = ShibaInu("Kuma", age=7)
        self.shiba_no_age = ShibaInu("Mystery")
        
    def test_count_shiba_inus_all_shibas(self):
        """Test counting when all items are Shiba Inus."""
        shiba_list = [self.shiba1, self.shiba2, self.shiba3]
        self.assertEqual(count_shiba_inus(shiba_list), 3)
        
    def test_count_shiba_inus_mixed_list(self):
        """Test counting in a mixed list."""
        mixed_list = [self.shiba1, "not a shiba", self.shiba2, 42, self.shiba3]
        self.assertEqual(count_shiba_inus(mixed_list), 3)
        
    def test_count_shiba_inus_empty_list(self):
        """Test counting in an empty list."""
        self.assertEqual(count_shiba_inus([]), 0)
        
    def test_count_shiba_inus_no_shibas(self):
        """Test counting when no Shiba Inus are present."""
        non_shiba_list = ["dog", 123, {"breed": "labrador"}]
        self.assertEqual(count_shiba_inus(non_shiba_list), 0)
        
    def test_get_oldest_shiba_normal_case(self):
        """Test finding the oldest Shiba Inu."""
        shiba_list = [self.shiba1, self.shiba2, self.shiba3]
        oldest = get_oldest_shiba(shiba_list)
        self.assertEqual(oldest, self.shiba3)
        self.assertEqual(oldest.age, 7)
        
    def test_get_oldest_shiba_with_no_ages(self):
        """Test finding oldest when no Shiba Inus have ages."""
        shiba_list = [self.shiba_no_age, ShibaInu("Another")]
        oldest = get_oldest_shiba(shiba_list)
        self.assertIsNone(oldest)
        
    def test_get_oldest_shiba_mixed_ages(self):
        """Test finding oldest in a mix of Shibas with and without ages."""
        shiba_list = [self.shiba1, self.shiba_no_age, self.shiba3]
        oldest = get_oldest_shiba(shiba_list)
        self.assertEqual(oldest, self.shiba3)
        
    def test_get_oldest_shiba_empty_list(self):
        """Test finding oldest in an empty list."""
        oldest = get_oldest_shiba([])
        self.assertIsNone(oldest)
        
    def test_get_oldest_shiba_single_item(self):
        """Test finding oldest with a single Shiba Inu."""
        oldest = get_oldest_shiba([self.shiba1])
        self.assertEqual(oldest, self.shiba1)


if __name__ == "__main__":
    unittest.main()