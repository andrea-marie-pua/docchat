
"""Evaluate arithmetic expressions without executing arbitrary Python code."""

import ast
import operator


_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _evaluate(node):
    """Evaluate numbers and supported arithmetic syntax-tree nodes.

    >>> _evaluate(ast.parse('3 + 4', mode='eval').body)
    7
    >>> _evaluate(ast.parse('-(2)', mode='eval').body)
    -2
    >>> _evaluate(ast.parse('2 ** 101', mode='eval').body)
    Traceback (most recent call last):
    ...
    ValueError: Exponent is too large
    >>> _evaluate(ast.parse('10 ** 100 * 10', mode='eval').body)
    Traceback (most recent call last):
    ...
    ValueError: Result is too large
    >>> _evaluate(ast.parse('abs(5)', mode='eval').body)
    Traceback (most recent call last):
    ...
    ValueError: Invalid arithmetic expression
    """
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise ValueError('Exponent is too large')
        result = _OPERATORS[type(node.op)](left, right)
    elif isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
        result = _OPERATORS[type(node.op)](_evaluate(node.operand))
    else:
        raise ValueError('Invalid arithmetic expression')

    if isinstance(result, complex) or abs(result) > 1e100:
        raise ValueError('Result is too large')
    return result


def calculate(expression):
    """Return the result of a safe arithmetic expression or an error message.

    >>> calculate('2 + 3 * 4')
    14
    >>> calculate('(10 - 2) / 4')
    2.0
    >>> calculate('10 // 3')
    3
    >>> calculate('10 % 3')
    1
    >>> calculate('+5')
    5
    >>> calculate('abs(-5)')
    'Error: Invalid arithmetic expression'
    >>> calculate("__import__('os')")
    'Error: Invalid arithmetic expression'
    >>> calculate('2 ** 101')
    'Error: Exponent is too large'
    >>> calculate('10 ** 100 * 10')
    'Error: Result is too large'
    >>> calculate('1 / 0')
    'Error: division by zero'
    >>> calculate('2 +').startswith('Error:')
    True
    >>> calculate(123)
    'Error: Invalid arithmetic expression'
    >>> calculate('1' * 201)
    'Error: Expression is too long'
    """
    try:
        if not isinstance(expression, str):
            raise ValueError('Invalid arithmetic expression')
        if len(expression) > 200:
            raise ValueError('Expression is too long')
        tree = ast.parse(expression, mode='eval')
        return _evaluate(tree.body)
    except (ValueError, SyntaxError, ZeroDivisionError, OverflowError,
            RecursionError) as error:
        return f'Error: {error}'
