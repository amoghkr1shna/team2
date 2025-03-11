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

# Include GoogleTest module - this is critical for gtest_discover_tests
include(GoogleTest)

# Add your source code
file(GLOB SRC_FILES "src/*.cpp")
add_library(my_code ${SRC_FILES})
target_include_directories(my_code PUBLIC 
  ${CMAKE_CURRENT_SOURCE_DIR}/src
)

# Include GoogleTest
include(FetchContent)
FetchContent_Declare(
  googletest
  GIT_REPOSITORY https://github.com/google/googletest.git
  GIT_TAG        v1.14.0
)

# Print less noise during the build
set(FETCHCONTENT_QUIET OFF)

# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)

# Make GoogleTest available
FetchContent_MakeAvailable(googletest)

# Custom target to copy compile_commands.json to project root
add_custom_target(copy-compile-commands ALL
  ${CMAKE_COMMAND} -E copy_if_different
  ${CMAKE_BINARY_DIR}/compile_commands.json
  ${CMAKE_SOURCE_DIR}/compile_commands.json
  DEPENDS ${CMAKE_BINARY_DIR}/compile_commands.json
  COMMENT "Copying compile_commands.json to source directory"
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
  
  # Set properties for better test discovery
  set_target_properties(${target_name} PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
  )
  
  # Alternative approach for older CMake versions
  if(CMAKE_VERSION VERSION_LESS 3.10)
    # For older CMake versions without gtest_discover_tests
    add_test(NAME ${target_name} COMMAND ${target_name})
  else()
    # This enables CTest integration
    gtest_discover_tests(${target_name}
      PROPERTIES
        TIMEOUT 10  # Set timeout for tests
      DISCOVERY_TIMEOUT 20  # Set timeout for test discovery
    )
  endif()
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
message(STATUS "C++ Flags: ${CMAKE_CXX_FLAGS}")
message(STATUS "GoogleTest source directory: ${googletest_SOURCE_DIR}")
message(STATUS "GoogleTest include directory: ${googletest_SOURCE_DIR}/googletest/include")
