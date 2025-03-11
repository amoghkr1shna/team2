cmake_minimum_required(VERSION 3.15)
project(MyCppTemplate LANGUAGES CXX)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Use C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Define compiler flags based on compiler
if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  # Clang-specific flags
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wpedantic")
  # Disable specific warnings that are triggering errors
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-error=modernize-use-trailing-return-type -Wno-error=readability-named-parameter")
elseif(CMAKE_CXX_COMPILER_ID MATCHES "GNU")
  # GCC-specific flags
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wpedantic")
endif()

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

# Download and set up GoogleTest
include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.zip
)
# For older CMake versions
set(FETCHCONTENT_QUIET OFF)
# For newer CMake versions
set(FETCHCONTENT_UPDATES_DISCONNECTED ON)
FetchContent_MakeAvailable(googletest)

# Add GoogleTest
enable_testing()
include(GoogleTest)

# Function to create test targets with proper configuration
function(create_test_target TARGET_NAME SOURCE_FILES)
  add_executable(${TARGET_NAME} ${SOURCE_FILES})
  target_link_libraries(${TARGET_NAME} PRIVATE my_code gtest_main)
  target_include_directories(${TARGET_NAME} PRIVATE 
    ${gtest_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/src
  )
  gtest_discover_tests(${TARGET_NAME})
endfunction()

# Unit Tests
file(GLOB UNIT_TEST_FILES "tests/unit/*.cpp")
create_test_target(unit_tests "${UNIT_TEST_FILES}")

# Integration Tests
file(GLOB INT_TEST_FILES "tests/integration/*.cpp")
create_test_target(integration_tests "${INT_TEST_FILES}")

# End-to-End Tests
file(GLOB E2E_TEST_FILES "tests/e2e/*.cpp")
create_test_target(e2e_tests "${E2E_TEST_FILES}")

# Print debug information
message(STATUS "C++ Compiler: ${CMAKE_CXX_COMPILER_ID} ${CMAKE_CXX_COMPILER_VERSION}")
message(STATUS "C++ Flags: ${CMAKE_CXX_FLAGS}")
message(STATUS "GoogleTest source dir: ${gtest_SOURCE_DIR}")
