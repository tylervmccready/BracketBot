using System;
using NUnit.Framework;
using System.Collections.Generic;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using OpenQA.Selenium.Support.UI;

namespace BracketBotTest
{
    class Program
    {
        static void Main(string[] args)
        {
            IWebDriver driver = new ChromeDriver("C:\\Users\\tyler");
            driver.Manage().Window.Minimize();
            Browser browser = new Browser(driver);

            // Sets up starting lists of teams
            var allTeams = browser.RetrieveTeams();
            var firstFourTeams = allTeams.Take(8).ToList();
            var firstRoundTeams = allTeams.Skip(8).ToList();
            
            // Simulates First Four
            var (firstFourWinners, firstFourScores) = browser.RoundSim(firstFourTeams);
            
            // Inserts First Four Winners
            int replaceCounter = 0;
            for (int i = 0; i < firstRoundTeams.Count; i++)
            {
                if (firstRoundTeams[i].Contains('/'))
                {
                    firstRoundTeams[i] = firstFourWinners[replaceCounter];
                    replaceCounter++;
                }
            }

            (List<string>, List<int>)[] allResults = new (List<string>, List<int>)[7];
            allResults[0] = (firstFourWinners, firstFourScores);
            
            // Simulate First Round
            var (secondRoundTeams, firstRoundScores) = browser.RoundSim(firstRoundTeams);
            allResults[1] = (secondRoundTeams, firstRoundScores);

            // Simulate Second Round
            var (sweetSixteenTeams, secondRoundScores) = browser.RoundSim(secondRoundTeams);
            allResults[2] = (sweetSixteenTeams, secondRoundScores);

            // Simulate Sweet 16
            var(eliteEightTeams, sweetSixteenScores) = browser.RoundSim(sweetSixteenTeams);
            allResults[3] = (eliteEightTeams, sweetSixteenScores);

            // Simulate Elite 8
            var (finalFourTeams, eliteEightScores) = browser.RoundSim(eliteEightTeams);
            allResults[4] = (finalFourTeams, eliteEightScores);

            // Simulate Final Four
            var (finalists, finalFourScores) = browser.RoundSim(finalFourTeams);
            allResults[5] = (finalists, finalFourScores);

            // Simulate Championship
            var(champions, championshipScores) = browser.RoundSim(finalists);
            allResults[6] = (champions, championshipScores);
            
            browser.Close();

            Console.WriteLine($"{champions.ToString()} are the 2021 NCAA Tournament Champions");
        }
    }
}