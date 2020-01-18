import praw
import requests
import json
import datetime
import os
import usersettings as user


class ImageDownload():
    # INIT
    def __init__(self):
        self.time = datetime.datetime.now().strftime("%H%M%S")

        self.headers = {
            "User-Agent": user.useragent
        }

    # GETIMAGEURL
    def getimageurl(self, clientid="", clientsecret="", useragent="", limit="",
                    subred="", sortby="", saveurls=True):

        reddit = praw.Reddit(client_id=clientid,
                             client_secret=clientsecret,
                             user_agent=useragent)

        subreddit = reddit.subreddit(subred)

        links = []

        if sortby == "top":
            sub = subreddit.top(limit=limit)

        elif sortby == "hot":
            sub = subreddit.hot(limit=limit)

        elif sortby == "new":
            sub = subreddit.new(limit=limit)

        elif sortby == "rising":
            sub = subreddit.rising(limit=limit)
        else:
            return "SID: Sortby Argument error"

        for url in sub:
            # Getting JSON data
            res = requests.get(f"https://reddit.com/{url}/.json",
                               headers=self.headers)
            data = json.loads(res.text)

            # Getting link from the JSON data
            data = data[0]["data"]["children"][0]["data"]["url"]

            # Add to the links list if supported
            if ".png" in data:
                links.append(data)

            elif ".jpg" in data:
                links.append(data)

            # If not supported, move to the next link
            else:
                continue

            # Print, and save each supported link and saveurls is true
            if saveurls:
                with open(f"links{self.time}.txt", "a") as f:
                    f.write(f"{data}\n")
        return links

    # DOWNLOADIMAGES
    def downloadimages(self, links, filename="images",
                       foldername="images"):
        # Making sure imgs folder is here
        os.makedirs(foldername, exist_ok=True)
        i = 0
        for link in links:
            # Get the bytes of the image
            res = requests.get(link).content

            # Save the image
            filename_ = os.path.join(foldername, f"{filename}{i}.png")
            with open(filename_, "wb") as f:
                print(filename_)
                f.write(res)
            i += 1
