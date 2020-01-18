import sid
import usersettings as user

download = sid.ImageDownload()

links = download.getimageurl(clientid=user.clientid, clientsecret=user.clientsecret,
                             useragent=user.useragent, limit=user.limit,subred=user.subreddit
                             sortby = user.sortby, saveurls=False)

download.downloadimages(links, filename=user.filename, foldername=user.foldername)
