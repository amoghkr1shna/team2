cmake_minimum_required(VERSION 3.15)
project(MyCppTemplate LANGUAGES CXX)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Use C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Basic compiler flags
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wpedantic")

# Option to enable coverage
option(ENABLE_COVERAGE "Enable coverage flags" ON)
if(ENABLE_COVERAGE)
  if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fprofile-instr-generate -fcoverage-mapping")
  elseif(CMAKE_CXX_COMPILER_ID MATCHES "GNU")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} --coverage")
  endif()
endif()

# Enable testing
include(CTest)
enable_testing()

# Add your source code
file(GLOB SRC_FILES "src/*.cpp")
add_library(my_code ${SRC_FILES})
target_include_directories(my_code PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/src)

# Ensure vcpkg is used for package management
if(NOT DEFINED CMAKE_TOOLCHAIN_FILE)
  set(CMAKE_TOOLCHAIN_FILE "${CMAKE_SOURCE_DIR}/vcpkg/scripts/buildsystems/vcpkg.cmake" CACHE STRING "Vcpkg toolchain file")
endif()

# Download and set up GoogleTest
include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.zip
)
# Explicitly print progress
set(FETCHCONTENT_QUIET OFF)
FetchContent_MakeAvailable(googletest)

# Print debug information to help diagnose issues
message(STATUS "GoogleTest source directory: ${gtest_SOURCE_DIR}")
message(STATUS "GoogleTest binary directory: ${gtest_BINARY_DIR}")

# Add GoogleTest
enable_testing()
include(GoogleTest)

# Helper function to create and configure test targets
function(configure_test_target target_name)
  target_link_libraries(${target_name} PRIVATE my_code gtest gtest_main)
  
  # Explicitly add include directories for GoogleTest
  target_include_directories(${target_name} PRIVATE
    ${gtest_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/src
  )
  
  # Set properties for better test discovery
  set_target_properties(${target_name} PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
  )
  
  gtest_discover_tests(${target_name})
endfunction()

# Unit Tests
file(GLOB UNIT_TEST_FILES "tests/unit/*.cpp")
add_executable(unit_tests ${UNIT_TEST_FILES})
configure_test_target(unit_tests)

# Integration Tests
file(GLOB INT_TEST_FILES "tests/integration/*.cpp")
add_executable(integration_tests ${INT_TEST_FILES})
configure_test_target(integration_tests)

# End-to-End Tests
file(GLOB E2E_TEST_FILES "tests/e2e/*.cpp")
add_executable(e2e_tests ${E2E_TEST_FILES})
configure_test_target(e2e_tests)

# Print final configuration for debugging
message(STATUS "C++ Compiler: ${CMAKE_CXX_COMPILER_ID} ${CMAKE_CXX_COMPILER_VERSION}")
message(STATUS "C++ Flags: ${CMAKE_CXX_FLAGS}")
