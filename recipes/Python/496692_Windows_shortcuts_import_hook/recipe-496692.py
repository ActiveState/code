import ihooks
import os
from imp import PKG_DIRECTORY
from win32com.shell import shell
import pythoncom

def resolve_shortcut(filename):
    """resolve_shortcut("Notepad.lnk") => "C:\WINDOWS\system32\notepad.exe"
    
    Returns the path refered to by a windows shortcut (.lnk) file.
    """
    
    shell_link = pythoncom.CoCreateInstance(
        shell.CLSID_ShellLink, None,
        pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)
    
    persistant_file = shell_link.QueryInterface(pythoncom.IID_IPersistFile)
    
    persistant_file.Load(filename)
    
    shell_link.Resolve(0, 0)
    linked_to_file = shell_link.GetPath(shell.SLGP_UNCPRIORITY)[0]
    return linked_to_file
    
def get_shortcut_paths(directory):
    """get_shortcut_paths("Programs") => ["...\Internet Explorer.lnk", ...]
    
    Returns the list of Windows shortcuts contained in a directory.
    """
    return [os.path.join(directory, f) for f in os.listdir(directory)
                if os.path.splitext(f)[1] == '.lnk']
                 
class ShortcutLoader(ihooks.ModuleLoader):
    """A hook to resolve Python imports through Windows shortcuts"""
    
    def recursive_match(self, name, dir, level=1):
        names = name.split('.')
        short_name = names[0]
        remaining_names = names[1:]
        
        try:
            pairs = [(f, resolve_shortcut(f)) for f in get_shortcut_paths(dir)]
        except WindowsError:
            # might not have permissions, shortcut might be broken, etc.
            pass
        else:
            for alias, resolved_path in pairs:
                if (os.path.splitext(os.path.basename(alias))[0] ==
                                                            short_name) and \
                   os.path.isdir(resolved_path) and \
                   os.path.exists(os.path.join(resolved_path, '__init__.py')):
                    
                    if len(remaining_names) > 0:
                        next_part = self.recursive_match(
                                        '.'.join(remaining_names),
                                        resolved_path,
                                        level + 1)
                        
                        if next_part is not None:                        
                            return os.path.join(resolved_path, next_part)
                    else:
                        return resolved_path
                    
        return None
        
    def find_module_in_dir(self, name, dir, allow_packages=1):
        if dir is None:
            return ihooks.ModuleLoader.find_module_in_dir(
                self, name, dir, allow_packages)
        else:
            if allow_packages:
                resolved_path = self.recursive_match(name, dir)
                
                if resolved_path is not None:
                    return (None, resolved_path, ('', '', PKG_DIRECTORY))
                
            return ihooks.ModuleLoader.find_module_in_dir(
                self, name, dir, allow_packages)

def install():
    """Install the import hook"""
    ihooks.install(ihooks.ModuleImporter(ShortcutLoader()))
