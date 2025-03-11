cmake_minimum_required(VERSION 3.15)
project(MyCppTemplate LANGUAGES CXX)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Use C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wpedantic")

# Option to enable coverage
option(ENABLE_COVERAGE "Enable coverage flags" ON)
if(ENABLE_COVERAGE)
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fprofile-instr-generate -fcoverage-mapping")
endif()

# Enable testing
include(CTest)
enable_testing()

# Add your source code
file(GLOB SRC_FILES "src/*.cpp")
add_library(my_code ${SRC_FILES})
target_include_directories(my_code PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src)

# Set the vcpkg toolchain file if using vcpkg
if(EXISTS "${CMAKE_SOURCE_DIR}/vcpkg/scripts/buildsystems/vcpkg.cmake")
  set(CMAKE_TOOLCHAIN_FILE "${CMAKE_SOURCE_DIR}/vcpkg/scripts/buildsystems/vcpkg.cmake")
endif()

# Download and set up GoogleTest
include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.zip
)
FetchContent_MakeAvailable(googletest)

# Add GoogleTest
enable_testing()
include(GoogleTest)

# Unit Tests
file(GLOB UNIT_TEST_FILES "tests/unit/*.cpp")
add_executable(unit_tests ${UNIT_TEST_FILES})
target_link_libraries(unit_tests PRIVATE my_code gtest_main)
target_include_directories(unit_tests PRIVATE ${gtest_SOURCE_DIR}/include)
gtest_discover_tests(unit_tests)

# Integration Tests
file(GLOB INT_TEST_FILES "tests/integration/*.cpp")
add_executable(integration_tests ${INT_TEST_FILES})
target_link_libraries(integration_tests PRIVATE my_code gtest_main)
target_include_directories(integration_tests PRIVATE ${gtest_SOURCE_DIR}/include)
gtest_discover_tests(integration_tests)

# End-to-End Tests
file(GLOB E2E_TEST_FILES "tests/e2e/*.cpp")
add_executable(e2e_tests ${E2E_TEST_FILES})
target_link_libraries(e2e_tests PRIVATE my_code gtest_main)
target_include_directories(e2e_tests PRIVATE ${gtest_SOURCE_DIR}/include)
gtest_discover_tests(e2e_tests)
