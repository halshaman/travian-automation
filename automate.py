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
        config_json_fp = open('config.json')
        config = json.load(config_json_fp)
        # pprint(config)
        # sys.exit(0)

        self.username = config["username"]
        self.password = config["password"]
        self.server = config["server"]
        self.farmer = config["farmer"][0]
    def raid(self):
        print "opening farm list"
        self.driver.get(self.server + "build.php?tt=99&id=39")
        try:
            # Click on village from Raid has to be made
            print "Relecting raid village"
            self.driver.find_element_by_css_selector("#sidebarBoxVillagelist div a[href^='?newdid=" + self.farmer["village"] + "']").click()
        except NoSuchElementException:
            print "Logged out, Logging in"
            self.driver.find_element_by_name("name").clear()
            self.driver.find_element_by_name("name").send_keys(self.username)
            self.driver.find_element_by_name("password").clear()
            self.driver.find_element_by_name("password").send_keys(self.password)

            try:
                self.driver.find_element_by_id("reloginButton").click()
            except NoSuchElementException:
                self.driver.find_element_by_id("s1").click()

            # Open rally point again
            print "opening farm list again"
            self.driver.get(self.server + "build.php?tt=99&id=39")
            # Click on village from where Raid has to be made
            print "Selecting raid village again"
            self.driver.find_element_by_css_selector("#sidebarBoxVillagelist div a[href^='?newdid=" + self.farmer["village"] + "']").click()

        # Select all targets
        print "Selecting all targets"
        self.driver.find_element_by_id("raidListMarkAll1244").click()

        # Click on Raid
        print "Clicking on raid"
        self.driver.find_element_by_css_selector("#list" + self.farmer["list"] + " .listContent > button").click()

        # TODO: Check number of raids made and print

    def run(self):
        while(1):
            # raid all villages
            self.raid()
            wait_time = randint(15, 30)
            print "Waiting for " + str(wait_time) + " minutes"
            # Sleep for 15 - 30 minutes and try again
            time.sleep(60 * wait_time)

t = Travian()
t.run()
