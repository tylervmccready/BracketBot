using System.Collections.Generic;
using System.Linq;
using System.Threading;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Support.UI;

namespace BracketBotTest
{
    public class Browser
    {
        private IWebDriver browser = null;

        public Browser(IWebDriver browser)
        {
            this.browser = browser;
        }
        
        // Creates list of all team names
        public List<string> RetrieveTeams()
        {
            browser.Url = "http://www.espn.com/mens-college-basketball/bracketology";
            var allTeams = new List<string>();
            foreach (var element in browser.FindElements(By.ClassName("bracket__link")))
            {
                var team = element.GetProperty("text");
                team = AutoCorrect(team);
                if (team is { })
                {
                    allTeams.Add(team);
                }
            }
            return allTeams;
        }

        // Translates from ESPN to GameSim
        private static string AutoCorrect(string name)
        {
            Dictionary<string, string> abbreviationExceptions = new Dictionary<string, string>();
            abbreviationExceptions["W."] = "Western";
            abbreviationExceptions["E."] = "Eastern";
            abbreviationExceptions["Louisiana St."] = "LSU";
            abbreviationExceptions["N.C. A&T"] = "North Carolina A&T";
            abbreviationExceptions["UConn"] = "Connecticut";
            abbreviationExceptions["UNCG"] = "UNC Greensboro";
            abbreviationExceptions["UCSB"] = "UC Santa Barbara";
            abbreviationExceptions[" St."] = " State";
            abbreviationExceptions["Prairie View A&M"] = "Prairie View";
            foreach (KeyValuePair<string, string> kvp in abbreviationExceptions)
            {
                if (name.Contains(kvp.Key))
                {
                    name = name.Replace(kvp.Key, kvp.Value);
                    return name;
                }
            }
            return name;
        }
        
        // Retrieves and returns game result 
        private (string, int, string, int) GameSim(string homeTeam, string awayTeam)
        {
            
            browser.Url = "https://www.ncaagamesim.com/GameSimulator.asp";
            IWebElement home = browser.FindElement(By.Name("HomeTeam"));
            SelectElement homeSelect = new SelectElement(home);
            homeSelect.SelectByText(homeTeam);
            Thread.Sleep(200);
            IWebElement away = browser.FindElement(By.Name("AwayTeam"));
            SelectElement awaySelect = new SelectElement(away);
            awaySelect.SelectByText(awayTeam);
            IWebElement homeCourt = browser.FindElement(By.Name("HomeCourtAdv"));
            Thread.Sleep(200);
            homeCourt.Click();
            IWebElement submit = browser.FindElement(By.XPath("/html/body/div[3]/div/div/div[2]/div/div/div/div/form/a/button[1]"));
            submit.Click();
            var homeScoreRaw = browser.FindElement(
                    By.XPath("/html/body/div[3]/div/div/div[2]/div/div/a/center/div[3]/div[1]/table/tbody/tr[1]/td[2]"))
                .Text;
            var awayScoreRaw = browser.FindElement(
                    By.XPath("/html/body/div[3]/div/div/div[2]/div/div/a/center/div[3]/div[2]/table/tbody/tr[1]/td[1]"))
                .Text;
            var homeScore = int.Parse(homeScoreRaw);
            var awayScore = int.Parse(awayScoreRaw);
            return (homeTeam, homeScore, awayTeam, awayScore);
        }
        
        // Simulates next round and returns tuple of advancing teams and Round scores
        public (List<string>, List<int>) RoundSim(List<string> roundTeams)
        {
            // Simulates Round
            var roundResults = new List<(string, int, string, int)>();
            for (int i = 0; i < roundTeams.Count; i+=2)
            {
                roundResults.Add(GameSim(roundTeams[i], roundTeams[i + 1]));
            }
            
            // Creates array of advancing teams
            var advancingTeams = new List<string>();
            for (int i = 0; i < roundResults.Count; i++)
            {
                if (roundResults[i].Item2 > roundResults[i].Item4)
                {
                    advancingTeams.Add(roundResults[i].Item1);
                }
                else
                {
                    advancingTeams.Add(roundResults[i].Item3);
                }
            }
            
            // Creates array of all teams' scores
            var roundScores = new List<int>();
            for (int i = 0; i < roundResults.Count; i+=2)
            {
                roundScores.Add(roundResults[i].Item2);
                roundScores.Add(roundResults[i].Item4);
            }
            return (advancingTeams, roundScores);
        }

        // Closes Browser
        public void Close()
        {
            browser.Close();
        }
    }
}