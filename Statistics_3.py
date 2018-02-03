import requests, re, datetime

old_issues_count = requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+type:issue+state:open&sort=created')
data = old_issues_count.json()
print(data['items'][29]['created_at'])
