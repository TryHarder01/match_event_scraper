"""
Python3
parses XML from sportradar API and exports CSV of match facts
"""

import xml.etree.ElementTree as ET
import urllib.request
import csv

## Enter output filename
output_file = ''

## Enter your API key
api_key = ''

## Enter the match url
target_url = 'https://api.sportradar.us/soccer-t2/eu/matches/...?api_key=' + api_key


def main(file_name, match_url):
	## Download XML

	with urllib.request.urlopen(match_url) as webpage:
		data = webpage.read()
		text = data.decode('utf-8')

	## Parse XML
	parsed = ET.fromstring(text)

	## Find team names
	def team_names(root):
		"""
		takes root as input and returns dictions with home and away team names and team ID.
		"""
		homebranch = root[0][0].find('{http://feed.elasticstats.com/schema/soccer/sr/v2/matches-summary.xsd}home')
		homename = (homebranch.attrib.get('alias'))
		homeid = (homebranch.attrib.get('id'))


		awaybranch = root[0][0].find('{http://feed.elasticstats.com/schema/soccer/sr/v2/matches-summary.xsd}away')
		awayname = (awaybranch.attrib.get('alias'))
		awayid = (awaybranch.attrib.get('id'))

		teamnames = {homeid:homename, awayid:awayname}
		return(teamnames)

	names = team_names(parsed)

	## extract facts

	# create row headers
	rowlist =  [ [ 'time', 'facttype', 'team', 'clock', 'x', 'y']]

	# add facts
	for fact in parsed[0][0][9]:
		time = fact.get('time')
		facttype = fact.get('type')
		clock = fact.get('clock')

		team_id = fact.get('team_id')
		if team_id:
			factteam = names.get(team_id)
		else: 
			factteam = 'NA'

		fact_x = fact.get('x')

		if fact_x:
			x = fact_x
		else: 
			x = 'NA'

		fact_y = fact.get('y')

		if fact_y:
			y = fact_y
		else:
			y = 'NA'

		rowlist.append([time, facttype, factteam, clock, x, y])

	with open(file_name, 'w', newline='') as csvfile:
		my_writer = csv.writer(csvfile, delimiter=',')
		for row in rowlist:
			my_writer.writerow(row)

	print(match_url[:50] + '...' + '  scraped and saved to ' + file_name)

if __name__ == '__main__':
	main(output_file, target_url)