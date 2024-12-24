import os

# Template for the unit test file
test_template = """import unittest

class Test{class_name}(unittest.TestCase):

    def test_{method_name}(self):
        # Arrange

        # Act

        # Assert
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()
"""

def generate_unit_test_file(file_name, function_name, test_cases=None):
    """
    Generates a basic unit test file for a given function with optional test cases.

    Args:
        file_name (str): The name of the test file to create.
        function_name (str): The name of the function to test.
        test_cases (list of dict, optional): List of test cases. Each dict should have 'inputs' and 'expected' keys.

    Returns:
        None
    """
    # Extract class name and method name from the function
    class_name = "".join([word.capitalize() for word in function_name.split("_")])
    method_name = function_name.lower()

    # Generate the test content
    test_content = test_template.format(class_name=class_name, method_name=method_name)

    if test_cases:
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
        additional_tests = ""
        for index, test_case in enumerate(test_cases):
            additional_tests += test_case_template.format(
                method_name=method_name,
                index=index + 1,
                inputs=test_case['inputs'],
                expected=test_case['expected'],
                function_name=function_name
            )
        test_content = test_content.replace("# Arrange\n", additional_tests)

    # Write the content to a file
    with open(file_name, "w") as file:
        file.write(test_content)

    print(f"Test file '{file_name}' generated successfully!")

# Example usage
if __name__ == "__main__":
    print("Welcome to Unit Test Generator!")
    func_name = input("Enter the function name to test: ")
    file_name = input("Enter the test file name (e.g., test_my_function.py): ")

    add_test_cases = input("Do you want to add test cases? (yes/no): ").strip().lower() == "yes"
    test_cases = []
    if add_test_cases:
        print("Enter test cases in the format: inputs=1,2; expected=3")
        print("Type 'done' to finish adding test cases.")
        while True:
            test_case_input = input("Test case: ").strip()
            if test_case_input.lower() == "done":
                break
            try:
                parts = test_case_input.split(";")
                inputs = eval(parts[0].split("=")[1])
                expected = eval(parts[1].split("=")[1])
                test_cases.append({"inputs": inputs, "expected": expected})
            except (IndexError, ValueError):
                print("Invalid format. Please try again.")

    # Validate input
    if not file_name.endswith(".py"):
        print("Error: File name must end with .py")
    elif not func_name:
        print("Error: Function name cannot be empty")
    else:
        generate_unit_test_file(file_name, func_name, test_cases)
