# -*- coding: utf-8 -*-
"""
Single-file Calculator Example with History Persistence and a Service Layer.

Python 2 compatible version.

Features:
- Calculator: pure arithmetic functions.
- OperationRecord: plain class instead of dataclass.
- HistoryRepository: uses sqlite3 (built-in).
- CalculationService: orchestrates logic + persistence.
- CLI loop for demo.

Python: 2.7+
"""

import sqlite3

# 1) PURE LOGIC: Calculator
class Calculator(object):
    """Pure arithmetic operations."""
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return float(a) / float(b)

# 2) DATA MODEL: OperationRecord (simple class for Python 2)
class OperationRecord(object):
    def __init__(self, op, a, b, result):
        self.op = op
        self.a = a
        self.b = b
        self.result = result

# 3) SIDE-EFFECTS: HistoryRepository (SQLite)
class HistoryRepository(object):
    """SQLite repository for operation history."""

    def __init__(self, db_path="calc_py2.db"):
        self.db_path = db_path
        self._init_schema()

    def _init_schema(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            "CREATE TABLE IF NOT EXISTS history ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "op TEXT NOT NULL, a REAL NOT NULL, b REAL NOT NULL, result REAL NOT NULL)"
        )
        conn.commit()
        conn.close()

    def append(self, rec):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(
            "INSERT INTO history (op, a, b, result) VALUES (?, ?, ?, ?)",
            (rec.op, rec.a, rec.b, rec.result)
        )
        conn.commit()
        conn.close()

    def all(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT op, a, b, result FROM history ORDER BY id ASC")
        rows = c.fetchall()
        conn.close()
        return [OperationRecord(row[0], row[1], row[2], row[3]) for row in rows]

# 4) INTEGRATION: CalculationService
class CalculationService(object):
    def __init__(self, repo=None, calc=None):
        self.repo = repo or HistoryRepository()
        self.calc = calc or Calculator()
        self._ops = {
            "add": self.calc.add,
            "subtract": self.calc.subtract,
            "multiply": self.calc.multiply,
            "divide": self.calc.divide,
        }

    def compute(self, op, a, b):
        if op not in self._ops:
            raise ValueError(
                "Unsupported operation: %s. Use one of: %s" % (op, ", ".join(self._ops))
            )
        result = self._ops[op](a, b)
        self.repo.append(OperationRecord(op, a, b, result))
        return result

# 5) DEMO / CLI LOOP
def main():
    service = CalculationService()

    print("== Calculator (Python 2 compatible) ==")
    while True:
        print("\nChoose an operation:")
        print("1) Add")
        print("2) Subtract")
        print("3) Multiply")
        print("4) Divide")
        print("5) Show history")
        print("q) Quit")
        choice = input("Enter choice: ").strip()
        if choice == 'q':
            print("Goodbye!")
            break
        elif choice in ('1', '2', '3', '4'):
            try:
                a = float(input("Enter first number: "))
                b = float(input("Enter second number: "))
                if choice == '1':
                    op = "add"
                elif choice == '2':
                    op = "subtract"
                elif choice == '3':
                    op = "multiply"
                elif choice == '4':
                    op = "divide"
                result = service.compute(op, a, b)
                print("Result: %s" % result)
            except Exception as e:
                print("Error: %s" % e)
        elif choice == '5':
            history = service.repo.all()
            print("-- Calculation History --")
            for rec in history:
                print("%s(%s, %s) = %s" % (rec.op, rec.a, rec.b, rec.result))
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()

