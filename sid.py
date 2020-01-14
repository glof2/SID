import praw
import usersettings as user
import requests
import json
import datetime
import sys
import os


# Using sys argv to get subreddit name
sys.argv

# Making sure imgs folder is here
try:
    os.mkdir("images")
except FileExistsError:
    pass

# Checking if user provided a subreddit name
if len(sys.argv) != 3:
    print("Wrong format. The format should be:" +
          "'sid.py subreddit_name sort_by'.")
    quit()

# Getting curent time, and making a string out of it
time_ = datetime.datetime.now().strftime("%H%M%S")


def prawsetup():
    global reddit
    reddit = praw.Reddit(client_id=user.clientid,
                         client_secret=user.clientsecret,
                         user_agent=user.useragent)

    # Printing some information to the user
    print(f"Client-id: {user.clientid}")
    print(f"Client-secret: {user.clientsecret}")
    print(f"User-agent: {user.useragent}")
    print(f"Subreddit to scan: {sys.argv[1]}")
    print(f"Post limit: {user.limit}")


def getimageurl():
    # Setting headers for requests up
    headers = {
        "User-Agent": user.useragent
    }

    #
    subreddit = reddit.subreddit(sys.argv[1])

    # Getting image urls
    print("".center(27, "-"))
    print("Grabbing subreddit links...")

    global links
    links = []

    if sys.argv[2] == "top":
        sub = subreddit.top(limit=user.limit)

    elif sys.argv[2] == "hot":
        sub = subreddit.hot(limit=user.limit)

    elif sys.argv[2] == "new":
        sub = subreddit.new(limit=user.limit)

    elif sys.argv[2] == "rising":
        sub = subreddit.rising(limit=user.limit)
    else:
        print("sort_by should be equal to top/hot/new/rising.")
        quit()

    for url in sub:
        # Getting JSON data
        res = requests.get(f"https://reddit.com/{url}/.json", headers=headers)
        data = json.loads(res.text)

        # Getting link from the JSON data
        data = data[0]["data"]["children"][0]["data"]["url"]

        # Add to the links list if supported
        if ".jpg" or ".png" in data:
            links.append(data)

        # If not supported, move to the next link
        else:
            continue

        # Print, and save each supported link
        with open(f"links{time_}.txt", "a") as f:
            f.write(f"{data}\n")
            print(data)

    print("".center(27, "-"))
    print(f"Grabbed {len(links)} links.")


def downloadimages():
    i = 0
    for link in links:
        # Get the bytes of the image
        res = requests.get(link).content

        # Save the image
        filename = f"images\\image{i}.png"
        with open(filename, "wb") as f:
            print(filename)
            f.write(res)
        i += 1


# Main code
prawsetup()
getimageurl()
downloadimages()
