import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from datetime import datetime
from selenium import webdriver
import pyautogui
import json
import time

import logging
from settings.log_config import setup_logging

from settings.login_config import (
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


class ScheduledJob:
    def __init__(self, executed: bool, function, plant: Plantable, endless: bool):
        self.executed = executed
        self.endless = endless
        self.function = function
        self.plant = plant


class ScheduledJobQueue:
    def __init__(self, jobsList: list[ScheduledJob], position):
        self.jobsList = jobsList
        self.position = position
        self.lastTaskTime = datetime.now()


# INICJALIZACJA
window = webdriver
user_choose = []
user_input = ""
plantables = []
pole = []
jobsQueue: list[ScheduledJobQueue] = []
executed_plant_job: bool = False
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
    print("1. Schedule Farming")
    print("2. Manual Farming")
    print("3. Set up configuration")
    print("4. Exit")


def showScheduleMenu():
    print("----------------Schedule Job----------------")
    print("1. Add job to queue")
    print("2. Remove job from queue")
    print("3. Execute queue")
    print("4. Show queue")
    print("5. Exit")
    print("6. Add endless job")


def showCurrentQueue():
    print("----------------Queue statuses----------------")
    for queue in jobsQueue:
        print(f'Queue: {queue.position}')
        for job in queue.jobsList:
            print(f'Job: {job.plant.name} endless: {job.endless}')
        print("\n")


def showAvailablePositions():
    for x in range(int(config["farm"]["counter"])):
        print(f'Option {x + 1}: position: {config["farm"][intToStrNumber(x + 1)]}')

def addEndlessJobToQueue():
    showAvailablePositions()
    user_choose = input()
    position = config["farm"][intToStrNumber(int(user_choose))]["position"]
    plant: Plantable = setUpVegetables()

    exists = False

    for queue in jobsQueue:
        if queue.position == position:
            queue.jobsList.append(ScheduledJob(executed=False, function=executeSchedulePlant, plant=plant, endless=True))
            exists = True

    if not exists:
        job = ScheduledJob(executed=False, function=executeSchedulePlant, plant=plant, endless=True)
        jobList = list()
        jobList.append(job)
        queue = ScheduledJobQueue(jobList, position)
        jobsQueue.append(queue)

def addJobToQueue():
    showAvailablePositions()
    user_choose = input()
    position = config["farm"][intToStrNumber(int(user_choose))]["position"]
    plant: Plantable = setUpVegetables()

    exists = False

    for queue in jobsQueue:
        if queue.position == position:
            queue.jobsList.append(ScheduledJob(executed=False, function=executeSchedulePlant, plant=plant, endless=False))
            exists = True

    if not exists:
        job = ScheduledJob(executed=False, function=executeSchedulePlant, plant=plant, endless=False)
        jobList = list()
        jobList.append(job)
        queue = ScheduledJobQueue(jobList, position)
        jobsQueue.append(queue)


def removeJobsFromQueue():
    global jobsQueue
    jobsQueue = list()


def executeQueue():
    # immediately perform tasks from first position in queue
    for queue in jobsQueue:
        if queue.jobsList[0].endless:
            job: ScheduledJob = queue.jobsList[0]
        else:
            job: ScheduledJob = queue.jobsList.pop(0)
        logging.info(f"Executing job with plant {job.plant}")
        job.function(job.plant, queue.position)
        logging.info("Job executed")
        queue.lastTaskTime = datetime.now()

    while True:
        for queue in jobsQueue:
            timePassed = datetime.now() - queue.lastTaskTime
            if timePassed.seconds >= (queue.jobsList[0].plant.plantTime * 60 * 0.95):
                if queue.jobsList[0].endless:
                    job: ScheduledJob = queue.jobsList[0]
                else:
                    job: ScheduledJob = queue.jobsList.pop(0)
                logging.info(f"Executing job with plant {job.plant}")
                job.function(job.plant, queue.position)
                logging.info("Job executed")
                queue.lastTaskTime = datetime.now()

        time.sleep(5)
        print("----------------Queue statuses----------------")
        for queue in jobsQueue:
            if len(queue.jobsList) < 1:
                jobsQueue.remove(queue)
            else:
                timePassed = datetime.now() - queue.lastTaskTime
                timeLeft = (queue.jobsList[0].plant.plantTime * 60 * 0.97) - timePassed.seconds
                print(f"Queue: {queue.position} time for next task: {timeLeft} next task: {queue.jobsList[0].plant.name} endless: {queue.jobsList[0].endless} queue: {len(queue.jobsList)}")


def scheduleFarming():
    while True:
        showScheduleMenu()
        user_choose = input()
        if (user_choose == "1"):
            addJobToQueue()
        elif (user_choose == "2"):
            removeJobsFromQueue()
        elif (user_choose == "3"):
            executeQueue()
        elif (user_choose == "4"):
            showCurrentQueue()
        elif (user_choose == "5"):
            exit(1)
        elif (user_choose == "6"):
            addEndlessJobToQueue()
        else:
            print("Zły wybór")


def executeSchedulePlant(plant: Plantable, position):
    driver, checkIsCorrect = login()
    driver.fullscreen_window()  # TODO Temp solution
    planting(position, plant, 'true', driver)
    driver.close()
    # executed_plant_job = True


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


def planting(farm_position, vegetable: Plantable, watering, driver):
    findAndClick(driver, farm_position)
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


def execute(plant):
    driver, checkIsCorrect = login()
    driver.fullscreen_window()  # TODO Temp solution
    planting(config["farm"]["one"]["position"], plant, 'true', driver)
    planting(config["farm"]["two"]["position"], plant, 'true', driver)


def manualPlanting():
    plant: Plantable = setUpVegetables()
    execute(plant)


def intToStrNumber(user_choose):
    switcher = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
    }

    return switcher.get(user_choose, "nothing")


def setUpConfiguration():
    print("###################### SET UP CONFIGURATION ######################")
    print("Podaj liczbę pól")
    user_choose = input()
    i = int(user_choose)
    config["farm"]["counter"] = i
    for x in range(i):
        print("Podaj pozycję pola")
        user_choose = input()
        config["farm"][intToStrNumber(x + 1)]["position"] = f'farm1_pos{user_choose}'

        print("Podaj bonus podlewania")
        user_choose = input()
        config["farm"][intToStrNumber(x + 1)]["watering_bonus"] = int(user_choose)

    print("Podaj liczbę kurników")
    user_choose = input()
    i = int(user_choose)
    config["chicken"]["counter"] = i
    for x in range(i):
        print("Podaj pozycję kurnika")
        user_choose = input()
        config["chicken"][intToStrNumber(x + 1)]["position"] = f'farm1_pos{user_choose}'

    print("Podaj liczbę obór")
    user_choose = input()
    i = int(user_choose)
    config["cow"]["counter"] = i
    for x in range(i):
        print("Podaj pozycję obory")
        user_choose = input()
        config["cow"][intToStrNumber(x + 1)]["position"] = f'farm1_pos{user_choose}'

    file_to_write = json.dumps(config, indent=4)
    with open(config_file_name, "w") as outfile:
        outfile.write(file_to_write)


for x in range(1, 121):
    pole.append("field" + str(x))

while True:
    showMainMenu()
    user_choose = input()
    if (user_choose == "1"):
        scheduleFarming()
    elif (user_choose == "2"):
        manualPlanting()
    elif (user_choose == "3"):
        setUpConfiguration()
    elif (user_choose == "4"):
        exit(1)
    else:
        print("Zły wybór")
