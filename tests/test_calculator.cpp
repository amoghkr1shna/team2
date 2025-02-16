#include "calculator.h"
#include <gtest/gtest.h>

class CalculatorTest : public ::testing::Test {
  protected:
    Calculator calc;
};

TEST_F(CalculatorTest, Addition) {
    EXPECT_EQ(calc.add(2, 3), 5);
    EXPECT_EQ(calc.add(-2, -3), -5);
    EXPECT_EQ(calc.add(-2, 3), 1);
    EXPECT_EQ(calc.add(0, 0), 0);
}

TEST_F(CalculatorTest, Subtraction) {
    EXPECT_EQ(calc.subtract(5, 3), 2);
    EXPECT_EQ(calc.subtract(3, 5), -2);
    EXPECT_EQ(calc.subtract(-3, -5), 2);
    EXPECT_EQ(calc.subtract(0, 0), 0);
}

TEST_F(CalculatorTest, Multiplication) {
    EXPECT_EQ(calc.multiply(2, 3), 6);
    EXPECT_EQ(calc.multiply(-2, 3), -6);
    EXPECT_EQ(calc.multiply(-2, -3), 6);
    EXPECT_EQ(calc.multiply(0, 5), 0);
}

TEST_F(CalculatorTest, Division) {
    EXPECT_EQ(calc.divide(6, 3), 2);
    EXPECT_EQ(calc.divide(5, 2), 2);
    EXPECT_EQ(calc.divide(-6, 3), -2);
    EXPECT_EQ(calc.divide(-6, -3), 2);
    EXPECT_EQ(calc.divide(0, 1), 0);
    EXPECT_EQ(calc.divide(10, 0), -1);
}

int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
