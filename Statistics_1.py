import requests, json
ans = requests.get('https://api.github.com/repos/googlechrome/puppeteer/stats/contributors')
data = json.loads(ans.text)
count = 0
raw = []
for i in data:
	raw.append({"login": data[count]['author']['login'], "commits": data[count]['total']})
	count += 1

def byCommit(raw):
    return raw['commits']
 
arr = sorted(raw, key = byCommit, reverse=True)

for x in arr:
	print(x)
