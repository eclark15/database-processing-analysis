# Process & Analyze Unstructured Twitter Data using Python & SQLite 
**Project description:**  Extrapolate and parse 1M Twitter tweets. Python and SQLite are used to process and clean the unstructured data, populate SQL tables with Twitter attributes and values and run SQL queries. Batching is used to save on memory space .This was part of my take home final project for the DePaul Database processing for large-scale analytics class. 

**Data Description:** The Twitter data was a .txt file which was available online and consisted of 1,000,000 tweets. The tweets were organized in nested dictionaries (the internal dictionary for the tweet data and the nested dictionaries for the user and geo data). Sample data can be found here: . The input data is separated by a string “EndOfTweet” which serves as a delimiter. 


## 1. Create SQLite Tables & Open a DB Connection
### 1a. Create Empty SQL Tables  

Created 3 SQL tables: 
1. **Geo** - table to store variables related to the user's geo-coordinates   
2. **User** - table to store variables related to the user
3. **Tweets** - table to store variables related to the tweet 

**Created SQL Tables:**
```python

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
```

### 1b. Open a DB Connection
* Opened a database connection called Final_Database.db
* Created a cursor class to run SQL commands in the database session
* Save Twitter data in the variable wFD 
* Cleared all tables in case they already exist in the DB
* Add empty tables to the DB 


```python
conn = sqlite3.connect('Final_Database.db')
c = conn.cursor()
wFD = urllib.request.urlopen('http://rasinsrv07.cstcis.cti.depaul.edu/CSC455/OneDayOfTweets.txt')

c.execute('DROP TABLE IF EXISTS Tweets'); 
c.execute('DROP TABLE IF EXISTS User');
c.execute('DROP TABLE IF EXISTS Geo');
c.execute(GeoTable)
c.execute(UserTable)
c.execute(TweetsTable)
```

## 2. Clean the Unstructured Twitter Data & Populate the SQL Tables 
Created a function called `processTweets()` which takes the unprocessed Twitter data as an input and uses batching to load the data into the SQL tables once 500 tweets have been processed. 

### 2a. Clean & Process the Data 
In this process, one tweet is collected at a time, decoded via JSON, and stored in the variable `tweetDict`. From here, the list of attributes we wish to populate our SQL tables is created and its corresponding value is added into our batching list. 

**Python Code for Table:**
```python
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
```

### 2b. Populate SQL Tables using Batching 
Once we have processed 500 tweets, the statement `executemany` is used to insert the collect values into the SQL tables.  


```python
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

```


## 3. Write & Execute SQL Queries 
Now that the unstructured Twitter data has been nicely placed into each of our three SQL tables, we are able to analyze this data using several SQL queries. 

### 3a. Execute SQL Queries to Learn About our Twitter Data

Some questions we might ask about this data… 
1. How many unique values are there in the “in_reply_to_user_id” column? 
2. What are the tweet(s) with the shortest and longest text message? 
3. What is the average longitude and latitude value for each username? 

Below you can see these query statements for each of these questions. I’ve also included code to track the query runtime which is important when working with large datasets to see if further optimization is needed. 

```python
# Question 1 
start1 = time.time()
c.execute('SELECT COUNT(DISTINCT In_Reply_to_User_ID) from Tweets').fetchall()
stop1 = time.time()
print("Diff " + str(stop1-start1))

# Question 2
start1 = time.time()
c.execute("SELECT Text FROM Tweets GROUP BY Text HAVING LENGTH(Text) = (SELECT MAX(LENGTH(Text)) FROM Tweets)").fetchall()
c.execute("SELECT Text FROM Tweets GROUP BY Text HAVING LENGTH(Text) = (SELECT MIN(LENGTH(Text)) FROM Tweets)").fetchall()
stop1 = time.time()
print("Diff " + str(stop1-start1))

# Question 3
start1 = time.time()
c.execute("SELECT AVG(longitude), AVG(latitude) FROM Geo GROUP BY ID;").fetchall()
stop1 = time.time()
print("Diff " + str(stop1-start1))

```

