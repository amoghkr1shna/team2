#pragma once
#include <string>

class Notifier {
public:
    Notifier(int threshold) : threshold_(threshold) {}
    bool shouldNotify(int value) const;
    std::string notifyMessage(int value) const;

private:
    int threshold_;
};
