from playwright.sync_api import sync_playwright
import json
import os
import time
from threading import Lock
from concurrent.futures import ThreadPoolExecutor


def load_cookies(page, path):
    with open(path, 'r') as f:
        cookies = json.load(f)
        page.context.add_cookies(cookies)


# This should be named get_profile_data
def save_profile_data(username, cookies_path):
    profile_data = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        # browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        # Load cookies from the file
        load_cookies(page, cookies_path)

        # Go to the Twitter profile page
        page.goto(f"https://twitter.com/{username}", wait_until='load')

        # Wait for the profile data to load
        page.wait_for_selector('div[data-testid="UserCell"]')

        # Extract profile data
        profile_data['name'] = page.evaluate('''() => {
            return document.querySelector('div[data-testid="UserName"] div[dir="ltr"] span').innerText;
        }''')
        profile_data['username'] = username
        profile_data['profile_picture_link'] = page.evaluate('''() => {
            return document.querySelector('div[data-testid="UserCell"] a[href^="/"] img').src;
        }''')
        # Wait for the description to load
        try:
            page.wait_for_selector('div[data-testid="UserDescription"]', timeout=1000)
            profile_data['description'] = page.evaluate('''() => {
                return document.querySelector('div[data-testid="UserDescription"]').innerText;
            }''')
        except:
            print('Couldnt find user description, keeping it empty')
            profile_data['description'] = ""
        try:
             # Wait for the tweets to load
            # Extract the first two tweets
            page.wait_for_selector('div[data-testid="tweetText"]', timeout=1000)
            profile_data['first_two_tweets'] = page.evaluate('''() => {
                const tweets = Array.from(document.querySelectorAll('div[data-testid="tweetText"]'), el => el.innerText);
                return tweets.length > 0 ? tweets.slice(0, 2) : ["No tweets available"];
            }''')
        except:
            print('Couldnt find first two tweets, keeping it empty')
            profile_data['first_two_tweets'] = []
        

        browser.close()

    return profile_data


def save_data(username, lock):
    try:
        data = save_profile_data(username, 'twitter_cookies.json')
    except Exception as e:
        # Probably not a good idea
        print(f"Error in save_profile_data: {e}")
        data = {}
    lock.acquire()
    try:
        try:
            with open('following_data.json', 'r') as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = {}

        existing_data[username] = data

        with open('following_data.json', 'w') as f:
            json.dump(existing_data, f)
    finally:
        lock.release()


def process_following_list():
    with open('following_list.txt', 'r') as f:
        usernames = [line.replace('https://twitter.com/', '').strip() for line in f]
    if not os.path.exists('following_data.json'):
        with open('following_data.json', 'w') as f:
            pass

    with open('following_data.json', 'r') as f:
        processed_usernames = list(json.load(f).keys())

    usernames = [username for username in usernames if username not in processed_usernames]
    print(f'Number of usernames to process = {len(usernames)}')

    lock = Lock()

    for username in usernames:
        print(f'gettin data for {username}')
        save_data(username, lock)
        # executor.submit(save_data, username)
        time.sleep(0.3)

process_following_list()