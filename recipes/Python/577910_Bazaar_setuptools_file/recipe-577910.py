import setuptools
import os

def bzr_find_files(dirname):
    """Find versioned files using bzr, for use in 'setuptools.file_finders'
    entry point in setup.py."""
    cmd = 'bzr ls --versioned ' + dirname
    proc = subprocess.Popen(
        cmd.split(), stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, _stderr = proc.communicate()
    return stdout.splitlines()  # pylint: disable=E1103

setuptools.setup(
    name='example',
    entry_points={
        'setuptools.file_finders': [
            'bzr = bzr_find_files',
        ],
    },
)
