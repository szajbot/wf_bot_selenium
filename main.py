import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import schedule
from selenium import webdriver
import pyautogui
import configparser
import json
from datetime import datetime
import time

from settings.params import (
    PASSWORD,
    LOGIN,
    SERVER
)

from settings.settings import (
    FARM_COUNTER,
    FARM_ONE_WATERING_BONUS,
    FARM_ONE_POSITION,
    FARM_TWO_WATERING_BONUS,
    FARM_TWO_POSITION,
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
harvestAllButton = "cropall"
waterOneButton = "giessen"
exitFromFarmButton = "gardencancel"
animalCollect = "globalbox_button1"
animalFeed1 = "feed_item1_normal"
animalFeed2 = "feed_item2_normal"
animalFeed3 = "feed_item3_normal"
animalFeed4 = "feed_item4_normal"
config_file_name = 'settings/config.json'
with open(config_file_name, 'r') as file:
    config = json.loads(file.read())



# name, id, size, plant time
plantables.append(Plantable("Marchewki", "rackitem17", 1, 15))
plantables.append(Plantable("Truskawki", "rackitem20", 1, 480))
plantables.append(Plantable("Zboze", "rackitem1", 2, 20))
plantables.append(Plantable("Kukurydza", "rackitem2", 4, 45))
plantables.append(Plantable("Ogorki", "rackitem18", 1, 90))
plantables.append(Plantable("Cebule", "rackitem22", 1, 500))
plantables.append(Plantable("Koniczyna", "rackitem3", 2, 45))
plantables.append(Plantable("Pomidory", "rackitem21", 1, 600))
plantables.append(Plantable("Rzodkiewki", "rackitem19", 1, 240))
plantables.append(Plantable("Szpinak", "rackitem23", 1, 800))
plantables.append(Plantable("Kalafiory", "rackitem24", 1, 720))
plantables.append(Plantable("Rzepak", "rackitem4", 4, 90))


def showMainMenu():
    print("----------------WF_farm_bot----------------")
    print("1. Start planned farming")
    print("2. Manual plant")
    print("3. Set up configuration")
    print("4. Exit")


def schedulePlanting():

    pass


def findAndClick(driver, id):
    try:
        element = driver.find_element(by=By.ID, value=id)
        element.click()
    except:
        print(f"Cannot find element: {id}")


def findAndWrite(driver, id, write):
    try:
        element = driver.find_element(by=By.ID, value=id)
        element.click()
        time.sleep(0.5)
        pyautogui.write(str(write))
        time.sleep(0.5)
    except:
        print("Cannot find element: {id}" + id)


def findAndClickAndCheck(driver, id):
    try:
        element = driver.find_element(by=By.ID, value=id)
        element.click()
        return True
    except:
        return False


def harvest(window):
    time.sleep(1)
    findAndClick(window, harvestAllButton)
    time.sleep(1)
    findAndClick(window, "globalbox_button1")
    time.sleep(1)


def findAndSelect(driver, id, value):
    try:
        element = driver.find_element(by=By.ID, value=id)
        element.click()
        select = Select(element)
        select.select_by_value(value)
    except:
        print(f"Cannot find element: {id}")


def tryToCloseThatButton(driver):
    close_button = driver.find_element(By.CSS_SELECTOR, "div.mini_close.link[onclick='bonuspack.close();']")
    close_button.click()


def login():
    checkIsCorrect = True
    try:
        driver = webdriver.Chrome()
        driver.get("https://www.wolnifarmerzy.pl")
        time.sleep(4)
        findAndSelect(driver, 'loginserver', str(SERVER))
        findAndWrite(driver, "loginusername", LOGIN)
        findAndWrite(driver, "loginpassword", PASSWORD)
        findAndClick(driver, "loginbutton")
        time.sleep(3)
        for i in range(5):
            findAndClick(driver, "newsbox_close")
        tryToCloseThatButton(driver)
        checkIsCorrect = findAndClickAndCheck(driver, "rackcat1_img")
        time.sleep(1)
    except:
        print("Error occured when logging in")
    return driver, checkIsCorrect


def plant(vegetable: Plantable, window):
    findAndClick(window, vegetable.id)
    time.sleep(0.2)
    findAndClick(window, "rackcat1_img")
    time.sleep(0.2)
    number = 1
    for x in pole:
        if (vegetable.size == 1):
            findAndClick(window, x)
        if (vegetable.size == 2 and number % 2 == 1):
            findAndClick(window, x)
        if (vegetable.size == 4 and number % 2 == 1 and number % 24 < 12):
            findAndClick(window, x)
        time.sleep(0.075)
        number = number + 1
    time.sleep(0.2)


def water(vegetable: Plantable, window):
    findAndClick(window, waterOneButton)
    time.sleep(0.2)
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
        if (watered_fields > 5):
            findAndClick(window, waterOneButton)
            watered_fields = 0
        time.sleep(0.1)
        field_number = field_number + 1
    time.sleep(0.2)


def planting(farmPosition, vegetable: Plantable, watering, driver):
    findAndClick(driver, farmPosition)
    harvest(driver)
    plant(vegetable, driver)
    if watering:
        water(vegetable, driver)
    findAndClick(driver, exitFromFarmButton)
    time.sleep(1)
    pass


def setUpVegetables() -> Plantable:
    print("What would you like to plant?")
    i = 0
    for i in range(len(plantables)):
        print(
            f'Opcja nr {i + 1}, {plantables[i].name}: rozmiar: {plantables[i].size} czas do zbioru: {plantables[i].plantTime}')
    user_input = int(input()) - 1
    return plantables[user_input]


def manualPlanting():
    for x in range(1, 121):
        pole.append("field" + str(x))
    plant: Plantable = setUpVegetables()
    driver, checkIsCorrect = login()
    driver.fullscreen_window()  # TODO Temp solution
    planting(FARM_ONE_POSITION, plant, 'true', driver)
    planting(FARM_TWO_POSITION, plant, 'true', driver)


def setUpConfiguration():
    print("###################### SET UP CONFIGURATION ######################")
    # print("Podaj liczbę ..")
    # user_choose = input()
    file_to_write = json.dumps(config, indent=4)
    config["farm"]["counter"] = 3
    with open(config_file_name, "w") as outfile:
        outfile.write(file_to_write)



while True:
    # print(config["farm"])
    showMainMenu()
    user_choose = input()
    if (user_choose == "1"):
        schedulePlanting()
    elif (user_choose == "2"):
        manualPlanting()
    elif (user_choose == "3"):
        setUpConfiguration()
    elif (user_choose == "4"):
        exit(1)
    else:
        print("Zły wybór")
