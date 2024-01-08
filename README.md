# Twitter/X Bulk Sorter and Unfollower

## Why did I build this?
- Twitter has a limit on the number of accounts you can follow, and I wasn't able to follow more than 5K twitter account. As a workaround, I site every once in a while, and unfollow few dozen accounts so that I can follow the new accounts I find interesting.
- I also wanted to clean my feed and only follow the accounts I care about
- And have been itching a little bit to get my hands dirty with some browser automation scripts.

## How does it work?

### Parts:
- `get_follower_list.py`: Downloads the list of followers
- `get_profiles_data.py`: Get the name, description and the first two tweets for each profile
- `reviewer_frontend`: A UI to rapidly mark the profiles as `keep` or `unfollow`
- `bulk_unfollow.py`: Unfollows all accounts you are following except the ones `keep_list.txt`

## How to run it on a server?
- Install `xvfb` virtual display
- Export the display env variable
- Run as speciied

## Learnings
- The fast data sorter UI is a killer. I can sort through 500 twitter profiles in 10 minutes.
- I was impressed with the ability to easily load cookies and preserve them across sessions.
- The new thing (for me) was also the ability to run the script on a server with virtual display, that means I can run the script and forget it.
- Playwright is very stable and smooth. GPT is pretty good at writing Playwright automation scripts.
