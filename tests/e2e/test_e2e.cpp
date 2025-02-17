#include "calculator.hpp"
#include "logger.hpp"
#include "notifier.hpp"
#include <gtest/gtest.h>

// Full scenario: Calculate, log, notify if threshold exceeded
constexpr int kMultiplier1 = 5;
constexpr int kMultiplier2 = 3;
constexpr int kThreshold = 10;

TEST(EndToEndTests, FullFlow) {
  Calculator calc;
  Logger logger;
  Notifier notifier(kThreshold);

  int result = calc.multiply(kMultiplier1, kMultiplier2); // 15
  logger.logOperation("5 * 3", result);
  bool notify = notifier.shouldNotify(result);

  // Check logs
  auto logs = logger.getLogs();
  ASSERT_EQ(logs.size(), 1U);
  EXPECT_EQ(logs[0], "5 * 3 = 15");

  // Check notifier
  EXPECT_TRUE(notify);
  EXPECT_EQ(notifier.notifyMessage(result), "Threshold exceeded! Value: 15");
}
