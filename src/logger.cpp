#include "logger.hpp"

void Logger::logOperation(const std::string& operation, int result) {
    logs_.push_back(operation + " = " + std::to_string(result));
}

const std::vector<std::string>& Logger::getLogs() const {
    return logs_;
}
