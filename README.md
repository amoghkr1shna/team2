# C++ Template Repository

Welcome to the **C++ Template Repository**! This project provides a quick-start foundation for developing C++ applications with:

- **CMake** for build management
- **vcpkg** for dependency management (e.g., GoogleTest)
- **clang-format** and **clang-tidy** for style and static analysis
- **CircleCI** for continuous integration (build, test, coverage)
- **LLVM** coverage tools (`llvm-profdata`, `llvm-cov`) or `lcov/gcov` (configurable)
- **Issue** and **Pull Request** templates to standardize contributions

---

---

## Features

- **Modern CMake** project setup (`CMakeLists.txt` at the root)
- **Dependency management** with vcpkg for easy library installations (e.g., GoogleTest)
- **Unit, integration, and end-to-end tests** using GoogleTest
- **clang-format** for code formatting; **clang-tidy** for static analysis
- **Coverage** reports generated by `llvm-cov`/`llvm-profdata` or `lcov/gcov`
- **CircleCI** configuration that:
  - Installs dependencies (Clang, CMake, vcpkg, etc.)
  - Builds and tests the code
  - Collects coverage data
  - Uploads coverage reports as artifacts
- **Preconfigured** Issue and Pull Request templates for standardized contributions

---

## Prerequisites

### Local Development

- **C++ Compiler** (Clang or GCC)
- **CMake** (3.15+ recommended)
- **vcpkg** (optional but recommended for cross-platform dependency management)
- **clang-format** and **clang-tidy** (for style and static analysis)
- **GoogleTest** (installed via vcpkg or your system package manager)

#### macOS (Homebrew example)

```bash
brew install cmake llvm
brew install googletest
# Or install vcpkg for cross-platform dependencies:
git clone https://github.com/microsoft/vcpkg.git
cd vcpkg
./bootstrap-vcpkg.sh
./vcpkg integrate install
./vcpkg install gtest

#### macOS (Homebrew example)

bash
Copy
sudo apt-get update
sudo apt-get install -y clang cmake build-essential lcov
# For vcpkg:
git clone https://github.com/microsoft/vcpkg.git
cd vcpkg
./bootstrap-vcpkg.sh
./vcpkg integrate install
./vcpkg install gtest

Continuous Integration
A CircleCI account connected to your GitHub (or GitLab) repository.
(Optional) A GitHub repository with a .circleci/config.yml file in the root.

Getting Started
Clone this repository:

bash
Copy
git clone https://github.com/<your-username>/<cpp-template-repo>.git
cd <cpp-template-repo>
```

Install Dependencies:

If using vcpkg, install required packages (e.g., gtest):
bash
Copy
./vcpkg/vcpkg install gtest

Ensure clang-format and clang-tidy are installed for local checks.
(Optional) Configure vcpkg:

bash
Copy
cmake -B build -DCMAKE_TOOLCHAIN_FILE=./vcpkg/scripts/buildsystems/vcpkg.cmake

Ensure clang-format and clang-tidy are installed for local checks.
(Optional) Configure vcpkg:

bash
Copy
cmake -B build -DCMAKE_TOOLCHAIN_FILE=./vcpkg/scripts/buildsystems/vcpkg.cmake

Building
Configure and build the project using CMake:

bash
Copy
mkdir build && cd build
cmake -DCMAKE_CXX_FLAGS="--coverage" \
 -DCMAKE_TOOLCHAIN_FILE=../vcpkg/scripts/buildsystems/vcpkg.cmake \
 ..
make -j4
The --coverage flag is optional and adds instrumentation for coverage analysis.
Adjust paths if your vcpkg folder is elsewhere or if you are not using vcpkg.

Testing
Run tests using CTest:

bash
Copy
cd build
ctest --output-on-failure
Tests are organized as:

Unit tests (e.g., unit_tests executable)
Integration tests (e.g., integration_tests)
End-to-End tests (e.g., e2e_tests)

Coverage
This repository supports coverage using either LLVM or lcov/gcov.

LLVM Coverage Example
Build with coverage flags.
Run tests to generate .profraw files:
bash
Copy
export LLVM_PROFILE_FILE="%p.profraw"
ctest --output-on-failure

lcov/gcov Coverage Example
Build with coverage flags.
Run tests (ctest).
Collect coverage:
bash
Copy
lcov --capture --directory . --output-file coverage.info
lcov --remove coverage.info '/usr/_' 'tests/_' --output-file coverage.info
genhtml coverage.info --output-directory coverage_html
open coverage_html/index.html

Style & Static Analysis
clang-format
A .clang-format file is included. To auto-format your code:

bash
Copy
clang-format -i src/_.cpp src/_.hpp tests/\*_/_.cpp
In CI, a dry-run with --Werror ensures that code must adhere to the formatting rules.

clang-tidy
A .clang-tidy file is provided, which includes checks like modernize-_ and readability-_. Run clang-tidy as follows:

bash
Copy
clang-tidy -p build <file> -- -std=c++17
If certain rules are too strict (e.g., trailing return types or short parameter names), adjust the checks in the .clang-tidy file or fix your code accordingly.

Continuous Integration (CircleCI)
The repository includes a CircleCI configuration (.circleci/config.yml) that:

Installs dependencies (Clang, CMake, vcpkg, etc.)
Bootstraps vcpkg and installs GoogleTest
Builds the project with coverage flags
Runs tests (producing JUnit XML output for the CircleCI Tests tab)
Generates a coverage report (HTML)
Uploads coverage artifacts for easy access
Viewing CI Results
Push your code to GitHub (or create a pull request).
CircleCI will automatically trigger a build.
Check the Tests tab for test results.
Check the Artifacts tab for the coverage report (in the coverage_html folder).
Issue & PR Templates
This repository contains preconfigured templates for issues and pull requests:

.github/ISSUE_TEMPLATE/bug_report.md
.github/ISSUE_TEMPLATE/feature_request.md
pull_request_template.md (in the root or in .github/PULL_REQUEST_TEMPLATE/)
These templates ensure that all contributions follow a consistent format.

Contributing
Contributions are welcome! To contribute:

Fork this repository and create a new branch (e.g., feature/your-feature).
Implement your changes (ensure code is formatted and linted).
Add tests for any new features or bug fixes.
Open a Pull Request and follow the provided template.
Ensure all CircleCI checks (formatting, static analysis, tests, and coverage) pass.
Feel free to open an issue for any feature requests or bug reports.
