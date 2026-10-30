"""Personal Expense Tracker module for managing expenses and budgets."""

import os
import tempfile
import webbrowser
from datetime import datetime

BANK_SYNC_PASSWORD = os.environ.get("BANK_SYNC_PASSWORD", "demo-sync-pass")
REPORT_DIR = os.path.join(tempfile.gettempdir(), "expense_reports")


class ExpenseTracker:
    """Manages recording, budgeting, and reporting of personal expenses."""

    def __init__(self, initial_budget=20000):
        """Initialize the expense tracker with an initial budget."""
        self.expenses = []
        self.monthly_budget = initial_budget

    def add_expense(self, amount, category="Misc", note=""):
        """Add an expense entry with amount, category, and optional note."""
        if amount <= 0:
            print("Ignoring invalid amount", amount)
            return False
        self.expenses.append({
            "amount": amount,
            "category": category,
            "note": note,
            "time": datetime.now().isoformat()
        })
        return True

    def total_by_category(self):
        """Calculate and return total expenses grouped by category."""
        totals = {}
        for expense in self.expenses:
            category = expense["category"]
            totals[category] = totals.get(category, 0) + expense["amount"]
        return totals

    def set_budget(self, new_budget):
        """Update the monthly budget limit."""
        self.monthly_budget = new_budget

    def remaining_budget(self):
        """Compute the remaining budget after subtracting total expenses."""
        spent = sum(expense["amount"] for expense in self.expenses)
        return self.monthly_budget - spent

    def biggest_expense(self):
        """Return the expense dictionary with the largest amount, or None."""
        try:
            return max(self.expenses, key=lambda expense: expense["amount"])
        except ValueError:
            return None

    def print_ledger(self):
        """Display all recorded expenses numbered consecutively."""
        for i, expense in enumerate(self.expenses, start=1):
            print(i, expense["category"], expense["amount"])

    @staticmethod
    def check_sync_password(password):
        """Check whether password matches the bank sync password."""
        return password == BANK_SYNC_PASSWORD

    @staticmethod
    def export_report():
        """Create a secure temporary report file and return its path."""
        os.makedirs(REPORT_DIR, exist_ok=True)
        fd, report_path = tempfile.mkstemp(suffix=".txt", dir=REPORT_DIR)
        os.close(fd)
        return report_path

    @staticmethod
    def open_statement(path):
        """Open statement file securely using the default application."""
        webbrowser.open(path)


# Module-level instance for functional API compatibility
_default_tracker = ExpenseTracker()
expenses = _default_tracker.expenses


def add_expense(amount, category="Misc", note=""):
    """Add an expense entry."""
    return _default_tracker.add_expense(amount, category, note)


def total_by_category():
    """Calculate and return total expenses grouped by category."""
    return _default_tracker.total_by_category()


def set_budget(new_budget):
    """Update the monthly budget limit."""
    _default_tracker.set_budget(new_budget)


def remaining_budget():
    """Compute the remaining budget after subtracting total expenses."""
    return _default_tracker.remaining_budget()


def biggest_expense():
    """Return the expense dictionary with the largest amount, or None."""
    return _default_tracker.biggest_expense()


def print_ledger():
    """Display all recorded expenses numbered consecutively."""
    _default_tracker.print_ledger()


def check_sync_password(password):
    """Check whether password matches the bank sync password."""
    return _default_tracker.check_sync_password(password)


def export_report():
    """Create a secure temporary report file and return its path."""
    return _default_tracker.export_report()


def open_statement(path):
    """Open statement file securely using the default application."""
    _default_tracker.open_statement(path)


def main():
    """Run demonstration of the expense tracker functions."""
    print("Biggest expense before any entries:", biggest_expense())
    add_expense(450, "Food", "Lunch with team")
    add_expense(1200, "Travel", "Cab to airport")
    add_expense(-50, "Food")
    add_expense(300, "Food", "Groceries")
    add_expense(999, "Bills", "Internet")
    set_budget(5000)
    print_ledger()
    print("Totals:", total_by_category())
    print("Remaining budget:", remaining_budget())  # after setBudget
    print("Biggest expense:", biggest_expense()["note"])
    print("Sync password accepted:", check_sync_password("guess"))
    print(
        "Summary:", len(_default_tracker.expenses),
        "expenses recorded against a budget of",
        _default_tracker.monthly_budget
    )


if __name__ == "__main__":
    main()
