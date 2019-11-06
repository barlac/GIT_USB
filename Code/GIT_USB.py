import os
from git import Repo

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