#include <string>
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <functional>

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

    std::string buffer(size, '\0');
    if (!file.read(buffer.data(), size)) {
        throw std::runtime_error("Unable to read file");
    }

    return buffer;
}

inline size_t clength(const std::string& x){
    return x.size();
}
