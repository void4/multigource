import requests
import os

#username = "void4"#input("Enter the github username:")

usernames = "void4 void".split()
username = usernames[0]
#https://stackoverflow.com/questions/8713596/how-to-retrieve-the-list-of-all-github-repositories-of-a-person
#https://github.community/t5/GitHub-API-Development-and/Api-URL-to-find-all-github-repos-for-user/td-p/39980
request = requests.get(f'https://api.github.com/users/{username}/repos?per_page=500')

json = request.json()

repopath = f"{username}-repos"

os.system(f"mkdir {repopath}")

for i, project in list(enumerate(json)):#[:5]:
	print("Project Number:", i+1)
	projectname = project['name']
	print("Project Name:", projectname)
	git = project['git_url']
	print("Project URL:", git,"\n")

	#if project["fork"]:
	#	continue

	gitpath = f"{repopath}/{projectname}"
	os.system(f"git clone {git} {gitpath}")

	#https://github.com/acaudwell/Gource/wiki/Visualizing-Multiple-Repositories
	logpath = f"{repopath}/log{i}.txt"
	os.system(f"gource --output-custom-log {logpath} {gitpath}")

	# void is substring of void4, due to greedy matching, put void4 first by reversing the list
	usernamefilter = "|".join(usernames[::-1])

	# Only keep lines with one of the usernames
	os.system(f"sed -i -nE '/\|{usernamefilter}\|/p' {logpath}")

	# Replace all names by one name
	#os.system(f"sed -i -E 's/|{usernamefilter}|/|{username}|/' {logpath}")
	with open(logpath, "r+") as logfile:
		content = logfile.read()
		logfile.seek(0)
		logfile.truncate()
		for name in usernames:
			content = content.replace(f"|{name}|", "|"+username+"|")
		logfile.write(content)

	# Prepend project name to file path
	os.system(f"sed -i -r 's#(.+)\|#\\1|/{projectname}#' {logpath}")

os.system(f"cat {repopath}/log*.txt | sort -n > {repopath}/combined.txt")
os.system(f"gource {repopath}/combined.txt")
