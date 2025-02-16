#include "notifier.hpp"

bool Notifier::shouldNotify(int value) const {
    return value > threshold_;
}

std::string Notifier::notifyMessage(int value) const {
    if (shouldNotify(value)) {
        return "Threshold exceeded! Value: " + std::to_string(value);
    }
    return "Value within threshold.";
}
