import unittest
import inspect
import random
import string
from typing import Callable


def generate_test_cases(func: Callable):
    """
    Generates unit tests for any given function by inspecting the function signature and expected behavior.

    Args:
        func (Callable): The function for which to generate test cases.
    """
    # Extract function signature
    sig = inspect.signature(func)
    params = list(sig.parameters.values())

    # Generate basic test cases for the function based on its signature
    test_cases = []

    for param in params:
        param_name = param.name
        param_type = param.annotation
        default_value = param.default if param.default is not inspect.Parameter.empty else None

        # Generate test case values for different parameter types
        if param_type == int:
            test_cases.append({param_name: random.randint(-100, 100)})
        elif param_type == float:
            test_cases.append({param_name: random.uniform(-100, 100)})
        elif param_type == str:
            test_cases.append({param_name: ''.join(random.choices(string.ascii_letters, k=5))})
        elif param_type == bool:
            test_cases.append({param_name: random.choice([True, False])})
        elif param_type == list:
            test_cases.append({param_name: [random.randint(1, 10) for _ in range(5)]})
        elif param_type == dict:
            test_cases.append(
                {param_name: {random.choice(string.ascii_lowercase): random.randint(1, 100) for _ in range(3)}})
        elif param_type == None:
            test_cases.append({param_name: None})
        else:
            # Add fallback for unsupported types
            test_cases.append({param_name: None})

    # Automatically generate a class with test cases based on the function's behavior
    class TestFunction(unittest.TestCase):

        def _get_test_case_data(self, test_data):
            """ Helper to map test case data into function arguments """
            return {param: test_data[param] for param in test_data}

        def test_valid(self):
            """ Test with valid inputs """
            for case in test_cases:
                # Generate the argument mapping from case
                input_data = self._get_test_case_data(case)
                result = func(**input_data)
                self.assertIsNotNone(result, f"Failed for input: {input_data}")

        def test_invalid(self):
            """ Test with invalid inputs (e.g., type errors or None) """
            for case in test_cases:
                input_data = {param: None for param in case}  # Invalid input
                with self.assertRaises(TypeError, msg=f"Failed for input: {input_data}"):
                    func(**input_data)

        def test_edge_cases(self):
            """ Test with edge cases like zero or empty inputs """
            for case in test_cases:
                edge_case_data = {param: 0 if isinstance(val := case[param], (int, float)) else '' for param, val in
                                  case.items()}
                result = func(**edge_case_data)
                self.assertIsNotNone(result, f"Edge case failed for input: {edge_case_data}")

    return TestFunction


# Example function to test
def example_function(a: int, b: int) -> int:
    """ Simple function for demonstration. Adds two integers. """
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("Both arguments must be integers.")
    return a + b


# Generate test cases and run tests
TestExampleFunction = generate_test_cases(example_function)

# Run the unittest main method to automatically execute the tests
unittest.main(argv=[''], verbosity=2, exit=False)
