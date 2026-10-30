# Static Code Analysis Issues Table

This table lists all issues detected by **Bandit**, **Flake8**, and **Pylint** in `expense_tracker.py`, sorted by security severity first, followed by code design and style issues.

| Issue | Tool | Type / Severity | Line(s) | Description | Fix Approach |
|---|---|---|---|---|---|
| **B605** | Bandit | Security (High) | 61 | `os.system("xdg-open " + path)` runs through a system shell with concatenated strings, creating a command injection vulnerability (CWE-78). | Replaced with `webbrowser.open(path)` to open the file safely without invoking a system shell. |
| **B306** | Bandit | Security (Medium) | 55 | `tempfile.mktemp()` is deprecated and vulnerable to race conditions (CWE-377 / TOCTOU). | Replaced with `tempfile.mkstemp()`, which safely creates and opens the temporary file descriptor atomically. |
| **B108** | Bandit | Security (Medium) | 8 | `REPORT_DIR = "/tmp/expense_reports"` uses a hardcoded `/tmp` path, which fails on Windows and can be attacked via symlinks on shared Unix systems. | Replaced with `os.path.join(tempfile.gettempdir(), "expense_reports")` for safe cross-platform path resolution. |
| **B105** | Bandit | Security (Low) | 5 | `BANK_SYNC_PASSWORD = "demo-sync-pass"` stores a password directly in plain text in the script (CWE-259). | Read the password dynamically from the environment using `os.environ.get("BANK_SYNC_PASSWORD", "demo-sync-pass")`. |
| **W0718** | Pylint | Bug / Quality | 41 | `except Exception:` catches all exceptions blindly, hiding unexpected bugs. | Changed to `except ValueError:`, which is the exact exception raised when `max()` runs on an empty list. |
| **W0603** | Pylint | Code Smell | 29-30 | `global monthly_budget` modifies global state from inside a function, causing hidden side effects. | Grouped `expenses` and `monthly_budget` into an `ExpenseTracker` class. |
| **C0200** | Pylint | Code Quality | 45 | Loop uses `for i in range(len(expenses)):` instead of idiomatic `enumerate()`. | Changed to `for i, expense in enumerate(self.expenses, start=1):`. |
| **C0103** | Pylint | Naming Style | 11, 20, 28, 33, 38, 44, 49, 53, 59 | Functions and variables used camelCase (`addExpense`, `totalByCategory`, `setBudget`, `newBudget`, `reportPath`). | Renamed all functions, arguments, and local variables to PEP 8 standard `snake_case`. |
| **C0114, C0116** | Pylint | Documentation | 1, 11, 20, 28, 33, 38, 44, 49, 53, 59, 64 | The module and its functions were missing docstrings explaining their arguments and behavior. | Added clear, concise docstrings for the module, class, and each function. |
| **E203** | Flake8 | Formatting | 15 | Whitespace before colon in dictionary key (`{"amount" : amount}`). | Removed the extra space before the colon: `{"amount": amount}`. |
| **E302** | Flake8 | Formatting | 44 | Only 1 blank line before function definition instead of the expected 2 blank lines. | Added two blank lines before function definitions as required by PEP 8. |
| **E261** | Flake8 | Formatting | 74 | Only 1 space before inline comment (`remainingBudget()) # after setBudget`). | Put 2 spaces before the inline comment: `remaining_budget())  # after setBudget`. |
| **E501** | Flake8 | Line Length | 77 | Print statement was 93 characters long, exceeding the 79-character limit. | Split the print statement arguments across multiple lines so each line is under 79 characters. |
