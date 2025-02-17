cmake_minimum_required(VERSION 3.14)
project(TemplateProject)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Use Clang
set(CMAKE_C_COMPILER clang)
set(CMAKE_CXX_COMPILER clang++)

# Include vcpkg toolchain
set(CMAKE_TOOLCHAIN_FILE "${CMAKE_SOURCE_DIR}/vcpkg/scripts/buildsystems/vcpkg.cmake")

# Enable Testing
enable_testing()

# Find Google Test (ensure it's installed via vcpkg)
find_package(GTest REQUIRED)
include_directories(${GTEST_INCLUDE_DIRS})

# Automatically find all source files in src/
file(GLOB_RECURSE SRC_FILES "src/*.cpp" "src/*.h")

# Define a library for your core logic
add_library(core STATIC ${SRC_FILES})

# Add test executable (only test files)
file(GLOB TEST_FILES "tests/*.cpp")

add_executable(runTests ${TEST_FILES})

# Link the core library and GTest to the test executable
target_link_libraries(runTests PRIVATE core GTest::GTest GTest::Main)

# Enable code coverage flags (for Clang/GCC)
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU" OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    message(STATUS "Enabling Code Coverage for ${CMAKE_CXX_COMPILER_ID}")
    target_compile_options(runTests PRIVATE -O0 -g --coverage -fprofile-arcs -ftest-coverage)
    # NOTE: Linking gcov works with GCC. With Clang, you typically don’t need "gcov".
    # However, for simplicity, let's keep it the same. If linking fails on Clang, remove 'gcov'.
    target_link_libraries(runTests PRIVATE --coverage)
endif()


# Coverage report generation target
find_program(LCOV lcov)
find_program(GENHTML genhtml)

if(LCOV AND GENHTML)
    add_custom_target(coverage
            COMMAND ${LCOV} --capture --directory . --output-file coverage.info
            COMMAND ${LCOV} --remove coverage.info '/usr/*' '*/test/*' --output-file coverage_filtered.info
            COMMAND ${GENHTML} coverage_filtered.info --output-directory coverage_report
            COMMAND echo "Coverage report generated in coverage_report/index.html"
            WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    )
endif()