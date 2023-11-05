#!/usr/bin/env python
# coding: utf-8

# In[11]:


get_ipython().system('pip3 install snscrape')


# In[12]:


# import all the needed libraries
import snscrape.modules.twitter as sntwitter
import requests
from requests_oauthlib import OAuth1
import pandas as pd
import numpy as np
import time
import tweepy
import collections
import pickle
from datetime import date
#import twint


# In[13]:


today = date.today()
fileName = "Other_Files/ReetwetsFromUpLevel_"+str(today)+".xlsx"
fileName


# #### Credentials
# * to access tweepy
# * REST API call

# In[14]:


# TO ACCESS TWEEPY
## CONNECTION TO TWITTER: SOURCE OF THE DATA
# KEYS
# Variables that contains the credentials to access Twitter API
ACCESS_TOKEN = '1130999735190470656-t9RTSxHzCNhNitZaLwq4ngz1oAOUqf'
ACCESS_SECRET = 'SfTQT5H50D028d8VSEsfE3CjDr4d7oxIoORO9rXgPWHzL'
CONSUMER_KEY = 'SohZISfyGQNeMrHP11SeDjqgt'
CONSUMER_SECRET = '5reZLXL0fgbQnXoGiBiB4lkLxhcbdOoZ2lzP1Xlk2KW1nGL50q'

# online autentification, Twitter API set up
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN,ACCESS_SECRET)
api= tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


# In[15]:


# KEYS
# Variables that contains the credentials to access Twitter API
# Access Token
ACCESS_TOKEN = '981885112496394240-THEErFuo8gNtydKQwFSKivEcv3rBCS5'
# Access Token Secret
ACCESS_SECRET = 'tAwdYr05crVGj3lx1zFxDf49snze5jtZVcRQsndcHRCwd'
# API Key
CONSUMER_KEY = 'pqPBxUx5Ja7l6OfwYg7TErDU7'
# API Key Secret
CONSUMER_SECRET = 'OG38qVbtbxqOR6AsiQvLbaWoKuTQBRBiwylWkTOGiOke8gFqKF'

authrest = OAuth1(CONSUMER_KEY, CONSUMER_SECRET,
        ACCESS_TOKEN, ACCESS_SECRET)


# In[16]:


andreskeys = "Bearer AAAAAAAAAAAAAAAAAAAAACWwTwEAAAAAz%2FMC7WR3itn9FaCBnV8NyfJ%2BRf4%3DczSMxk1nDTjdZDh0dr27KNJ8qYIibsctiqRYf2fl1d3VgDnZHr"
myKey = "Bearer AAAAAAAAAAAAAAAAAAAAAJ3zSQEAAAAASV791LLHC1yCF7kQIPV%2BcktWu%2B4%3DzVBZNpUIuYhbXA6hKTt0TOW20hzkI2rjx2IiytuDYPZ3C2ppZV"


# ## Get Initial Data

# In[17]:


# Read the excel with the current users, this list of users is only use as reference
# this part is used to know the current users and as a list to pick wich users go next
currentFollowers = pd.read_excel(r'Input_File/Retweeter_DataSet_FullText.xlsx', sheet_name='users_level')
currentFollowersList = currentFollowers['Follower'].unique() # get unique values
currentFollowersList = currentFollowersList.tolist()
currentFollowersList.remove("eveslexie") # this is a private user - generates error
currentFollowersList.remove("Argeen19") # this is a private user - generates error
currentFollowersList


# ## Initialized variables to last state, to continue where the code left

# In[18]:


#last_user_used = 'cwebbonline'
#pickle.dump( last_user_used, open( "Pickle_Variables/last_user_used.p", "wb" ) )
last_user_used2 = pickle.load( open( "Pickle_Variables/last_user_used.p", "rb" ) )
last_user_used2


# In[19]:


upLevelUsers = []


# In[20]:


last_user_used = pickle.load( open( "Pickle_Variables/last_user_used.p", "rb" ) )
pos_last_user_used =  currentFollowersList.index(last_user_used)
pos_last_user_used


# In[21]:


upLevelUsers = currentFollowersList[pos_last_user_used+1:pos_last_user_used+5]
upLevelUsers


# In[22]:


last_user_used = upLevelUsers[3]
pickle.dump( last_user_used, open( "Pickle_Variables/last_user_used.p", "wb" ) )


# ### Find common followers for input users

# In[23]:


ids = []
complete = []
contador = 0
for uoi in upLevelUsers:
  try:
    for page in tweepy.Cursor(api.followers_ids, screen_name= uoi).pages():
      ids.extend(page)
      time.sleep(60) # time.sleep to avoid rate limit
      for id in ids:
        complete.append([id,uoi])
  except:
    continue # continue if user dosent exist or finds an exception
print(len(ids))


# In[24]:


# To find the ids of the common followers
import collections
commonF = [item for item, count in collections.Counter(ids).items() if count > 1]
len(commonF)


# In[25]:


# Get common followers screen names
commonFNames = []

for us in commonF:
  try:
    time.sleep(0.02)
    URL = "https://api.twitter.com/1.1/users/lookup.json"
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'user_id':us}
    
    # sending get request and saving the response as response object
    r = requests.get(url = URL, params = PARAMS,auth=authrest)
    # extracting data in json format
    data = r.json()
    screenName = data[0]['screen_name'] # to access the atributes and get only the user screen name
    #print(screenName)
    commonFNames.append(screenName) # save the result in array
  except:
    continue
    
# Check the result
commonFNames


# In[26]:


if len(commonFNames) > 200:
    commonFNames = commonFNames[0:200]
else:
    commonFNames = commonFNames[0:len(commonFNames)-1]


# In[27]:


len(commonFNames)


# #### Get all and specifict (origin users) retweets from common followers
# 
# snscraper have timline limit when it comes to get all tweets including retweets
# 
# https://github.com/JustAnotherArchivist/snscrape/issues/83
# 
# https://github.com/JustAnotherArchivist/snscrape/issues/8

# In[28]:


deepLevelRetweeter = []
keepGoing = 1


# In[29]:


last_user_used_deepLevel = commonFNames[0]
last_user_used_deepLevel


# In[30]:


pos_last_user_used_deepLevel =  commonFNames.index(last_user_used_deepLevel)
pos_last_user_used_deepLevel


# In[31]:


pickle.dump( last_user_used_deepLevel, open( "Pickle_Variables/last_user_used_deepLevel.p", "wb" ) )


# In[32]:


def refresh_deepLevel_array():
    deepLevelRetweeter = []
    last_user_used_deepLevel = pickle.load( open( "Pickle_Variables/last_user_used_deepLevel.p", "rb" ) )
    pos_last_user_used_deepLevel =  commonFNames.index(last_user_used_deepLevel)+1

    if len(commonFNames)<=30:
        deepLevelRetweeter = commonFNames[pos_last_user_used_deepLevel:len(commonFNames)]

    else:
        deepLevelRetweeter = commonFNames[pos_last_user_used_deepLevel:pos_last_user_used_deepLevel+30]
  
    last_user_used_deepLevel = deepLevelRetweeter[len(deepLevelRetweeter)-1]
    pickle.dump( last_user_used_deepLevel, open( "Pickle_Variables/last_user_used_deepLevel.p", "wb" ) )
 
    pos_last_user_used_deepLevel = commonFNames.index(last_user_used_deepLevel)

    return deepLevelRetweeter,keepGoing,pos_last_user_used_deepLevel


# In[33]:


deepLevelRetweeter,keepGoing,pos_last_user_used_deepLevel = refresh_deepLevel_array()


# In[34]:


# To save the results
retweetsForUser1 = []
retweetsForUser2 = []
retweetsForUser3 = []
retweetsForUser4 = []
usersRetweetFrom = []
info = []


# In[ ]:


# This part of the code finds retweets from input users
# and also the retweets from specific users in this case origin users
while keepGoing == 1:

  userToFind1 = 'MichelleObama'
  userToFind2 = 'BarackObama'
  userToFind3 = 'HillaryClinton'
  userToFind4 = 'POTUS'

  for u in deepLevelRetweeter:
    try:
        counter1 = 0
        counter2 = 0
        counter3 = 0
        counter4 = 0
        numRT = 0

        getUser = api.get_user(u)
        count = getUser.statuses_count
        
        for tweet in tweepy.Cursor(api.user_timeline,u,tweet_mode="extended").items(count):
                  
            tweet_text = tweet.full_text
            number_of_retweets = tweet.retweet_count
            number_of_likes = tweet.favorite_count
            author = tweet.author.screen_name
            tweet_ID = str(tweet.id)
            #time.sleep(5) 
            
            if tweet_text.startswith('RT @'):
                retweet_text = tweet.full_text
                pos = retweet_text.find(':')
                originalUser = retweet_text[4:pos]
                usersRetweetFrom.append([tweet_ID,tweet_text,originalUser,u])    
                numRT = numRT + 1
            
            if tweet_text.startswith('RT @'+userToFind1):
                retweet_text = tweet.full_text
                pos = retweet_text.find(':')
                originalUser = retweet_text[4:pos]
                retweetsForUser1.append([tweet_ID,tweet_text,originalUser,u,userToFind1])
                counter1 = counter1 + 1
            
            if tweet_text.startswith('RT @'+userToFind2):
                retweet_text = tweet.full_text
                pos = retweet_text.find(':')
                originalUser = retweet_text[4:pos]
                retweetsForUser2.append([tweet_ID,tweet_text,originalUser,u,userToFind2])
                counter2 = counter2 + 1

            if tweet_text.startswith('RT @'+userToFind3):
                retweet_text = tweet.full_text
                pos = retweet_text.find(':')
                originalUser = retweet_text[4:pos]
                retweetsForUser3.append([tweet_ID,tweet_text,originalUser,u,userToFind3])
                counter3 = counter3 + 1
            
            if tweet_text.startswith('RT @'+userToFind4):
                retweet_text = tweet.full_text
                pos = retweet_text.find(':')
                originalUser = retweet_text[4:pos]
                retweetsForUser4.append([tweet_ID,tweet_text,originalUser,u,userToFind4])
                counter4 = counter4 + 1
                        
        info.append([numRT,counter1,u,userToFind1])
        info.append([numRT,counter2,u,userToFind2])
        info.append([numRT,counter3,u,userToFind3])
        info.append([numRT,counter4,u,userToFind4])
        print('Number of tweets of',u,'is: ',count)
        print('total RT: ',numRT)
        print('total from user 1: ',counter1)
        print('total from user 2: ',counter2)
        print('total from user 3: ',counter3)
        print('total from user 4: ',counter4)
    except Exception as error:
        continue
        
  deepLevelRetweeter,keepGoing,pos_last_user_used_deepLevel = refresh_deepLevel_array()
  
  if pos_last_user_used_deepLevel == len(commonFNames)-1: #len(commonFNames)-1:
    keepGoing = 0
    print('no hay mas ids')
    
  else:
    time.sleep(300)
    keepGoing = 1


# In[ ]:


# check final results
info


# In[ ]:


# from result arrays to Dataframe
infos = pd.DataFrame(info)
retweetsForUser1 = pd.DataFrame(retweetsForUser1)
retweetsForUser2 = pd.DataFrame(retweetsForUser2)
retweetsForUser3 = pd.DataFrame(retweetsForUser3)
retweetsForUser4 = pd.DataFrame(retweetsForUser4)
usersRetweetFrom = pd.DataFrame(usersRetweetFrom)


# In[ ]:


# Concatenate all dataframes
tweetContDownLevel = pd.concat([retweetsForUser1,retweetsForUser2,retweetsForUser3,retweetsForUser4])


# In[ ]:


#tweetContDownLevel.to_excel("toReviewIDs.xlsx",sheet_name='ids test')


# #### check if in the result there is any retweet from up level user (the first input)

# In[ ]:


today = date.today()
#fileName = "Other_Files/ReetwetsFromUpLevel_"+today+".xlsx"
#fileName


# In[ ]:


# To check if any of the common followers have retweeted from up level users
ReetwetsFromUpLevel = usersRetweetFrom[usersRetweetFrom[2].isin(upLevelUsers)]
ReetwetsFromUpLevel


# In[ ]:


# save the result in a excel file
ReetwetsFromUpLevel.to_excel("Other_Files/ReetwetsFromUpLevel_"+str(today)+".xlsx",sheet_name='retweets')


# #### check if in the result there is any retweet from any other retweeter in the dataset

# In[ ]:


# TRY to find retweets also from retweters
ReetwetsFromCurrentUsers = usersRetweetFrom[usersRetweetFrom[2].isin(currentFollowersList)]
ReetwetsFromCurrentUsers


# In[ ]:


# save the result in a excel file
ReetwetsFromCurrentUsers.to_excel("Other_Files/ReetwetsFromCurrentUsers_"+str(today)+".xlsx",sheet_name='retweets')


# ### Get all and specifict (origin users) retweets from up level users
# This part is the reference to get the deeper level retweeters

# In[ ]:


retweetsForUpUser1 = []
retweetsForUpUser2 = []
retweetsForUpUser3 = []
retweetsForUpUser4 = []
usersRetweetUpFrom = []
Upinfo = []


# In[ ]:


# This part of the code finds retweets from input users
# and also the retweets from specific users in this case origin users
userToFind1 = 'MichelleObama'
userToFind2 = 'BarackObama'
userToFind3 =  'HillaryClinton'
userToFind4 = 'POTUS'

for u in upLevelUsers:
  try:
      
    counter1 = 0
    counter2 = 0
    counter3 = 0
    counter4 = 0
    numRT = 0

    getUser = api.get_user(u)
    count = getUser.statuses_count
      
    for tweet in tweepy.Cursor(api.user_timeline,u,tweet_mode="extended").items(count):
        time.sleep(0.09)          
        tweet_text = tweet.full_text
        number_of_retweets = tweet.retweet_count
        number_of_likes = tweet.favorite_count
        author = tweet.author.screen_name
        tweet_ID = str(tweet.id)
        #time.sleep(50)
          
        if tweet_text.startswith('RT @'):
            retweet_text = tweet.full_text
            pos = retweet_text.find(':')
            originalUser = retweet_text[4:pos]
            usersRetweetUpFrom.append([tweet_ID,tweet_text,originalUser,u])     
            numRT = numRT + 1
          
        if tweet_text.startswith('RT @'+userToFind1):
            retweet_text = tweet.full_text
            pos = retweet_text.find(':')
            originalUser = retweet_text[4:pos]
            retweetsForUpUser1.append([tweet_ID,tweet_text,originalUser,u,userToFind1])
            counter1 = counter1 + 1
          
        if tweet_text.startswith('RT @'+userToFind2):
            retweet_text = tweet.full_text
            pos = retweet_text.find(':')
            originalUser = retweet_text[4:pos]
            retweetsForUpUser2.append([tweet_ID,tweet_text,originalUser,u,userToFind2])
            counter2 = counter2 + 1

        if tweet_text.startswith('RT @'+userToFind3):
            retweet_text = tweet.full_text
            pos = retweet_text.find(':')
            originalUser = retweet_text[4:pos]
            retweetsForUpUser3.append([tweet_ID,tweet_text,originalUser,u,userToFind3])
            counter3 = counter3 + 1
          
        if tweet_text.startswith('RT @'+userToFind4):
            retweet_text = tweet.full_text
            pos = retweet_text.find(':')
            originalUser = retweet_text[4:pos]
            retweetsForUpUser4.append([tweet_ID,tweet_text,originalUser,u,userToFind4])
            counter4 = counter4 + 1

    Upinfo.append([numRT,counter1,u,userToFind1])
    Upinfo.append([numRT,counter2,u,userToFind2])
    Upinfo.append([numRT,counter3,u,userToFind3])
    Upinfo.append([numRT,counter4,u,userToFind4])
    print('Number of tweets of',u,'is: ',count)
    print('total RT: ',numRT)
    print('total from user 1: ',counter1)
    print('total from user 2: ',counter2)
    print('total from user 3: ',counter3)
    print('total from user 4: ',counter4)
  except Exception as error:
    #errorCode = error.args[0][0]['code']
    #if errorCode == 50: # code 50 indicates user not found error
      continue
    #else:
      #print(error.args[0][0]['code'])


# In[ ]:


Upinfos = pd.DataFrame(Upinfo)
retweetsForUpUser1 = pd.DataFrame(retweetsForUpUser1)
retweetsForUpUser2 = pd.DataFrame(retweetsForUpUser2)
retweetsForUpUser3 = pd.DataFrame(retweetsForUpUser3)
retweetsForUpUser4 = pd.DataFrame(retweetsForUpUser4)
usersRetweetUpFrom = pd.DataFrame(usersRetweetUpFrom)


# In[ ]:


tweetContUpLevel = pd.concat([retweetsForUpUser1,retweetsForUpUser2,retweetsForUpUser3,retweetsForUpUser4])


# #### check if in the result there is any retweet from any other retweeter in the dataset (Up level users)

# In[ ]:


# TRY to find retweets also from retweters
ReetwetsFromCurrentUsersUp = usersRetweetUpFrom[usersRetweetUpFrom[2].isin(currentFollowersList)]
ReetwetsFromCurrentUsersUp


# In[ ]:


# save the result in a excel file
ReetwetsFromCurrentUsersUp.to_excel("Other_Files/ReetwetsFromCurrentUsersUp_"+str(today)+".xlsx",sheet_name='retweets')


# ## To add the original tweet ID to the dataset

# In[ ]:


original_Tweet_Down = []
original_Tweet_Up = []


# In[ ]:


idListToGetOriginalId = []
keepGoing = 1


# In[ ]:


idListDownLevel =tweetContDownLevel[0].tolist()
idListUpLevel = tweetContUpLevel[0].tolist()


# In[ ]:


last_tweet_id_processed = idListUpLevel[0]
last_tweet_id_processed_down = idListDownLevel[0]


# In[ ]:


pickle.dump(last_tweet_id_processed, open( "Pickle_Variables/last_tweet_id_processed.p", "wb" ) )
pickle.dump(last_tweet_id_processed_down, open( "Pickle_Variables/last_tweet_id_processed_down.p", "wb" ) )


# In[ ]:


def divide_up_level_array():
    idListToGetOriginalId = []
    last_tweet_id_processed = pickle.load( open( "Pickle_Variables/last_tweet_id_processed.p", "rb" ) )
    last_tweet_id_pos_processed = idListUpLevel.index(last_tweet_id_processed)#+1

    if len(idListUpLevel)<=100:
        idListToGetOriginalId = idListUpLevel[last_tweet_id_pos_processed:len(idListUpLevel)]

    else:
        idListToGetOriginalId = idListUpLevel[last_tweet_id_pos_processed:last_tweet_id_pos_processed+100]

    last_tweet_id_processed= idListToGetOriginalId[len(idListToGetOriginalId)-1]
    pickle.dump( last_tweet_id_processed, open( "Pickle_Variables/last_tweet_id_processed.p", "wb" ) )
 
    last_tweet_id_pos_processed = idListUpLevel.index(last_tweet_id_processed)

    return idListToGetOriginalId,keepGoing,last_tweet_id_pos_processed


# In[ ]:


idListToGetOriginalId,keepGoing,last_tweet_id_pos_processed = divide_up_level_array()


# In[ ]:


def divide_down_level_array():
    idListToGetOriginalId = []
    last_tweet_id_processed_down = pickle.load( open( "Pickle_Variables/last_tweet_id_processed_down.p", "rb" ) )
    last_tweet_id_pos_processed_down = idListDownLevel.index(last_tweet_id_processed_down)#+1

    if len(idListDownLevel)<=100:
        
        idListToGetOriginalId = idListDownLevel[last_tweet_id_pos_processed_down:len(idListDownLevel)]
    
        last_tweet_id_processed_down= idListToGetOriginalId[len(idListToGetOriginalId)-1]
        pickle.dump( last_tweet_id_processed_down, open( "Pickle_Variables/last_tweet_id_processed_down.p", "wb" ) )
        last_tweet_id_pos_processed_down = idListDownLevel.index(last_tweet_id_processed_down)

    else:
        idListToGetOriginalId = idListDownLevel[last_tweet_id_pos_processed_down:last_tweet_id_pos_processed_down+100]
    
        last_tweet_id_processed_down= idListToGetOriginalId[len(idListToGetOriginalId)-1]
        pickle.dump( last_tweet_id_processed_down, open( "Pickle_Variables/last_tweet_id_processed_down.p", "wb" ) ) 
        last_tweet_id_pos_processed_down = idListDownLevel.index(last_tweet_id_processed_down)

  #last_tweet_id_processed_down= idListToGetOriginalId[len(idListToGetOriginalId)-1]
  #pickle.dump( last_tweet_id_processed_down, open( "Pickle_Variables/last_tweet_id_processed_down.p", "wb" ) )
 
  #last_tweet_id_pos_processed_down = idListDownLevel.index(last_tweet_id_processed_down)

    return idListToGetOriginalId,keepGoing,last_tweet_id_pos_processed_down


# In[ ]:


last_tweet_id_processed_down


# In[ ]:


idListDownLevel


# In[ ]:


count


# In[ ]:


while keepGoing == 1:
    try:
        for id in idListToGetOriginalId:
            # api-endpoint
            URL = "https://api.twitter.com/2/tweets/"

            # defining a params dict for the parameters to be sent to the API
            # source is going to be the retweeter and target to see if also follows author
            PARAMS = {'ids':id,'tweet.fields':'author_id,referenced_tweets'} 

            # Using only bearer tokens, this form of authentication uses headers in the documentation it apperas in the request example as -H this h indicates headers
            HEADERS = {"Authorization": andreskeys} #andreskeys

            # sending get request and saving the response as response object
            r = requests.get(url = URL, params = PARAMS,headers= HEADERS)

            # extracting data in json format
            data1 = r.json()
            referenced_tweet_id = data1['data'][0]['referenced_tweets'][0]['id']
            retweet_id = data1['data'][0]['id']

            original_Tweet_Up.append([referenced_tweet_id,retweet_id])
    except:
        continue 
  
    idListToGetOriginalId,keepGoing,last_tweet_id_pos_processed = divide_up_level_array()
  
    if last_tweet_id_pos_processed == len(idListUpLevel)-1:
        keepGoing = 0
        #last_user_used_deepLevel = deepLevelRetweeter[0]
        #pickle.dump( last_user_used_deepLevel, open( "last_user_used_deepLevel.p", "wb" ) )
        print('no hay mas ids')
    
    else:
        time.sleep(300)
        keepGoing = 1


# In[ ]:


idListUpLevel 


# In[ ]:


original_Tweet_Up


# In[ ]:


# covert to dataframe
original_Tweet = pd.DataFrame(original_Tweet_Up)
#Add to dataframe column names
original_Tweet.columns = ['Original tweet ID','Retweet ID']
original_Tweet


# In[ ]:


tweetContUpLevel = pd.merge(tweetContUpLevel, original_Tweet, how='left',left_on=0, right_on='Retweet ID')
tweetContUpLevel


# In[ ]:


idListToGetOriginalId = []
original_Tweet_Down = []
keepGoing = 1


# In[ ]:


last_tweet_id_processed_down = idListDownLevel[0]
pickle.dump(last_tweet_id_processed_down, open( "Pickle_Variables/last_tweet_id_processed_down.p", "wb" ) )


# In[ ]:


idListToGetOriginalId,keepGoing,last_tweet_id_pos_processed_down = divide_down_level_array()


# In[ ]:


while keepGoing == 1:
  try:
    for id in idListToGetOriginalId:
        # api-endpoint
        URL = "https://api.twitter.com/2/tweets/"

        # defining a params dict for the parameters to be sent to the API
        # source is going to be the retweeter and target to see if also follows author
        PARAMS = {'ids':id,'tweet.fields':'author_id,referenced_tweets'} 

        # Using only bearer tokens, this form of authentication uses headers in the documentation it apperas in the request example as -H this h indicates headers
        HEADERS = {"Authorization": andreskeys} #andreskeys

        # sending get request and saving the response as response object
        r = requests.get(url = URL, params = PARAMS,headers= HEADERS)

        # extracting data in json format
        data1 = r.json()
        referenced_tweet_id = data1['data'][0]['referenced_tweets'][0]['id']
        retweet_id = data1['data'][0]['id']

        original_Tweet_Down.append([referenced_tweet_id,retweet_id])
  except:
    continue 
  
  idListToGetOriginalId,keepGoing,last_tweet_id_pos_processed = divide_down_level_array()
  
  if last_tweet_id_pos_processed == len(idListDownLevel)-1:
    keepGoing = 0
    #last_user_used_deepLevel = deepLevelRetweeter[0]
    #pickle.dump( last_user_used_deepLevel, open( "last_user_used_deepLevel.p", "wb" ) )
    print('no hay mas ids')
    
  else:
    time.sleep(300)
    keepGoing = 1


# In[ ]:


keepGoing


# In[ ]:


original_Tweet_Down


# In[ ]:


original_Tweet_Down


# In[ ]:


# covert to dataframe
original_Tweet = pd.DataFrame(original_Tweet_Down)
#Add to dataframe column names
original_Tweet.columns = ['Original tweet ID','Retweet ID']
original_Tweet


# In[ ]:


tweetContDownLevel = pd.merge(tweetContDownLevel, original_Tweet, how='left',left_on=0, right_on='Retweet ID')
tweetContDownLevel


# In[ ]:


tweetContUpLevel


# ### To compare retweets

# In[ ]:


# create an empty DataFrame object to store the matching retweets
dfUp = pd.DataFrame()
dfDown = pd.DataFrame()


# In[ ]:


listOfTweetsToSearch = tweetContDownLevel['Original tweet ID'].unique()
listOfTweetsToSearch2 = tweetContUpLevel['Original tweet ID'].unique()


# In[ ]:


dfUp = tweetContUpLevel[tweetContUpLevel['Original tweet ID'].isin(listOfTweetsToSearch)]
dfDown = tweetContDownLevel[tweetContDownLevel['Original tweet ID'].isin(listOfTweetsToSearch2)]


# ## To find Relationships
# Once the matching retweets are found, to see if any of retweeters can be used is necessary to check relation between up and depper level retweeters.

# ### Check if follows level 0 (origin Users)

# In[ ]:


# this array only gives results if in the previous steps the code found matching retweets
# if the array is empty there is not need to execute next steps

# Define source users
sourceUsers = dfDown[3].unique().tolist()
sourceUsers


# In[ ]:


# Define target users
targetUsers = dfDown[2].unique().tolist()
targetUsers


# In[ ]:


sourceUsersSelected = []
keepGoing = 1


# In[ ]:


last_source_user = sourceUsers[0]
pickle.dump( last_source_user, open( "Pickle_Variables/last_source_user.p", "wb" ) )
last_source_user


# In[ ]:


def split_input_source_users():
    sourceUsersSelected = []
    last_source_user = pickle.load( open( "Pickle_Variables/last_source_user.p", "rb" ) )
    last_source_user_pos = sourceUsers.index(last_source_user)#+1

    if len(sourceUsers)<=30:
        sourceUsersSelected = sourceUsers[last_source_user_pos:len(sourceUsers)]

    else:
        sourceUsersSelected = sourceUsers[last_source_user_pos:last_source_user_pos+30]

    last_source_user= sourceUsersSelected[len(sourceUsersSelected)-1]
    pickle.dump( last_source_user, open( "Pickle_Variables/last_source_user.p", "wb" ) )
 
    last_source_user_pos = sourceUsers.index(last_source_user)

    return sourceUsersSelected,keepGoing,last_source_user_pos


# In[ ]:


sourceUsersSelected,keepGoing,last_source_user_pos = split_input_source_users()


# In[ ]:


# to store the result of the relationships
followerRetweeter = []
followsTarget = []
dontFollowTarget = []


# In[ ]:


while keepGoing == 1 and len(sourceUsers)!=0:
    try:
        # these part of the code is used to check if source user follows target user
        for targetU in targetUsers:
          #time.sleep(60)
          for sourceU in sourceUsersSelected:
            # api-endpoint
            URL = "https://api.twitter.com/1.1/friendships/show.json?"

            # defining a params dict for the parameters to be sent to the API
            # source is going to be the retweeter and target to see if also follows author
            PARAMS = {'source_screen_name':sourceU,'target_screen_name':targetU} 

            # sending get request and saving the response as response object
            r = requests.get(url = URL, params = PARAMS,auth=authrest)

            # extracting data in json format
            data = r.json()
            retweeterFollowsAuthor = data['relationship']['source']['following']
            retweeterScreenName = data['relationship']['source']['screen_name']
            authorScreenName = data['relationship']['target']['screen_name']

            if retweeterFollowsAuthor == True:
              followerRetweeter.append([retweeterScreenName,'follows',authorScreenName])
              followsTarget.append([retweeterScreenName,authorScreenName])
            else:
              followerRetweeter.append([retweeterScreenName,'dont follow',authorScreenName])
              dontFollowTarget.append([retweeterScreenName,authorScreenName])
    except:
        continue 
  
    sourceUsersSelected,keepGoing,last_source_user_pos = split_input_source_users()
  
    if last_source_user_pos == len(sourceUsers)-1:
        keepGoing = 0
        #last_user_used_deepLevel = deepLevelRetweeter[0]
        #pickle.dump( last_user_used_deepLevel, open( "last_user_used_deepLevel.p", "wb" ) )
        print('no hay mas ids')
    
    else:
        time.sleep(300)
        keepGoing = 1


# In[ ]:


followerRetweeter


# In[ ]:


# if retweter follows origin user, it means the retweeter cant be used as deeper level user
# so it is eliminated from the results.

for i in range(len(followerRetweeter)):
    sourceUser = followerRetweeter[i][0]
    isFollower = followerRetweeter[i][1]
    targetUser = followerRetweeter[i][2]

    for index, row in dfDown.iterrows():
        if row[2] == targetUser and row[3] == sourceUser and isFollower == 'follows':
            
            indexName = dfDown[(dfDown[2] == row[2]) & (dfDown[3] == row[3])].index
            finalDf = dfDown.drop(indexName , inplace=True)
            print('are followers',indexName)


# In[ ]:


dfDown


# ### Check if follows up level
#  the remaind list are retweeters that don't follow origin but have retweets from them, so they must retweeted this tweets from up level user, it is necessary to check if the retweeter follows up level user

# In[ ]:


RemaindListsource = dfDown[3].unique().tolist()


# In[ ]:


RemaindListTarget = dfUp[3].unique().tolist()


# In[ ]:


RemainsourceUsersSelected = []
keepGoing = 1


# In[ ]:


last_Remain_source_user = RemaindListsource[0]
pickle.dump( last_Remain_source_user, open( "Pickle_Variables/last_Remain_source_user.p", "wb" ) )
last_Remain_source_user


# In[ ]:


def split_input_remain_source_users():
    
    RemainsourceUsersSelected = []
    last_Remain_source_user = pickle.load( open( "Pickle_Variables/last_Remain_source_user.p", "rb" ) )
    last_Remain_source_user_pos = RemaindListsource.index(last_Remain_source_user)#+1

    if len(RemaindListsource)<=30 and len(RemaindListsource)>1:

        RemainsourceUsersSelected = RemaindListsource[RemaindListsource.index(last_Remain_source_user):RemaindListsource.index(last_Remain_source_user)+(len(RemaindListsource))]
    
        last_Remain_source_user= RemainsourceUsersSelected[len(RemainsourceUsersSelected)-1]
        pickle.dump( last_Remain_source_user, open( "Pickle_Variables/last_Remain_source_user.p", "wb" ) )
        last_Remain_source_user_pos = RemaindListsource.index(last_Remain_source_user)
  
    else:
        RemainsourceUsersSelected = RemaindListsource[last_Remain_source_user_pos:last_Remain_source_user_pos+30]
        last_Remain_source_user= RemainsourceUsersSelected[len(RemainsourceUsersSelected)-1]
        pickle.dump( last_Remain_source_user, open( "Pickle_Variables/last_Remain_source_user.p", "wb" ) )
        last_Remain_source_user_pos = RemaindListsource.index(last_Remain_source_user)
  
    return RemainsourceUsersSelected,keepGoing,last_Remain_source_user_pos


# In[ ]:


RemainsourceUsersSelected,keepGoing,last_Remain_source_user_pos = split_input_remain_source_users()


# In[ ]:


# to store the result of the found relationships
followerRetweeter2 = []
followsTarget2 = []
dontFollowTarget2 = []


# In[ ]:


while keepGoing == 1 and len(RemaindListsource)!= 0:
    try:
        for targetU in RemaindListTarget:
            #time.sleep(60)
            for sourceU in RemainsourceUsersSelected:
                # api-endpoint
                URL = "https://api.twitter.com/1.1/friendships/show.json?"

                # defining a params dict for the parameters to be sent to the API
                # source is going to be the retweeter and target to see if also follows author
                PARAMS = {'source_screen_name':sourceU,'target_screen_name':targetU} 

                # sending get request and saving the response as response object
                r = requests.get(url = URL, params = PARAMS,auth=authrest)

                # extracting data in json format
                data = r.json()
                retweeterFollowsAuthor = data['relationship']['source']['following']
                retweeterScreenName = data['relationship']['source']['screen_name']
                authorScreenName = data['relationship']['target']['screen_name']

                if retweeterFollowsAuthor == True:
                    followerRetweeter2.append([retweeterScreenName,'follows',authorScreenName])
                    followsTarget2.append([retweeterScreenName,authorScreenName])
                else:
                    followerRetweeter2.append([retweeterScreenName,'dont follow',authorScreenName])
                    dontFollowTarget2.append([retweeterScreenName,authorScreenName])
    except:
        continue 
  
    RemainsourceUsersSelected,keepGoing,last_Remain_source_user_pos = split_input_remain_source_users()
  
    if last_Remain_source_user_pos == len(RemaindListsource)-1:
        keepGoing = 0
        #last_user_used_deepLevel = deepLevelRetweeter[0]
        #pickle.dump( last_user_used_deepLevel, open( "last_user_used_deepLevel.p", "wb" ) )
        print('no hay mas ids')

    else:
        time.sleep(300)
        keepGoing = 1
  
    #RemainsourceUsersSelected,keepGoing,last_Remain_source_user_pos = split_input_remain_source_users()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


# To keep only the users of up level that are followed
followsList = []
for i in range(len(followsTarget2)):
    followsList.append(followsTarget2[i][1])
followsList = pd.DataFrame(followsList,columns=['follower'])
followsList = followsList['follower'].unique()
dfUpFinal = dfUp[dfUp[3].isin(followsList)]


# In[ ]:


# the final users have retweeted from origin but dont follow origin users so the retweets
# come from up level user (not origin)

finalResult = []


# In[ ]:


# to check if follows up level user
for index, row1 in dfDown.iterrows():
  tweetText = row1[1]
  downUser = row1[3]
  for index, row in dfUpFinal.iterrows():
    if tweetText == row[1]:
      for i in range(len(followerRetweeter2)):
        sourceUser = followerRetweeter2[i][0]
        isFollower = followerRetweeter2[i][1]
        targetUser = followerRetweeter2[i][2]

        if downUser == sourceUser and targetUser == row[3] and isFollower == 'follows':
          print('is in followers')
          finalResult.append([sourceUser,targetUser,row['Retweet ID'],row[1],row[2],row[3],row['Original tweet ID']])


# In[ ]:


final = pd.DataFrame(finalResult)
final


# ### Get the info for the final user and give structure of the DataSet

# In[ ]:


infos.columns = ['Number of RTs','Retweets from User','Follower','Origin user']
infos


# In[ ]:


# to check if follows up level user
infoResult = []
for index, row in infos.iterrows():
  numRt = row['Number of RTs']
  userHandle = row['Follower']
  originUser = row['Origin user']
  for index, rowf in final.iterrows():
    userHandlef = rowf[0]
    originUserf = rowf[4]
    if userHandlef == userHandle and originUserf == originUser:
      print('is in followers')
      infoResult.append([userHandlef,originUserf,numRt])


# In[ ]:


infoResult = pd.DataFrame(infoResult)
infoResult


# In[ ]:


# count number of RT for each user
final['key'] = final[0] + final[1]
final


# In[ ]:


final['RT from user'] = final['key'].map(final['key'].value_counts())
final


# In[ ]:


# to check if follows up level user
userSheet = []
for index, row in infoResult.iterrows():
  numRt = row[2]
  userHandle = row[0]
  for index, rowf in final.iterrows():
    userHandlef = rowf[0]
    originUserf = rowf[1]
    RTfromUser = rowf['RT from user']
    if userHandlef == userHandle:
      print('found something')
      userSheet.append([numRt,RTfromUser,userHandlef,originUserf])


# In[ ]:


userSheet = pd.DataFrame(userSheet)
userSheet.columns = ['follower total number of retweets','number of retweets from origin user','Follower','Origin User']
userSheet


# In[ ]:


# Save the information recolected
userSheet.to_excel("Output_Variables/retweetersSheet_"+str(today)+".xlsx",sheet_name='retweeters')


# In[ ]:


retweetSheet = []
for index, rowf in final.iterrows():
  RtId = rowf[2]
  RTText = rowf[3]
  originUserf = rowf[1]
  userHandlef = rowf[0]
  originlTweetId = rowf[6]
  retweetSheet.append([RtId,RTText,originUserf,userHandlef,originlTweetId])


# In[ ]:


retweetSheet = pd.DataFrame(retweetSheet)
retweetSheet.columns = ['Retweet ID','Retweet Text','Author/Origin User','Follower','Original tweet ID']
retweetSheet


# In[ ]:


# Save the information recolected
retweetSheet.to_excel("Output_Variables/retweetsSheet_"+str(today)+".xlsx",sheet_name='retweets')


# In[ ]:




