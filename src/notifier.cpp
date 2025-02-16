#include "notifier.h"
void Notifier::notify(int result, int threshold) {
    if (result > threshold) {
        std::cout << "Alert: Result " << result << " exceeds threshold " << threshold << std::endl;
    }
}
