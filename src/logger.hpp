#pragma once
#include <string>
#include <vector>

class Logger {
public:
    void logOperation(const std::string& operation, int result);
    const std::vector<std::string>& getLogs() const;

private:
    std::vector<std::string> logs_;
};
