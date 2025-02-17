#pragma once
#include <string>

class Notifier {
public:
    Notifier(int threshold) : threshold_(threshold) {}
    
    [[nodiscard]] auto shouldNotify(int value) const -> bool;
    [[nodiscard]] auto notifyMessage(int value) const -> std::string;

private:
    int threshold_;
};
