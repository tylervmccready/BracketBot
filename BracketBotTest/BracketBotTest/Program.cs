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
            Browser browser = new Browser(driver);

            var teams = browser.RetrieveTeams();
            browser.SimulateFirstFour(teams);
            browser.SimulateTournament();
            
            Console.WriteLine($"{champions.ToString()} are the 2021 NCAA Tournament Champions");
        }
    }
}