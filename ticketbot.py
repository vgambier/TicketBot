#! /usr/bin/env python3

import datetime
import json
import os
import re
import requests
import sys
import time
from random import random, choice

import selenium.webdriver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

def is_page_valid(response):
    '''Used to detect 403 (IP bans) and captcha (VPN-related suspicious traffic)'''
    al = response.text
    title = re.search('<\W*title\W*(.*)</title', al, re.IGNORECASE).group(1)
    is_valid = title.endswith('TicketSwap')
    return is_valid

def selenium_is_page_valid(browser):
    try:
        return browser.title.endswith('TicketSwap')
    except:
        return False

def get_available_proxies():
    '''Gathers and returns a list of public proxies'''
    proxies_list_params = {
        'request': 'displayproxies',
        'protocol': 'http',
        'timeout': '10000',
        'country': 'all',
        'ssl': 'all',
        'anonymity': 'all'
    }
    return requests.get('https://api.proxyscrape.com/v2/', params=proxies_list_params).text.splitlines()

def automatic_login(browser):
    try:
        with open('cookies', 'r') as f:
            for cookie in f.read().splitlines():
                browser.add_cookie(json.loads(cookie))
        browser.refresh()
        print('logged in automatically')
    except:
        print('you have 60 seconds to log in')
        print("if the page doesn't load, wait")

def write_login_cookies(browser):
    cookies = browser.get_cookies()
    with open('cookies', 'w') as f:
        for cookie in cookies:
            if cookie['name'] in ('lastLoginMethod', 'token', 'userId'):
                f.write(json.dumps(cookie) + '\n')

def need_login(browser):
    try:
        browser.find_element(By.CLASS_NAME, "css-n4f2wf")
        return False
    except:
        return True

def login(browser):
    automatic_login(browser)
    WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "css-n4f2wf"))) # wait until logged in
    write_login_cookies(browser)

def grab_ticket(browser):
    browser.execute_script("arguments[0].click();", continue_click)
    time.sleep(3)

    # add to cart
    add_cart = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "e1nefpxg2"))
    )
    add_cart.click()

    try:
        os.system("paplay /usr/share/sounds/freedesktop/stereo/complete.oga")
        os.system('notify-send -u critical "ticket has been grabbed"')
        os.system('notify-send -u critical !!!')
    except:
        print('could not play system-specific notifications')

    browser.refresh()

    print('\nat cart - you have 10 minutes to start paying!')
    if use_proxy:
        print('IMPORTANT: using a public proxy is insecure, please switch to a secure session instead of sending your credit card details into the abyss. use your phone connection, ask a friend, or reboot your router if necessary.')
        print('since you are using a public proxy, the browser will now close')
        print('go to https://www.ticketswap.com/cart')
        browser.quit()
    else:
        print('if you accidentally close your browser, just go to https://www.ticketswap.com/cart')

    try:
        for i in range(100):
            os.system("paplay /usr/share/sounds/freedesktop/stereo/phone-outgoing-busy.oga")
    except:
        print('could not play system-specific alarm')

# Initialization

REFRESH_PERIOD = 0.5 # in seconds
BASE_URL = "https://www.ticketswap.com"
DEFAULT_URL = "https://www.ticketswap.com/event/le-guess-who-2022/4-day-ticket-tickets/7a8bc49d-471d-4963-85b8-322d2fa80285/2216953"
url = sys.argv[1] if len(sys.argv) == 2 else DEFAULT_URL
available_proxies = get_available_proxies()
number_attempts = 0
use_proxy = False
session = requests.Session()
session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} # Google Chrome
browser = None

# Main loop

while True:

    # login and/or check for ban, captcha

    while need_login(browser) or browser == None or not selenium_is_page_valid(browser):
        print('finding a new connection...')
        # try to open the url without a proxy. if that fails, find a proxy that works and opens the url
        response = session.get(url)
        if is_page_valid(response):
            print('no proxy necessary!')
            options = webdriver.ChromeOptions() # remove proxy settings
            # open browser without proxy
            browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            browser.get(url)
            use_proxy = False
        else:
            print('looking for a working proxy...')
            while not is_page_valid(response):
                random_proxy = choice(available_proxies)
                proxies = {'https': f"http://{random_proxy}"}
                try:
                    session.get(url, timeout=8, proxies=proxies)
                    response = session.get(url, timeout=4, proxies=proxies) # second attempt is faster, we are less lenient
                    if is_page_valid(response):
                        print('%s seems to work!' % random_proxy)
                        # open browser with proxy
                        options = webdriver.ChromeOptions()
                        options.add_argument('--proxy-server=%s' % random_proxy)
                        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
                        browser.get(url)
                        use_proxy = True
                except:
                    pass

        number_attempts = 0
        if need_login(browser):
            # we need a try/except block because sometimes the proxy dies between the check and the login,
            # making it impossible to log in manually or automatically
            # would also crash if user takes longer than 60 seconds to log in manually
            try:
                login(browser)
            except:
                continue

    try:
        number_attempts += 1
        continue_click = browser.find_element(By.CLASS_NAME, "css-19fqo0n")
        # did not raise an error, ticket must be available
        print('ticket is here :)')
        grab_ticket(browser)
        break

    except:
        print(f"ticket is not here (attempt #{number_attempts})")
        # refresh the page until ticket is found
        time.sleep(REFRESH_PERIOD)
        browser.refresh()

# Keep script running

while True:
    time.sleep(10000)
