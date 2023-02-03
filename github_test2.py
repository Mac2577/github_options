import requests
import csv
from getpass import getpass

# GitHub API endpoint to get a list of enterprise orgs
enterprise_orgs_url = "https://api.github.com/orgs"

# GitHub API endpoint to get a list of repos for a specific org
repos_url = "https://api.github.com/orgs/{}/repos"

# Request headers
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"token {getpass('Enter your GitHub personal access token: ')}"
}

# CSV file to store the repo information
filename = "repos.csv"

# Open the CSV file for writing
with open(filename, "w", newline="") as csvfile:
    # Create a CSV writer
    writer = csv.writer(csvfile)

    # Write the header row to the CSV file
    writer.writerow(["Repo Name", "Description", "URL", "Archived", "Author", "Author Email", "Author Type"])

    # Get the list of enterprise orgs
    response = requests.get(enterprise_orgs_url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Get the list of orgs
        orgs = response.json()

        # Loop through each org
        for org in orgs:
            # Get the list of repos for the org
            response = requests.get(repos_url.format(org["login"]), headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                # Get the list of repos
                repos = response.json()

                # Loop through each repo
                for repo in repos:
                    # Get the repo information
                    repo_info = [
                        repo["name"],
                        repo["description"] if "description" in repo else "",
                        repo["html_url"],
                        repo["archived"],
                        repo["owner"]["login"],
                        repo["owner"]["email"] if "email" in repo["owner"] else "",
                        repo["owner"]["type"],
                    ]

                    # Write the repo information to the CSV file
                    writer.writerow(repo_info)
            else:
                print(f"Error: Failed to get repos for org {org['login']}. Status code: {response.status_code}")
    else:
        print(f"Error: Failed to get enterprise orgs. Status code: {response.status_code}")
