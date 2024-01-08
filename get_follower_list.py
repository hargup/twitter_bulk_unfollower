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

def get_twitter_following(username, cookies_path):
    followers = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Load cookies from the file
        load_cookies(page, cookies_path)

        # Go to the Twitter followers page
        page.goto(f"https://twitter.com/{username}/following")

        # Wait for the followers list to load
        page.wait_for_selector('div[data-testid="UserCell"]')

        # Scroll and collect followers
        last_height = page.evaluate("() => document.body.scrollHeight")
        while True:
            # Extract followers from the current view
            followers += page.evaluate('''() => {
                return Array.from(document.querySelectorAll('div[data-testid="UserCell"] a[href^="/"]')).map(el => "https://twitter.com" + el.getAttribute('href'));
            }''')
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


if not os.path.exists('twitter_cookies.json'):
    login_and_save_cookies('username', 'password', 'twitter_cookies.json')

# Replace 'username' with your Twitter username
followers = get_twitter_following('username', 'twitter_cookies.json')

# Save the followers list to a file
with open('followers_list.txt', 'w') as f:
    for follower in followers:
        f.write(f"{follower}\n")

print(f"Saved {len(followers)} followers to followers_list.txt")