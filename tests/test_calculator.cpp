#include "../src/calculator.h"
#include <gtest/gtest.h>

// Create a Calculator object
Calculator calc;

// Test Addition
TEST(CalculatorTest, Addition) {
  EXPECT_EQ(calc.add(2, 3), 5);
  EXPECT_EQ(calc.add(-2, -3), -5);
  EXPECT_EQ(calc.add(-2, 3), 1);
  EXPECT_EQ(calc.add(0, 0), 0);
}

// Test Subtraction
TEST(CalculatorTest, Subtraction) {
  EXPECT_EQ(calc.subtract(5, 3), 2);
  EXPECT_EQ(calc.subtract(-5, -3), -2);
  EXPECT_EQ(calc.subtract(-3, 5), -8);
  EXPECT_EQ(calc.subtract(0, 0), 0);
}

// Test Multiplication
TEST(CalculatorTest, Multiplication) {
  EXPECT_EQ(calc.multiply(4, 5), 20);
  EXPECT_EQ(calc.multiply(-4, 5), -20);
  EXPECT_EQ(calc.multiply(0, 5), 0);
  EXPECT_EQ(calc.multiply(-4, -5), 20);
}

// Test Division
TEST(CalculatorTest, Division) {
  EXPECT_EQ(calc.divide(10, 2), 5);
  EXPECT_EQ(calc.divide(9, 3), 3);
  EXPECT_EQ(calc.divide(-10, 2), -5);
  EXPECT_EQ(calc.divide(0, 5), 0);
}

// Test Division by Zero
TEST(CalculatorTest, DivisionByZero) {
  EXPECT_EQ(calc.divide(10, 0), -1); // Ensure division by zero returns -1
  EXPECT_EQ(calc.divide(-5, 0), -1);
  EXPECT_EQ(calc.divide(0, 0), -1);
}

// Main function for Google Test
int main(int argc, char **argv) {
  ::testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
