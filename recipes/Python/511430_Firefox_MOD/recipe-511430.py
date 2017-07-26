import os

################################################################################

# Keys / Fixes

AUTOCONFIG_URL = 'user_pref("network.proxy.autoconfig_url",', \
                 'user_pref("network.proxy.autoconfig_url", "http://home.my-name.edu/my-name.proxy");'
TYPE = 'user_pref("network.proxy.type",', \
       'user_pref("network.proxy.type", 2);'

################################################################################

# Configuration Options

IGNORE_USERS = 'All Users', 'LocalService', 'NetworkService'
SELECTED_FIXES = AUTOCONFIG_URL, TYPE

################################################################################

# Program Code

def main():
    user_folders = get_user_folders()
    for folder in user_folders:
        profiles_folder = os.path.join(folder, 'Application Data', 'Mozilla', 'Firefox', 'Profiles')
        if os.path.exists(profiles_folder):
            profiles = [os.path.join(profiles_folder, profile) for profile in os.listdir(profiles_folder)]
            fix_profiles(profiles)

def get_user_folders():
    return [os.path.join(r'C:\Documents and Settings', user) for user in os.listdir(r'C:\Documents and Settings') if user not in IGNORE_USERS]

def fix_profiles(profiles):
    for folder in profiles:
        file_name = os.path.join(folder, 'prefs.js')
        if os.path.exists(file_name):
            fix_file(file_name)

def fix_file(file_name):
    selected_fixes = get_selected_fixes()
    file_lines = file(file_name, 'rU').read().splitlines()
    for index, line in enumerate(file_lines):
        line = clean(line)
        for item in selected_fixes:
            key, fix = item[:2]
            if line.startswith(key):
                file_lines[index] = fix
                item[2] = False
                break
    for key, fix, not_fixed in selected_fixes:
        if not_fixed:
            file_lines.append(fix)
    file(file_name, 'w').write('\n'.join(file_lines))

def get_selected_fixes():
    return [[clean(key), fix, True] for key, fix in SELECTED_FIXES]

def clean(string):
    return string.strip().lower()

################################################################################

if __name__ == '__main__':
    main()
