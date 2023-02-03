import csv
import requests
import json
from datetime import datetime, timedelta

# API endpoint for getting the list of orgs
enterprise_orgs_url = "https://hostname/api/v3/orgs"

# API endpoint for getting the list of repos for an org
repos_url = "https://hostname/api/v3/repos/orgs/{org}?per_page=100"

# API endpoint for getting the details of a repo
repo_url = "https://hostname/api/v3/repos/{owner}/{repo}"

# API request headers
headers = {
    "Authorization": "token <your_access_token>",
    "Accept": "application/vnd.github+json",
}

# Get the list of orgs
response = requests.get(enterprise_orgs_url, headers=headers)

if response.status_code == 200:
    # Get the list of orgs
    orgs = response.json()

    # Open a CSV file for writing
    with open("repos.csv", "w", newline="") as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(["Org", "Repo", "Description", "URL", "Archived", "Author", "Email", "Last Commit Date"])

        # Loop through each org
        for org in orgs:
            org_name = org["login"]
            org_repos_url = repos_url.format(org=org_name)

            # Get the list of repos for the org
            org_repos = requests.get(org_repos_url, headers=headers).json()

            # Loop through each repo
            for repo in org_repos:
                repo_name = repo["name"]
                repo_details_url = repo_url.format(owner=org_name, repo=repo_name)

                # Get the details of the repo
                repo_details = requests.get(repo_details_url, headers=headers).json()

                # Write the repo data to the CSV file
                writer.writerow([org_name, repo_name, repo_details.get("description", ""), repo_details.get("html_url", ""),
                                 repo_details.get("archived", False), repo_details.get("owner", {}).get("login", ""),
                                 repo_details.get("owner", {}).get("email", ""), repo_details.get("pushed_at", "")])
else:
    print(f"Error: Failed to get enterprise orgs. Status code: {response.status_code}")
    print(f"Response content: {response.content}")
