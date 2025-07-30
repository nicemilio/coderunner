# C++ Programming Guidelines
## 1. Motivation and Benefits

* **Goal:** To establish a consistent style in all C++ source code created by Sander & Doll employees.
* **Advantages:**
    * Avoids error-prone constructs.
    * Facilitates understanding and modification of existing code.
    * Minimizes friction and increases efficiency.

## 2. Scope of Application

* Primarily applies to **newly created source code**.
* For **existing source code**: Decisions are made on a case-by-case basis, with a long-term goal of achieving a uniform style.
* **Important points for new code:**
    * New class members must follow the new rules.
    * Overriding virtual functions must be marked with `override`.
    * New functions, types, and variables must always include a documentation comment.
    * The `NULL` macro is to be replaced by `nullptr`.

## 3. Essential Guidelines

### 3.1. General

* **Indentation:** 4 spaces, no tabs.
* **Line Length:** Max. 135 characters (exceptions possible).
* **Whitespace:** One space before opening brackets (`(`, `{`, `[`, `<`), no spaces inside them.
* **Operators:** Separated from operands by spaces (exceptions: `::`, `,`, `>`, `>>`, `++`, comma operator).
* Large commented-out code blocks should be removed (use version control).

### 3.2. Variables

* **Names:** `camelCase`, starting with a lowercase letter (e.g., `variableName`). Single-word variables are entirely lowercase (e.g., `count`).
* No Hungarian notation.
* Names should be descriptive; abbreviations only if obvious or commented.
* Only one variable declaration per statement.
* **Pointers/References:** Sign bound to the variable name (e.g., `int* pointerName`).
* **`const`:** Bound to the type, between type and pointer/reference sign (e.g., `double const pi`).
* **Initialization:** Preferred with assignment syntax (`=`).
* **`auto`:** To be used judiciously; can improve readability.

### 3.3. Typedef

* **`using`** is preferred over **`typedef`** (better readability, template support).

### 3.4. Functions

* **Names:** `CamelCase`, starting with an uppercase letter (e.g., `FunctionName`).
* Global functions should be explicitly prefixed with `::`.
* Mostly imperative (e.g., `Move`, `Close`).
* **Parameter List:** Opening parenthesis separated from function name by a space.
* **Function Body:** Opening curly brace on a new line.
* **Parameter Names:** Prefixed with `the` and then `CamelCase` (e.g., `theParameter`).
* Parameters that don't fit on one line should be split across multiple lines (one parameter per line, indented).
* Parameter names must match in declaration and definition (if unused, comment out the name, do not remove it).
* **Type Passing:**
    * User-defined types: Passed as references (optionally `const` references).
    * Built-in types: Passed by value (never as `const` references).
* Functions should not exceed a certain length (refactoring encouraged).
* **`inline`:** Only use when clear performance benefit is evident.
* **C-Style Variadic Functions (`...`):** Forbidden (type unsafety); alternatives like C++ streams or `std::format` should be used.
* **Variadic Templates (C++11):** Allowed (type-safe).

### 3.5. Control Structures

* **`if`:** Space after `if`, no spaces inside condition parentheses. Curly braces optional for single statements. `else` follows on the same line as the preceding closing brace. Explicit comparisons to 0 required; `bool` expressions used directly. Literals on the right in comparisons.
* **`for`:** Space after `for`, no spaces in control statements. Prefer prefix increment/decrement (`++i`, `--i`).
* **`while`:** Space after `while`, no spaces inside condition parentheses.
* **`do-while`:** Body always enclosed in curly braces, `while` follows on the same line as the closing brace of the body.
* **`switch`:** Space after `switch`, no spaces inside expression parentheses. `case` labels and statements are indented. `break` on a new line. Fall-through must be marked with `[[fallthrough]]` (C++17). `default` is always the last case.

### 3.6. Type Casting

* **Forbidden:** C-style and function-style casts.
* **Allowed:** C++ casts (`static_cast<>`, `const_cast<>`, `reinterpret_cast<>`, `dynamic_cast<>`).
* **Special Casts:** `pointer_cast<>` (for `dynamic_cast<>` of pointers that should throw an exception on failure), `implicit_cast<>` (when a conversion would otherwise be implicit).
* **`const_cast<>`:** Only allowed if the object is genuinely not `const` or when dealing with a defective interface.
* **`reinterpret_cast`:** Only as a last resort.

### 3.7. `sizeof`

* Expression for `sizeof` always enclosed in parentheses.
* Prefer using the variable name over its type with `sizeof`.

### 3.8. Namespaces

* **Names:** Lowercase, short, single-word (e.g., `tools`).
* Content not indented within namespace blocks.
* Opening curly brace on the same line as the namespace name.
* Each module has its own namespace.
* `// namespace <Name>` comment after the closing brace.
* Namespaces opened only for declarations and class definitions.
* Anonymous namespaces for local helper constructs in implementation files (max. one per file).
* **Forbidden in Headers:** `using` declarations and `using namespace` directives.
* **Allowed in Implementation Files:** `using` declarations and `using namespace` directives.

### 3.9. Enumerations

* **Names:** `CamelCase` with an `E`-prefix (e.g., `EWindowsVersion`).
* Opening curly brace on the same line.
* **Old Enums:** Values with lowercase abbreviation of the enum name, then `CamelCase`.
* **New Enums (`enum class`):** No prefix, uppercase letter, then `CamelCase`.
* New enums are preferred.

### 3.10. Classes

* **Names:** `CamelCase` with a `C`-prefix (e.g., `CStyleGuide`), also applies to structs.
* **Inheritance List:** Space after class name, colon, then derivation specifier (public, protected, private).
* Opening curly brace on the same line as the last base class or class name.
* Maximum one `public:`, `protected:`, `private:` block in that order.
* Visibility specifiers at the same indentation level as `class`, declarations indented further.
* **Order of Declarations:** Standard constructor, Copy constructor, Other constructors, Destructor, (blank line), Operators, (blank line), Member variables, Member functions.
* Member functions alphabetically sorted.
* Definition of member functions within the class definition is forbidden.
* Inline member functions are defined below the class in the header.
