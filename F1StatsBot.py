import praw
import config
import time
import os
import re
import F1Parsing

#Login Reddit Bot
def botLogin():
    print("Reddit Bot is logging in...")
    redditBot = praw.Reddit( username = config.username,
                             password = config.password,
                             client_id = config.client_id,
                             client_secret = config.client_secret,
                             user_agent="/u/F1StatsBot's Formula 1 Statistic Bot")
    print("Reddit Bot has logged in!")
    return redditBot


#Perform Reddit Bot Actions
def runBot(redditBot, repliedCommentsList, fileName):
    for comment in redditBot.subreddit('test').comments(limit=1000):
        if "!f1stats" in comment.body.lower() and comment.id not in repliedCommentsList:       
            if"!f1stats drivers " in comment.body.lower():
                possibleYear = re.findall('[0-9]{4}', comment.body.lower())
                try:
                    year = possibleYear[0]
                    comment.reply("Drivers Standing For " + year + " Provided By: https://ergast.com\n\n" +
                                  F1Parsing.driverStanding(F1Parsing.driverStandingList(year)))
                    print("Reply Successful! "+"\""+ comment.body.lower()
                           + "\"" + " by " + str(comment.author) + " " + str(comment.id))
                except:
                    print("Error Occured When Replying! " + "\"" + comment.body.lower() 
                           + "\"" +" by:" + str(comment.author) + "," + str(comment.id))
                    
            elif "!f1stats constructors " in comment.body.lower():
                possibleYear = re.findall('[0-9]{4}', comment.body.lower())
                try:
                    year = possibleYear[0]
                    comment.reply("Constructors Standing For " + year + " Provided By: https://ergast.com\n\n" +
                                  F1Parsing.constructorStandings(F1Parsing.constructorStandingList(year)))
                    print("Reply Successful! "+"\""+ comment.body.lower()
                          + "\"" + " by " + str(comment.author) + " " + str(comment.id))
                except:
                    print("Error Occured When Replying! " +"\""+ comment.body.lower() 
                          + "\"" +" by:" + str(comment.author) + "," + str(comment.id))
            else:
                print("Invalid Command: " +"\""+ comment.body.lower()
                      + "\"" + " by " + str(comment.author) + " " + str(comment.id))
                comment.reply("Invalid usage. Check Spelling or Formatting!\n")
    
            #store the replied to comment in the list and textfile
            repliedCommentsList.append(comment.id)
            with open(fileName, "a") as f:
                f.write(comment.id + "\n")


#Get Saved Comments for a text file and store them into a list 
def getSavedComments(fileName):
    if not os.path.isfile(fileName):
        print("file: " + fileName + " not found")
        repliedCommentsList = []
    else:
        with open(fileName, "r") as f:
            repliedCommentsList = f.read()
            repliedCommentsList = repliedCommentsList.split("\n")
    
    return repliedCommentsList


def main():
    f1RedditBot = botLogin()
    repliedCommentsList = getSavedComments("commentsRepliedTo.txt")
    print(repliedCommentsList)
    
    while True:
        runBot(f1RedditBot, repliedCommentsList,"commentsRepliedTo.txt")
        print(repliedCommentsList)
        time.sleep(10)

if __name__=="__main__":
    main()
