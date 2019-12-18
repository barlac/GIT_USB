import pytest
from .. import git_usb
from git import Repo
import os
import shutil
import stat

# Globals and constants
REPO = None
Shared_Folder_SSH = "git@github.com:barlac/Shared_Folder.git"
SF_repo_path =  os.path.join(os.path.dirname(__file__), "Shared Folder")

def setup_module(module):
    """ setup any state specific to the execution of the given module."""
    try:
        os.mkdir(SF_repo_path)
    except FileExistsError:
        pass
    global REPO
    REPO = Repo.clone_from(Shared_Folder_SSH, SF_repo_path)

def teardown_module(module):
    """ teardown any state that was previously setup with a setup_module
    method.
    """
    print("Deleting...")
    try:
        shutil.rmtree(SF_repo_path, onerror=onerror)
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))

def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    if not os.access(path, os.W_OK):
        # Is the error an access error ?
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

def test_file1_method1():
    x=5
    y=6
    assert x+1 == y, "test failed"
    assert x == y, "test failed"

def test_file1_method2():
    x=5
    y=6
    assert x+1 == y, "test failed" 

def test_file1_repo_method():
    usb1 = git_usb
    local_behind = usb1.local_behind(REPO)
    usb1.Destruct()
    assert local_behind != 0,"test failed" 

