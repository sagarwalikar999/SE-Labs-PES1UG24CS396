# Lab 5: Static Code Analysis — Reflection

## Question 1: What is the primary difference in scope and division of labor between Flake8, Pylint, and Bandit?

The three tools check for different types of problems in Python code:

- **Flake8 (Style & Formatting):** Flake8 checks PEP 8 compliance and basic syntax. In `expense_tracker.py`, it caught formatting mistakes like extra whitespace before a colon (`"amount" : amount`), missing blank lines between functions, and lines longer than 79 characters. It runs quickly and focuses on keeping the code readable and consistent.
- **Pylint (Code Quality & Design):** Pylint evaluates overall code structure, maintainability, and naming standards. It flagged issues like using camelCase instead of snake_case (`addExpense`, `totalByCategory`), missing docstrings, catching a generic `Exception` instead of `ValueError`, modifying global variables with `global monthly_budget`, and looping with `range(len(expenses))` instead of `enumerate()`. It assigns a numeric score out of 10 to measure overall code health.
- **Bandit (Security / SAST):** Bandit only looks for security vulnerabilities. It checks the AST for known insecure patterns (mapped to CWEs). It flagged the plaintext password variable (`BANK_SYNC_PASSWORD`), the hardcoded `/tmp` directory, the insecure `tempfile.mktemp()` function, and the `os.system()` shell execution call. Bandit does not check formatting or docstrings at all.

---

## Question 2: Why might code pass Flake8 and Pylint cleanly yet still fail a Bandit security audit?

Flake8 and Pylint only verify that code follows Python grammar, PEP 8 styling, and standard quality rules. They do not analyze code from a security or threat-modeling perspective.

For example, look at line 61 in the original code:
```python
os.system("xdg-open " + path)
```
This line is syntactically valid Python. With proper spacing, variable naming, and a docstring, both Flake8 and Pylint would give it a passing score. However, Bandit flags it immediately as a High severity issue (B605 / CWE-78) because passing unvalidated strings to `os.system()` invokes a system shell, allowing an attacker to inject arbitrary commands (e.g., passing a path containing `; rm -rf /`).

The same applies to `tempfile.mktemp()`. It is valid Python code, but it has a known race condition vulnerability (CWE-377 / TOCTOU) that only Bandit checks for. Code can be clean and well-styled while still having severe security holes.

---

## Question 3: How do static analysis tools balance developer velocity with code safety?

Static analysis helps catch bugs early, but it has to be configured carefully so it does not slow developers down:

- **Fast local checks:** Fast linters like Flake8 can run directly in the IDE or as pre-commit Git hooks. This gives immediate feedback on whitespace or syntax issues without interrupting developer workflow.
- **CI/CD pipeline gates:** Slower and deeper tools like Pylint and Bandit can run automatically in the build pipeline when a pull request is opened. Security vulnerabilities (Bandit High/Medium) should act as hard blockers to keep insecure code out of production.
- **Tuning rules:** To avoid alert fatigue, teams configure their linter settings (like `.pylintrc`) to disable noisy or unimportant warnings while keeping critical quality and security rules enforced.

---

## Question 4: Why is relying on a single static analysis tool insufficient for a production Python application?

Each tool has a specific purpose and misses what the other tools catch:

- If you only use **Flake8**, the code will look neat and follow PEP 8, but you will miss security vulnerabilities like shell injection and code quality bugs like broad exception handling.
- If you only use **Bandit**, you will catch common security vulnerabilities, but the code could still be unreadable, poorly structured, unmaintainable, and full of runtime logic bugs.
- If you only use **Pylint**, you get good general code review, but Pylint does not have the specialized vulnerability database and CWE checks that Bandit provides.
- None of these tools replace static type checkers like **Mypy** (for type correctness) or automated unit tests (for verifying program logic).

In real-world projects, using all three tools together provides defense-in-depth: Flake8 for consistent style, Pylint for clean architecture, and Bandit for application security.

---

## Summary of Fixes Made in `expense_tracker.py`

| Tool | Before Fix | After Fix | Fix Summary |
|---|---|---|---|
| **Bandit** | 4 issues (1 High, 2 Medium, 1 Low) | **0 issues** | Fixed `os.system` command injection using `webbrowser.open()`, replaced `mktemp` with `mkstemp()`, resolved temp directory path safely, read password from environment variable. |
| **Flake8** | 4 style violations | **0 violations** | Fixed whitespace before colon, added required blank lines before function definitions, fixed inline comment spacing, wrapped lines under 79 characters. |
| **Pylint** | Score: 5.27 / 10.00 | **Score: 10.00 / 10.00** | Added module and function docstrings, converted all names to `snake_case`, caught `ValueError` instead of broad `Exception`, refactored into `ExpenseTracker` class to avoid global state, used `enumerate()`. |
