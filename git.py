from git import Repo, GitCommandError, InvalidGitRepositoryError

def git():
    try:
        repo = Repo()
        origin = repo.remotes.origin
        origin.fetch(config.UPSTREAM_BRANCH)
        origin.refs[config.UPSTREAM_BRANCH].checkout()
        repo.git.reset("--hard", "FETCH_HEAD")
    except (InvalidGitRepositoryError, GitCommandError, IndexError) as e:
        print(f"Error during Git setup: {e}")

git()
