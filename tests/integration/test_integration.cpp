#include "../../src/calculator.hpp"
#include "../../src/logger.hpp"
#include "../../src/notifier.hpp"
#include <gtest/gtest.h>

TEST(IntegrationTests, CalculatorLoggerIntegration) {
  Calculator calc;
  Logger logger;
  int result = calc.add(2, 3);
  logger.logOperation("2 + 3", result);

  auto logs = logger.getLogs();
  ASSERT_EQ(logs.size(), 1u);
  EXPECT_EQ(logs[0], "2 + 3 = 5");
}

// Add additional integration tests that might mock or skip the real Notifier,
// etc.
