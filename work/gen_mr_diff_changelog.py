# """
# -- Executing the script --

# Min. python version required is [v3.11]

# Set up a virtual environment:

# -> python -m venv venv
# [Windows]
# -> venv\Scripts\activate
# [Mac]
# -> source venv/bin/activate

# Install the required packages:

# -> python -m pip install --upgrade pip
# -> pip install -r requirements.txt

# Provide the required env. vars:

# -> export GITLAB_PRIVATE_TOKEN="your-gitlab-token"
# -> export PROJECT_ID="your-project-id"
# -> export MR_ID_1="your-mr-id-1"
# -> export MR_ID_2="your-mr-id-2"
# -> export CONFLUENCE_USERNAME="your-confluence-username"
# -> export CONFLUENCE_API_TOKEN="your-confluence-api-token"
# -> export CONFLUENCE_PAGE_ID="your-confluence-page-id"
# -> [Optional] export CONFLUENCE_BASE_URL="https://your-confluence-instance.atlassian.net/wiki"

# And execute the script:

# -> python generate-changelogs.py

# """

import asyncio
import json
import os
import traceback
from dataclasses import dataclass
from datetime import datetime
from typing import List

import aiohttp
import gitlab
import pyperclip

# Data class for holding MR commit details


@dataclass
class MergeRequestCommit:
    title: str


# Data class for holding MR diff details


@dataclass
class MergeRequestDiff:
    file_path: str
    old_path: str
    new_file: bool
    renamed_file: bool
    deleted_file: bool
    diff: str


# Data class for holding MR details


@dataclass
class MergeRequestDetails:
    title: str
    author: str
    created_at: str
    commits: List[MergeRequestCommit]
    changes: List[MergeRequestDiff]


# Function to fetch MR details, commits, and diffs


async def fetch_mr_details(
    project_id: int, mr_id: int, gl: gitlab.Gitlab
) -> MergeRequestDetails:
    """
    Fetches merge request details including commits and diffs from GitLab.

    Args:
        project_id (int): The GitLab project ID.
        mr_id (int): The merge request ID.
        gl (gitlab.Gitlab): An instance of the GitLab client.

    Returns:
        MergeRequestDetails: A data class containing MR title, author, creation date, commits, and changes.

    Raises:
        gitlab.exceptions.GitlabGetError: If there is an error retrieving the merge request.
        Exception: For any other unexpected errors.
    """

    try:
        project = gl.projects.get(project_id)
        mr = project.mergerequests.get(mr_id)

        # Fetch commits for the merge request
        commits: List[MergeRequestCommit] = []
        for commit in mr.commits():
            commit_details = project.commits.get(commit.id)
            if (
                len(commit_details.parent_ids) == 1
            ):  # Regular commit, not a merge commit
                commits.append(MergeRequestCommit(title=commit.title))

        # Fetch changes (diffs) for the merge request
        diffs: List[MergeRequestDiff] = []
        changes = mr.changes()
        for change in changes["changes"]:
            diffs.append(
                MergeRequestDiff(
                    file_path=change["new_path"],
                    old_path=change["old_path"],
                    new_file=change["new_file"],
                    renamed_file=change["renamed_file"],
                    deleted_file=change["deleted_file"],
                    diff=change["diff"],
                )
            )

        return MergeRequestDetails(
            title=mr.title,
            author=mr.author["name"],
            created_at=mr.created_at,
            commits=commits,
            changes=diffs,
        )
    except gitlab.exceptions.GitlabGetError as e:
        print(f"Failed to retrieve merge request {mr_id}: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred while fetching MR details: {e}")
        traceback.print_exc()
        raise


# Function to generate diff between two MRs


async def generate_diff_between_mrs(
    project_id: int, mr_id_1: int, mr_id_2: int, gl: gitlab.Gitlab
) -> str:
    """
    Generates a diff report between two merge requests by comparing their commits and changes.

    Args:
        project_id (int): The GitLab project ID.
        mr_id_1 (int): The first merge request ID.
        mr_id_2 (int): The second merge request ID.
        gl (gitlab.Gitlab): An instance of the GitLab client.

    Returns:
        str: A formatted string showing the diff between the two merge requests.

    Raises:
        Exception: For any unexpected errors during the diff generation process.
    """

    try:
        # Fetch diffs for both MRs concurrently
        mr1_details_task: asyncio.Future[MergeRequestDetails] = asyncio.create_task(
            fetch_mr_details(project_id, mr_id_1, gl)
        )
        mr2_details_task: asyncio.Future[MergeRequestDetails] = asyncio.create_task(
            fetch_mr_details(project_id, mr_id_2, gl)
        )

        # Await the tasks
        mr1_details: MergeRequestDetails = await mr1_details_task
        mr2_details: MergeRequestDetails = await mr2_details_task

        print(f"Fetched details for MR#${mr_id_1} and MR#${mr_id_2}")

        # Compare the diffs between MR1 and MR2
        diff_output: str = f"# Diff between MR {mr_id_1} and MR {mr_id_2}\n\n"

        def format_change(mr_details: MergeRequestDetails) -> str:
            diff_output = f"## {mr_details.title} by {mr_details.author} (Created on {mr_details.created_at})\n"
            diff_output += f"### Commits:\n"
            for commit in mr_details.commits:
                diff_output += f"- {commit.title}\n"
            # Uncomment below lines of code to capture complete changelist
            # diff_output += f"\n### Changes:\n"
            # for change in mr_details.changes:
            #     diff_output += f"\nFile: {change.file_path}\n"
            #     diff_output += f"Old Path: {change.old_path}\n"
            #     diff_output += f"New File: {change.new_file}\n"
            #     diff_output += f"Renamed File: {change.renamed_file}\n"
            #     diff_output += f"Deleted File: {change.deleted_file}\n"
            #     diff_output += f"Diff:\n{change.diff}\n"
            return diff_output

        # Generate diff report for MR1 and MR2
        diff_output += f"\n### MR {mr_id_1}:\n" + format_change(mr1_details)
        diff_output += f"\n### MR {mr_id_2}:\n" + format_change(mr2_details)

        return diff_output

    except Exception as e:
        print(f"An unexpected error occurred while generating the diff: {e}")
        traceback.print_exc()
        raise


# Function to create Confluence page


async def get_space_key(
    session, confluence_base_url: str, page_id: str, username: str, api_token: str
) -> str:
    """
    Retrieves the Confluence space key for a given page.

    Args:
        session (aiohttp.ClientSession): An aiohttp session for making HTTP requests.
        confluence_base_url (str): The base URL of the Confluence instance.
        page_id (str): The ID of the Confluence page.
        username (str): The Confluence username.
        api_token (str): The Confluence API token.

    Returns:
        str: The space key of the specified Confluence page.

    Raises:
        aiohttp.ClientResponseError: If the API request fails.
    """

    async with session.get(
        f"{confluence_base_url}/rest/api/content/{page_id}?expand=space",
        auth=aiohttp.BasicAuth(username, api_token),
        headers={"Accept": "application/json"},
    ) as response:
        response.raise_for_status()
        page_data = await response.json()
        return page_data["space"]["key"]


# Function to update Confluence page


async def create_confluence_subpage(
    confluence_base_url: str,
    parent_page_id: str,
    username: str,
    api_token: str,
    content: str,
) -> None:
    """
    Creates a new subpage in Confluence under the specified parent page.

    Args:
        confluence_base_url (str): The base URL of the Confluence instance.
        parent_page_id (str): The ID of the parent page.
        username (str): The Confluence username.
        api_token (str): The Confluence API token.
        content (str): The content to be added to the new page.

    Raises:
        aiohttp.ClientResponseError: If there is an error during the HTTP request.
        Exception: For any other unexpected errors.
    """

    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    async with aiohttp.ClientSession() as session:
        try:
            # Generate a title for the new page
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_page_title = f"Changelog {current_time}"

            # Prepare the payload for creating a new page
            create_payload = {
                "type": "page",
                "title": new_page_title,
                "space": {
                    "key": await get_space_key(
                        session,
                        confluence_base_url,
                        parent_page_id,
                        username,
                        api_token,
                    )
                },
                "body": {"storage": {"value": content, "representation": "storage"}},
                "ancestors": [{"id": parent_page_id}],
            }

            # Create the new page
            async with session.post(
                f"{confluence_base_url}/rest/api/content",
                auth=aiohttp.BasicAuth(username, api_token),
                headers=headers,
                json=create_payload,
            ) as response:
                if response.status == 403:
                    print(
                        f"403 Forbidden: Unable to create the page. Check your permissions and API token."
                    )
                    print(f"Response headers: {response.headers}")
                    print(f"Response body: {await response.text()}")
                    return
                response.raise_for_status()
                result = await response.json()
                print(
                    f"New Confluence page created successfully: {result['_links']['webui']}"
                )

        except aiohttp.ClientResponseError as e:
            print(f"HTTP error occurred: {e.status}: {e.message}")
            print(f"Response headers: {e.headers}")
            print(f"Request info: {e.request_info}")
            raise
        except aiohttp.ClientError as e:
            print(f"Network error occurred: {str(e)}")
            raise
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {str(e)}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")
            raise


# Main script


async def main() -> None:
    try:
        # Use environment variables for project_id, mr_ids, and tokens
        project_id: int = int(os.getenv("PROJECT_ID", "58272764"))

        mr_id_1_str = os.getenv("MR_ID_1")
        if not mr_id_1_str:
            raise ValueError("MR_ID_1 environment variable is not set or empty.")
        mr_id_1 = int(mr_id_1_str)

        mr_id_2_str: int = int(os.getenv("MR_ID_2"))
        if not mr_id_2_str:
            raise ValueError("MR_ID_1 environment variable is not set or empty.")
        mr_id_2 = int(mr_id_2_str)

        gitlab_token: str = os.getenv("GITLAB_PRIVATE_TOKEN")

        if not gitlab_token:
            raise ValueError("GITLAB_PRIVATE_TOKEN environment variable not set.")
        if project_id <= 0 or mr_id_1 <= 0 or mr_id_2 <= 0:
            raise ValueError("Invalid project or MR IDs provided.")

        # Initialize GitLab API client
        gl = gitlab.Gitlab("https://gitlab.com", private_token=gitlab_token)

        # Generate diff between the two MRs
        diff_report: str = await generate_diff_between_mrs(
            project_id, mr_id_1, mr_id_2, gl
        )

        # Write the diff report to a text file
        with open("data/diff_report.ignore.txt", "w", encoding="utf-8") as file:
            file.write(diff_report)
        print("Diff report generated, saved to diff_report.txt")

        # Copy the diff report to the clipboard
        pyperclip.copy(diff_report)
        print("Diff report copied to clipboard.")

    except ValueError as ve:
        print(f"Value error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()


# Run the main script
if __name__ == "__main__":
    asyncio.run(main())
