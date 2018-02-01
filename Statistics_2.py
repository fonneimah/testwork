import requests, json, re

#GET /repos/:owner/:repo/pulls
ans = requests.get('https://api.github.com/repos/googlechrome/puppeteer/pulls?state=closed&per_page=100')
print(ans.headers['Link'])
header = ans.headers['Link'].rpartition('&')
s_regex = re.compile(r'\d+')
needed_s = s_regex.search(header[2])
lastPage = needed_s.group()
print("Last page is: " + lastPage)

ans = requests.get('https://api.github.com/repos/googlechrome/puppeteer/pulls?state=closed&per_page=100&page=%s'%(lastPage))
rawData = json.loads(ans.text)
el = 0
count = 0
for i in rawData:
	if rawData[el]['state'] == 'closed':
		count += 1
	el +=1

totalClosedPulls = ((int(lastPage) - 1) * 100) + count
print("Total closed pulls: %d" % (totalClosedPulls))