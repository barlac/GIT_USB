"""
Authors: Lachlan Barnes & Freeman Porten
Description:

"""
import os
import threading

from git import Repo
from git import GitCommandError
# Global semaphore to ensure two sync folders instances are not called
SEMAPHORE = False

# Branch name
BRANCH = 'master'

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

def resolve_merge_results(merge_results):
    return True


def behind_master(repo):
    """
    Return a True/False if the local repo is behind master or not
    """
    commits_behind_gen = repo.iter_commits('{}..origin/{}'.format(BRANCH, BRANCH))
    commits_behind = sum(1 for c2 in commits_behind_gen)
    #commits_ahead_gen = repo.iter_commits('origin/master..master')
    #commits_ahead = sum(1 for c1 in commits_ahead_gen)
    return bool(commits_behind)

def uncommitted_changes(repo):
    """
    Return a True/False if the local repo has uncommitted changes or not
    """
    changed_files = [item.a_path for item in repo.index.diff(None)]
    untracked_files = repo.untracked_files
    return bool(len(changed_files) + len(untracked_files) + len(repo.index.diff("HEAD")))

def stage_and_commit_all(repo):
    """
    Stage and commit all
    """
    print("Staging and commiting all")
    repo.git.add(A=True)
    repo.git.commit('-m', 'test commit')
    return True

def check_for_conflicts(repo, origin):
    conflict_found = False
    try:
        origin.pull()
    except GitCommandError:
        conflict_found = True
        pass
    return conflict_found

def sync_folder(repo, origin):
    """
    Implements the flowchart on GitHub and syncs the "Shared_Folder" with another other users
    """
    print('Starting Sync!')
    origin.fetch()
    commit_needed = uncommitted_changes(repo)
    master_ahead = behind_master(repo)
    if commit_needed:
        stage_and_commit_all(repo)
    if master_ahead:
        print("Pulling from master")
        conflicts_found = check_for_conflicts(repo, origin)
    if(conflicts_found):
        merge_results = get_merge_results(repo)

    return False

def mytimer(repo, origin):
    """
    Timer object that creates a thread to call the sync folder function every X seconds.
    Uses the global semaphore to ensure that only one instance of the sync_folder is created.
    """
    global SEMAPHORE
    threading.Timer(5.0, mytimer, args=(repo, origin,)).start()
    if not SEMAPHORE:
        SEMAPHORE = True
        SEMAPHORE = sync_folder(repo, origin)

def main():
    """
    Function Main
    """
    #Create repo object
    repo = Repo(os.path.join(os.path.dirname(os.path.dirname(
        os.path.realpath(__file__))), "Shared_Folder"))
    #Create origin object 
    origin = repo.remotes.origin
    threading.Timer(5.0, mytimer, args=(repo, origin,)).start()

if __name__ == '__main__':
    main()
