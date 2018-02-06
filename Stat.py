import requests, re, datetime, sys

print("""Greeting. For analyze any public repository, please input the owner name and it's repository.
First input the owner name.""")
while True:
	input_owner = input("\nInput owner:\n")
	if input_owner == 'exit':
		sys.exit()
	owner = requests.get('https://api.github.com/users/%s'%(input_owner))
	if (owner.headers['Status'] == '200 OK'):
		repos = requests.get('https://api.github.com/users/%s/repos'%(owner.json()["login"]))
		print("\nOk, the owner has found. Now choose public repository.\n")
		for i in range(len(repos.json())):
			print(repos.json()[i]["name"]) if repos.json()[i]["private"] == False else None
		while True:
			input_repo = input("\nInput repository name:\n")
			if input_repo == 'exit':
				sys.exit()
			repo = requests.get('https://api.github.com/repos/%s/%s'%(owner.json()["login"], input_repo))
			if (repo.headers['Status'] == '200 OK'):
				print("Done. Analyze start.")
				break
			else: print('Not found owner with this name. Try again or input exit')
		break
	else: print('Not found owner with this name. Try again or input exit')

repository = owner.json()["login"] + '/' + repo.json()["name"]
print(repository)
# raw = list(map(lambda x: (x['author']['login'], x['total']), requests.get('https://api.github.com/repos/googlechrome/puppeteer/stats/contributors').json()))
# top30 = raw[::-1][:30]
# print('+' + ('-'*22) + '+' + ('-'*22) + '+')
# print('|' + (' '*9) + 'LOGIN' + (' '*8) + '|' + (' '*7) + 'COMMITS' + (' '*8) + '|')
# print('+' + ('-'*22) + '+' + ('-'*22) + '+')
# for k in range(len(top30)):
# 		print('\t' + top30[k][0] + '\t\t\t' + str(top30[k][1])) if len(top30[k][0]) <= 7 else print('\t' + top30[k][0] + '\t\t' + str(top30[k][1]))

# print('+' + ('-'*20) + '+' + ('-'*20) + '+'+ ('-'*20) + '+' + ('-'*20) + '+')
# print('|' + '  TOTAL OPEN PULLS  ' + '|' + ' TOTAL CLOSED PULLS ' + '|' + ' TOTAL OPEN ISSUES  ' + '|' + ' TOTAL CLOSED ISSUES' + '|')
# print('+' + ('-'*20) + '+' + ('-'*20) + '+'+ ('-'*20) + '+' + ('-'*20) + '+')
# print('\t' + str(requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+type:pr+state:open').json()['total_count']) + '\t'*3 +
# 	  str(requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+type:pr+state:closed').json()['total_count']) + '\t'*2 +
# 	  str(requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+type:issue+state:open').json()['total_count']) + '\t'*3 +
# 	  str(requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+type:issue+state:closed').json()['total_count']))

# old_issues = requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+created%3A%3C%3D' + (datetime.datetime.now() - datetime.timedelta(days = 14)).strftime('%Y-%m-%d') + '+state%3Aopen+is%3Aissue').json()['total_count']
# old_pulls = requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+created%3A%3C%3D' + (datetime.datetime.now() - datetime.timedelta(days = 30)).strftime('%Y-%m-%d') + '+state%3Aopen+is%3Apr').json()['total_count']
# print("\nOld issues count: %s"%(old_issues) + "\nOld pulls count: %s"%(old_pulls))