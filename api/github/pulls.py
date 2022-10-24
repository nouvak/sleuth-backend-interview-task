import logging
from enum import Enum


class PullState(Enum):
    OPEN = "open"
    CLOSE = "close"
    ALL = "all"


class GithubPulls:
    # "logger" and "rest_client" are provided as external dependencies of the class to improve testability.
    def __init__(self, logger, rest_client):
        self.logger = logger
        self.rest_client = rest_client

    def list_open(self, repository: str):
        self.logger.info(f"Listing pull requests: repository={repository}")
        response = self.rest_client.get(url_path=f"/repos/{repository}/pulls", params={"state": PullState.OPEN})
        self.logger.debug(f"Listing pull requests response: {response}")
        pull_requests = list(map(
            lambda pull_request: self.extract_attributes(pull_request, repository),
            response["data"]))
        self.logger.debug(f"pull_requests={pull_requests}")
        return pull_requests

    def extract_attributes(self, pull_request, repository):
        pull_request_number = pull_request["number"]
        pull_request_commits = self.rest_client.get(url_path=f"/repos/{repository}/pulls/{pull_request_number}/commits")
        self.logger.debug(f"Pull request {pull_request_number} commits: {pull_request_commits}")
        return {
            "title": pull_request["title"],
            "author": pull_request["user"]["login"],
            "number_of_commits": len(pull_request_commits["data"]),
            "head_sha": pull_request["head"]["sha"],
            "last_update_time": pull_request["updated_at"]
        }
