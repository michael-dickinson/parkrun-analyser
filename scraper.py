import json
import requests

from bs4 import BeautifulSoup

HEADERS = {
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate',
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}

URL = 'http://www.parkrun.org.uk/conkers/results/weeklyresults/?runSeqNumber=1'
URL = 'http://www.parkrun.org.uk/conkers/results/latestresults/'

response = requests.get(
    URL,
    headers=HEADERS
)

page = BeautifulSoup(response.text, "html.parser")

results = {}

for row in page.find_all('tr'):
    cols = row.findAll('td')
    try:
        if 'pos' in cols[0]['class']:
            position, athlete, time, category, grade, gender, gender_position, club, note, total_runs, other = [c.text for c in cols]
            results[int(position)] = {
                "parkrunner": athlete,
                "time": time,
                "age_category": category,
                "age_grade": grade,
                "gender": gender,
                "gender_position": gender_position,
                "club": club,
                "note": note,
                "total_runs": total_runs,
                "other": other
            }
    except (IndexError, KeyError):
        pass

print json.dumps(results, sort_keys=True, indent=4, separators=(',', ': '))

cate = {
    p: a
    for p, a in results.iteritems()
    if a['age_category'] == 'VW35-39'
}
