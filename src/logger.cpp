#include "logger.h"
#include <iostream>
void Logger::logOperation(const std::string& operation) {
    std::cout << "Logged: " << operation << std::endl;
}



