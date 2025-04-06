
# Components Documentation

This repository follows a component-based architecture, where each component is encapsulated into its own folder, containing all relevant source files, headers, and tests. This modular approach allows for clear responsibilities and easier maintenance.

## Directory Structure

```
src/
├── calculator/
│   ├── include/
│   │   └── calculator.hpp        # Header file for Calculator class
│   ├── test/
│   │   └── test_calculator.cpp   # Unit tests for Calculator component
│   └── calculator.cpp            # Implementation of Calculator class
│
├── logger/
│   ├── include/
│   │   └── logger.hpp            # Header file for Logger class
│   ├── test/
│   │   └── test_logger.cpp       # Unit tests for Logger component
│   └── logger.cpp                # Implementation of Logger class
│
└── notifier/
    ├── include/
    │   └── notifier.hpp          # Header file for Notifier class
    ├── test/
    │   └── test_notifier.cpp     # Unit tests for Notifier component
    └── notifier.cpp              # Implementation of Notifier class
```

Each component follows a structure where:

- **Header file** (`.hpp`) defines the interface of the component.
- **Implementation file** (`.cpp`) contains the logic and methods of the component.
- **Test file** (`test_<component>.cpp`) includes unit tests to verify the functionality of the component.

---

## Calculator Component

### Purpose

The `Calculator` component performs basic arithmetic operations. It is a lightweight utility designed to handle operations such as addition, subtraction, and multiplication.

### Methods and Inputs/Outputs

- **add(int num1, int num2) -> int**  
  Adds two integers and returns the result.

- **subtract(int num1, int num2) -> int**  
  Subtracts the second integer from the first and returns the result.

- **multiply(int num1, int num2) -> int**  
  Multiplies two integers and returns the result.

### Example Usage

```cpp
Calculator calc;
int sum = calc.add(5, 3);           // sum = 8
int difference = calc.subtract(5, 3); // difference = 2
int product = calc.multiply(5, 3);   // product = 15
```

### Interactions

The `Calculator` component is independent and does not interact directly with other components like `Logger` or `Notifier`. However, its operations may trigger logging or notifications through integration with the other components.

---

## Logger Component

### Purpose

The `Logger` component keeps a record of operations and their results. It stores logs of executed operations and can retrieve them for display or further analysis.

### Methods and Inputs/Outputs

- **logOperation(const std::string &operation, int result) const**  
  Logs a string representing the operation and its result (e.g., "5 + 3 = 8").

- **getLogs() const -> const std::vector<std::string>&**  
  Retrieves a list of all recorded logs.

### Example Usage

```cpp
Logger logger;
logger.logOperation("5 + 3", 8);
auto logs = logger.getLogs();
for (const auto& log : logs) {
  std::cout << log << std::endl;
}
```

### Interactions

The `Logger` component is typically used in conjunction with the `Calculator` to record the results of arithmetic operations. For example, after performing a calculation, the `Calculator` might call `Logger::logOperation` to record the operation and its result.

---

## Notifier Component

### Purpose

The `Notifier` component is responsible for sending alerts when certain thresholds are exceeded. It evaluates a value and determines if it exceeds a predefined threshold, triggering an appropriate notification message.

### Methods and Inputs/Outputs

- **shouldNotify(int value) const -> bool**  
  Determines if a value exceeds the threshold. Returns `true` if the value exceeds the threshold, `false` otherwise.

- **notifyMessage(int value) const -> std::string**  
  Returns a notification message based on whether the value exceeds the threshold.

### Example Usage

```cpp
Notifier notifier(10); // Set threshold to 10
int value = 15;
if (notifier.shouldNotify(value)) {
    std::cout << notifier.notifyMessage(value) << std::endl;
}
```

### Interactions

The `Notifier` component may interact with the `Calculator` to monitor and alert when calculation results exceed a specific threshold. It could also be integrated with the `Logger` to store notifications.

---

## Component Interaction and Integration

While each component is modular, they can interact in the following ways:

- **Calculator and Logger:**  
  After performing an arithmetic operation, the `Calculator` can log the operation using the `Logger` component.

- **Calculator and Notifier:**  
  If the result of a calculation exceeds the threshold defined in the `Notifier`, the `Notifier` can send an alert about the threshold being exceeded.

### Example Scenario: Calculator, Logger, and Notifier

```cpp
Calculator calc;
Logger logger;
Notifier notifier(10);

int result = calc.add(7, 8);
logger.logOperation("7 + 8", result);

if (notifier.shouldNotify(result)) {
    std::cout << notifier.notifyMessage(result) << std::endl;
}
```

---

## Conclusion

This modular component based structure allows for easy testing and reuse. The components are designed to be loosely coupled, meaning each one can function independently but can also be integrated for more complex workflows, such as performing calculations, logging them, and notifying when certain conditions are made.
