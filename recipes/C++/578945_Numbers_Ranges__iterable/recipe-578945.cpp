#ifndef NUM_RANGE
#define NUM_RANGE

template<typename T>
struct Derefable { 
        const T& operator*() const { return x; }
        operator T&() { return x; }
        Derefable(const T& x=T{}) : x{x} { }
private:
        T x;
};      

namespace std {
template <typename T> Derefable<T> begin(const T&) { return {}; }
template <typename T> Derefable<T> end(const T& x) { return x; }
}

// usage example
// for (int i : 5) { ... }

#endif
