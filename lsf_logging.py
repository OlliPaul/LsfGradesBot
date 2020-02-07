from selenium import webdriver
from time import sleep

class LsfBot():
    def __init__(self, username, pwd):
        self.driver = webdriver.Chrome('C:\\Users\\max-1\\Downloads\\chromedriver_win32\\chromedriver.exe')
        self.username = username
        self.pwd = pwd
        self.notenSpiegel = ''

    def login(self):
        self.driver.get('https://lsf.ovgu.de')
        sleep(1)
        login = self.driver.find_element_by_xpath('//*[@id="asdf"]')
        login.send_keys(self.username)
        password = self.driver.find_element_by_xpath('//*[@id="fdsa"]')
        password.send_keys(self.pwd)
        anmelden = self.driver.find_element_by_xpath('/html/body/div/div[6]/div[2]/div/div/form/div/div/ol/li[3]/input')
        anmelden.click()
        sleep(1)

    def selectNotenSeite(self):
        pruefungsverwaltung = self.driver.find_element_by_xpath('/html/body/div/div[6]/div[1]/ul/li[2]/a')
        pruefungsverwaltung.click()
        sleep(1)
        notenspiegel = self.driver.find_element_by_xpath('/html/body/div/div[6]/div[2]/div/form/div/ul/li[3]/a')
        notenspiegel.click()
        sleep(1)
        gotonoten = self.driver.find_element_by_xpath('/html/body/div/div[6]/div[2]/form/ul/li/a[2]')
        gotonoten.click()
        sleep(1)

    def getNotenSpiegel(self):
        html = self.driver.find_element_by_xpath('/html').text
        print(html)
        self.notenSpiegel = html

    def close(self):
        self.driver.quit()
