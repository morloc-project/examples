#include <string>
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <functional>
#include <iostream>

// copy a string, swap the first and last 
std::string cmock(const std::string& x) {
    if(x.size() <= 2){
        return x;
    }
    std::string y = x;
    char c = y[0];
    y[0] = y[y.size()-1];
    y[y.size()-1] = c;
    return y;
}

template<typename T, typename F>
T cnTimes(int n, F f, const T& x) {
    if(n <= 0){
        return x;
    }
    T y = f(x);
    for (int i = 1; i < n; ++i) {
        y = f(y);
    }
    return y;
}

std::string cslurp(const std::string& filename) {
    std::ifstream file(filename, std::ios::binary | std::ios::ate);
    if (!file.is_open()) {
        throw std::runtime_error("Unable to open file");
    }

    std::streamsize size = file.tellg();
    file.seekg(0, std::ios::beg);

    std::string result(size, '\0');
    if (!file.read(result.data(), size)) {
        throw std::runtime_error("Unable to read file");
    }

    return result;
}



int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <n> <filename>" << std::endl;
        return 1;
    }

    int n;
    std::string filename;

    n = std::stoi(argv[1]);
    filename = argv[2];

    // Read the file content
    std::string content = cslurp(filename);

    // Apply cmock n times
    std::string result = cnTimes(n, cmock, content);

    // Get the length of the final string
    size_t finalLength = result.size();

    // Print the final length
    std::cout << "Final length: " << finalLength << std::endl;

    return 0;
}
