    relative_to_current = lambda *x: __import__('os').path.join(__import__('os').path.dirname(__file__), *x)
