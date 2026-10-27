import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def add(a: float, b: float) -> float:
    result = a + b
    logging.info(f"Operation ADD: {a} + {b} = {result}")
    return result

def subtract(a: float, b: float) -> float:
    result = a - b
    logging.info(f"Operation SUBTRACT: {a} - {b} = {result}")
    return result

def multiply(a: float, b: float) -> float:
    result = a * b
    logging.info(f"Operation MULTIPLY: {a} * {b} = {result}")
    return result

def divide(a: float, b: float) -> float:
    if b == 0:
        logging.error("Operation DIVIDE failed: Division by zero")
        raise ZeroDivisionError("Cannot divide by zero.")
    result = a / b
    logging.info(f"Operation DIVIDE: {a} / {b} = {result}")
    return result
