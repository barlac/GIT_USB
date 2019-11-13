import os
from git import Repo
import threading

# Global semaphore to ensure two sync folders instances are not called 
semaphore = False

def get_merge_results(file_list):
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
    return {'fileA': True, 'fileB': False, 'fileC': True}

def behind_master(repo):
    """
    Return a True/False if the local repo is behind master or not
    """
    commits_behind_gen = repo.iter_commits('master..origin/master')
    commits_behind = sum(1 for c2 in commits_behind_gen)
    # commits_ahead_gen = repo.iter_commits('origin/master..master')
    # commits_ahead = sum(1 for c1 in commits_ahead_gen)
    return bool(commits_behind)

def uncommitted_changes(repo):
    """
    Return a True/False if the local repo has uncommitted changes or not
    """
    changedFiles = [ item.a_path for item in repo.index.diff(None) ]
    untrackedFiles = repo.untracked_files
    return bool(len(changedFiles) + len(untrackedFiles))

def stage_and_commit_all(repo):
    print("Staging and commiting all")
    return 1

def sync_folder(repo):
    """
    Implements the flowchart on GitHub and when called syncs the "Shared_Folder" with another other users
    """
    print('Starting Sync!')
    commit_needed = uncommitted_changes(repo)
    master_ahead = behind_master(repo)
    if(master_ahead & commit_needed):
        stage_and_commit_all(repo)
    return False

def mytimer(repo):
    """
    Timer object that creates a thread to call the sync folder function every X seconds.
    Uses the global semaphore to ensure that only one instance of the sync_folder is created.
    """
    global semaphore
    threading.Timer(3.0, mytimer, args=(repo,)).start()
    if(not semaphore):
        semaphore = True
        semaphore = sync_folder(repo)

def main():
    """
    Function Main
    """
    #Create repo object
    repo = Repo(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Shared_Folder"))
    threading.Timer(3.0, mytimer, args=(repo,)).start()

if __name__ == '__main__':
    main()