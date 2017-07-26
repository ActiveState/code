#include <memory>

typedef std::auto_ptr<PyObject> auto_py_base;

class auto_py : public auto_py_base {
public:
	auto_py(PyObject * obj = NULL) : auto_py_base(obj) {
	}
	~auto_py() {
		reset();
	}
	void reset(PyObject * obj = NULL) {
		if(obj != get()) {
			PyObject * old = release(); // Avoid the delete call
			Py_XDECREF(old);
			auto_py_base::reset(obj);
		}
	}
	void inc() {
		PyObject * ptr = get();
		if(ptr)
			Py_INCREF(ptr);
	}
};
