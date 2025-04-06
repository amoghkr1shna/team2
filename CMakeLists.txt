cmake_minimum_required(VERSION 3.15)
project(MyCppTemplate LANGUAGES CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Use C++20
set(CMAKE_CXX_STANDARD 20)
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

# Collect all .cpp files excluding tests
file(GLOB_RECURSE ALL_SRC_FILES CONFIGURE_DEPENDS "src/*/*.cpp")

# Filter out test files
set(SRC_FILES "")
foreach(file ${ALL_SRC_FILES})
  if(NOT file MATCHES "/test/")
    list(APPEND SRC_FILES ${file})
  endif()
endforeach()

# Collect include directories from src/*/include
file(GLOB_RECURSE INCLUDE_HEADERS CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/src/*/include/*.hpp")

set(ALL_INCLUDES "")
foreach(header ${INCLUDE_HEADERS})
  get_filename_component(dir ${header} DIRECTORY)
  list(APPEND ALL_INCLUDES ${dir})
endforeach()
list(REMOVE_DUPLICATES ALL_INCLUDES)

# Add the main library
add_library(my_code ${SRC_FILES})

# Add include directories to the library
target_include_directories(my_code PUBLIC ${ALL_INCLUDES})

# Include GoogleTest
include(FetchContent)
FetchContent_Declare(
  googletest
  GIT_REPOSITORY https://github.com/google/googletest.git
  GIT_TAG        v1.14.0
)

# Make GoogleTest available
FetchContent_MakeAvailable(googletest)
include(GoogleTest)

# Function to configure test targets
function(configure_test_target target_name test_sources)
  add_executable(${target_name} ${test_sources})

  target_link_libraries(${target_name} PRIVATE 
    my_code
    gtest_main
  )
  
  # Make include paths explicit for tests
  target_include_directories(${target_name} PRIVATE
    ${ALL_INCLUDES}
    ${googletest_SOURCE_DIR}
    ${googletest_SOURCE_DIR}/googletest/include
  )
  
  # Set properties for better test discovery
  set_target_properties(${target_name} PROPERTIES
    CXX_STANDARD 20
    CXX_STANDARD_REQUIRED ON
  )
  
  # Use gtest_discover_tests for all CMake versions that support it
  gtest_discover_tests(${target_name}
    PROPERTIES
      TIMEOUT 10  # Set timeout for tests
    DISCOVERY_TIMEOUT 20  # Set timeout for test discovery
  )
endfunction()

# Unit Tests
file(GLOB_RECURSE UNIT_TEST_FILES CONFIGURE_DEPENDS "src/*/test/test_*.cpp")
configure_test_target(unit_tests "${UNIT_TEST_FILES}")

# Integration Tests
file(GLOB INTEGRATION_TEST_FILES CONFIGURE_DEPENDS "tests/integration/*.cpp")
configure_test_target(integration_tests "${INTEGRATION_TEST_FILES}")

# End-to-End Tests
file(GLOB E2E_TEST_FILES CONFIGURE_DEPENDS "tests/e2e/*.cpp")
configure_test_target(e2e_tests "${E2E_TEST_FILES}")

# Copy compile_commands.json to project root
add_custom_target(copy-compile-commands ALL
  COMMAND ${CMAKE_COMMAND} -E copy_if_different
    ${CMAKE_BINARY_DIR}/compile_commands.json
    ${CMAKE_SOURCE_DIR}/compile_commands.json
  BYPRODUCTS ${CMAKE_SOURCE_DIR}/compile_commands.json
  COMMENT "Copying compile_commands.json to source directory"
)

# Debug info
message(STATUS "C++ Compiler: ${CMAKE_CXX_COMPILER_ID} ${CMAKE_CXX_COMPILER_VERSION}")
message(STATUS "C++ Flags: ${CMAKE_CXX_FLAGS}")
message(STATUS "GoogleTest source dir: ${googletest_SOURCE_DIR}")
message(STATUS "GoogleTest include: ${googletest_SOURCE_DIR}/googletest/include")
message(STATUS "Project include directories: ${ALL_INCLUDES}")
