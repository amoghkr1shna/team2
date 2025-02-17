#include "logger.hpp"
#include <string>  // Include for std::string
#include <vector>  // Include for std::vector
#include <string>  // Include for std::to_string

void Logger::logOperation(const std::string& operation, int result) {
    logs_.push_back(operation + " = " + std::to_string(result));
}

auto Logger::getLogs() const -> const std::vector<std::string>& {
    return logs_;
}
