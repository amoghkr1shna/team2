#include <gtest/gtest.h>
#include "calculator.hpp"
#include "logger.hpp"
#include "notifier.hpp"

// Full scenario: Calculate, log, notify if threshold exceeded
TEST(EndToEndTests, FullFlow) {
    Calculator calc;
    Logger logger;
    Notifier notifier(10);

    int result = calc.multiply(5, 3); // 15
    logger.logOperation("5 * 3", result);
    bool notify = notifier.shouldNotify(result);

    // Check logs
    auto logs = logger.getLogs();
    ASSERT_EQ(logs.size(), 1u);
    EXPECT_EQ(logs[0], "5 * 3 = 15");

    // Check notifier
    EXPECT_TRUE(notify);
    EXPECT_EQ(notifier.notifyMessage(result), "Threshold exceeded! Value: 15");
}
