#include "logger.h"
#include <gtest/gtest.h>
#include <iostream>
#include <sstream>

class LoggerTest : public ::testing::Test {
  protected:
    Logger logger;
};

TEST_F(LoggerTest, LogsCorrectOperation) {
    std::stringstream buffer;
    std::streambuf *oldCout = std::cout.rdbuf(buffer.rdbuf());
    logger.logOperation("Test operation");
    std::cout.rdbuf(oldCout);
    EXPECT_EQ(buffer.str(), "Logged: Test operation\n");
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
