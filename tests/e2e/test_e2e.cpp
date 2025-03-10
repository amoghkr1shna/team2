#include "../../src/calculator.hpp"
#include "../../src/logger.hpp"
#include "../../src/notifier.hpp"
#include <gtest/gtest.h>

// Full scenario: Calculate, log, notify if threshold exceeded
constexpr int kMultiplier1 = 5;
constexpr int kMultiplier2 = 3;
constexpr int kThreshold = 10;

TEST(EndToEndTests, FullFlow) {
  const Calculator calc;
  const Logger logger;
  const Notifier notifier(kThreshold);

  const int result = Calculator::multiply(kMultiplier1, kMultiplier2);
  logger.logOperation("5 * 3", result);
  const bool notify = notifier.shouldNotify(result);

  // Check logs
  auto logs = logger.getLogs();
  ASSERT_EQ(logs.size(), 1U);
  EXPECT_EQ(logs[0], "5 * 3 = 15");

  // Check notifier
  EXPECT_TRUE(notify);
  EXPECT_EQ(notifier.notifyMessage(result), "Threshold exceeded! Value: 15");
  return;
}
