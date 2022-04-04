# Processing Unstructured Twitter Data using SQLite 
**Project description:**  Extrapolate and parse 1M Twitter tweets. Python and SQLite are used to process and clean the unstructured data, populate SQL tables with Twitter attributes and values and run SQL queries. This was my take home final project for the DePaul Database processing for large-scale analytics class. 

**Data Description:** The Twitter data was a .txt file which was available online and consisted of 1,000,000 lines of tweets. The tweets were organized in nested dictionaries (one dictionary for the tweet data and one dictionary for the user data). Sample data can be found here: [TwitterTweets.txt](https://github.com/eclark15/database-processing-analysis/files/8412892/TwitterTweets.txt). The input data is separated by a string “EndOfTweet” which serves as a delimiter. 


## 1. Create SQLite Tables, Open a DB Connection & Clean the Unstructured Data
### 1a. Create Empty SQL Tables  

Created 3 SQL tables: 
1. GeoTable - 
2. UserTable
3. TweetsTable

Sample: 
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

### 1b.   SQLite Table


```python
conn = sqlite3.connect('Final_Database.db')
c = conn.cursor()
wFD = urllib.request.urlopen('http://rasinsrv07.cstcis.cti.depaul.edu/CSC455/OneDayOfTweets.txt')

# Tweet table gets dropped first and created last (Referential Integirty)
c.execute('DROP TABLE IF EXISTS Tweets');
c.execute('DROP TABLE IF EXISTS User');
c.execute('DROP TABLE IF EXISTS Geo');
c.execute(GeoTable)
c.execute(UserTable)
c.execute(TweetsTable)
```

### 1c. Populate SQL Tables


Write python code to read through the Assignment4.txt file and populate your table from part a.  Make sure your python code reads through the file and loads the data properly (including NULLs). 



## 2. Query Interface 
Now that the index has been generated and saved, we are able to move into the queryRetrieve.py file. queryRetrieve.py imports the dictionary indexes and is used to return the most relevant web pages associated with a user’s search query. 

### 2a. Calculating the Cosine Similarity
A query is processed based on its relevant terms and evaluated on its associated TF-IDF values using the previously generated index dictionaries. Next, I converted the relevant query words and TF-IDF values into a DataFrame to manually calculate the cosine similarity using numpy for every web page. 

```python
def getCosineSimiliarty(postingsDictQueryDFClean, queryList):   #computing cosine similarity between our query and all website pages
    import numpy as np
    from numpy.linalg import norm
    
    def cosine_similarity(QueryVect, DocVect):                  #returns cosine similarity when 2 lists are entered 
        cosine = np.dot(QueryVect,DocVect)/(norm(QueryVect) * norm(DocVect))
        return cosine

```
## 3. Tests and Results
### 3a. Query #1 'internships in marketing or design'
In the table, the top 7 pages that the system calculated as being the most relevant based on the user’s search query. However, we can see that only Search Result Number 1,2,3 and 6 are actually relevant while search result numbers 4, 5, and 7 are not relevant. 

<img width="633" alt="queryTest_internships" src="https://user-images.githubusercontent.com/50348032/160932829-75c72d00-7fdb-4b78-a462-0c25a1e66dc2.png">

### 3b. Query #2 'environmental sustainability responsibility'
<img width="626" alt="queryTest_sustainability" src="https://user-images.githubusercontent.com/50348032/160932842-6a392452-855b-4663-9534-fd0ff035688e.png">

## 3. Further Improvements and Enhancements






