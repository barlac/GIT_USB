"""
Authors: Lachlan Barnes & Freeman Porten
Description:

"""
import os
import sys #DELETE AFTER NEEDED
import threading

from git import Repo
from git import GitCommandError

#UI importing
from PyQt5 import QtCore, QtGui, QtWidgets, uic

# Global semaphore to ensure two sync folders instances are not called
SEMAPHORE = False

# Branch name
BRANCH = 'master'

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('MergeConflictWindow.ui', self) # Load the .ui file
        self.show() # Show the GUI



def Destruct():
    """ Stops the program from running"""
    sys.exit()

def GUI_merge_results(repo, file_list):
    
    
    """
    Freeman to potentially implement.
    Description:
    Use PythonQt to generate a GUI and allow users to select for each of
    the files with merge conflicts if they want to keep their version or the incoming
    version.

    Input: [0] file_list = A list of file names with merge conflicts.
    Outputs [0] ...to be named... = A dictionary of file names and status of if the
    current changed will be kept or overwritten by incoming changes.
    *** I/O types can change easily, just a sugestion :) ***
    """
    #return {'fileA': True, 'fileB': False, 'fileC': True}
    return dict.fromkeys(file_list , False)

def resolve_conflicts(repo, merge_results):
    unmerged_blobs = repo.index.unmerged_blobs()
    for file in merge_results:
        with open(file, 'wb') as fp:
            num_blobs = len(unmerged_blobs[os.path.basename(file)])
            if(merge_results[file]) and num_blobs < 3: # stay with current version
                #Extract blob object and write to file, first square braces indicates
                # which merge copy to take. ([0] = auto-merge, [1]= current [2] = incoming)
                (((unmerged_blobs[os.path.basename(file)])[num_blobs-2])[1]).stream_data(fp)
            elif(not merge_results[file]) and num_blobs < 3: 
                (((unmerged_blobs[os.path.basename(file)])[num_blobs-1])[1]).stream_data(fp)
            elif(merge_results[file]) and num_blobs < 2: 
                (((unmerged_blobs[os.path.basename(file)])[num_blobs-1])[1]).stream_data(fp)
            elif(not merge_results[file]) and num_blobs < 2: 
                (((unmerged_blobs[os.path.basename(file)])[num_blobs-0])[1]).stream_data(fp)
    print("Resolved Conflicts!")


def local_behind(repo):
    """
    Return a True/False if the local repo is behind master or not

    FUTURE CHANGES:
    Need to remove the local_behind output to reduce code in sync_folder
    """
    commits_behind_gen = repo.iter_commits('{}..origin/{}'.format(BRANCH, BRANCH))
    commits_behind = sum(1 for c2 in commits_behind_gen)
    return bool(commits_behind), commits_behind

def local_ahead(repo):
    """
    Return a True/False if the local repo is ahead of master or not
    
    FUTURE CHANGES:
    Need to remove the local_ahead output to reduce code in sync_folder
    """
    commits_ahead_gen = repo.iter_commits('origin/{}..{}'.format(BRANCH, BRANCH))
    commits_ahead = sum(1 for c1 in commits_ahead_gen)
    return bool(commits_ahead), commits_ahead

def uncommitted_changes(repo):
    """
    Return a True/False if the local repo has uncommitted changes or not
    """
    changed_files = [item.a_path for item in repo.index.diff(None)]
    untracked_files = repo.untracked_files
    return bool(len(changed_files) + len(untracked_files) + len(repo.index.diff("HEAD")))

def stage_and_commit_all(repo, commit_message):
    """
    Stage and commit all
    """
    print("Staging and commiting all")
    repo.git.add(A=True)
    repo.git.commit('-m', commit_message)
    return True

def check_for_conflicts(repo, origin):
    conflicts_found = False
    try:
        origin.pull()
    except GitCommandError:
        conflicts_found = True
        pass
    # Extract absolute file paths as a list
    conflicts_list = []
    for file in repo.index.unmerged_blobs().values():
        conflicts_list.append((file[1])[1].abspath)

    if(conflicts_found): print("The following files had merge conflicts; {}".format(conflicts_list))
    return conflicts_found, conflicts_list

def sync_folder(repo, origin):
    """
    Implements the flowchart on GitHub and syncs the "Shared_Folder" with another other users
    """
    print('\nStarting Sync!')
    origin.fetch()
    commit_needed = uncommitted_changes(repo)
    master_ahead, _ = local_behind(repo)
    if commit_needed:
        stage_and_commit_all(repo, 'Change in folder')
    if master_ahead:
        print("Pulling from master")
        conflicts_found, conflicts_list = check_for_conflicts(repo, origin)
        if(conflicts_found):
            merge_results = GUI_merge_results(repo, conflicts_list)
            resolve_conflicts(repo, merge_results)
            stage_and_commit_all(repo, 'Change from a merge')
    master_behind, _ = local_ahead(repo)
    _, x = local_behind(repo)
    _, y = local_ahead(repo)
    print("Behind {} commits, ahead {} commits.".format(x, y))

    if master_behind:
        print("Pushing to remote")
        origin.push()
    return False

def mytimer(repo, origin):
    """
    Timer object that creates a thread to call the sync folder function every X seconds.
    Uses the global semaphore to ensure that only one instance of the sync_folder is created.
    """
    threading.Timer(30.0, mytimer, args=(repo, origin,)).start()
    global SEMAPHORE
    if not SEMAPHORE:
        SEMAPHORE = True
        SEMAPHORE = sync_folder(repo, origin)

def main():
    """
    Function Main
    """
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()

    #Create repo object
    #print("Path = {}".format(sys.path))
    repo = Repo(os.path.join(os.path.dirname(os.path.dirname(
        os.path.realpath(__file__))), "Shared_Folder"))
    #Create origin object 
    origin = repo.remotes.origin
    threading.Timer(20.0, mytimer, args=(repo, origin,)).start()

if __name__ == '__main__':
    main()
