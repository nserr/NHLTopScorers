import requests
import datetime
import re
from bs4 import BeautifulSoup

def main():
	maxRank = int(input("Display up to what rank? (max 50): "))

	now = datetime.datetime.now()
	year = str(now.year)
	url = 'https://www.foxsports.com/nhl/stats?season=' + year + '&category=SCORING&time=0'

	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')

	players = soup.find_all(class_="wisbb_playerContainer")
	pointsAll = soup.find_all(class_="wisbb_priorityColumn wisbb_selected")

	getTopScorers(players, pointsAll, maxRank)


# Pull the statistics of the top scorers in the league.
# maxRank dictates what rank in the points standings to display up to (max 50).
def getTopScorers(players, pointsAll, maxRank):
	index = 0

	for player in players:
		playerInfo = player.find_all('span')

		rankMatch = re.search(r"\d{1,2}", str(playerInfo[0]))
		if rankMatch:
			rank = int(rankMatch[0])
			if rank > maxRank:
				break

		nameMatch = re.search(r"\w{,}, \w{,}", str(playerInfo[1]))
		if nameMatch:
			name = str(nameMatch[0])

		teamMatch = re.search(r"[A-Z]{2,3}", str(playerInfo[3]))
		if teamMatch:
			team = str(teamMatch[0])

		pointMatch = re.search(r"\d{1,3}", str(pointsAll[index]))
		if pointMatch:
			points = int(pointMatch[0])

		index = index + 1
		printFmt(rank, name, team, points)


# Formats and prints statistics.
def printFmt(rank, name, team, points):

	if len(name) > 11:
		print("{}: {}	[{}]	{} pts".format(rank, name, team, points))
	else:
		print("{}: {}		[{}]	{} pts".format(rank, name, team, points))


if __name__ == "__main__":
	main()