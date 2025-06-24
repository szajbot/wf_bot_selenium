import datetime
import logging
import os
import json
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from datetime import datetime, timedelta

from structure.JobType import JobType
from structure.Juice import Juice
from structure.Plantable import Plantable
from structure.predefined_lists import juices, farmPlants, chickenPlants, cowPlants, field
from settings.logging_config import LoggingConfig

LoggingConfig(logging)

from settings.login import (
    PASSWORD,
    LOGIN,
    SERVER
)

from settings.params import (
    HARVEST_ALL_BUTTON,
    WATER_ONE_BUTTON,
    EXIT_FROM_FARM_BUTTON,
    COLLECT_BUTTON,
    ANIMAL_FEED_1,
    ANIMAL_FEED_2,
    ANIMAL_FEED_3,
    ANIMAL_FEED_4,
    CONFIG_FILE_NAME,
    CLOSE_NEWSBOX
)


class ScheduledJob:
    def __init__(self, executed: bool, function, endless: bool, type: JobType, plant: Plantable = None,
                 juice: Juice = None):
        self.executed = executed
        self.endless = endless
        self.function = function
        self.plant = plant
        self.juice = juice
        self.type = type


class FarmConfig:
    def __init__(self, number, position, wateringBonus):
        self.number = number
        self.position = position
        self.wateringBonus = wateringBonus


class CowConfig:
    def __init__(self, number, position):
        self.number = number
        self.position = position


class ChickenConfig:
    def __init__(self, number, position):
        self.number = number
        self.position = position


class ScheduledJobQueue:
    def __init__(self, jobsList: list[ScheduledJob], position, config, type: JobType):
        self.jobsList = jobsList
        self.config = config
        self.position = position
        self.lastTaskEndTime = datetime.now()
        self.type = type


# INICJALIZACJA
window = webdriver
user_choose = []
user_input = ""
jobsQueue: list[ScheduledJobQueue] = []
with open(CONFIG_FILE_NAME, 'r') as file:
    config = json.loads(file.read())


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def showMainMenu():
    cls()
    print("----------------WF_farm_bot----------------")
    print("1. Schedule Farming")
    print("2. Manual Farming")
    print("3. Set up configuration")
    print("4. Exit")


def showScheduleMenu():
    cls()
    print("----------------Schedule Job----------------")
    print("1. Add job to queue")
    print("2. Remove job from queue")
    print("3. Execute queue")
    print("4. Show queue")
    print("5. Exit")
    print("6. Add endless job")


def showAvailableJobs():
    cls()
    print("----------------Schedule Job----------------")
    print("0. Go back")
    print("1. Planting")
    print("2. Chicken")
    print("3. Cow")
    print("4. Juices")
    pass


def showCurrentQueue():
    cls()
    print("----------------Queue statuses----------------")
    for queue in jobsQueue:
        print(f'Queue: {queue.position}')
        for job in queue.jobsList:
            print(f'Job: {job.type}, {job.plant.name} endless: {job.endless}')
        print("\n")


def showAvailableFarms():
    cls()
    for x in range(int(config["farm"]["counter"])):
        print(f'Option {x + 1}: position: {config["farm"][intToStrNumber(x + 1)]}')


def showAvailableChciken():
    cls()
    for x in range(int(config["chicken"]["counter"])):
        print(f'Option {x + 1}: position: {config["chicken"][intToStrNumber(x + 1)]}')


def showAvailableCow():
    cls()
    for x in range(int(config["cow"]["counter"])):
        print(f'Option {x + 1}: position: {config["cow"][intToStrNumber(x + 1)]}')


def setUpPlantForFarming():
    cls()
    print("What would you like to plant?")
    print("Opcja nr 0, go back")
    for i in range(len(farmPlants)):
        print(
            f'Opcja nr {i + 1}, {farmPlants[i].name}: rozmiar: {farmPlants[i].size} czas do zbioru: {farmPlants[i].plantTime}')


def addEndlessJobToQueue():
    showAvailableFarms()
    user_choose = input()
    position = config["farm"][intToStrNumber(int(user_choose))]["position"]
    setUpPlantForFarming()
    user_input = int(input())
    plant = farmPlants[user_input - 1]

    exists = False

    for queue in jobsQueue:
        if queue.position == position:
            queue.jobsList.append(ScheduledJob(executed=False, function=executeSchedulePlant, plant=plant, endless=True,
                                               type=JobType.Farming))
            exists = True

    if not exists:
        job = ScheduledJob(executed=False, function=executeSchedulePlant, plant=plant, endless=True,
                           type=JobType.Farming)
        jobList = list()
        jobList.append(job)
        farmConfig = FarmConfig([intToStrNumber(int(user_choose))], position,
                                config["farm"][intToStrNumber(int(user_choose))]["watering_bonus"])
        queue = ScheduledJobQueue(jobList, position, farmConfig, JobType.Farming)
        jobsQueue.append(queue)


def addPlantingJobToPosition(position):
    while True:
        setUpPlantForFarming()
        user_input = int(input())
        if user_input == 0:
            break
        else:
            plant = farmPlants[user_input - 1]
            exists = False

            for queue in jobsQueue:
                if queue.position == position:
                    queue.jobsList.append(
                        ScheduledJob(executed=False, function=executeSchedulePlant, plant=plant, endless=False,
                                     type=JobType.Farming))
                    exists = True

            if not exists:
                job = ScheduledJob(executed=False, function=executeSchedulePlant, plant=plant, endless=False,
                                   type=JobType.Farming)
                jobList = list()
                jobList.append(job)
                farmConfig = FarmConfig([intToStrNumber(int(user_choose))], position,
                                        config["farm"][intToStrNumber(int(user_choose))]["watering_bonus"])
                queue = ScheduledJobQueue(jobList, position, farmConfig, JobType.Farming)
                jobsQueue.append(queue)


def addPlantingJob():
    showAvailableFarms()
    user_choose = input()
    position = config["farm"][intToStrNumber(int(user_choose))]["position"]
    addPlantingJobToPosition(position)


def setUpPlantForChciken():
    print("Feed chickens with what?")
    i = 0

    for i in range(len(chickenPlants)):
        print(
            f'Opcja nr {i + 1}, {chickenPlants[i].name}')
    user_input = int(input()) - 1
    return chickenPlants[user_input]


def setUpPlantForCow():
    print("Feed cows with what?")
    i = 0

    for i in range(len(cowPlants)):
        print(
            f'Opcja nr {i + 1}, {cowPlants[i].name}')
    user_input = int(input()) - 1
    return cowPlants[user_input]


def scheduleChicken():
    showAvailableChciken()
    user_choose = input()
    position = config["chicken"][intToStrNumber(int(user_choose))]["position"]
    plant: Plantable = setUpPlantForChciken()

    exists = False

    for queue in jobsQueue:
        if queue.position == position:
            queue.jobsList.append(
                ScheduledJob(executed=False, function=executeScheduleChicken, plant=plant, endless=True,
                             type=JobType.Chicken))
            exists = True

    if not exists:
        job = ScheduledJob(executed=False, function=executeScheduleChicken, plant=plant, endless=True,
                           type=JobType.Chicken)
        jobList = list()
        jobList.append(job)
        chickenConfig = ChickenConfig([intToStrNumber(int(user_choose))], position)
        queue = ScheduledJobQueue(jobList, position, chickenConfig, JobType.Chicken)
        jobsQueue.append(queue)


def scheduleCow():
    showAvailableCow()
    user_choose = input()
    position = config["cow"][intToStrNumber(int(user_choose))]["position"]
    plant: Plantable = setUpPlantForCow()

    exists = False

    for queue in jobsQueue:
        if queue.position == position:
            queue.jobsList.append(
                ScheduledJob(executed=False, function=executeScheduleCow, plant=plant, endless=True,
                             type=JobType.Cow))
            exists = True

    if not exists:
        job = ScheduledJob(executed=False, function=executeScheduleCow, plant=plant, endless=True,
                           type=JobType.Cow)
        jobList = list()
        jobList.append(job)
        cowConfig = ChickenConfig([intToStrNumber(int(user_choose))], position)
        queue = ScheduledJobQueue(jobList, position, cowConfig, JobType.Cow)
        jobsQueue.append(queue)


def showAvailableJuice():
    # TODO
    pass


def scheduleJuices():
    # TODO
    pass


def removeJobsFromQueue():
    global jobsQueue
    jobsQueue = list()


def configureStartingTime():
    driver, checkIsCorrect = login()
    driver.fullscreen_window()
    for queue in jobsQueue:
        if queue.type.Farming or queue.type.Cow or queue.type.Chicken:
            position = queue.config.position.replace('farm', '').replace('pos', '')
            try:
                timer = driver.find_element(by=By.ID, value="farm_production_timer" + position).text
            except:
                timer = "Gotowe!"

            if timer == "Gotowe!":
                queue.lastTaskEndTime = datetime.now()
            else:
                if timer[0:2] == '00':
                    hours = 0
                else:
                    hours = int(timer[0:2].lstrip("0"))
                if timer[3:5] == '00':
                    minutes = 0
                else:
                    minutes = int(timer[3:5].lstrip("0"))
                if timer[6:8] == '00':
                    seconds = 0
                else:
                    seconds = int(timer[6:8].lstrip("0"))
                queue.lastTaskEndTime = datetime.now() + timedelta(hours=hours, minutes=minutes, seconds=seconds)
        if queue.type.Juices:
            pass

    driver.close()


def executeQueue():
    configureStartingTime()

    while True:
        for queue in jobsQueue:
            if queue.jobsList[0].type == JobType.Farming and queue.lastTaskEndTime <= datetime.now():
                if queue.jobsList[0].endless:
                    job: ScheduledJob = queue.jobsList[0]
                else:
                    job: ScheduledJob = queue.jobsList.pop(0)
                logging.info(f"Executing job: {job.type.name} with plant {job.plant.name}")
                job.function(job.plant, queue.position)
                logging.info("Job executed")
                queue.lastTaskEndTime = datetime.now() + (
                    timedelta(seconds=(job.plant.plantTime * 60 * (100 - queue.config.wateringBonus)/ 100) + 5))
            elif queue.jobsList[0].type == JobType.Chicken and queue.lastTaskEndTime <= datetime.now():
                if queue.jobsList[0].endless:
                    job: ScheduledJob = queue.jobsList[0]
                else:
                    job: ScheduledJob = queue.jobsList.pop(0)
                logging.info(f"Executing job: {job.type.name} with plant {job.plant.name}")
                job.function(job.plant, queue.position)
                logging.info("Job executed")
                queue.lastTaskEndTime = datetime.now() + (timedelta(seconds=2 * 60 * 60))
            elif queue.jobsList[0].type == JobType.Cow and queue.lastTaskEndTime <= datetime.now():
                if queue.jobsList[0].endless:
                    job: ScheduledJob = queue.jobsList[0]
                else:
                    job: ScheduledJob = queue.jobsList.pop(0)
                logging.info(f"Executing job: {job.type.name} with plant {job.plant.name}")
                job.function(job.plant, queue.position)
                logging.info("Job executed")
                queue.lastTaskEndTime = datetime.now() + (timedelta(seconds=6 * 60 * 60))

        time.sleep(5)
        print("----------------Queue statuses----------------")
        for queue in jobsQueue:
            if len(queue.jobsList) < 1:
                jobsQueue.remove(queue)
            else:
                timeLeft = queue.lastTaskEndTime - datetime.now()
                if queue.jobsList[0].type == JobType.Farming:
                    print(
                        f"Queue: {queue.position} time for next task: {timeLeft} next task: {queue.jobsList[0].plant.name} endless: {queue.jobsList[0].endless} queue: {len(queue.jobsList)}")
                if queue.jobsList[0].type == JobType.Cow:
                    print(
                        f"Queue: {queue.position} time for {queue.jobsList[0].type.name}: {timeLeft} endless: {queue.jobsList[0].endless}")
                if queue.jobsList[0].type == JobType.Chicken:
                    print(
                        f"Queue: {queue.position} time for {queue.jobsList[0].type.name}: {timeLeft} endless: {queue.jobsList[0].endless}")


def executeSchedulePlant(plant: Plantable, position):
    driver, checkIsCorrect = login()
    try:
        driver.fullscreen_window()  # TODO Temp solution
        planting(position, plant, 'true', driver)
    except:
        logging.info("Exception occurred trying planting once again")
        driver.fullscreen_window()  # TODO Temp solution
        planting(position, plant, 'true', driver)
    driver.close()


def collectingEggs(position, plant, driver):
    findAndClick(driver, position)
    time.sleep(3)
    findAndClick(driver, COLLECT_BUTTON)
    time.sleep(2)

    if plant.id == "rackitem1":
        for x in range(1, 120):
            findAndClick(driver, ANIMAL_FEED_1)
            time.sleep(0.5)
    if plant.id == "rackitem2":
        for x in range(1, 60):
            findAndClick(driver, ANIMAL_FEED_2)
            time.sleep(0.5)

    time.sleep(2)
    logging.info("Zebrano jajka")


def collectingMilk(position, plant, driver):
    findAndClick(driver, position)
    time.sleep(3)
    findAndClick(driver, COLLECT_BUTTON)
    time.sleep(2)

    if plant.id == "rackitem3":
        for x in range(1, 48):
            findAndClick(driver, ANIMAL_FEED_3)
            time.sleep(0.7)
    if plant.id == "rackitem4":
        for x in range(1, 48):
            findAndClick(driver, ANIMAL_FEED_4)
            time.sleep(0.7)

    time.sleep(2)
    logging.info("Zebrano mleko")


def executeScheduleChicken(plant: Plantable, position):
    driver, checkIsCorrect = login()
    driver.fullscreen_window()  # TODO Temp solution
    collectingEggs(position, plant, driver)
    driver.close()


def executeScheduleCow(plant: Plantable, position):
    driver, checkIsCorrect = login()
    driver.fullscreen_window()  # TODO Temp solution
    collectingMilk(position, plant, driver)
    driver.close()


def closeNewsBox(driver):
    element = driver.find_element(by=By.ID, value=CLOSE_NEWSBOX)
    element.click()


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
        element.send_keys(str(write))
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
    findAndClick(window, HARVEST_ALL_BUTTON)
    time.sleep(1)
    findAndClick(window, COLLECT_BUTTON)
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
            closeNewsBox(driver)
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
    for x in field:
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
    findAndClick(window, WATER_ONE_BUTTON)
    time.sleep(0.2)
    field_number = 1
    watered_fields = 0
    for x in field:
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
            findAndClick(window, WATER_ONE_BUTTON)
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
    findAndClick(driver, EXIT_FROM_FARM_BUTTON)
    time.sleep(1)
    pass


def execute(plant):
    driver, checkIsCorrect = login()
    driver.fullscreen_window()  # TODO Temp solution
    planting(config["farm"]["one"]["position"], plant, 'true', driver)
    planting(config["farm"]["two"]["position"], plant, 'true', driver)


def manualPlanting():
    setUpPlantForFarming()
    user_input = int(input())
    plant = farmPlants[user_input - 1]
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
    with open(CONFIG_FILE_NAME, "w") as outfile:
        outfile.write(file_to_write)


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


def addJobToQueue():
    while True:
        showAvailableJobs()
        user_choose = input()
        if (user_choose == "1"):
            addPlantingJob()
        elif (user_choose == "2"):
            scheduleChicken()
        elif (user_choose == "3"):
            scheduleCow()
        elif (user_choose == "4"):
            scheduleJuices()
        elif (user_choose == "0"):
            break
        else:
            print("Zły wybór")


while True:
    logging.info("##################################")
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
