cmake_minimum_required(VERSION 3.15)
project(MyCppTemplate LANGUAGES CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Use C++20
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Option to enable coverage
option(ENABLE_COVERAGE "Enable coverage flags" ON)

# Enable testing
include(CTest)
enable_testing()

# Include GoogleTest module
include(GoogleTest)

# Added source code
file(GLOB SRC_FILES "src/*.cpp")
add_library(my_code ${SRC_FILES})
target_include_directories(my_code PUBLIC 
    ${CMAKE_CURRENT_SOURCE_DIR}/src
)

# Add compiler warnings
target_compile_options(my_code PRIVATE
    $<$<CXX_COMPILER_ID:GNU>:-Wall -Wextra -Wpedantic>
    $<$<CXX_COMPILER_ID:Clang>:-Wall -Wextra -Wpedantic>
    $<$<CXX_COMPILER_ID:MSVC>:/W4>
)

# Add coverage flags if enabled
if(ENABLE_COVERAGE)
  if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    target_compile_options(my_code PRIVATE -fprofile-instr-generate -fcoverage-mapping)
    target_link_options(my_code PRIVATE -fprofile-instr-generate -fcoverage-mapping)
  elseif(CMAKE_CXX_COMPILER_ID MATCHES "GNU")
    target_compile_options(my_code PRIVATE --coverage)
    target_link_options(my_code PRIVATE --coverage)
  endif()
endif()

# Include GoogleTest
include(FetchContent)
FetchContent_Declare(
  googletest
  GIT_REPOSITORY https://github.com/google/googletest.git
  GIT_TAG        v1.14.0
)

# Make GoogleTest available
FetchContent_MakeAvailable(googletest)

# Custom target to copy compile_commands.json to project root if it exists
add_custom_target(copy-compile-commands ALL
  COMMAND ${CMAKE_COMMAND} -E copy_if_different
          ${CMAKE_BINARY_DIR}/compile_commands.json
          ${CMAKE_SOURCE_DIR}/compile_commands.json
  BYPRODUCTS ${CMAKE_SOURCE_DIR}/compile_commands.json
  COMMENT "Copying compile_commands.json to source directory"
  VERBATIM
)
# Make the target optional so it doesn't fail if the file doesn't exist
set_target_properties(copy-compile-commands PROPERTIES
  ADDITIONAL_CLEAN_FILES "${CMAKE_SOURCE_DIR}/compile_commands.json"
)

# Helper function to create and configure test targets
function(configure_test_target target_name test_sources)
  add_executable(${target_name} ${test_sources})
  
  target_link_libraries(${target_name} PRIVATE 
    my_code
    gtest_main
  )
  
  # Make include paths explicit for tests
  target_include_directories(${target_name} PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/src
    ${googletest_SOURCE_DIR}/googletest/include
  )
  
  # Add same compiler flags as the main target
  target_compile_options(${target_name} PRIVATE
    $<$<CXX_COMPILER_ID:GNU>:-Wall -Wextra -Wpedantic>
    $<$<CXX_COMPILER_ID:Clang>:-Wall -Wextra -Wpedantic>
    $<$<CXX_COMPILER_ID:MSVC>:/W4>
  )
  
  # This enables CTest integration
  gtest_discover_tests(${target_name}
    PROPERTIES
      TIMEOUT 10  # Set timeout for tests
    DISCOVERY_TIMEOUT 20  # Set timeout for test discovery
  )
endfunction()

# Unit Tests
file(GLOB UNIT_TEST_FILES "tests/unit/*.cpp")
configure_test_target(unit_tests "${UNIT_TEST_FILES}")

# Integration Tests
file(GLOB INT_TEST_FILES "tests/integration/*.cpp")
configure_test_target(integration_tests "${INT_TEST_FILES}")

# End-to-End Tests
file(GLOB E2E_TEST_FILES "tests/e2e/*.cpp")
configure_test_target(e2e_tests "${E2E_TEST_FILES}")

# Print final configuration for debugging
message(STATUS "C++ Compiler: ${CMAKE_CXX_COMPILER_ID} ${CMAKE_CXX_COMPILER_VERSION}")
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "GoogleTest source directory: ${googletest_SOURCE_DIR}")
message(STATUS "GoogleTest include directory: ${googletest_SOURCE_DIR}/googletest/include")
