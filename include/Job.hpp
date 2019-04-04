#ifndef Job_hpp
#define Job_hpp

#include <atomic>
#include <vector>

template <class T>
class Job{
    private:
        std::atomic<char> status;
        std::vector<T> jobElements();
    public:
        Job();
        ~Job();
};

#endif
