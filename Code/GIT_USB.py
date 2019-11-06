import os
from git import Repo

def get_merge_results(file_list):
    # Freeman to potentially implement.
    # Description:
    # Use PythonQt to generate a GUI and allow users to select for each of
    # the files with merge conflicts if they want to keep their version or the incoming
    # version.

    # Input: [0] file_list = A list of file names with merge conflicts.
    # Outputs [0] ...to be named... = A dictionary of file names and status of if the 
    # current changed will be kept or overwritten by incoming changes.
    # *** I/O types can change easily, just a sugestion :) ***
    return {'fileA': True, 'fileB': False, 'fileC': True}

def behind_master(repo):
    commits_behind_gen = repo.iter_commits('master..origin/master')
    commits_behind = sum(1 for c2 in commits_behind_gen)
    # commits_ahead_gen = repo.iter_commits('origin/master..master')
    # commits_ahead = sum(1 for c1 in commits_ahead_gen)
    return bool(commits_behind)

def uncommitted_changes(repo):
    print(repo.is_dirty())
    changedFiles = [ item.a_path for item in repo.index.diff(None) ]
    untrackedFiles = repo.untracked_files
    return bool(len(changedFiles) + len(untrackedFiles))


def main():
    #Create repo object
    repo = Repo(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "Shared_Folder"))
    
    # Working out if a pull, and/or and commit is needed.
    pull_req = behind_master(repo)
    commit_needed = uncommitted_changes(repo)

if __name__ == '__main__':
    main()