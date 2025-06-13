import datetime
import schedule
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pyautogui
from datetime import datetime
import time

from settings.params import (
    PASSWORD,
    LOGIN,
    SERVER
)

class Plantable:
  def __init__(self, name, id, size, plantTime):
    self.name = name
    self.id = id
    self.size = size
    self.plantTime = plantTime

# INICJALIZACJA
window = webdriver
user_choose = []
user_input = ""
plantables = []
pole = []
farmOnePosition = "farm1_pos1"
farmTwoPosition = "farm1_pos3"
harvestAllButton = "cropall"
waterOneButton = "giessen"
exitFromFarmButton = "gardencancel"

# name, id, size, plant time
plantables.append(Plantable("Marchewki","rackitem17",1,15))
plantables.append(Plantable("Truskawki","rackitem20",1,480))
plantables.append(Plantable("Zboze","rackitem1",2,20))
plantables.append(Plantable("Kukurydza","rackitem2",4,45))
plantables.append(Plantable("Ogorki","rackitem18",1,90))
plantables.append(Plantable("Cebule", "rackitem22", 1, 500))
plantables.append(Plantable("Koniczyna","rackitem3",2,45))
plantables.append(Plantable("Pomidory","rackitem21",1,600))
plantables.append(Plantable("Rzodkiewki","rackitem19",1,240))
plantables.append(Plantable("Szpinak","rackitem23",1,800))
plantables.append(Plantable("Kalafiory", "rackitem24", 1, 720))
plantables.append(Plantable("Rzepak","rackitem4",4,90))

def showMainMenu():
    print("----------------WF_farm_bot----------------")
    print("1. Start planned farming")
    print("2. Manual plant")
    print("3. Exit")

def schedulePlanting():
    pass

def findAndClickAndWrite(window, id, write):
    try:
        find = window.find_element(by=By.ID, value=id)
        find.click()
        time.sleep(0.5)
        pyautogui.write(str(write))
        time.sleep(0.5)
    except:
        print("some error at: " + id)

def findAndClickAndCheck(window, id):
    try:
        find = window.find_element(by=By.ID, value=id)
        find.click()
    except:
        return False

def findAndClick(window, id):
    try:
        find = window.find_element(by=By.ID, value=id)
        find.click()
    except:
        None

def harvest(window):
    time.sleep(1)
    findAndClick(window, harvestAllButton)
    time.sleep(1)
    findAndClick(window, "globalbox_button1")
    time.sleep(1)

def login():
    try:
        service = Service(executable_path="chromedriver.exe")
        window = webdriver.Chrome(service=service)
        window.get("https://www.wolnifarmerzy.pl")
        time.sleep(4)
        findAndClickAndWrite(window, "loginusername", PASSWORD)
        findAndClickAndWrite(window, "loginpassword", LOGIN)
        time.sleep(4)
        for i in range(3):
            findAndClickAndWrite(window, "newsbox_close")
        checkIsCorrect = findAndClickAndCheck(window, "rackcat1_img")
        time.sleep(0.2)
    except:
        checkIsCorrect = False
    return window, checkIsCorrect

def plant(vegetable: Plantable, window):
    findAndClick(window, vegetable.id)
    time.sleep(0.2)
    findAndClick(window, "rackcat1_img")
    time.sleep(0.2)
    number = 1
    for x in pole:
        if(vegetable.size == 1):
            findAndClick(window, x)
        if(vegetable.size == 2 and number%2 == 1):
            findAndClick(window, x)
        if(vegetable.size == 4 and number%2 == 1 and number%24 < 12):
            findAndClick(window, x)
        time.sleep(0.075)
        number = number + 1
    time.sleep(1)

def water(vegetable: Plantable, window):
    findAndClick(window, waterOneButton)
    time.sleep(1)
    field_number = 1
    watered_fields = 0
    for x in pole:
        if (vegetable.size == 1):
            findAndClick(window, x)
            watered_fields = watered_fields + 1
        if (vegetable.size == 2 and field_number % 2 == 1):
            findAndClick(window, x)
            watered_fields = watered_fields + 1
        if (vegetable.size == 4 and field_number % 2 == 1 and field_number % 24 < 12):
            findAndClick(window, x)
            watered_fields = watered_fields + 1
        if(watered_fields > 5):
            findAndClick(window, waterOneButton)
            watered_fields = 0
        time.sleep(0.1)
        field_number = field_number + 1
    time.sleep(1)

def planting(farmPosition, vegetable: Plantable, watering):
    window, checkIsCorrect = login()
    findAndClick(window, farmOnePosition)
    harvest(window)
    plant(vegetable, window)
    water(vegetable, window)
    findAndClick(window, exitFromFarmButton)
    time.sleep(2)
    pass


def showVegetables():
    i = 0
    for i in range(len(plantables)):
        print(f'Opcja nr {i + 1}, {plantables[i].name}: rozmiar: {plantables[i].size} czas do zbioru: {plantables[i].plantTime}')
    user_input = int(input())
    planting(farmOnePosition, plantables[user_input], 'true')


def manualPlanting():
    print("What would you like to plant?")
    showVegetables()


while True:
    showMainMenu()
    user_choose = input()
    if (user_choose == "1"):
        schedulePlanting()
    elif (user_choose == "2"):
        manualPlanting()
    elif(user_choose == "3"):
        exit(1)
    else:
        print("Zły wybór")