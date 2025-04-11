#include "logger.hpp"
// #include "src/logger/include/logger.hpp"
#include <string> // Include for std::string and std::to_string
#include <vector> // Include for std::vector

void Logger::logOperation(const std::string &operation, int result) const {
  logs_.push_back(operation + " = " + std::to_string(result));
}

auto Logger::getLogs() const -> const std::vector<std::string> & {
  return logs_;
}
