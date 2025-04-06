// #include "notifier.hpp"
#include "src/notifier/include/notifier.hpp"
#include <gtest/gtest.h>

TEST(NotifierTests, TestThresholdNotExceeded) {
  Notifier notifier(10);
  EXPECT_FALSE(notifier.shouldNotify(5));
  EXPECT_EQ(notifier.notifyMessage(5), "Value within threshold.");
}

TEST(NotifierTests, TestThresholdExceeded) {
  Notifier notifier(10);
  EXPECT_TRUE(notifier.shouldNotify(15));
  EXPECT_EQ(notifier.notifyMessage(15), "Threshold exceeded! Value: 15");
}
