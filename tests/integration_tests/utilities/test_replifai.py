"""Integration test for Replifai."""
from langchain.utilities import Replifai

code = """
def fibonacci(n):
    if n <= 0:
        return "Invalid parameter. Please provide a positive integer."
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        a, b = 0, 1
        for i in range(n - 2):
            a, b = b, a + b
        return b

return fibonacci(5)
"""

def test_call() -> None:
    """Test that call gives the correct answer."""
    chain = Replifai()
    output = chain.run(code)
    assert output == "3"
