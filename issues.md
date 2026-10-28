# Lab 5: Static Code Analysis — Issues Log
**Repository:** `L5_47_ecommerce_cart_system`  
**Student:** Alakh Gupta (PES2UG24CS051)  
**Target File:** `ecommerce_cart_system.py`

---

## Documented Static Analysis Issues

The following table documents the static code quality, style, and security vulnerabilities identified across Pylint, Flake8, and Bandit in the initial script, ordered with High and Medium severity issues first.

| Issue | Type | Tool & ID | Line(s) (Before) | Description | Fix Approach |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Command Injection Vulnerability** | Security (High) | Bandit `B605` | Line 60 | Calling `os.system("echo Receipt saved to: " + filename)` starts a shell process with unsanitized string concatenation, allowing arbitrary command execution. | Replaced shell process execution with safe standard Python `print(f"Receipt saved to: {filename}")`. |
| **Weak Cryptographic Hash (MD5)** | Security (High) | Bandit `B324` | Line 49 | `hashlib.md5(...)` uses the deprecated MD5 algorithm which is vulnerable to collision attacks and insecure for identifier integrity. | Upgraded hashing algorithm to cryptographically secure `hashlib.sha256(...)`. |
| **Dangerous `eval()` Execution** | Security (Medium) / Bug | Bandit `B307` / Pylint `W0123` | Line 44 | Executing dynamic string expressions using `eval(discount_expr)` allows arbitrary code injection if user-supplied input reaches the evaluator. | Replaced `eval()` with typed numerical calculation: `base_price * (1.0 - discount_rate)` with input bounds validation `[0.0, 1.0]`. |
| **Hardcoded Secret Key** | Security (High) / Quality | Static Inspection / Pylint | Line 72 | Hardcoded Stripe secret key `payment_gateway_key = "STRIPE_SECRET_KEY_LIVE_2026"` committed directly in source code. | Replaced plaintext secret with environment variable lookup: `os.getenv("STRIPE_SECRET_KEY")`. |
| **Insecure Pseudo-Random Number Generator** | Security (Low) | Bandit `B311` | Line 53 | `random.randint(1000, 9999)` uses Mersenne Twister PRNG, which is predictable and unsuitable for security credentials / PINs. | Replaced standard `random` with cryptographically secure `secrets.randbelow(9000) + 1000`. |
| **Mutable Default Argument** | Bug / Quality | Pylint `W0102` | Line 15 | `def addItemToCart(..., audit_log=[]):` binds default mutable list at function definition time, causing logs to persist across calls. | Changed default argument to `None` and initialized `if audit_log is None: audit_log = []` inside the function body. |
| **Bare `except:` & Silent Exception Pass** | Quality / Bug | Bandit `B110`, Flake8 `E722`, Pylint `W0702` | Lines 28–29 | `try: del cart_items[item_id] except: pass` catches all exceptions including `KeyboardInterrupt` and hides runtime bugs silently. | Caught specific `KeyError` exception explicitly and returned a boolean status (`True`/`False`). |
| **Resource Leak (Unmanaged File Handling)** | Quality | Pylint `R1732` | Lines 57–59 | `f = open(filename, "w")` without context management risks file descriptor leaks if exceptions occur before `f.close()`. | Refactored using context manager: `with open(filename, "w", encoding="utf-8") as receipt_file:`. |
| **PEP 8 Naming Conventions** | Style | Pylint `C0103` | Lines 15, 25, 32, 42, 48, 52, 56, 63 | Functions used camelCase naming (`addItemToCart`, `removeItemFromCart`, etc.) violating PEP 8 naming standards. | Renamed all functions to snake_case (`add_item_to_cart`, `remove_item_from_cart`, etc.). |
| **Missing Docstrings** | Documentation | Pylint `C0114`, `C0116` | Lines 1, 15, 25, 32, 42, 48, 52, 56, 63, 71 | Entire module and all public functions lacked explanatory docstrings. | Added comprehensive module and function docstrings explaining purpose, arguments, and return types. |
| **Unused Imports & Variables** | Quality | Flake8 `F401`, `F841`, Pylint `W0611`, `W0612` | Lines 4, 33, 43, 65 | `math` was imported but never used; `handling_fee`, `base_price`, and key `k` were assigned but never utilized. | Removed unused import `math`, eliminated dead variables, and iterated directly over dictionary values `.values()`. |
| **Variable Shadowing & Global Statement** | Quality | Pylint `W0603`, `W0621` | Lines 16, 63 | Global mutable state was modified via `global total_sales`; function parameter `cart_items` shadowed global variable. | Eliminated unnecessary global mutation and renamed parameter to `items` to avoid scope shadowing. |

---

## Verification Summary

| Tool | Before Clean-Up | After Clean-Up | Status |
| :--- | :--- | :--- | :--- |
| **Bandit** | 5 Issues (2 High, 1 Medium, 2 Low) | **0 Issues Identified** | **PASSED** |
| **Flake8** | 7 Violations (E722, E711, F401, F841, E501, W292) | **0 Violations** | **PASSED** |
| **Pylint** | Score: **4.04 / 10** | Score: **10.00 / 10** | **PASSED** (Exceeded 9.5 target) |
