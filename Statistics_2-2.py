import requests, json, re

#GET /repos/:owner/:repo/pulls
ans = requests.get('https://api.github.com/repos/bazelbuild/bazel/pulls?state=open&per_page=25')
header = ans.headers['Link'].rpartition('&')
s_regex = re.compile(r'\d+')
needed_s = s_regex.search(header[2])
lastPage = needed_s.group()
print("Last page is: " + lastPage)

ans = requests.get('https://api.github.com/repos/bazelbuild/bazel/pulls?state=open&per_page=25&page=%s'%(lastPage))
rawData = json.loads(ans.text)
el = 0
count = 0
for i in rawData:
	if rawData[el]['state'] == 'open':
		count += 1
	el +=1

totalOpenPulls = ((int(lastPage) - 1) * 25) + count
print("Total open pulls: %d" % (totalOpenPulls))