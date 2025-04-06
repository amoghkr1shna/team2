// #include "logger.hpp"
#include "src\logger\include\logger.hpp"
#include <gtest/gtest.h>

TEST(LoggerTests, TestLogOperation) {
  Logger logger;
  logger.logOperation("2 + 3", 5);
  logger.logOperation("5 * 2", 10);

  auto logs = logger.getLogs();
  ASSERT_EQ(logs.size(), 2u);
  EXPECT_EQ(logs[0], "2 + 3 = 5");
  EXPECT_EQ(logs[1], "5 * 2 = 10");
}
