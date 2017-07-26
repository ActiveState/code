import ctypes

class disable_file_system_redirection:
    _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
    _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection
    def __enter__(self):
        self.old_value = ctypes.c_long()
        self.success = self._disable(ctypes.byref(self.old_value))
    def __exit__(self, type, value, traceback):
        if self.success:
            self._revert(self.old_value)


#Example usage
import os

path = 'C:\\Windows\\System32\\msg.exe'

print os.path.exists(path)
with disable_file_system_redirection():
    print os.path.exists(path)
print os.path.exists(path)
