#pragma once
#include <string>
#include <vector>

class Logger {
public:
  void logOperation(const std::string &operation, int result) const;
  [[nodiscard]] auto getLogs() const -> const std::vector<std::string> &;

private:
  mutable std::vector<std::string> logs_;
};
