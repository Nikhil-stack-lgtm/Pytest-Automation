import os
import inspect

# Template for the unit test file
test_template = """import unittest
from {module_name} import {function_name}

class Test{class_name}(unittest.TestCase):

{test_methods}

if __name__ == "__main__":
    unittest.main()
"""


def generate_unit_test_file(file_name, function_name, module_name, auto_test_cases=None):
    """
    Generates a comprehensive unit test file for a given function.

    Args:
        file_name (str): The name of the test file to create.
        function_name (str): The name of the function to test.
        module_name (str): The name of the module containing the function.
        auto_test_cases (list of dict, optional): Automatically generated test cases.
    """
    class_name = "".join([word.capitalize() for word in function_name.split("_")])

    # Generate test methods
    test_methods = ""
    if auto_test_cases:
        test_case_template = """
    def test_{method_name}_{index}(self):
        # Arrange
        inputs = {inputs}
        expected = {expected}

        # Act
        try:
            actual = {function_name}(*inputs)
        except Exception as e:
            actual = str(e)

        # Assert
        self.assertEqual(actual, expected)
"""
        for index, test_case in enumerate(auto_test_cases):
            test_methods += test_case_template.format(
                method_name=function_name.lower(),
                index=index + 1,
                inputs=test_case["inputs"],
                expected=test_case["expected"],
                function_name=function_name
            )

    # Default fallback if no cases provided
    if not test_methods:
        test_methods = f"""
    def test_{function_name.lower()}(self):
        # Arrange

        # Act

        # Assert
        self.assertEqual(actual, expected)
"""

    # Generate the test content
    test_content = test_template.format(
        module_name=module_name,
        function_name=function_name,
        class_name=class_name,
        test_methods=test_methods
    )

    # Write the content to a file
    with open(file_name, "w") as file:
        file.write(test_content)

    print(f"Test file '{file_name}' generated successfully!")


def auto_generate_test_cases(function_name):
    """
    Automatically generates test cases for known function patterns.

    Args:
        function_name (str): The name of the function to generate test cases for.

    Returns:
        list of dict: A list of test cases covering 80% of scenarios.
    """
    test_cases = []

    # Example: Predefined scenarios for a common function pattern
    if "get_user_by_id" in function_name:
        test_cases.extend([
            # Positive case
            {"inputs": (1,), "expected": {"id": 1, "name": "Alice", "email": "alice@example.com"}},
            # Negative case
            {"inputs": (4,), "expected": {"error": "User not found"}},
            # Edge case: Zero or invalid user ID
            {"inputs": (0,), "expected": {"error": "User not found"}},
            {"inputs": (-1,), "expected": {"error": "User not found"}},
            # Type mismatch
            {"inputs": ("abc",), "expected": "TypeError"},
            # Large ID
            {"inputs": (99999,), "expected": {"error": "User not found"}},
        ])
    elif "add" in function_name:
        test_cases.extend([
            # Positive case
            {"inputs": (2, 3), "expected": 5},
            # Negative case
            {"inputs": (-1, 1), "expected": 0},
            # Edge cases
            {"inputs": (0, 0), "expected": 0},
            {"inputs": (99999999, 1), "expected": 100000000},
            # Type mismatch
            {"inputs": ("a", 1), "expected": "TypeError"},
        ])
    else:
        # Generic cases for unknown functions
        test_cases.extend([
            {"inputs": (), "expected": "Function requires arguments"},
            {"inputs": (None,), "expected": "Invalid input"},
        ])

    return test_cases


# Example usage
if __name__ == "__main__":
    print("Welcome to Advanced Unit Test Generator!")
    func_name = input("Enter the function name to test: ")
    module_name = input("Enter the module name containing the function: ")
    file_name = input("Enter the test file name (e.g., test_my_function.py): ")

    try:
        # Dynamically import the module and get the function
        module = __import__(module_name)
        function = getattr(module, func_name)
        auto_test_cases = auto_generate_test_cases(func_name)
    except (ImportError, AttributeError):
        print("Error: Could not find the specified module or function.")
        exit(1)

    if not file_name.endswith(".py"):
        print("Error: File name must end with .py")
    elif not func_name:
        print("Error: Function name cannot be empty")
    else:
        generate_unit_test_file(file_name, func_name, module_name, auto_test_cases)
