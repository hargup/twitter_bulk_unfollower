# Twitter/X Bulk Sorter and Unfollower

## Why did I build this?
- Twitter has a limit on the number of accounts you can follow, and I wasn't able to follow more than 5K twitter account. As a workaround, I site every once in a while, and unfollow few dozen accounts so that I can follow the new accounts I find interesting.
- I also wanted to clean my feed and only follow the accounts I care about
- And have been itching a little bit to get my hands dirty with some browser automation scripts.

## How does it work?

1. *Downloads the list of accounts you are following*

- Go to `get_follower_list.py`, update the username and password. This script will download your following list in `followers_list.txt`

2. *Get profiles data*

- Then you collect the name, description and the first two tweets for each profile in `followers_list.txt`. The output is saved in `following_data.json`

3. *Sort through the profiles*
- First copy `following_data.json` to `reviewer_frontend/data.json`
- Then `cd reviewer_frontend`
- `npm install`
- `npm run dev`
Go to `http://localhost:3000` and you'll be able to mark profiles ot unfollow by pressing `u` and profiles to keep by pressing `k`. Can sort through 500 profiles in 10 minutes.
- Click download sorted data button to get the marked profiles
 
4. *Unfollow the marked profiles in bulk*
- Run `bulk_unfollow.py` to unfollows all accounts you are following except the ones `keep_list.txt`


## How to run it on a server?
- Install `xvfb` virtual display
- Export the display env variable
- Run as speciied

## Learnings
- The fast data sorter UI is a killer. I can sort through 500 twitter profiles in 10 minutes.
- I was impressed with the ability to easily load cookies and preserve them across sessions.
- The new thing (for me) was also the ability to run the script on a server with virtual display, that means I can run the script and forget it.
- Playwright is very stable and smooth. GPT is pretty good at writing Playwright automation scripts.
