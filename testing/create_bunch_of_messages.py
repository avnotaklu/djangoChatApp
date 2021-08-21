
import random
import string
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

no_of_tests = 1
rooms = []
for _ in range(no_of_tests):
    random_room_name = ""
    for _ in range(15):
        random_room_name += random.choice(string.ascii_letters)
    rooms.append(random_room_name)

optionsFirefox = Options()
#optionsFirefox.headless = True
driver = webdriver.Firefox(options=optionsFirefox)

def login():
    searchurl = "http://127.0.0.1:8000/accounts/login/"
    driver.get(searchurl)

    username_box = driver.find_element(By.ID,"id_username")
    username_box.click()
    username_box.send_keys('generic')

    password_box = driver.find_element(By.ID,"id_password")
    password_box.click()
    password_box.send_keys('genericpass')

    login_first_button  = driver.find_element(By.ID,"submit_login")
    login_first_button.click()
    for room in rooms:
        enter_room(room)

def enter_room(room):
    room_url = "http://127.0.0.1:8000/chat/" + room + "/"
    driver.get(room_url)
    #room_input_box      = driver.find_element(By.ID,"room-name-input")
    #room_input_box.click()
    #room_input_box.send_keys(room)

    #room_enter_button   = driver.find_element(By.ID,"room-name-submit")
    #room_enter_button.click()

    message_length = 10000
    no_of_msgs = 1000
    post_message(no_of_msgs,message_length)
    test_time(room,no_of_msgs,message_length)

def post_message(no_of_msgs,message_length):
    for _ in range(no_of_msgs):
        random_message = ""
        for _ in range(message_length):
            random_message += random.choice(string.ascii_letters)

        #print(random_message)
        #search_bar = driver.find_elements(By.CLASS_NAME,"high-rating")
        #
        message_input       = driver.find_element(By.ID,"chat-message-input")
        message_input.click()
        message_input.send_keys(random_message)
        send_message_button = driver.find_element(By.ID,"chat-message-submit")
        send_message_button.click()

def test_time(room,no_of_msgs,message_length):
    room_url = "http://127.0.0.1:8000/chat/" + room + "/"
    start_time = time.time()
    driver.get(room_url)
    end_time = time.time()
    with open("times.txt","a") as f:
        f.write("test data")
        f.write(str(no_of_msgs) + str(message_length))
        f.write(str(end_time-start_time))
        f.write("\n")

login()
driver.quit()
