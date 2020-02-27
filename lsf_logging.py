from selenium import webdriver
from time import sleep
from pyvirtualdisplay import Display
import re

class LsfBot():
    def __init__(self, username, pwd):
        ### Einkommentieren wenn auf Server ###
        ### display = Display(visible=0, size=(1024, 768))
        ### display.start()
        ### self.driver = webdriver.Chrome('/home/ksoll/dev/chromedriver')

        self.driver = webdriver.Chrome('C:\\Users\\max-1\\Downloads\\chromedriver_win32\\chromedriver.exe')
        self.username = username
        self.pwd = pwd
        self.notenSpiegel = ''

    def login(self):
        self.driver.get('https://lsf.ovgu.de')
        sleep(3)
        login = self.driver.find_element_by_xpath('//*[@id="asdf"]')
        login.send_keys(self.username)
        password = self.driver.find_element_by_xpath('//*[@id="fdsa"]')
        password.send_keys(self.pwd)
        anmelden = self.driver.find_element_by_xpath('/html/body/div/div[6]/div[2]/div/div/form/div/div/ol/li[3]/input')
        anmelden.click()
        sleep(3)

    def selectNotenSeite(self):
        pruefungsverwaltung = self.driver.find_element_by_xpath('/html/body/div/div[6]/div[1]/ul/li[2]/a')
        pruefungsverwaltung.click()
        sleep(3)
        notenspiegel = self.driver.find_element_by_xpath('/html/body/div/div[6]/div[2]/div/form/div/ul/li[3]/a')
        notenspiegel.click()
        sleep(3)
        gotonoten = self.driver.find_element_by_xpath('/html/body/div/div[6]/div[2]/form/ul/li/a[2]')
        gotonoten.click()
        sleep(3)

    def getNotenSpiegel(self):
        html = self.driver.find_element_by_xpath('/html').text
        matches = re.findall("(\d{4,}\s[a-zA-Z0-9\söäüß/,.()-]*)", html)
        complete = ""
        for n in range(len(matches)):
            complete += matches[n]
        self.notenSpiegel = complete

    def close(self):
        self.driver.quit()
