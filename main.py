import requests
import os

#username = "void4"#input("Enter the github username:")

usernames = "void4 void".split()
username = usernames[0]
#https://stackoverflow.com/questions/8713596/how-to-retrieve-the-list-of-all-github-repositories-of-a-person
#https://github.community/t5/GitHub-API-Development-and/Api-URL-to-find-all-github-repos-for-user/td-p/39980
request = requests.get(f'https://api.github.com/users/{username}/repos?per_page=500')

json = request.json()

os.system("mkdir repos")

for i, project in list(enumerate(json)):#[:5]:
	print("Project Number:", i+1)
	projectname = project['name']
	print("Project Name:", projectname)
	git = project['git_url']
	print("Project URL:", git,"\n")

	if project["fork"]:
		continue

	gitpath = f"repos/{projectname}"
	os.system(f"git clone {git} {gitpath}")
	
	#https://github.com/acaudwell/Gource/wiki/Visualizing-Multiple-Repositories
	logpath = f"repos/log{i}.txt"
	os.system(f"gource --output-custom-log {logpath} {gitpath}")
	usernamefilter = "|".join(usernames)
	os.system(f"sed -i -nE '/{usernamefilter}/p' {logpath}")
	os.system(f"sed -i -r 's#(.+)\|#\\1|/{projectname}#' {logpath}")

os.system("cat repos/log*.txt | sort -n > repos/combined.txt")
os.system("gource repos/combined.txt")
