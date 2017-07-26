## Check for package updates on PyPI (works best in pip+virtualenv)  
Originally published: 2011-05-19 17:54:42  
Last updated: 2011-05-19 17:54:43  
Author: Artur Siekielski  
  
Pip has an option to upgrade a package (_pip install -U_), however it always downloads sources even if there is already a newest version installed. If you want to check updates for all installed packages then some scripting is required.

This script checks if there is a newer version on PyPI for every installed package. It only prints information about available version and doesn't do any updates. Example output:

    distribute 0.6.15                        0.6.16 available
    Baker 1.1                                up to date
    Django 1.3                               up to date
    ipython 0.10.2                           up to date
    gunicorn 0.12.1                          0.12.2 available
    pyprof2calltree 1.1.0                    up to date
    profilestats 1.0.2                       up to date
    mercurial 1.8.3                          up to date
