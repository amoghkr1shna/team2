#include "notifier.h"
#include <gtest/gtest.h>
#include <iostream>
#include <sstream>

class NotifierTest : public ::testing::Test {
  protected:
    Notifier notifier;
};

TEST_F(NotifierTest, NotificationTriggeredWhenThresholdExceeded) {
    std::stringstream buffer;
    std::streambuf *oldCout = std::cout.rdbuf(buffer.rdbuf());
    notifier.notify(15, 10);
    std::cout.rdbuf(oldCout);
    EXPECT_EQ(buffer.str(), "Alert: Result 15 exceeds threshold 10\n");
}

TEST_F(NotifierTest, NoNotificationWhenThresholdNotExceeded) {
    std::stringstream buffer;
    std::streambuf *oldCout = std::cout.rdbuf(buffer.rdbuf());
    notifier.notify(8, 10);
    std::cout.rdbuf(oldCout);
    EXPECT_EQ(buffer.str(), "");
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
