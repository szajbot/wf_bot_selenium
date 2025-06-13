import datetime
import schedule
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pyautogui
from datetime import datetime
import time


# INICJALIZACJA
pole = []
window = webdriver
i = 0
user_input = ""
user_choose = []
plantables = []
queue = []

# WCZYTYWANIE HASLA
f = open("../settings/params.py", "r")
f.readline()
password = f.readline()
f.readline()
username = f.readline()
f.close()

marchewki = ["marchewki","rackitem17",1,15]
truskawki = ["truskawki","rackitem20",1,480]
zboze = ["zboze","rackitem1",2,20]
kukurydza = ["kukurydza","rackitem2",4,45]
ogorki = ["ogorki","rackitem18",1,90]
cebule = ["cebule", "rackitem22", 1, 500]
koniczyna = ["koniczyna","rackitem3",2,45]
pomidory = ["pomidory","rackitem21",1,600]
rzodkiewki = ["rzodkiewki","rackitem19",1,240]
szpinak = ["szpinak","rackitem23",1,800]
kalafiory = ["kalafiory", "rackitem24", 1, 720]
rzepak = ["rzepak","rackitem4",4,90]

plantables.append(marchewki[0])
plantables.append(zboze[0])
plantables.append(kukurydza[0])
plantables.append(ogorki[0])
plantables.append(truskawki[0])
plantables.append(cebule[0])
plantables.append(koniczyna[0])
plantables.append(pomidory[0])
plantables.append(rzodkiewki[0])
plantables.append(szpinak[0])
plantables.append(kalafiory[0])
plantables.append(rzepak[0])

farmOnePosition = "farm1_pos1"
farmTwoPosition = "farm1_pos3"
waterAllButton = "waterall"
harvestAllButton = "cropall"
exitFromFarmButton = "gardencancel"
waterOneButton = "giessen"

chickenCoopPosition = "farm1_pos2"
cowPossition = "farm1_pos4"

animalCollect = "globalbox_button1"
animalFeed1 = "feed_item1_normal"
animalFeed2 = "feed_item2_normal"
animalFeed3 = "feed_item3_normal"
animalFeed4 = "feed_item4_normal"


#DEFAULT SETTINGS
chickenCoopON = True
farm1ON = True
farm2ON = True
cowON = True
startingChickenCoop = True
startingFarm1 = True
startingFarm2 = True
startingCow = True
defaultCrop = marchewki

# FUNKCJE
def findAndClick(window, id):
    try:
        find = window.find_element(by=By.ID, value=id)
        find.click()
    except:
        None

def findAndClickAndShowErrorTime(window, id):
    try:
        find = window.find_element(by=By.ID, value=id)
        find.click()
    except:
        print("some error at: " + id)
        print(str(datetime.now().strftime("%H:%M:%S")))

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


def showMainMenu():
    print("----------------WF_farm_bot----------------")
    print("1. Settings")
    print("2. Start")
    print("3. Exit")
    print("4. Queue")


def showPlants():
    i = 1
    for x in plantables:
        print(str(i) + ". " + x)
        i = i + 1


def showSaveOption():
    print("Do you want to save settings?")
    print("1. Yes")
    print("2. No")


def showSettings():
    print()
    print()
    print("Your current settings:")
    print("1. chickenCoopON: " + str(chickenCoopON))
    print("2. farm1ON: " + str(farm1ON))
    print("3. farm2ON: " + str(farm2ON))
    print("4. cowOn: " + str(cowON))
    print("5. startingChickenCoop: " + str(startingChickenCoop))
    print("6. startingFarm1: " + str(startingFarm1))
    print("7. startingFarm2: " + str(startingFarm2))
    print("8. startingCow: " + str(startingCow))
    print("9. default crop: " + str(defaultCrop[0]))
    print("10. exit")


def scheduldedTiming():
    print("Time for next job: ")
    print(str(schedule.idle_seconds()))


def stringToBoolean(string):
    if string == "False":
        return False
    else:
        return True


def login():
    checkIsCorrect = True
    try:
        service = Service(executable_path="../chromedriver.exe")
        window = webdriver.Chrome(service=service)
        window.get("https://www.wolnifarmerzy.pl")
        time.sleep(4)
        findAndClickAndWrite(window, "loginusername", password)
        findAndClickAndWrite(window, "loginpassword", username)
        # findAndClickAndShowErrorTime(window, "loginbutton")
        time.sleep(4)
        for i in range(3):
            findAndClick(window, "newsbox_close")
        checkIsCorrect = findAndClickAndCheck(window, "rackcat1_img")
        time.sleep(0.2)
    except:
        checkIsCorrect = False
    return window, checkIsCorrect


def stringToCrop(user_input):
    return {
        "marchewki": marchewki,
        "zboze": zboze,
        "kukurydza": kukurydza,
        "ogorki": ogorki,
        "truskawki":truskawki,
        "cebula":cebule,
        "koniczyna":koniczyna,
        "pomidory":pomidory,
        "rzodkiewki":rzodkiewki,
        "szpinak":szpinak,
        "kalafior": kalafiory,
        "rzepak":rzepak,
    }[user_input]


def numberToCrop(user_input):
    return {
        "1": marchewki,
        "2": zboze,
        "3": kukurydza,
        "4": ogorki,
        "5":truskawki,
        "6":cebule,
        "7":koniczyna,
        "8":pomidory,
        "9":rzodkiewki,
        "10":szpinak,
        "11":kalafiory,
        "12":rzepak,
    }[user_input]


def changeSettings(userChoose):
    if(userChoose == "1"):
        global chickenCoopON
        chickenCoopON = not chickenCoopON
    if(userChoose == "2"):
        global farm1ON
        farm1ON = not farm1ON
    if(userChoose == "3"):
        global farm2ON
        farm2ON = not farm2ON
    if (userChoose == "4"):
        global cowON
        cowON = not cowON
    if(userChoose == "5"):
        global startingChickenCoop
        startingChickenCoop = not startingChickenCoop
    if(userChoose == "6"):
        global startingFarm1
        startingFarm1 = not startingFarm1
    if(userChoose == "7"):
        global startingFarm2
        startingFarm2 = not startingFarm2
    if (userChoose == "8"):
        global startingCow
        startingCow = not startingCow
    if(userChoose == "9"):
        showPlants()
        user_input = input()
        global defaultCrop
        defaultCrop = numberToCrop(str(user_input))
        # global defaultCrop
        # defaultCrop = choosedCrop


def loadSettings():
    settingsFile = open("settings.txt", "r")
    settingsFile.readline()

    global chickenCoopON
    chickenCoopON = stringToBoolean(settingsFile.readline().strip())
    global farm1ON
    farm1ON = stringToBoolean(settingsFile.readline().strip())
    global farm2ON
    farm2ON = stringToBoolean(settingsFile.readline().strip())
    global cowON
    cowON = stringToBoolean(settingsFile.readline().strip())
    global startingChickenCoop
    startingChickenCoop = stringToBoolean(settingsFile.readline().strip())
    global startingFarm1
    startingFarm1 = stringToBoolean(settingsFile.readline().strip())
    global startingFarm2
    startingFarm2 = stringToBoolean(settingsFile.readline().strip())
    global startingCow
    startingCow = stringToBoolean(settingsFile.readline().strip())

    settingsFile.readline()
    x = settingsFile.readline().strip()
    global defaultCrop
    defaultCrop = stringToCrop(x)
    # global choosedCrop
    # choosedCrop = defaultCrop
    settingsFile.close()


def saveSettings():
    settingFile = open("settings.txt", "w")
    settingFile.write("#STARTING PROGRAM PARAM\n")
    global chickenCoopON
    settingFile.writelines(str(chickenCoopON) + "\n")
    global farm1ON
    settingFile.writelines(str(farm1ON)+ "\n")
    global farm2ON
    settingFile.writelines(str(farm2ON)+ "\n")
    global cowON
    settingFile.writelines(str(cowON) + "\n")
    global startingChickenCoop
    settingFile.writelines(str(startingChickenCoop)+ "\n")
    global startingFarm1
    settingFile.writelines(str(startingFarm1)+ "\n")
    global startingFarm2
    settingFile.writelines(str(startingFarm2)+ "\n")
    global startingCow
    settingFile.writelines(str(startingCow) + "\n")

    settingFile.writelines("#default crop\n")
    global defaultCrop
    settingFile.writelines(str(defaultCrop[0])+ "\n")
    settingFile.close()


def water(user_choose, window):
    findAndClick(window, waterOneButton)
    time.sleep(1)
    field_number = 1
    watered_fields = 0
    for x in pole:
        if (user_choose[2] == 1):
            findAndClick(window, x)
            watered_fields = watered_fields + 1
        if (user_choose[2] == 2 and field_number % 2 == 1):
            findAndClick(window, x)
            watered_fields = watered_fields + 1
        if (user_choose[2] == 4 and field_number % 2 == 1 and field_number % 24 < 12):
            findAndClick(window, x)
            watered_fields = watered_fields + 1
        if(watered_fields > 5):
            findAndClick(window, waterOneButton)
            watered_fields = 0
        time.sleep(0.1)
        field_number = field_number + 1
    time.sleep(1)


def plant(defaultCrop, window):
    findAndClick(window, defaultCrop[1])
    time.sleep(0.2)
    findAndClick(window, "rackcat1_img")
    time.sleep(0.2)
    number = 1
    for x in pole:
        if(defaultCrop[2] == 1):
            findAndClick(window, x)
        if(defaultCrop[2] == 2 and number%2 == 1):
            findAndClick(window, x)
        if(defaultCrop[2] == 4 and number%2 == 1 and number%24 < 12):
            findAndClick(window, x)
        time.sleep(0.075)
        number = number + 1
    time.sleep(1)


def harvest(window):
    time.sleep(1)
    findAndClick(window, harvestAllButton)
    time.sleep(1)
    findAndClick(window, "globalbox_button1")
    time.sleep(1)


def scheduldedPlanting(defaultCrop):
    window, checkIsCorrect= login()
    while (checkIsCorrect == False):
        window, checkIsCorrect = login()

    if(farm1ON):
        findAndClick(window, farmOnePosition)
        harvest(window)
        plant(defaultCrop, window)
        water(defaultCrop, window)
        findAndClick(window, exitFromFarmButton)
        time.sleep(2)

    if(farm2ON):
        findAndClick(window, farmTwoPosition)
        harvest(window)
        plant(defaultCrop, window)
        water(defaultCrop, window)
        findAndClick(window, exitFromFarmButton)
        time.sleep(2)
    print("Wykonano sadzenie: " + str(datetime.now().strftime("%H:%M:%S")))
    window.close()


def scheduldedCollectingEggs():
    window, checkIsCorrect = login()
    while (checkIsCorrect == False):
        window, checkIsCorrect = login()
    time.sleep(3)
    findAndClick(window, chickenCoopPosition)
    time.sleep(3)
    findAndClick(window, animalCollect)
    time.sleep(2)
    for x in range(1, 30):
        findAndClick(window, animalFeed2)
        time.sleep(0.7)
    time.sleep(2)
    print("Zebrano jajka: " + str(datetime.now().strftime("%H:%M:%S")))
    window.close()

def scheduldedCollectingMilk():
    window, checkIsCorrect = login()
    while (checkIsCorrect == False):
        window, checkIsCorrect = login()
    time.sleep(3)
    findAndClick(window, cowPossition)
    time.sleep(3)
    findAndClick(window, animalCollect)
    time.sleep(2)
    for x in range(1, 48):
        findAndClick(window, animalFeed3)
        time.sleep(0.7)
    time.sleep(2)
    print("Zebrano mleko: " + str(datetime.now().strftime("%H:%M:%S")))
    window.close()


def startProgram():
    if (startingFarm1 and startingFarm2):
        scheduldedPlanting(defaultCrop)
    if (startingChickenCoop):
        scheduldedCollectingEggs()
    if (startingCow):
        scheduldedCollectingMilk()
    if (farm1ON or farm2ON):
        schedule.every(int((defaultCrop[3]) * 0.95)).minutes.do(scheduldedPlanting, user_choose=defaultCrop)
    if (chickenCoopON):
        schedule.every(125).minutes.do(scheduldedCollectingEggs)
    if (cowON):
        schedule.every(375).minutes.do(scheduldedCollectingMilk)
    i = 0
    while True:
        if i > 10:
            seconds = schedule.idle_seconds()
            minutes = seconds / 60
            minutes = int(minutes)
            seconds = seconds - (60 * minutes)
            print("Do następnego zadania zostało: " + str(minutes) + " minut i " + str(int(seconds)) + " sekund")
            i = 0
        schedule.run_pending()
        i = i + 1
        time.sleep(5)


def settingsMenu():
    showSettings()
    user_choose = input()
    while (user_choose != "10"):
        changeSettings(user_choose)
        showSettings()
        user_choose = input()
    showSaveOption()
    user_choose = input()
    if (user_choose == "1"):
        saveSettings()


def loadQueue():
    with open("queue.txt") as file:
        for line in file:
            queue.append(line.replace("\n", ""))

def queueScheduldedPlanting(crop):
    if len(queue) > 1:
        f = queue.pop(0)
    else:
        f = queue[0]
    f = stringToCrop(f)
    window, checkIsCorrect = login()
    while (checkIsCorrect == False):
        window, checkIsCorrect = login()

    if (farm1ON):
        findAndClick(window, farmOnePosition)
        harvest(window)
        plant(crop, window)
        water(crop, window)
        findAndClick(window, exitFromFarmButton)
        time.sleep(2)

    if (farm2ON):
        findAndClick(window, farmTwoPosition)
        harvest(window)
        plant(crop, window)
        water(crop, window)
        findAndClick(window, exitFromFarmButton)
        time.sleep(2)
    print("Wykonano sadzenie: " + crop[0] + str(datetime.now().strftime("%H:%M:%S")))
    window.close()

    schedule.every(int((crop[3])*0.95)).minutes.do(queueScheduldedPlanting, crop = f)
    return schedule.CancelJob

def queueScheduldedPlantingFirst(crop):
    window, checkIsCorrect = login()
    while (checkIsCorrect == False):
        window, checkIsCorrect = login()

    if (farm1ON):
        findAndClick(window, farmOnePosition)
        harvest(window)
        plant(crop, window)
        water(crop, window)
        findAndClick(window, exitFromFarmButton)
        time.sleep(2)

    if (farm2ON):
        findAndClick(window, farmTwoPosition)
        harvest(window)
        plant(crop, window)
        water(crop, window)
        findAndClick(window, exitFromFarmButton)
        time.sleep(2)
    print("Wykonano sadzenie: " + crop[0] + str(datetime.now().strftime("%H:%M:%S")))
    window.close()


def queueProgram():
    loadQueue()
    if (startingFarm1 and startingFarm2):
        f = queue.pop(0)
        f = stringToCrop(f)
        queueScheduldedPlantingFirst(f)
    if (startingChickenCoop):
        scheduldedCollectingEggs()
    if (startingCow):
        scheduldedCollectingMilk()
    if (farm1ON or farm2ON):
        g = queue.pop(0)
        g = stringToCrop(g)
        schedule.every(int((f[3])*0.95)).minutes.do(queueScheduldedPlanting, crop=g)
    if (chickenCoopON):
        schedule.every(125).minutes.do(scheduldedCollectingEggs)
    if (cowON):
        schedule.every(375).minutes.do(scheduldedCollectingMilk)
    i = 0
    while True:
        if i > 10:
            seconds = schedule.idle_seconds()
            minutes = seconds / 60
            minutes = int(minutes)
            seconds = seconds - (60 * minutes)
            print("Do następnego zadania zostało: " + str(minutes) + " minut i " + str(int(seconds)) + " sekund")
            i = -40
        schedule.run_pending()
        i = i + 1
        time.sleep(6)

for x in range (1,121):
    pole.append("field"+str(x))
time.sleep(1.5)

loadSettings()





while True:
    showMainMenu()
    user_choose = input()
    if (user_choose == "1"):
        settingsMenu()
    elif (user_choose == "2"):
        startProgram()
    elif(user_choose == "3"):
        exit(1)
    elif(user_choose == "4"):
        queueProgram()
    else:
        print("Zly wybor")

