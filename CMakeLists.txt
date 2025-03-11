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

# GoogleTest setup - The proper way
# First, set policy to avoid unnecessary warnings
if(POLICY CMP0135)
  cmake_policy(SET CMP0135 NEW)
endif()

# Include GoogleTest directly
include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.zip
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
)

# GoogleTest's CMake setup provides proper targets and includes
FetchContent_MakeAvailable(googletest)

# For debugging, print the directories
get_target_property(GTEST_INCLUDE_DIRS GTest::gtest INTERFACE_INCLUDE_DIRECTORIES)
message(STATUS "GoogleTest include directories: ${GTEST_INCLUDE_DIRS}")

# Create a common test setup function
function(setup_test TEST_NAME TEST_SOURCES)
  add_executable(${TEST_NAME} ${TEST_SOURCES})
  target_link_libraries(${TEST_NAME} PRIVATE
    my_code
    GTest::gtest_main
  )
  # GTest::gtest_main already brings in the correct include paths
  
  # For clang-tidy to find headers, add explicit include path
  target_include_directories(${TEST_NAME} PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/src
  )
  
  # Set up test discovery
  gtest_discover_tests(${TEST_NAME}
    PROPERTIES
      ENVIRONMENT "PATH=$ENV{PATH}"
  )
endfunction()

# Unit Tests
file(GLOB UNIT_TEST_FILES "tests/unit/*.cpp")
setup_test(unit_tests "${UNIT_TEST_FILES}")

# Integration Tests
file(GLOB INT_TEST_FILES "tests/integration/*.cpp")
setup_test(integration_tests "${INT_TEST_FILES}")

# End-to-End Tests
file(GLOB E2E_TEST_FILES "tests/e2e/*.cpp")
setup_test(e2e_tests "${E2E_TEST_FILES}")

# Print build configuration for debugging
message(STATUS "C++ Compiler: ${CMAKE_CXX_COMPILER_ID} ${CMAKE_CXX_COMPILER_VERSION}")
message(STATUS "C++ Flags: ${CMAKE_CXX_FLAGS}")
