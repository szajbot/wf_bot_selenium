import datetime
import time

import schedule

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pyautogui
import threading
from datetime import datetime
import time


# INICJALIZACJA
pole = []
window = webdriver
i = 0
f = open("pass.txt", "r")
f.readline()
password = f.readline()
f.readline()
username = f.readline()
user_input = ""
user_choose = []
plantables = []






marchewki = ["marchewki","rackitem17",1,15]
truskawki = ["truskawki","rackitem20",1,480]
zboze = ["zboze","rackitem1",2,20]
kukurydza = ["kukurydza","rackitem2",4,45]
ogorki = ["ogorki","rackitem18",1,90]
cebula = ["cebula","rackitem22",1,500]
koniczyna = ["koniczyna","rackitem3",2,45]
pomidory = ["pomidory","rackitem21",1,600]
rzodkiewki = ["rzodkiewki","rackitem19",1,240]
szpinak = ["szpinak","rackitem23",1,800]


plantables.append(marchewki[0])
plantables.append(zboze[0])
plantables.append(kukurydza[0])
plantables.append(ogorki[0])
plantables.append(truskawki[0])
plantables.append(cebula[0])
plantables.append(koniczyna[0])
plantables.append(pomidory[0])
plantables.append(rzodkiewki[0])
plantables.append(szpinak[0])

farma1_id = "farm1_pos1"
farma2_id = "farm1_pos3"
waterall_id = "waterall"
harvestall_id = "cropall"
exit_from_farm = "gardencancel"
waterone_id = "giessen"

kurnik_id = "farm1_pos2"
kurnik_acc = "globalbox_button1"
kurnik_feed = "feed_item2_normal"

# settings
chickenCoopON = True
farm1ON = True
farm2ON = True
startingChickenCoop = True
startingFarm1 = True
startingFarm2 = True
defaultCrop = marchewki

# FUNKCJE
def findAndClick(window, id):
    try:
        find = window.find_element(by=By.ID, value=id)
        find.click()
    except:
        print("some error at: " + id)
        print(str(datetime.now().strftime("%H:%M:%S")))
        print()

def findAndClickAndWrite(window, id, write):
    try:
        find = window.find_element(by=By.ID, value=id)
        find.click()
        time.sleep(0.5)
        pyautogui.write(str(write))
        time.sleep(1)
    except:
        print("some error at: " + id)


def findAndClickAndCheck(window, id):
    try:
        find = window.find_element(by=By.ID, value=id)
        find.click()
    except:
        return False


def findAndClickNews(window, id):
    try:
        find = window.find_element(by=By.ID, value=id)
        find.click()
        return False
    except:
        return True


def login():
    check = True
    check2 = True
    check3 = True
    try:
        service = Service(executable_path="chromedriver.exe")
        window = webdriver.Chrome(service=service)
        window.get("https://www.wolnifarmerzy.pl")
        time.sleep(4)
        findAndClickAndWrite(window, "loginusername", password)
        findAndClickAndWrite(window, "loginpassword", username)
        check = findAndClickAndCheck(window, "loginbutton")
        time.sleep(4)
        news = findAndClickNews(window, "newsbox_close")

        check3 = findAndClickAndCheck(window, "rackcat1_img")
        time.sleep(0.2)
    except:
        check2 = False
    if check3 == False:
        check2 == False
    return window, check, check2


def water(user_choose, window):
    findAndClick(window, waterone_id)
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

        if(watered_fields > 4):
            findAndClick(window, waterone_id)
            watered_fields = 0
        time.sleep(0.1)
        field_number = field_number + 1
    time.sleep(1)

def plant(user_choose, window):
    findAndClick(window, choosedCrop[1])
    time.sleep(0.2)
    findAndClick(window, "rackcat1_img")
    time.sleep(0.2)
    number = 1
    for x in pole:
        if(choosedCrop[2] == 1):
            findAndClick(window, x)
        if(choosedCrop[2] == 2 and number%2 == 1):
            findAndClick(window, x)
        if(choosedCrop[2] == 4 and number%2 == 1 and number%24 < 12):
            findAndClick(window, x)
        time.sleep(0.075)
        number = number + 1
    time.sleep(1)

def harvest(window):
    time.sleep(1)
    findAndClick(window, harvestall_id)
    time.sleep(1)
    findAndClick(window, "globalbox_button1")
    time.sleep(1)

def choose(user_input):
    return {
        "1": marchewki,
        "2": zboze,
        "3": kukurydza,
        "4": ogorki,
        "5":truskawki,
        "6":cebula,
        "7":koniczyna,
        "8":pomidory,
        "9":rzodkiewki,
        "10":szpinak
    }[user_input]

def chooseFromSettings(user_input):
    return {
        "marchewki": marchewki,
        "zboze": zboze,
        "kukurydza": kukurydza,
        "ogorki": ogorki,
        "truskawki":truskawki,
        "cebula":cebula,
        "koniczyna":koniczyna,
        "pomidory":pomidory,
        "rzodkiewki":rzodkiewki,
        "szpiank":szpinak
    }[user_input]

def mainMenu():
    print("----------------WF_farm_bot----------------")
    print("1. Settings")
    print("2. Start")
    print("3. Exit")

def showPlants():
    i = 1
    for x in plantables:
        print(str(i) + ". " + x)
        i = i + 1

for x in range (1,121):
    pole.append("field"+str(x))
time.sleep(1.5)



def scheduldedPlanting(user_choose):
    window, check, check2 = login()
    while (check == False or check2 == False):
        window, check, check2 = login()



    if(farm1ON):
        findAndClick(window, farma1_id)
        harvest(window)
        plant(user_choose, window)
        water(user_choose, window)
        findAndClick(window, exit_from_farm)
        time.sleep(2)

    if(farm2ON):
        findAndClick(window, farma2_id)
        harvest(window)
        plant(user_choose, window)
        water(user_choose, window)
        findAndClick(window, exit_from_farm)
        time.sleep(2)
    print("Wykonano sadzenie: " + str(datetime.now().strftime("%H:%M:%S")))
    window.close()

def scheduldedCollecting():
    window, check, check2 = login()
    while (check == False or check2 == False):
        window, check, check2 = login()
    time.sleep(3)
    findAndClick(window, kurnik_id)
    time.sleep(3)
    findAndClick(window, kurnik_acc)
    time.sleep(2)
    for x in range(1, 30):
        findAndClick(window, kurnik_feed)
        time.sleep(0.7)
    time.sleep(2)
    print("Zebrano jajka: " + str(datetime.now().strftime("%H:%M:%S")))
    window.close()

def scheduldedTiming():
    print("Time for next job: ")
    print(str(schedule.idle_seconds()))






# DOBRE TO DZIALA
def showSettings():
    print()
    print()
    print()
    print("Your current settings:")
    print("1. chickenCoopON: " + str(chickenCoopON))
    print("2. farm1ON: " + str(farm1ON))
    print("3. farm2ON: " + str(farm2ON))
    print("4. startingChickenCoop: " + str(startingChickenCoop))
    print("5. startingFarm1: " + str(startingFarm1))
    print("6. startingFarm2: " + str(startingFarm2))
    print("7. default crop: " + str(choosedCrop[0]))
    print("8. exit")

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
    if(userChoose == "4"):
        global startingChickenCoop
        startingChickenCoop = not startingChickenCoop
    if(userChoose == "5"):
        global startingFarm1
        startingFarm1 = not startingFarm1
    if(userChoose == "6"):
        global startingFarm2
        startingFarm2 = not startingFarm2
    if(userChoose == "7"):
        showPlants()
        user_input = input()
        global choosedCrop
        choosedCrop = choose(str(user_input))
        global defaultCrop
        defaultCrop = choosedCrop


def stringToBoolean(string):
    if string == "False":
        return False
    else:
        return True


def loadSettings():
    settingsFile = open("settings.txt", "r")
    settingsFile.readline()

    global chickenCoopON
    chickenCoopON = stringToBoolean(settingsFile.readline().strip())
    global farm1ON
    farm1ON = stringToBoolean(settingsFile.readline().strip())
    global farm2ON
    farm2ON = stringToBoolean(settingsFile.readline().strip())
    global startingChickenCoop
    startingChickenCoop = stringToBoolean(settingsFile.readline().strip())
    global startingFarm1
    startingFarm1 = stringToBoolean(settingsFile.readline().strip())
    global startingFarm2
    startingFarm2 = stringToBoolean(settingsFile.readline().strip())
    settingsFile.readline()
    x = settingsFile.readline().strip()
    global defaultCrop
    defaultCrop = chooseFromSettings(x)
    global choosedCrop
    choosedCrop = defaultCrop
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
    global startingChickenCoop
    settingFile.writelines(str(startingChickenCoop)+ "\n")
    global startingFarm1
    settingFile.writelines(str(startingFarm1)+ "\n")
    global startingFarm2
    settingFile.writelines(str(startingFarm2)+ "\n")
    settingFile.writelines("#default crop\n")
    global defaultCrop
    settingFile.writelines(str(defaultCrop[0])+ "\n")
    settingFile.close()

def showSaveOption():
    print("Do you want to save settings?")
    print("1. Yes")
    print("2. No")




loadSettings()
while True:
    mainMenu()
    user_choose = input()
    if (user_choose == "1"):
        while(user_choose != "8"):
            showSettings()
            user_choose = input()
            changeSettings(user_choose)
        showSaveOption()
        user_choose = input()
        if (user_choose == "1"):
            saveSettings()
    elif (user_choose == "2"):
        if(startingFarm1 and startingFarm2):
            scheduldedPlanting(choosedCrop)
        if(startingChickenCoop):
            scheduldedCollecting()
        if(farm1ON or farm2ON):
            schedule.every((choosedCrop[3])*0.95).minutes.do(scheduldedPlanting,user_choose = choosedCrop )
        if(chickenCoopON):
            schedule.every(125).minutes.do(scheduldedCollecting)
        i = 0
        while True:
            if i > 10:
                seconds = schedule.idle_seconds()
                minutes = seconds/60
                minutes = int(minutes)
                seconds = seconds - (60*minutes)
                print("Do następnego zadania zostało: " + str(minutes) + " minut i " + str(int(seconds)) + " sekund")
                i = 0
            schedule.run_pending()
            i = i + 1
            time.sleep(5)
    elif(user_choose == "3"):
        exit(1)
    else:
        print("Zly wybor")

