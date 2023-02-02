import requests
import csv
import json
import datetime

# Set your Github authentication token
auth_token = "YOUR_AUTH_TOKEN"

# Define headers with the authentication token
headers = {
    "Authorization": f"Token {auth_token}"
}

# Define the enterprise orgs
enterprise_orgs = ["org1", "org2", "org3"]

# Define the date for the four months ago
four_months_ago = (datetime.datetime.now() - datetime.timedelta(days=120)).strftime("%Y-%m-%dT%H:%M:%SZ")

# Define the data that will be written to the CSV file
data = []

# Loop through each enterprise org
for org in enterprise_orgs:
    # Get the list of repos for the org
    repos_url = f"https://api.github.com/orgs/{org}/repos?per_page=100"
    repos_response = requests.get(repos_url, headers=headers)
    repos = repos_response.json()

    while "next" in repos_response.links.keys():
        repos_response = requests.get(repos_response.links["next"]["url"], headers=headers)
        repos += repos_response.json()
        
    # Loop through each repo
    for repo in repos:
        # Check if the repo was updated within the last 4 months
        if repo["pushed_at"] >= four_months_ago:
            repo_url = repo["url"]
            repo_response = requests.get(repo_url, headers=headers)
            repo_details = repo_response.json()

            # Get the repo description
            description = repo_details.get("description", "")

            # Get the Github URL for the repo
            html_url = repo_details.get("html_url", "")

            # Check if the repo is archived
            archived = repo_details.get("archived", False)

            # Get the author information
            commit_url = repo_details.get("commits_url", "").split("{")[0] + "?per_page=1"
            commit_response = requests.get(commit_url, headers=headers)
            commit_details = commit_response.json()
            author_name = commit_details[0]["commit"]["author"]["name"] if commit_details else ""
            author_email = commit_details[0]["commit"]["author"]["email"] if commit_details else ""
            last_commit_date = commit_details[0]["commit"]["author"]["date"] if commit_details else ""

            # Add the repo information to the data list
            data.append([org, repo["name"], repo["pushed_at"], description, html_url, archived, author_name, author_email, last_commit_date])


# Write the data to a CSV file
with open("repo_data.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Org", "Repo", "Last Updated", "Description", "URL", "Archived", "Author Name", "Author Email", "Last Commit Date"])
    for row in data:
        writer.writerow(row)