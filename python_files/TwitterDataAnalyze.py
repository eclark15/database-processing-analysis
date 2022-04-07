# -*- coding: utf-8 -*-
"""

@author: emily
"""

import json, sqlite3, urllib, time

# creating empty SQL tables
GeoTable = '''CREATE TABLE Geo (
                 type        VARCHAR(140),
                 ID          NUMBER(20),
                 longitude NUMBER(10),
                 latitude NUMBER(10),
                 CONSTRAINT Geo_PK  PRIMARY KEY (ID)
              );'''


UserTable = '''CREATE TABLE User (
                 ID          NUMBER(20),
                 name        VARCHAR(140),
                 screen_name VARCHAR(200),
                 description VARCHAR(500),
                 friends_count Number(100),
                 CONSTRAINT User_PK  PRIMARY KEY (id)
              );'''

TweetsTable = '''CREATE TABLE Tweets (
                 id          NUMBER(20),               
                 Created_At       DATE,
                 Text             VARCHAR(400),
                 Source VARCHAR(200) DEFAULT NULL,
                 In_Reply_to_User_ID NUMBER(20),
                 In_Reply_to_Screen_Name VARCHAR(60),
                 In_Reply_to_Status_ID NUMBER(20),
                 Retweet_Count    NUMBER(10),
                 Contributors     VARCHAR(200),
                 user_id     NUMBER(20),
                 geo_id      NUMBER(20),
                 CONSTRAINT Tweets_PK  PRIMARY KEY (id)
                 CONSTRAINT Tweets_FK1 FOREIGN KEY (user_id)
                     REFERENCES User(ID)
                 CONSTRAINT Tweets_FK2 FOREIGN KEY (geo_id)
                     REFERENCES Geo(ID)
              );'''

# opening a DB connection on local machine 
conn = sqlite3.connect('Final_Database.db')
c = conn.cursor()
wFD = urllib.request.urlopen('http://rasinsrv07.cstcis.cti.depaul.edu/CSC455/OneDayOfTweets.txt')

# drop all tables and load 3 empty SQL tables into DB 
c.execute('DROP TABLE IF EXISTS Tweets');
c.execute('DROP TABLE IF EXISTS User');
c.execute('DROP TABLE IF EXISTS Geo');
c.execute(GeoTable)
c.execute(UserTable)
c.execute(TweetsTable)


def processTweets(wFD):  # processing tweets and populating SQL tables 

    fdErr = open('Final_error.txt', 'w', errors = 'replace')
    tweetBatch = []   # collect batch data for Tweets table 
    userBatch = []    # collect batch data for User table 
    geoBatch = []     # collect batch data for Geo table
    loadCounter = 0   # keeping count for our batching 

    for i in range(500000):  # process 500,000 lines of tweets
        
        if i % 10000 == 0:   # print a message every 10,000th tweet 
            print ("Processed " + str(i) + " tweets")
        
        try:     
            line = wFD.pop(0)  # remove 1st item from the list 
            tweetDict = json.loads(line.decode('utf8')) # processing one tweet at a time 
            loadCounter += 1        
            
            ### Collect 1 row/tweet for Tweets table ###
            newRowTweet = []  # store text to be inserted for Tweet data
            tweetKeys = ['id', 'created_at', 'text', 'source', 'in_reply_to_user_id',
                         'in_reply_to_screen_name', 'in_reply_to_status_id', 'retweet_count', 
                         'contributors']
            
            for key in tweetKeys:     # For each attribute key we want for the Tweets table  
                if tweetDict[key] == 'null' or tweetDict[key] == '':
                    newRowTweet.append(None)   # ensure a proper NULL is added for blank values 
                else:
                    newRowTweet.append(tweetDict[key]) # if value is present add it to the newRowTweet list 
            
            ### Collect 1 row/tweet for User table ###
            newRowUser = [] # hold individual values of to-be-inserted row for user table
            userKeys = ['id', ['user']['name'], ['user']['screen_name'], ['user']['description'], ['user']['friends_count']]
            
            for key in userKeys:     # For each attribute key we want for the User table  
                if userKeys[key] == 'null' or tweetDict[key] == '':
                    newRowUser.append(None)   # ensure a proper NULL is added for blank values 
                else:
                    newRowUser.append(tweetDict[key]) # if value is present add it to the newRowUser list 
    
            ### Collect 1 row/tweet for Geo table ### 
            newRowGeo = []    # store text to be inserted for Geo data
            geoKeys = [['geo']['type'], 'id', ['geo']['coordinates'][0], ['geo']['coordinates'][1]]
            
            for key in geoKeys:     # For each attribute key we want for the Geo table  
                if geoKeys[key] == 'null' or tweetDict[key] == '':
                    newRowGeo.append(None)   # ensure a proper NULL is added for blank values 
                else:
                    newRowGeo.append(tweetDict[key]) # if value is present add it to the newRowGeo list 
            
            
            # add full new row to each table batch
            tweetBatch.append(newRowTweet)
            userBatch.append(newRowUser)
            geoBatch.append(newRowGeo)
            
            # once 500 tweets have been processed or there are no more tweets to process, add data to SQL tables
            if loadCounter > 500 or len(wFD) == 0:
                c.executemany ('INSERT OR IGNORE INTO Tweets VALUES(?,?,?,?,?,?,?,?,?,?,?)', tweetBatch)
                tweetBatch = [] # Reset list of batched tweet data

                c.executemany ('INSERT OR IGNORE INTO User VALUES(?,?,?,?,?)', userBatch)
                userBatch = [] # Reset list of batched user data 
                
                c.executemany ('INSERT OR IGNORE INTO Geo VALUES(?,?,?,?)', geoBatch)
                geoBatch = []  # Reset list of batched geo data 
                
                loadCounter = 0 # reset batch counter 
                    
        except (ValueError, KeyError, UnicodeEncodeError, TypeError):  # Handle the error of JSON parsing
            fdErr.write(line.decode() + '\n')     



# checking that all table data has been filled in 
c.execute('select Count(*) from Tweets').fetchall()
c.execute('select Count(*) from User').fetchall()
c.execute('select Count(*) from Geo').fetchall()


## running SQL queries ## 

# Find tweets where tweet id_str contains “55” or “88” anywhere in the column
start1 = time.time()
c.execute("select id, text from Tweets WHERE id LIKE '%88%' OR '%55%'").fetchall()
stop1 = time.time()
print("Diff " + str(stop1-start1))

# Find how many unique values are there in the “in_reply_to_user_id” column
start1 = time.time()
c.execute('SELECT COUNT(DISTINCT In_Reply_to_User_ID) from Tweets').fetchall()
stop1 = time.time()
print("Diff " + str(stop1-start1))

# Find the tweet(s) with the shortest, longest text message.
start1 = time.time()
c.execute("SELECT Text FROM Tweets GROUP BY Text HAVING LENGTH(Text) = (SELECT MAX(LENGTH(Text)) FROM Tweets)").fetchall()
c.execute("SELECT Text FROM Tweets GROUP BY Text HAVING LENGTH(Text) = (SELECT MIN(LENGTH(Text)) FROM Tweets)").fetchall()
stop1 = time.time()
print("Diff " + str(stop1-start1))

c.execute("SELECT AVG(LENGTH(Text)) FROM Tweets").fetchall()
#the average text length is a decimal 

# Find the average longitude and latitude value for each username. 
start1 = time.time()
c.execute("SELECT AVG(longitude), AVG(latitude) FROM Geo GROUP BY ID;").fetchall()
stop1 = time.time()
print("Diff " + str(stop1-start1))

# Find how many known/unknown locations there were in total (e.g., 50,000 known, 950,000 unknown,  5% locations are available)
start1 = time.time()
c.execute("select COUNT(*) FROM Tweets WHERE geo_id IS NULL").fetchall()
stop1 = time.time()
print("Diff " + str(stop1-start1))


