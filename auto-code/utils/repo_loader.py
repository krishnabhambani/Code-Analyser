import os
import logging
import git
from typing import Optional
from config import REPOS_DIR

logger = logging.getLogger(__name__)

def clone_repo(repo_url: str) -> Optional[str]:
    """
    Clones a GitHub repository locally or returns the path if it already exists.

    Args:
        repo_url (str): The URL of the GitHub repository to clone.

    Returns:
        Optional[str]: The local fallback path of the cloned repository, or None if cloning fails.
    """
    try:
        if not os.path.exists(REPOS_DIR):
            os.makedirs(REPOS_DIR)
            logger.info("Created repositories directory at %s", REPOS_DIR)
            
        repo_name = repo_url.rstrip("/").split("/")[-1]
        if repo_name.endswith(".git"):
            repo_name = repo_name[:-4]
            
        local_path = os.path.join(REPOS_DIR, repo_name)
        
        if os.path.exists(local_path):
            logger.info("Repository already exists at %s. Skipping cloning.", local_path)
        else:
            logger.info("Cloning repository %s into %s...", repo_url, local_path)
            git.Repo.clone_from(repo_url, local_path)
            logger.info("Successfully cloned repository.")
            
        return local_path
    except git.GitCommandError as git_err:
        logger.error("Git error occurred while cloning the repository: %s", git_err)
    except Exception as e:
        logger.error("An unexpected error occurred while processing the repository: %s", e)
    
    return None
