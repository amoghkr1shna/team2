# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.31

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /opt/homebrew/bin/cmake

# The command to remove a file.
RM = /opt/homebrew/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/adithyahnair/Downloads/OSPSD/team2

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/adithyahnair/Downloads/OSPSD/team2/build

# Include any dependencies generated for this target.
include CMakeFiles/e2e_tests.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/e2e_tests.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/e2e_tests.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/e2e_tests.dir/flags.make

CMakeFiles/e2e_tests.dir/codegen:
.PHONY : CMakeFiles/e2e_tests.dir/codegen

CMakeFiles/e2e_tests.dir/tests/e2e/test_e2e.cpp.o: CMakeFiles/e2e_tests.dir/flags.make
CMakeFiles/e2e_tests.dir/tests/e2e/test_e2e.cpp.o: /Users/adithyahnair/Downloads/OSPSD/team2/tests/e2e/test_e2e.cpp
CMakeFiles/e2e_tests.dir/tests/e2e/test_e2e.cpp.o: CMakeFiles/e2e_tests.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/Users/adithyahnair/Downloads/OSPSD/team2/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/e2e_tests.dir/tests/e2e/test_e2e.cpp.o"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT CMakeFiles/e2e_tests.dir/tests/e2e/test_e2e.cpp.o -MF CMakeFiles/e2e_tests.dir/tests/e2e/test_e2e.cpp.o.d -o CMakeFiles/e2e_tests.dir/tests/e2e/test_e2e.cpp.o -c /Users/adithyahnair/Downloads/OSPSD/team2/tests/e2e/test_e2e.cpp

CMakeFiles/e2e_tests.dir/tests/e2e/test_e2e.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing CXX source to CMakeFiles/e2e_tests.dir/tests/e2e/test_e2e.cpp.i"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/adithyahnair/Downloads/OSPSD/team2/tests/e2e/test_e2e.cpp > CMakeFiles/e2e_tests.dir/tests/e2e/test_e2e.cpp.i

CMakeFiles/e2e_tests.dir/tests/e2e/test_e2e.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling CXX source to assembly CMakeFiles/e2e_tests.dir/tests/e2e/test_e2e.cpp.s"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/adithyahnair/Downloads/OSPSD/team2/tests/e2e/test_e2e.cpp -o CMakeFiles/e2e_tests.dir/tests/e2e/test_e2e.cpp.s

# Object files for target e2e_tests
e2e_tests_OBJECTS = \
"CMakeFiles/e2e_tests.dir/tests/e2e/test_e2e.cpp.o"

# External object files for target e2e_tests
e2e_tests_EXTERNAL_OBJECTS =

e2e_tests: CMakeFiles/e2e_tests.dir/tests/e2e/test_e2e.cpp.o
e2e_tests: CMakeFiles/e2e_tests.dir/build.make
e2e_tests: libmy_code.a
e2e_tests: /opt/homebrew/opt/googletest/lib/libgtest_main.a
e2e_tests: /opt/homebrew/opt/googletest/lib/libgtest.a
e2e_tests: CMakeFiles/e2e_tests.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --bold --progress-dir=/Users/adithyahnair/Downloads/OSPSD/team2/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable e2e_tests"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/e2e_tests.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/e2e_tests.dir/build: e2e_tests
.PHONY : CMakeFiles/e2e_tests.dir/build

CMakeFiles/e2e_tests.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/e2e_tests.dir/cmake_clean.cmake
.PHONY : CMakeFiles/e2e_tests.dir/clean

CMakeFiles/e2e_tests.dir/depend:
	cd /Users/adithyahnair/Downloads/OSPSD/team2/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/adithyahnair/Downloads/OSPSD/team2 /Users/adithyahnair/Downloads/OSPSD/team2 /Users/adithyahnair/Downloads/OSPSD/team2/build /Users/adithyahnair/Downloads/OSPSD/team2/build /Users/adithyahnair/Downloads/OSPSD/team2/build/CMakeFiles/e2e_tests.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : CMakeFiles/e2e_tests.dir/depend

