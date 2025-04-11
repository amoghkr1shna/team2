#include "calculator.hpp"
// #include "src\calculator\include\calculator.hpp"

#include <gtest/gtest.h>

TEST(CalculatorTests, TestAddition) {
  Calculator calc;
  EXPECT_EQ(calc.add(2, 3), 5);
}

TEST(CalculatorTests, TestSubtraction) {
  Calculator calc;
  EXPECT_EQ(calc.subtract(5, 3), 2);
}

TEST(CalculatorTests, TestMultiplication) {
  Calculator calc;
  EXPECT_EQ(calc.multiply(4, 2), 8);
}
