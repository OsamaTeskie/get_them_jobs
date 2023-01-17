from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from getOTP import otp
from datetime import datetime
from sendEmText import sendMessage
import os


def logInAndAuth(driver, url):
    # function to login using Username and password to any TMU related service
    driver.get(url)

    # Fetch and insert the user's username and password
    driver.find_element(
        "xpath", "//input[@name='username']").send_keys(os.environ["TMU_USERNAME"])
    driver.find_element(
        "xpath", "//input[@name='password']").send_keys(os.environ["TMU_PASSWORD"])
    driver.find_element("xpath", "//input[@name='submit']").click()

    # Fetch and insert the verification code
    try:
        driver.find_element(
            "xpath", "//a[text()[contains(., 'Log in with verification code instead')]]").click()
    except:
        print("")
    driver.find_element("xpath", "//input[@name='token']").send_keys(otp())
    driver.find_element("xpath", "//input[@name='submit']").click()


def getJobs(driver):
    # Function to get jobs posted on the TMU's Co-op Portal
    # Login onto TMU's Co-op portal
    logInAndAuth(driver, "https://recruitstudents.ryerson.ca/students.htm")

    # Navigate to the main page of the job postings
    driver.find_element("xpath", "//a[text()[contains(., 'Coop')]]").click()
    driver.find_element(
        "xpath", "//a[text()[contains(., 'Job Postings')]]").click()

    # Navigate and make a new custom search since the last time logged in
    driver.find_element(
        "xpath", "//a[text()[contains(., 'Job Search')]]").click()
    driver.find_element(
        "xpath", "//input[@name='dateLiveFrom']").send_keys(lastRead().split()[0])
    driver.find_element("xpath", "//select[@name='Term']").click()
    # select the term you want to search for
    driver.find_element(
        "xpath", "//option[text()[contains(., '2023 - Summer')]]").click()
    driver.find_element("xpath", "//input[@value='16 Months']").click()
    driver.find_element("xpath", "//input[@value='12 Months']").click()
    driver.find_element("xpath", "//input[@value='8 Months']").click()
    driver.execute_script("scrollBy(0,-50);")
    driver.find_element(
        "xpath", "//a[text()[contains(., 'Search Job Postings')]]").click()

    # Get postings and send them for parsing using the parseJobs function
    postings = driver.find_element("xpath", "//span[contains(@class, 'badge badge-info')]").get_attribute("innerHTML").replace("<!--STU-0013-TST-->", "").strip()
    return parseJobs(postings, "https://recruitstudents.ryerson.ca/students.htm")


def parseJobs(postings, url):

    today = datetime.datetime.now()
    time = today.strftime("%m/%d/%Y %H:%M")
    currentDate = lastRead()

    # Update last read date
    updateLastRead()

    if int(postings) == 0:
        return f"Since {currentDate}, and as of {time}:\nThere are no new postings."
    # elif 0 < len(postings) < 10:
    #     finalText = ""
    #     for i in range(len(postings)):
    #         jobTitle = postings[i].find_elements("xpath", "//td[contains(@class, 'align--middle')]")[i].get_attribute("data-totitle")
    #         company = postings[i].find_elements("xpath", "//td[@class='orgDivTitleMaxWidth']")[i].get_attribute("data-totitle")
    #         finalText += f"{jobTitle.strip()} - {company.strip()}\n"

    #     return f"Since {currentDate}, here are the new job postings:\n{finalText}"
    else:
        return f"Since {currentDate}, there are {postings} postings available, visit:\n{url}"


def lastRead():
    # fetch the last time we fetched jobs

    with open("date.txt", "r") as file:
        return file.readline()


def updateLastRead():
    # update the new last read date

    today = datetime.datetime.now()
    d1 = today.strftime("%m/%d/%Y %H:%M")
    with open("date.txt", "w") as file:
        if lastRead() != d1:
            file.write(d1)


if __name__ == '__main__':
    import datetime
    import time
    today = datetime.datetime.now()
    d1 = today.strftime("%m/%d/%Y %H:%M")
    print("System Started...")
    print(f"Current date and time are: {d1}")

    while True:

        today = datetime.datetime.now()
        d1 = today.strftime("%m/%d/%Y %H:%M")
        # get the day and hour of day
        weekDay = datetime.datetime.today().weekday()
        dayHour = int(time.strftime("%H"))
        dayMin = int(time.strftime("%M"))
        if 0 <= weekDay <= 4 and 9 <= dayHour <= 17:
            print("------------------------------")
            try:
                option = Options()
                option.add_experimental_option("detach", False)
                # option.add_argument('headless')

                driver = webdriver.Chrome(service=Service(
                    ChromeDriverManager().install()), options=option)
                driver.maximize_window()
                sendMessage(getJobs(driver))
                driver.close()
            except:
                sendMessage("There was an error parsing.")

            print(f"Message sent on: {d1}.\nNow sleeping for 60 minutes")
        else:
            print(
                f"No messages sent\n, now sleeping for 60 minutes\ncurrent time and date are: {d1}.")

        print("------------------------------")
        # Sleep for 60 minutes
        time.sleep(3600)
