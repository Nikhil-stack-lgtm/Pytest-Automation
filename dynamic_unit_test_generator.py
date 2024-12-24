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
    Generates a basic unit test file for a given function with optional automated test cases.

    Args:
        file_name (str): The name of the test file to create.
        function_name (str): The name of the function to test.
        module_name (str): The name of the module containing the function.
        auto_test_cases (list of dict, optional): Automatically generated test cases. Each dict should have 'inputs' and 'expected' keys.

    Returns:
        None
    """
    # Extract class name and method name from the function
    class_name = "".join([word.capitalize() for word in function_name.split("_")])

    # Generate test methods
    if auto_test_cases:
        test_case_template = """
    def test_{method_name}_{index}(self):
        # Arrange
        inputs = {inputs}
        expected = {expected}

        # Act
        actual = {function_name}(*inputs)

        # Assert
        self.assertEqual(actual, expected)
"""
        test_methods = ""
        for index, test_case in enumerate(auto_test_cases):
            test_methods += test_case_template.format(
                method_name=function_name.lower(),
                index=index + 1,
                inputs=test_case['inputs'],
                expected=test_case['expected'],
                function_name=function_name
            )
    else:
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
        list of dict: A list of test cases with 'inputs' and 'expected' keys.
    """
    if "get_user_by_id" in function_name:
        return [
            {"inputs": (1,), "expected": {"id": 1, "name": "Alice", "email": "alice@example.com"}},
            {"inputs": (4,), "expected": {"error": "User not found"}},
        ]
    return []

# Example usage
if __name__ == "__main__":
    print("Welcome to Unit Test Generator!")
    func_name = input("Enter the function name to test: ")
    module_name = input("Enter the module name containing the function: ")
    file_name = input("Enter the test file name (e.g., test_my_function.py): ")

    # Dynamically import the module and get the function
    try:
        module = __import__(module_name)
        function = getattr(module, func_name)
        auto_test_cases = auto_generate_test_cases(func_name)
    except (ImportError, AttributeError):
        print("Error: Could not find the specified module or function.")
        exit(1)

    # Validate input
    if not file_name.endswith(".py"):
        print("Error: File name must end with .py")
    elif not func_name:
        print("Error: Function name cannot be empty")
    else:
        generate_unit_test_file(file_name, func_name, module_name, auto_test_cases)
