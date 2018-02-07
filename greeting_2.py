import requests, sys

print("""\n	Greeting. For analyze any public repository, please input the owner name and it's repository in this format
\towner/repository
\tE.g.: googlechrome/puppeteer 
\n\tIf you dont know public repositories, please enter '2' and you will see top public repositories, 
\tthan enter the name one of them. For quit enter 'exit'.""")

while True:
	repository = input("\n\tInput repository in this format: owner/repository\n\n>")
	if repository == 'exit':
		sys.exit()
	if len(repository) == 0:
		False
	if repository == '2':
		pub = requests.get('https://api.github.com/repositories').json()
		for repos in range(len(pub)):
			print('\t' + pub[repos]['full_name'])
		while True:
			repository = input("\n\tInput repository in this format: owner/repository\n\n>")
			if repository == 'exit':
				sys.exit()
			if len(repository) != 0:
				break
			else: False
	branches = requests.get('https://api.github.com/repos/%s/branches'%repository)
	if branches.headers['Status'] == '200 OK':
		print('\n\tAvailable branches for %s. Please choose one or skip (default: master)\n'%repository)
		for items in range(len(branches.json())):
			print('\t' + branches.json()[items]['name'])
		while True:
			branch = input("\n\tInput branch name:\n>")
			if branch == 'exit':
				sys.exit()
			if len(branch) == 0:
				branch = 'master'
				break
			for item in range(len(branches.json())):
				if branch == branches.json()[item]["name"]:
					break
			break
		break
	else:
		print('[Somethibg wrong. Try again or exit.]')

print(repository, '\n', branch)