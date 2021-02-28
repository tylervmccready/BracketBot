import pandas as pd
import time

from selenium import webdriver
browser = webdriver.Chrome()


# Translates from ESPN to GameSim
def autoCorrect(name):
    abbreviationExceptions = {'W.': 'Western', 'E.': 'Eastern', 'Louisiana St.': 'LSU', 'N.C. A&T': 'North Carolina A&T', 'UConn': 'Connecticut', 'UNCG': 'UNC Greensboro', 'UCSB': 'UC Santa Barbara'}
    for key in abbreviationExceptions:
        if key in name:
            name = name.replace(key, abbreviationExceptions[key])
            return name
    return name


# Retrieves game result and returns winning team
def gameSim(homeTeam, awayTeam):
    browser.get(r'https://www.ncaagamesim.com/GameSimulator.asp')
    team1 = browser.find_element_by_name('HomeTeam')
    team1.send_keys(homeTeam)
    team2 = browser.find_element_by_name('AwayTeam')
    team2.send_keys(awayTeam)
    homeCourt = browser.find_element_by_name('HomeCourtAdv')
    time.sleep(.2)
    homeCourt.click()
    browser.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/div/div/div/div/form/a/button[1]').click()
    homeScore = browser.find_element_by_xpath(
        r'/html/body/div[3]/div/div/div[2]/div/div/a/center/div[3]/div[1]/table/tbody/tr[1]/td[2]').text
    awayScore = browser.find_element_by_xpath(
        r'/html/body/div[3]/div/div/div[2]/div/div/a/center/div[3]/div[2]/table/tbody/tr[1]/td[1]').text
    return homeTeam, homeScore, awayTeam, awayScore


# Siimulates next round and returns advancing teams
def roundSim(roundTeams: list):
    # Simulates Round
    roundResults = []
    roundCounter = 0
    while roundCounter < len(roundTeams):
        roundResults.append(gameSim(roundTeams[roundCounter], roundTeams[roundCounter + 1]))
        roundCounter += 2

    # Creates List of advancing teams
    gameCounter = 0
    advancingTeams = []
    for game in roundResults:
        if roundResults[gameCounter][1] > roundResults[gameCounter][3]:
            advancingTeams.append(roundResults[gameCounter][0])
        else:
            advancingTeams.append(roundResults[gameCounter][2])
        gameCounter += 1

    # Creates List of teams' scores
    roundScores = []
    for game in roundResults:
        roundScores.append(game[1])
        roundScores.append(game[3])
    return advancingTeams, roundScores


# Creates list of all team names
browser.get(r'http://www.espn.com/mens-college-basketball/bracketology')
elements = browser.find_elements_by_class_name('bracket__link')
allTeams = []
for element in elements:
    team = element.get_property('text')
    team = autoCorrect(team)
    allTeams.append(team)

# Simulates First Four
firstFourTeams = allTeams[:8]
firstFourWinners, firstFourScores = roundSim(firstFourTeams)

# Eliminates First Four duplicates
firstRoundTeams = allTeams[8:]

# Inserts First Four Winners
replaceCounter = 0
stringCounter = 0
slash = '/'
while stringCounter < len(firstRoundTeams):
    if slash in firstRoundTeams[stringCounter]:
        firstRoundTeams[stringCounter] = firstFourWinners[replaceCounter]
        replaceCounter += 1
    stringCounter += 1

# Simulate First Round
secondRoundTeams, firstRoundScores = roundSim(firstRoundTeams)

# Simulate Second Round
sweetSixteenTeams, secondRoundScores = roundSim(secondRoundTeams)

# Simulate Sweet 16
eliteEightTeams, sweetSixteenScores = roundSim(sweetSixteenTeams)

# Simulate Elite 8
finalFourTeams, eliteEightScores = roundSim(eliteEightTeams)

# Simulate Final Four
finalists, finalFourScores = roundSim(finalFourTeams)

# Simulate Championship
champions, championshipScores = roundSim(finalists)

# End Program
browser.quit()

firstFour = pd.DataFrame({'First Four': firstFourTeams})
firstFour2 = pd.DataFrame({'First Four Scores': firstFourScores})
firstRound = pd.DataFrame({'First Round': firstRoundTeams})
firstRound2 = pd.DataFrame({'First Round Scores': firstRoundScores})
secondRound = pd.DataFrame({'Second Round': secondRoundTeams})
secondRound2 = pd.DataFrame({'Second Round Scores': secondRoundScores})
sweetSixteen = pd.DataFrame({'Sweet Sixteen': sweetSixteenTeams})
sweetSixteen2 = pd.DataFrame({'Sweet Sixteen Scores': sweetSixteenScores})
eliteEight = pd.DataFrame({'Elite Eight': eliteEightTeams})
eliteEight2 = pd.DataFrame({'Elite Eight Scores': eliteEightScores})
finalFour = pd.DataFrame({'Final Four': finalFourTeams})
finalFour2 = pd.DataFrame({'Final Four Scores': finalFourScores})
championship = pd.DataFrame({'Championship Game': finalists})
championship2 = pd.DataFrame({'Championship Scores': championshipScores})
champion = pd.DataFrame({'Champions': champions})

df1 = pd.concat([firstFour, firstFour2, firstRound, firstRound2, secondRound, secondRound2,
                 sweetSixteen, sweetSixteen2, eliteEight, eliteEight2, finalFour,
                 finalFour2, championship, championship2, champion], ignore_index=False, axis=1)

df1.to_excel('Results.xlsx')
