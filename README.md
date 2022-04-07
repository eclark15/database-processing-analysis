# Processing Unstructured Twitter Data using SQLite 
**Project description:**  Extrapolate and parse 1M Twitter tweets. Python and SQLite are used to process and clean the unstructured data, populate SQL tables with Twitter attributes and values and run SQL queries. This was my take home final project for the DePaul Database processing for large-scale analytics class. 

**Data Description:** The Twitter data was a .txt file which was available online and consisted of 1,000,000 lines of tweets. The tweets were organized in nested dictionaries (one dictionary for the tweet data and one dictionary for the user data). Sample data can be found here: [TwitterTweets.txt](https://github.com/eclark15/database-processing-analysis/files/8412892/TwitterTweets.txt). The input data is separated by a string “EndOfTweet” which serves as a delimiter. 


## 1. Create SQLite Tables, Open a DB Connection & Clean the Unstructured Data
### 1a. Create Empty SQL Tables  

Created 3 SQL tables: 
1. **Geo** - table to store variables related to the user's geo-coordinates   
2. **User** - table to store variables related to the user
3. **Tweets** - table to store variables related to the tweet 

**Sample Table:**
```python

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

### 1c. Populate SQL Tables 
Used JSON to decode and load all of the tweet information into a dictionary called `tweetDict`.  This is done using batching to load 500 tweets at a time to save on memory space. The python code reads through all of the Twitter data and loads it properly including NULLs when there is any missing data. 


**Sample Python Code for Tweets Table:**
```python
tweetKeys = ['id', 'created_at', 'text', 'source', 'in_reply_to_user_id',
            'in_reply_to_screen_name', 'in_reply_to_status_id', 
            'retweet_count', 'contributors']


if loadCounter < 500: # Batching 500 at a time
            tweetBatch.append(newRowTweet)
        else:
            c.executemany ('INSERT OR IGNORE INTO Tweets VALUES(?,?,?,?,?,?,?,?,?,?,?)', tweetBatch)
            tweetBatch = [] # Reset the list of batched tweets
```

## 2. Write & Execute SQL Queries 
Now that the unstructured Twitter data has been nicely placed into each of our three SQL tables, we are able to analyze this data using several SQL queries. 

### 2a. Execute SQL Queries to Learn About our Twitter Data

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
## 3. Add New Columns to Tables 
### 3a. 
DESCRIPTION

### 3b. Add two new columns (“name” and “screen_name”) from User table

## 3. Further Improvements and Enhancements






