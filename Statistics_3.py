import requests, re, datetime

old_issues = requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+created%3A%3C%3D' + (datetime.datetime.now() - datetime.timedelta(days = 14)).strftime('%Y-%m-%d') + '+state%3Aopen+is%3Aissue').json()['total_count']
old_pulls = requests.get('https://api.github.com/search/issues?q=repo:googlechrome/puppeteer+created%3A%3C%3D' + (datetime.datetime.now() - datetime.timedelta(days = 30)).strftime('%Y-%m-%d') + '+state%3Aopen+is%3Apr').json()['total_count']
print("Old issues count: %s"%(old_issues) + "\n" + "Old pulls count: %s"%(old_pulls))