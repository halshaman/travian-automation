from selenium import webdriver
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
from random import randint
import json
from pprint import pprint
import sys

class Travian:
    def __init__(self):
        self.setup()
    def setup(self):
        self.driver = webdriver.PhantomJS()
        # self.driver = webdriver.Firefox()
        config_json_fp = open('config.json')
        config = json.load(config_json_fp)
        # pprint(config)
        # sys.exit(0)

        self.username = config["username"]
        self.password = config["password"]
        self.server = config["server"]
        self.farmers = config["farmer"]
    def raid(self):
        for farmer in self.farmers:
            print "opening farm list for village " + farmer["village"]
            self.driver.get(self.server + "build.php?tt=99&id=39")
            try:
                # Click on village from Raid has to be made
                print "Relecting raid village"
                self.driver.find_element_by_css_selector("#sidebarBoxVillagelist div a[href^='?newdid=" + farmer["village"] + "']").click()
            except NoSuchElementException:
                self.login()

                # Open rally point again
                print "opening farm list again"
                self.driver.get(self.server + "build.php?tt=99&id=39")
                # Click on village from where Raid has to be made
                print "Selecting raid village again"
                self.driver.find_element_by_css_selector("#sidebarBoxVillagelist div a[href^='?newdid=" + farmer["village"] + "']").click()

            # Select all targets
            print "Selecting all targets"
            self.driver.find_element_by_id("raidListMarkAll" + farmer["list"]).click()

            # Click on Raid
            print "Clicking on raid"
            self.driver.find_element_by_css_selector("#list" + farmer["list"] + " .listContent > button").click()

            # TODO: Check number of raids made and print

    def login(self):
        print "Logged out, Logging in"
        self.driver.find_element_by_name("name").clear()
        self.driver.find_element_by_name("name").send_keys(self.username)
        self.driver.find_element_by_name("password").clear()
        self.driver.find_element_by_name("password").send_keys(self.password)

        try:
            self.driver.find_element_by_id("reloginButton").click()
        except NoSuchElementException:
            self.driver.find_element_by_id("s1").click()

    def is_logged_out(self):
        print "Checking if user is loggedout"
        try:
            self.driver.find_element_by_name("password")
            print "User is loggedout"
            return True
        except NoSuchElementException:
            print "User is loggedin"
            return False

    def manage_raid_report(self):
        # Open reports page
        print "Opening reports page"
        self.driver.get(self.server + "berichte.php")
        self.delete_raid_report()

    def delete_raid_report(self):
        # Read unread raid reports (made by me) [Won as attacker without losses.]
        # TODO: Attack a player and get some damage check if the the css selector is still valid

        try:
            print "Finding messages with raids with non loss"
            # messages = self.driver.find_elements_by_css_selector("#overview img[alt='Won as attacker without losses.']")
            messages = self.driver.find_element_by_xpath("//img[@alt='Won as attacker without losses.']/../../td[@class='sel']/input")
            if messages.__len__() == 0:
                # Either user is loggedout or there is no such report
                if self.is_logged_out():
                    print "Login"
                    self.login()
                    self.manage_raid_report()
                    return
            else:
                self.driver.find_elements_by_xpath("//img[@alt='Won as attacker without losses.']/../../td[@class='sel']/input").click()
                # selected = False
                # for message in messages:
                #     selected = True
                #     print "Selecting all the such reports"
                    # message.parent.parent.find_elements_by_css_selector("td.sel input").click()

                # Delete these reports (if found)
                # if selected:
                print "Deleting selected reports"
                self.driver.find_element_by_id("del").click()
        except NoSuchElementException:
            if self.is_logged_out():
                print "Login"
                self.login()
                self.manage_raid_report()
                return

        # Click on next if present (repeat) if not present break out
        try:
            print "Clicking next report"
            self.driver.find_elements_by_css_selector(".paginator a.next").click()
            print "Repeating delete report"
            self.delete_raid_report()
        except NoSuchElementException:
            return

    def run(self):
        # self.manage_raid_report()
        # sys.exit(0)
        while(1):
            # raid all villages
            self.raid()

            wait_time = randint(15, 30)
            print "Waiting for " + str(wait_time) + " minutes"
            # Sleep for 15 - 30 minutes and try again
            time.sleep(60 * wait_time)

t = Travian()
t.run()
