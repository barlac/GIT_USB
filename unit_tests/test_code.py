import pytest
from git import Repo
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname( os.path.realpath(__file__))))
print(sys.path)
from Code import git_usb
import shutil
import stat
import time



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
    remove_dir(SF_repo_path)
    global REPO   
    if not os.path.exists(SF_repo_path):
        REPO = Repo.clone_from(Shared_Folder_SSH, SF_repo_path)
    else:
        repo = Repo(SF_repo_path)
        origin = repo.remotes.origin
        origin.pull()

def teardown_module(module):
    """Teardown module"""

def remove_dir(path):
    """ teardown any state that was previously setup with a setup_module
    method.
    """
    try:
        shutil.rmtree(path, onerror=onerror)
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

def test_adding_a_file():
    """
    Unit test of adding a file involving pushing to remote.
    Goes through the process of adding a dummy file (removing an pushing it if it already exist)
    and checking all the outputs of the functions assosiated with checking the REPO status before
    and after the file is added.
    """
    usb1 = git_usb.GitUSB(SF_repo_path)
    origin = REPO.remotes.origin
    usb1.destruct()
    assert usb1.local_behind(REPO) == 0,"test failed, local_behind != 0"
    assert usb1.local_ahead(REPO) == 0,"test failed, local_ahead != 0"
    f_path = os.path.join(SF_repo_path, 'test_add_file.txt')
    if os.path.exists(os.path.join(SF_repo_path, 'test_add_file.txt')):
        # remove file and push
        os.remove(f_path)
        usb1.stage_and_commit_all(REPO, "UNIT TEST: Testing local ahead/behind - file delete.")
        print("f_path = {}".format(f_path))
        origin.push()
    with open(os.path.join(SF_repo_path, 'test_add_file.txt'), "w+") as file_1:
        file_1.write("This is a line of text to test")
    assert usb1.uncommitted_changes(REPO) == True, "test failed, testing for uncommitted changes"
    usb1.stage_and_commit_all(REPO, "UNIT TEST: Testing local ahead/behind.")
    assert usb1.local_ahead(REPO) == 1,"test failed, local_ahead != 0"
    origin.push()
    assert usb1.uncommitted_changes(REPO) == False, "test failed, testing for uncommitted changes"
    assert usb1.local_behind(REPO) == 0,"test failed, local_behind == 0"
    assert usb1.local_ahead(REPO) == 0,"test failed, local_ahead == 0"
    
def test_file1_repo_method():
    usb1 = git_usb.GitUSB(SF_repo_path)
    local_behind = usb1.local_behind(REPO)
    assert local_behind == 0,"test failed"

def test_two_git_usbs():
    usb1 = git_usb.GitUSB(SF_repo_path)
    usb2 = git_usb.GitUSB(SF_repo_path)
    assert True == False, "dummy failed"