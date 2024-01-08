from playwright.sync_api import sync_playwright
import json
import os
import time


def save_cookies(page, path):
    with open(path, 'w') as f:
        json.dump(page.context.cookies(), f)

def login_and_save_cookies(twitter_username, twitter_password, cookies_path):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Go to Twitter login page
        page.goto("https://twitter.com/i/flow/login")

        # Log in to Twitter
        # <div class="css-175oi2r r-18u37iz r-16y2uox r-1wbh5a2 r-1wzrnnt r-1udh08x r-xd6kpl r-1pn2ns4 r-ttdzmv"><div dir="ltr" class="css-1rynq56 r-bcqeeo r-qvutc0 r-37j5jr r-135wba7 r-16dba41 r-1awozwy r-6koalj r-1inkyih r-13qz1uu" style="color: rgb(15, 20, 25); text-overflow: unset;"><input autocapitalize="sentences" autocomplete="username" autocorrect="on" name="text" spellcheck="true" type="text" dir="auto" class="r-30o5oe r-1dz5y72 r-13qz1uu r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-fdjqy7" value=""></div></div>
        page.fill('input[autocomplete="username"]', twitter_username)
        page.click("text='Next'")
        page.fill('input[name="password"]', twitter_password)
        time.sleep(5)

        page.click("text='Log in'")

        time.sleep(5)
        
        # page.click('div[aria-label="Reveal password"]')

        # Wait for navigation after login
        # Save cookies to a file
        save_cookies(page, cookies_path)
        time.sleep(10)


        browser.close()

def load_cookies(page, path):
    with open(path, 'r') as f:
        cookies = json.load(f)
        page.context.add_cookies(cookies)

def unfollow_visible_followers(username, cookies_path, keep_list={}):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Load cookies from the file
        load_cookies(page, cookies_path)

        # Go to the Twitter followers page
        page.goto(f"https://twitter.com/{username}/following", wait_until='load') 

        # Scroll and unfollow
        last_height = page.evaluate("() => document.body.scrollHeight")
        while True:
            elements = page.query_selector_all('div[data-testid="UserCell"]')
            for el in elements:
                username_ = el.query_selector('a[href^="/"]').get_attribute('href')
                username = username_.replace('/', '')
                print(username)
                if username in keep_list:
                    print(f'{username} is keep list, skipping')
                    continue
                followButtons = el.query_selector_all('span')
                for button in followButtons:
                    try:
                        if button.inner_text() == "Following":
                            button.click()
                            page.wait_for_timeout(2000)  # wait for the unfollow button to appear
                            page.click("text='Unfollow'")
                    except Exception as e:
                        print(f"Exception occurred: {e}")

            # Scroll down
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)  # wait for more followers to load

            # Check if the end of the page is reached
            new_height = page.evaluate("() => document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        browser.close()

def get_twitter_following(username, cookies_path):
    followers = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Load cookies from the file
        load_cookies(page, cookies_path)

        # Go to the Twitter followers page
        page.goto(f"https://twitter.com/{username}/following", wait_until='load')

        # Wait for the followers list to load
        page.wait_for_selector('div[data-testid="UserCell"]')

        # Scroll and collect followers
        last_height = page.evaluate("() => document.body.scrollHeight")
        while True:
            # Extract followers from the current view and unfollow
            elements = page.query_selector_all('div[data-testid="UserCell"]')
            new_followers = []
            for el in elements:
                followButton = el.query_selector('span:contains("Following")')
                if followButton:
                    followButton.click()
                    page.wait_for_timeout(2000)  # wait for the unfollow button to appear
                    page.click("text='Unfollow'")

                new_followers.append("https://twitter.com" + el.query_selector('a[href^="/"]').get_attribute('href'))
            followers += new_followers
            print(f'{len(followers)=}')
            print(f'First 5 followers {followers[:5]}')
            print(f'Last 5 followers {followers[-5:]}')

            # Scroll down
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)  # wait for more followers to load

            # Check if the end of the page is reached
            new_height = page.evaluate("() => document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        browser.close()

    return list(set(followers))  # Remove duplicates

# Replace 'your_twitter_username' and 'your_twitter_password' with your Twitter credentials
with open('keep_list.txt', 'r') as f:
    keep_list = set(f.read().split(','))

# if not os.path.exists('twitter_cookies.json'):
#     login_and_save_cookies('<username>', '<password>', 'twitter_cookies.json')

unfollow_visible_followers('hargup13', 'twitter_cookies.json', keep_list)
