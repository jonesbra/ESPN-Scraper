import urllib2
from bs4 import BeautifulSoup

class Player:
    def __init__(self, rank=None, name=None, position=None, team=None, salary=None, id=None, totals=dict()):
        self.rank = rank
        self.name = name
        self.position = position
        self.team = team
        self.salary = salary
        self.totals = totals

def getPlayers():
    playerList = []
    for i in range(1, 13):
        url = 'http://www.espn.com/nba/salaries/_/page/{}'.format(i)
        page = urllib2.urlopen(url)
        mainParser = BeautifulSoup(page, 'html.parser')
        tableRows = mainParser.find('div', attrs={'class': 'span-4', 'id': 'my-players-table'}).find('table', attrs={'class': 'tablehead'}).findAll('tr')

        pagePlayerList = []
        headerLocation = 0
        for index, row in enumerate(tableRows):
            player = Player()

            if index == headerLocation:
                headerLocation += 11
                continue

            for index, data in enumerate(row.findAll('td')):
                if index == 0:
                    player.rank = data.contents[0]

                if index == 1:
                    player.id = data.find('a')['href'].split('/')[-2]
                    player.name = data.find('a').contents[0]
                    player.position = data.contents[-1].replace(',', '').strip()

                if index == 2:
                    try:
                        player.team = data.find('a').contents[0]
                    except:
                        player.team = data.contents[0]

                if index == 3:
                    player.salary = data.contents[0]

            pagePlayerList.append(player)

        playerList.extend(pagePlayerList)

    return playerList

def getTotals(player):
    url = "http://www.espn.com/nba/player/stats/_/id/{}/".format(player.id)
    page = urllib2.urlopen(url)
    mainParser = BeautifulSoup(page, 'html.parser')

    try:
        careerAverages = mainParser.findAll('tr', attrs={'class': 'total'})[0].findAll('td')
        careerTotals = mainParser.findAll('tr', attrs={'class': 'total'})[1].findAll('td')
        careerMiscTotals = mainParser.findAll('tr', attrs={'class': 'total'})[2].findAll('td')

        for index, data in enumerate(careerAverages):
            if index == 18:
                player.totals['averagePoints'] = data.contents[0]
    except:
        player.totals['averagePoints'] = 0




def main():
    playerList = getPlayers()

    for player in playerList:
        getTotals(player)
        print '{0}\t{1}\t{2}'.format(player.name, player.salary, player.totals['averagePoints'])
        print

if __name__ == "__main__":
    main()
