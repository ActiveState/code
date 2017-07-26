class SessionStatusListenerCallback : public SessionStatusListener
{
public:
	SessionStatusListenerCallback(PyObject *pyObject)
		: self(pyObject) {}

	SessionStatusListenerCallback(PyObject* pyObject, const SessionStatusListener& listener)
		: self(pyObject), SessionStatusListener(listener) {}

	void onSessionStatusChanged(O2GSessionStatus status)
	{
		// GIL state handler
		PyGILState_STATE gstate;
		gstate = PyGILState_Ensure();
		// Python callback
		call_method<void>(self, "onSessionStatusChanged", status);
		// GIL handler release
		PyGILState_Release(gstate);
	}
	
	void onLoginFailed(const char* error)
	{
		// GIL state handler
		PyGILState_STATE gstate;
		gstate = PyGILState_Ensure();
		// Python callback
		call_method<void>(self, "onLoginFailed", error);
		// GIL handler release
		PyGILState_Release(gstate);
	}
private:
	PyObject* const self;
};
