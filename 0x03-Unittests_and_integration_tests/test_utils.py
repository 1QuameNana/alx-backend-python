#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map

class TestAccessNestedMap(unittest.TestCase):
    """
    Unit test class for the access_nested_map function from utils.py.
    """

    @parameterized.expand([
        # Test when the key exists at the top level
        ({"a": 1}, ("a",), 1),
        
        # Test when the key points to a nested dictionary
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        
        # Test when accessing a nested key within nested dictionaries
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test that access_nested_map returns the correct value for a valid path.
        
        Parameters:
        - nested_map (dict): The nested dictionary to access.
        - path (tuple): Sequence of keys to follow.
        - expected: The expected value returned from the function.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        # Test accessing a non-existent top-level key
        ({}, ("a",), "'a'"),
        
        # Test accessing a second-level key that doesn't exist
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_msg):
        """
        Test that access_nested_map raises a KeyError when accessing a missing key.
        
        Parameters:
        - nested_map (dict): The nested dictionary to access.
        - path (tuple): Sequence of keys to follow.
        - expected_msg (str): The expected error message (the missing key).
        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        # Check that the raised KeyError contains the correct missing key
        self.assertEqual(str(cm.exception), expected_msg)


class TestGetJson(unittest.TestCase):
    """
    Unit test class for the get_json function from utils.py.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Test that get_json returns the expected payload and that requests.get is called correctly.

        Parameters:
        - test_url (str): URL to request.
        - test_payload (dict): Expected JSON response from the mocked request.
        - mock_get: Automatically passed mock of requests.get.
        """

        # Create a mock response object with a .json() method that returns test_payload
        mock_response = Mock()
        mock_response.json.return_value = test_payload

        # Set the return value of requests.get to our mock response
        mock_get.return_value = mock_response

        # Call the function under test
        result = get_json(test_url)

        # Assert that requests.get was called once with the expected URL
        mock_get.assert_called_once_with(test_url)

        # Assert that the returned result matches the expected payload
        self.assertEqual(result, test_payload)



from unittest.mock import patch
from utils import memoize

class TestMemoize(unittest.TestCase):
    """
    Unit test class for the memoize decorator from utils.py.
    """

    def test_memoize(self):
        """
        Test that a memoized method calls the original method only once.
        """

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            obj = TestClass()

            # Call a_property twice
            result1 = obj.a_property
            result2 = obj.a_property

            # Ensure both results are correct and equal
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Confirm that a_method was only called once due to memoization
            mock_method.assert_called_once()



