// #include "notifier.hpp"
#include "src/notifier/include/notifier.hpp"
#include <string> // Include for std::string and std::to_string

auto Notifier::shouldNotify(int value) const -> bool {
  return value > threshold_;
}

auto Notifier::notifyMessage(int value) const -> std::string {
  if (shouldNotify(value)) {
    return "Threshold exceeded! Value: " + std::to_string(value);
  }
  return "Value within threshold.";
}
