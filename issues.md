# Lab 5: Identified Static Code Analysis Issues Table

**Student Name:** Subramani B M  
**SRN:** PES1UG24CS473  
**Section:** H  
**Course:** Software Engineering Lab — PES University  
**Target File:** `restaurant_order_system.py`

---

## 📋 Comprehensive Issue Documentation Table

| # | Issue Code | Tool | Type / Severity | Line(s) | Description | Fix Approach |
|:---:|:---|:---:|:---:|:---:|:---|:---|
| **1** | **B605** | **Bandit** | Security (High) | 58 | Starting a process with a shell (`os.system`) to execute an echo command creates severe shell injection vulnerability if filename contains malicious characters. | Replaced `os.system(...)` with safe built-in Python `print()` function, eliminating subshell execution and shell command injection entirely. |
| **2** | **B324** | **Bandit** | Security (High) | 47 | Use of weak, cryptographically broken MD5 hash algorithm (`hashlib.md5`) for ticket verification hashes. | Replaced `hashlib.md5` with modern, collision-resistant SHA-256 (`hashlib.sha256`) cryptographic hashing. |
| **3** | **B307** / **W0123** | **Bandit & Pylint** | Security (Medium) / Code Quality | 42 | Insecure `eval(promo_expr)` used to evaluate promotional discounts dynamically, allowing arbitrary remote code execution (RCE). | Removed `eval()`; implemented safe arithmetic parsing that extracts numeric multiplier and computes `base_bill * multiplier` safely. |
| **4** | **B311** | **Bandit** | Security (Low) | 51 | Pseudo-random number generator (`random.randint`) used for POS terminal authorization PIN generation. Insecure for security tokens. | Replaced `random` with cryptographically secure `secrets.SystemRandom().randint(1000, 9999)` suitable for authentication tokens. |
| **5** | **B110** / **W0702** / **E722** | **Bandit, Pylint, Flake8** | Security (Low) / Error Handling | 26 | Bare `try: ... except: pass` silently suppresses all exceptions (including syntax errors and system interrupts) without logging or handling. | Replaced broad `try/except: pass` with explicit membership check `if table_id in orders: del orders[table_id]`, eliminating unhandled suppression. |
| **6** | **W0102** | **Pylint** | Bug / Warning | 15 | Dangerous mutable default argument `order_log=[]` shared across all invocations of `placeTableOrder`, causing data leakage between calls. | Changed default parameter to `order_log=None` and initialized `order_log = []` inside the function body. |
| **7** | **C0103** | **Pylint** | Naming Style | 15, 23, 30, 40 | CamelCase function names (`placeTableOrder`, `voidTableOrder`, `checkTableStatus`, `calculateDiscountedBill`) violate PEP 8 snake_case conventions. | Renamed functions to standard snake_case: `place_table_order`, `void_table_order`, `check_table_status`, `calculate_discounted_bill`. |
| **8** | **C0116** | **Pylint** | Documentation | 15, 23, 30, 40, 46, 50, 54, 61 | Missing function and method docstrings across 8 module functions. | Authored detailed, descriptive docstrings for all functions detailing parameters, purpose, and return values. |
| **9** | **R1732** / **W1514** | **Pylint** | Resource / Encoding | 55 | `open()` invoked without `with` context manager and without specifying explicit text encoding, risking file descriptor leaks and cross-platform encoding errors. | Refactored file I/O to use `with open(filename, "w", encoding="utf-8") as file_handle:`. |
| **10** | **W0621** / **W0612** | **Pylint** | Scope / Unused Var | 61, 63 | Parameter `orders` in `get_pending_summary` shadowed outer global dictionary; loop variable `t` was assigned but never used. | Renamed parameter to `orders_dict` and iterated over values directly: `sum(1 for details in orders_dict.values() if not details["is_settled"])`. |
| **11** | **E711** / **C0121** | **Flake8 & Pylint** | Style (PEP 8) | 30 | Comparison `orders.get(table_id) == None` violates Python singleton comparison standards. | Changed to idiomatic identity check `if orders.get(table_id) is None:`. |
| **12** | **F401** / **W0611** | **Flake8 & Pylint** | Unused Import | 4, 6 | Unused module imports `os` and `math` consume unnecessary namespace overhead. | Removed redundant `import os` and `import math`. |
| **13** | **F841** / **W0612** | **Flake8 & Pylint** | Dead Code | 29, 39 | Unused local variables `service_tax = 3.50` and redundant assignment `base_bill` stored but unused. | Removed dead variable assignments to keep function scopes clean. |
| **14** | **E501** / **C0301** | **Flake8 & Pylint** | Formatting (PEP 8) | 18, 19, 42, 75 | Multiple lines exceeded PEP 8 79-character and 100-character line length limits (e.g. line 18 had 110 chars). | Reformatted dict assignments, function calls, and print expressions across multiple indented lines ($\le 79$ characters). |
| **15** | **W292** / **C0304** | **Flake8 & Pylint** | Formatting (POSIX) | 83 | File missing terminating newline at end of file. | Appended terminating newline character (`\n`) conforming to standard POSIX file conventions. |

---

## 📊 Quantitative Quality Improvement Summary

| Metric / Tool | Before Analysis & Fixes | After Static Analysis Remediation | Net Improvement |
|:---|:---:|:---:|:---:|
| **Pylint Code Quality Score** | **4.81 / 10.00** | **10.00 / 10.00** | **+5.19 (+107.9%)** |
| **Bandit Security Vulnerabilities** | **5 Issues** (2 High, 1 Medium, 2 Low) | **0 Issues** (Clean Scan) | **100% Remediation** |
| **Flake8 PEP 8 Violations** | **9 Violations** | **0 Violations** (Clean Scan) | **100% Compliance** |
| **Total Tracked Defect Count** | **22 Pylint + 5 Bandit + 9 Flake8 = 36** | **0 Defects Remaining** | **Zero Defect State** |
