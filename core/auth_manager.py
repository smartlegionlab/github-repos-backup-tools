from core.github_tools import GitHubDataMaster


class GithubAuthManager:

    @classmethod
    def token_verify(cls, token, timeout, max_retries=3):
        github_client = GitHubDataMaster(token)
        success = github_client.fetch_user_data(max_retries=max_retries, timeout=timeout)
        if not success or not github_client.login:
            return False, None
        return True, github_client
