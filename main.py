import datetime
import logging
from typing import Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from datetime import datetime, timedelta
from selenium import webdriver
import pyautogui
import json
import time
from enum import Enum

from settings.logging_config import LoggingConfig

LoggingConfig(logging)

from settings.login import (
    PASSWORD,
    LOGIN,
    SERVER
)


class JobType(Enum):
    Farming = 1
    Cow = 2
    Chicken = 3
    Juices = 4


class Plantable:
    def __init__(self, name, id, size, plantTime):
        self.name = name
        self.id = id
        self.size = size
        self.plantTime = plantTime

class Juice:
    def __init__(self, name, id, jobTime):
        self.name = name
        self.id = id
        self.jobTime = jobTime


class ScheduledJob:
    def __init__(self, executed: bool, function, endless: bool, type: JobType, plant: Plantable = None, juice: Juice = None):
        self.executed = executed
        self.endless = endless
        self.function = function
        self.plant = plant
        self.juice = juice
        self.type = type


class ScheduledJobQueue:
    def __init__(self, jobsList: list[ScheduledJob], position):
        self.jobsList = jobsList
        self.position = position
        self.lastTaskTime = datetime.now()


# INICJALIZACJA
window = webdriver
user_choose = []
user_input = ""
juices = []
farmPlants = []
chickenPlants = []
cowPlants = []
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

juices.append(Juice("Sok marchwiowy", "foodworld_selection_item130", 180))
juices.append(Juice("Sok pomidorowy", "foodworld_selection_item131", 180))
juices.append(Juice("Mleko truskawkowe", "foodworld_selection_item132", 90))
juices.append(Juice("Mleko rzodkiewkowe", "foodworld_selection_item134", 90))

# name, id, size, plant time
farmPlants.append(Plantable("Marchewki", "rackitem17", 1, 15))
farmPlants.append(Plantable("Truskawki", "rackitem20", 1, 480))
farmPlants.append(Plantable("Zboze", "rackitem1", 2, 20))
farmPlants.append(Plantable("Kukurydza", "rackitem2", 4, 45))
farmPlants.append(Plantable("Ogorki", "rackitem18", 1, 90))
farmPlants.append(Plantable("Cebule", "rackitem22", 1, 500))
farmPlants.append(Plantable("Koniczyna", "rackitem3", 2, 45))
farmPlants.append(Plantable("Pomidory", "rackitem21", 1, 600))
farmPlants.append(Plantable("Rzodkiewki", "rackitem19", 1, 240))
farmPlants.append(Plantable("Szpinak", "rackitem23", 1, 800))
farmPlants.append(Plantable("Kalafiory", "rackitem24", 1, 720))
farmPlants.append(Plantable("Rzepak", "rackitem4", 4, 90))

chickenPlants.append(Plantable("Zboze", "rackitem1", 2, 20))
chickenPlants.append(Plantable("Kukurydza", "rackitem2", 4, 45))

cowPlants.append(Plantable("Koniczyna", "rackitem3", 2, 45))
cowPlants.append(Plantable("Rzepak", "rackitem4", 4, 90))


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


def showAvailableJobs():
    print("----------------Schedule Job----------------")
    print("1. Planting")
    print("2. Chicken")
    print("3. Cow")
    print("4. Juices")
    pass


def showCurrentQueue():
    print("----------------Queue statuses----------------")
    for queue in jobsQueue:
        print(f'Queue: {queue.position}')
        for job in queue.jobsList:
            print(f'Job: {job.plant.name} endless: {job.endless}')
        print("\n")


def showAvailableFarms():
    for x in range(int(config["farm"]["counter"])):
        print(f'Option {x + 1}: position: {config["farm"][intToStrNumber(x + 1)]}')


def showAvailableChciken():
    for x in range(int(config["chicken"]["counter"])):
        print(f'Option {x + 1}: position: {config["chicken"][intToStrNumber(x + 1)]}')


def showAvailableCow():
    for x in range(int(config["cow"]["counter"])):
        print(f'Option {x + 1}: position: {config["cow"][intToStrNumber(x + 1)]}')


def addEndlessJobToQueue():
    showAvailableFarms()
    user_choose = input()
    position = config["farm"][intToStrNumber(int(user_choose))]["position"]
    plant: Plantable = setUpPlantForFarming()

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
        queue = ScheduledJobQueue(jobList, position)
        jobsQueue.append(queue)


def schedulePlanting():
    showAvailableFarms()
    user_choose = input()
    position = config["farm"][intToStrNumber(int(user_choose))]["position"]
    plant: Plantable = setUpPlantForFarming()

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
        queue = ScheduledJobQueue(jobList, position)
        jobsQueue.append(queue)


def setUpPlantForChciken():
    print("What would you like to plant?")
    i = 0

    for i in range(len(chickenPlants)):
        print(
            f'Opcja nr {i + 1}, {chickenPlants[i].name}')
    user_input = int(input()) - 1
    return chickenPlants[user_input]


def setUpPlantForCow():
    print("What would you like to plant?")
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
        queue = ScheduledJobQueue(jobList, position)
        print("Time in minutes for finish chicken (0 if null)")
        user_input = int(input())
        queue.lastTaskTime = datetime.now() - (timedelta(hours=2) - timedelta(minutes=user_input))
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
        queue = ScheduledJobQueue(jobList, position)
        print("Time in minutes for finish cow (0 if null)")
        user_input = int(input())
        queue.lastTaskTime = datetime.now() - (timedelta(hours=6) - timedelta(minutes=user_input))
        jobsQueue.append(queue)


def showAvailableJuice():
    pass


def scheduleJuices():
    pass
    # showAvailableJuice()
    # user_choose = input()
    # position = 'JuiceStand'
    # juice: Juice = setUpJuice()
    #
    # exists = False
    #
    # for queue in jobsQueue:
    #     if queue.position == position:
    #         queue.jobsList.append(
    #             ScheduledJob(executed=False, function=executeScheduleCow, plant=plant, endless=False,
    #                          type=JobType.Cow))
    #         exists = True
    #
    # if not exists:
    #     job = ScheduledJob(executed=False, function=executeScheduleCow, plant=plant, endless=False,
    #                        type=JobType.Cow)
    #     jobList = list()
    #     jobList.append(job)
    #     queue = ScheduledJobQueue(jobList, position)
    #     print("Time in minutes for finish juiceStand work (0 if null)")
    #     user_input = int(input())
    #     queue.lastTaskTime = datetime.now() - (timedelta(hours=6) - timedelta(minutes=user_input))
    #     jobsQueue.append(queue)


def addJobToQueue():
    showAvailableJobs()
    user_choose = input()
    if (user_choose == "1"):
        schedulePlanting()
    elif (user_choose == "2"):
        scheduleChicken()
    elif (user_choose == "3"):
        scheduleCow()
    elif (user_choose == "4"):
        scheduleJuices()
    else:
        print("Zły wybór")


def removeJobsFromQueue():
    global jobsQueue
    jobsQueue = list()


def executeQueue():
    # immediately perform tasks from first position in queue
    for queue in jobsQueue:
        if queue.jobsList[0].type == JobType.Farming:
            if queue.jobsList[0].endless:
                job: ScheduledJob = queue.jobsList[0]
            else:
                job: ScheduledJob = queue.jobsList.pop(0)
            logging.info(f"Executing job: {job.type.name} with plant {job.plant.name}")
            job.function(job.plant, queue.position)
            logging.info("Job executed")
            queue.lastTaskTime = datetime.now()

    while True:
        for queue in jobsQueue:
            timePassed = datetime.now() - queue.lastTaskTime
            if queue.jobsList[0].type == JobType.Farming and timePassed.seconds >= (queue.jobsList[0].plant.plantTime * 60 * 0.95):
                if queue.jobsList[0].endless:
                    job: ScheduledJob = queue.jobsList[0]
                else:
                    job: ScheduledJob = queue.jobsList.pop(0)
                logging.info(f"Executing job: {job.type.name} with plant {job.plant.name}")
                job.function(job.plant, queue.position)
                logging.info("Job executed")
                queue.lastTaskTime = datetime.now()
            elif queue.jobsList[0].type == JobType.Chicken and timePassed.seconds >= (2 * 60 * 60):
                if queue.jobsList[0].endless:
                    job: ScheduledJob = queue.jobsList[0]
                else:
                    job: ScheduledJob = queue.jobsList.pop(0)
                logging.info(f"Executing job: {job.type.name} with plant {job.plant.name}")
                job.function(job.plant, queue.position)
                logging.info("Job executed")
                queue.lastTaskTime = datetime.now()
            elif queue.jobsList[0].type == JobType.Cow and timePassed.seconds >= (6 * 60 * 60):
                if queue.jobsList[0].endless:
                    job: ScheduledJob = queue.jobsList[0]
                else:
                    job: ScheduledJob = queue.jobsList.pop(0)
                logging.info(f"Executing job: {job.type.name} with plant {job.plant.name}")
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
                if queue.jobsList[0].type == JobType.Farming:
                    timeLeft = (queue.jobsList[0].plant.plantTime * 60 * 0.97) - timePassed.seconds
                    print(f"Queue: {queue.position} time for next task: {timeLeft} next task: {queue.jobsList[0].plant.name} endless: {queue.jobsList[0].endless} queue: {len(queue.jobsList)}")
                if queue.jobsList[0].type == JobType.Cow:
                    timeLeft = (6 * 60 * 60) - timePassed.seconds
                    print(f"Queue: {queue.position} time for {queue.jobsList[0].type.name}: {timeLeft} endless: {queue.jobsList[0].endless}")
                if queue.jobsList[0].type == JobType.Chicken:
                    timeLeft = (2 * 60 * 60) - timePassed.seconds
                    print(f"Queue: {queue.position} time for {queue.jobsList[0].type.name}: {timeLeft} endless: {queue.jobsList[0].endless}")



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


def collectingEggs(position, plant, driver):
    findAndClick(driver, position)
    time.sleep(3)
    findAndClick(driver, animalCollect)
    time.sleep(2)

    if plant.id == "rackitem1":
        for x in range(1, 60):
            findAndClick(driver, animalFeed1)
            time.sleep(0.5)
    if plant.id == "rackitem2":
        for x in range(1, 30):
            findAndClick(driver, animalFeed2)
            time.sleep(0.5)

    time.sleep(2)
    logging.info("Zebrano jajka")


def collectingMilk(position, plant, driver):
    findAndClick(driver, position)
    time.sleep(3)
    findAndClick(driver, animalCollect)
    time.sleep(2)

    if plant.id == "rackitem3":
        for x in range(1, 48):
            findAndClick(driver, animalFeed3)
            time.sleep(0.7)
    if plant.id == "rackitem4":
        for x in range(1, 48):
            findAndClick(driver, animalFeed4)
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


def setUpPlantForFarming() -> Plantable:
    print("What would you like to plant?")
    i = 0
    for i in range(len(farmPlants)):
        print(
            f'Opcja nr {i + 1}, {farmPlants[i].name}: rozmiar: {farmPlants[i].size} czas do zbioru: {farmPlants[i].plantTime}')
    user_input = int(input()) - 1
    return farmPlants[user_input]


def execute(plant):
    driver, checkIsCorrect = login()
    driver.fullscreen_window()  # TODO Temp solution
    planting(config["farm"]["one"]["position"], plant, 'true', driver)
    planting(config["farm"]["two"]["position"], plant, 'true', driver)


def manualPlanting():
    plant: Plantable = setUpPlantForFarming()
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
