from datetime import time

from selenium import webdriver

# Translates from ESPN to GameSim
abbreviationExceptions = [('N.C. A&T','North Carolina A&T')]


browser = webdriver.Chrome()


# Retrieves game result and returns winning team
def gameSim(homeTeam, awayTeam):
    if homeTeam == 'N.C. A&T':
        homeTeam = 'North Carolina A&T'
    elif awayTeam == 'N.C. A&T':
        awayTeam = 'North Carolina A&T'
    browser.get('https://www.ncaagamesim.com/GameSimulator.asp')
    team1 = browser.find_element_by_name('HomeTeam')
    team1.send_keys(homeTeam)
    team2 = browser.find_element_by_name('AwayTeam')
    team2.send_keys(awayTeam)
    homeCourt = browser.find_element_by_name('HomeCourtAdv')
    homeCourt.click()
    browser.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/div/div/div/div/form/a/button[1]').click()
    homeScore = browser.find_element_by_xpath(
        '/html/body/div[3]/div/div/div[2]/div/div/a/center/div[3]/div[1]/table/tbody/tr[1]/td[2]').text
    awayScore = browser.find_element_by_xpath(
        '/html/body/div[3]/div/div/div[2]/div/div/a/center/div[3]/div[2]/table/tbody/tr[1]/td[1]').text
    if homeScore > awayScore:
        return homeTeam
    else:
        return awayTeam


# Stores all elements containing team names
browser.get('http://www.espn.com/mens-college-basketball/bracketology')
elements = browser.find_elements_by_class_name('bracket__link')
print(elements[0])


# Stores teams in First Four
firstFour = []
i = 0
while i < 8:
    firstFour.append(elements[i].get_property('text'))
    i += 1
print(firstFour)





print(gameSim(firstFour[0], firstFour[1]))
# for game in firstFour:

# firstFour.append(browser.find_element_by_xpath('//*[@id="68-teams"]/article/div[1]/article/div/ol[1]/li[1]/div/a').get_property('text'))
# firstFour.append(browser.find_element_by_xpath('').get_property('text'))
# firstFour.append(browser.find_element_by_xpath('').get_property('text'))
# firstFour.append(browser.find_element_by_xpath('').get_property('text'))
# firstFour.append(browser.find_element_by_xpath('').get_property('text'))
# firstFour.append(browser.find_element_by_xpath('').get_property('text'))
# firstFour.append(browser.find_element_by_xpath('').get_property('text'))
# firstFour.append(browser.find_element_by_xpath('').get_property('text'))
#
#
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')
# team1_1 = browser.find_element_by_xpath('').get_property('text')


browser.quit()
