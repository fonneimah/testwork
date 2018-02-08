import requests, datetime, re, sys, time 	# импорт стандартных модулей

now = datetime.datetime.now() # в переменной now - текущая дата и время

def recognize(date):			# функция по распознаванию и валидации даты введенной пользователем
	regexp = re.compile(r'201[0-9]-(0[1-9]|1[012])-(0[1-9]|1[0-9]|2[0-9]|3[01])')
	raw = regexp.search(date)
	if raw != None:
		return raw.group()
	else: return False

# приветствие и краткая инструкция, для корректной работы программы рекомендуется ознакомиться с ней
print("""\n	Greeting. For analyze any public repository, please input the owner name and it's repository in this format
\towner/repository
\tE.g.: googlechrome/puppeteer 
\n\tIf you dont know public repositories, please enter '2' and you will see top public repositories, 
\tthan enter the name one of them. For quit enter 'exit'.""")

# использовал старый, объемный, но быстросоздаваемый метод для ввода данных,
# работет по принципу "пока не будет корректных данных и брейка, буду выполняться вновь и вновь"
while True:
	repository = input('\n\tInput repository in this format: owner/repository\n\n>')
	if repository == 'exit':
		sys.exit()
	if len(repository) == 0:
		False
	if repository == '2':
		pub = requests.get('https://api.github.com/repositories').json()
		for repos in range(len(pub)):
			print('\t' + pub[repos]['full_name'])
		while True:
			repository = input('\n\tInput repository in this format: owner/repository\n\n>')
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
			branch = input('\n\tInput branch name:\n>')
			if branch == 'exit':
				sys.exit()
			if len(branch) == 0:
				branch = 'master'
				break
			for item in range(len(branches.json())):
				if branch == branches.json()[item]['name']:
					break
			break
		break
	else:
		print('[Somethibg wrong. Try again or exit.]')

print('Analyze: %s [%s branch]'%(repository, branch))

time.sleep(1)
# ввод данных для начала и окончания анализа, которые сразу же проверяются функцией recognize
since = recognize(input('\nSINCE from which date repository should analyze.\nWARNING! FORMAT: YYYY-MM-DD\nSkip or error date transform value to default which is unlimited.\n'))
until = recognize(input('\nUNTIL till date repository should analyze.\nWARNING! FORMAT: YYYY-MM-DD\nSkip or error date transform value to default which is unlimited.\n'))

time.sleep(3)# в ходе многократных тестов выполнения программы выяснилось, что Guthub API накладывает некоторые ограничения на количество запросов не только в течении часа,
			# но и в течении коротких промежутков времени, поэтому было принято решение "искусственно" замедлять время между запросами, для корректного получения данных

# получаем json-массив всех контриюьюторов элеметы которого передаем лямбда функции
# для создания map-объекта, состоящего из кортежей (логин, число коммитов), далее превращая объект в список
raw = list(map(lambda x: (x['author']['login'], x['total']), requests.get('https://api.github.com/repos/%s/stats/contributors'%(repository)).json()))
top30 = raw[::-1][:30]							# делаем срез исходного массива и получаем наш топ-30
print('+' + ('-'*30) + '+' + ('-'*30) + '+')	# создаем шапку таблицы
print('|' + (' '*13) + 'LOGIN' + (' '*12) + '|' + (' '*12) + 'COMMITS' + (' '*11) + '|')
print('+' + ('-'*30) + '+' + ('-'*30) + '+')
for k in range(len(top30)):						# запись результатов
		print('\t' + top30[k][0] + '\t\t\t' + str(top30[k][1])) if len(top30[k][0]) <= 7 else print('\t' + top30[k][0] + '\t\t' + str(top30[k][1]))

# создаем шапку таблицы по данным об issues и pull-requests
print('+' + ('-'*20) + '+' + ('-'*20) + '+'+ ('-'*20) + '+' + ('-'*20) + '+')
print('|' + '  TOTAL OPEN PULLS  ' + '|' + ' TOTAL CLOSED PULLS ' + '|' + ' TOTAL OPEN ISSUES  ' + '|' + ' TOTAL CLOSED ISSUES' + '|')
print('+' + ('-'*20) + '+' + ('-'*20) + '+'+ ('-'*20) + '+' + ('-'*20) + '+')

time.sleep(3)
# если пользователь ввел корректные даты начала и окончания анализа, и они прошли валидацию, то будет выполняться ветка True с учетом этих дат, если нет, то
# будет выполняться ветка со значениями по умолчанию, т.е. неограниченными
if ((since != False and until != False) and ((len(since) != 0) and (len(until) != 0)) and (since < until) ((since < str(now)[:10]) and (until <= str(now)[:10]))):
	print('\t' + str(requests.get('https://api.github.com/search/issues?q=repo:' + repository + '+type:pr+state:open+created%3A' + since + '..' + until).json()['total_count']) + '\t'*3 +
	str(requests.get('https://api.github.com/search/issues?q=repo:' + repository + '+type:pr+state:closed+created%3A' + since + '..' + until).json()['total_count']) + '\t'*2 +
	str(requests.get('https://api.github.com/search/issues?q=repo:' + repository + '+type:issue+state:open+created%3A' + since + '..' + until).json()['total_count']) + '\t'*3 +
	str(requests.get('https://api.github.com/search/issues?q=repo:' + repository + '+type:issue+state:closed+created%3A' + since + '..' + until).json()['total_count']))
else:
	print('\t' + str(requests.get('https://api.github.com/search/issues?q=repo:%s+type:pr+state:open'%repository).json()['total_count']) + '\t'*3 +
	str(requests.get('https://api.github.com/search/issues?q=repo:%s+type:pr+state:closed'%repository).json()['total_count']) + '\t'*2 +
	str(requests.get('https://api.github.com/search/issues?q=repo:%s+type:issue+state:open'%repository).json()['total_count']) + '\t'*3 +
	str(requests.get('https://api.github.com/search/issues?q=repo:%s+type:issue+state:closed'%repository).json()['total_count']))

time.sleep(5)
# вычисляем даты для "старых" issues и pull-requests, далее вставляем их в запрос
dateissues = (now - datetime.timedelta(days = 14)).strftime('%Y-%m-%d')
datepulls = (now - datetime.timedelta(days = 30)).strftime('%Y-%m-%d')
old_issues = requests.get('https://api.github.com/search/issues?q=repo:%s'%repository + '+created%3A%3C%3D' + dateissues + '+state%3Aopen+is%3Aissue').json()
old_pulls = requests.get('https://api.github.com/search/issues?q=repo:%s'%repository  + '+created%3A%3C%3D' + datepulls + '+state%3Aopen+is%3Apr').json()
print("\nOld issues count: %s"%(old_issues['total_count']) + "\nOld pulls count: %s"%(old_pulls['total_count']))