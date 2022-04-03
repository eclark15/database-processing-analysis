# database-processing-analysis
Database processing for large-scale analytics to extrapolate 1M Twitter tweets. Using Python and SQLite to process unstructured data and run SQL queries 
## Search Engine Retrieval System 

**Project description:** 

In this IR project, I created a search engine retrieval system from scratch that crawls the web pages in the domain https://www.bosch.us and returns the top 7 most relevant web pages based on the user’s search query. The base implementation includes a **VSM (vector-space model) using TF-IDF with Cosine similarity** which is used for matching queries and indexed documents. In addition, the system includes the primary elements of a document retrieval system such as a web crawler, indexer, and query processing components. 

The search retrieval system consists of two python files, one that contains the index of the website ([final_index.py](https://github.com/eclark15/intelligent_information_retrieval/blob/c6f9a69339e48d05afc0749053f34ca27af04d95/python_files/final_index.py)) and the second file which retrieves the user’s search query and returns the relevant web pages ([queryRetrieve.py](https://github.com/eclark15/intelligent_information_retrieval/blob/c6f9a69339e48d05afc0749053f34ca27af04d95/python_files/queryRetrieve.py)). Feel free to refer to the [README.txt](https://github.com/eclark15/intelligent_information_retrieval/blob/c509d128820c353551ca44f0741f26c7edd1a641/python_files/README.txt) file for further details. 

![gif](https://user-images.githubusercontent.com/50348032/160918448-38bbac51-cba0-4f9c-b353-c022873711f3.gif)

## 1. Creating a Website Index 
### 1a. Identify and Collect Relevant Web Pages

First, using final_index.py I collected the list of relevant URLs on bosch.us. The system crawls every website page recursively using a `crawl()` function and gathers the web page links using Beautiful Soup while simultaneously cleaning the URLs and removing unwanted pages such as PDFs.

```python
def crawl(url):                            #crawls all web pages to discover all page links and content 
    webPageID = urlIndex(url)  
    print(webPageID, url)                  
    soup, url = gatherPageLinks(url)                  
    gatherPageText(url, soup, webPageID)      
    visited.append(url)                     
    
    for link in links:            
        if link not in visited:   
            try:
                crawl(link)                #recursively crawl all pages 
            except:
                pass
```

### 1b. Gather, Preprocess, and Store Relevent Words 

Next, `gatherPageText()` was used to gather the relevant text from each page. By passing in the Beautiful Soup class, I was able to parse through the webpages and exclude any tags that do not contain relevant text. 

Additionally, preprocessing tasks were performed such as removing stop words (using NLTK), creating a dictionary to accumulate each full word and its token, and lastly creating a `postingDict` that will manually calculate the TF (term frequency) values for each word on each page. 

```python
porter = PorterStemmer()
for word in fullWords:                      
    stemmedWord = porter.stem(word)        
    if word not in termTokenDict.keys(): 
        termTokenDict.update({word : stemmedWord})                     #updating dictionary with full word + token word
    
    if stemmedWord not in postingsDict.keys():                         #brand new word in our postings dict
        postingsDict.update({stemmedWord : {webPageID : [1, 'idf']}})  #stemmed word : {webpageID :[TF, IDF], DocFreq : DF}
    
    elif webPageID not in postingsDict[stemmedWord].keys():            #if the term is in dictionary but has not appeared in current document
        postingsDict[stemmedWord][webPageID] = [1, 'idf']
        
    else:
        TF = postingsDict[stemmedWord][webPageID][0]                   #updating the term frequency value if the term has appeared on the current page already 
        TF = TF + 1 
        postingsDict[stemmedWord][webPageID][0] = TF
```

### 1c. Using TF-IDF to Identify Word Importance 

Once all the pages have been crawled and each word is sorted into the dictionaries, I can calculate the DF (document frequency) and IDF (inverse document frequency) values. The TF-IDF values will be used, in this case, to quantify the importance of each word on our web pages. 

Each DF, IDF calculation is done manually. The DF values by finding the length of the `postingsDict` and the IDF values by using the following equation: `IDF = math.log((numofPages/DF), 2)`. 

The IDF value is then stored into our `postingsDict`. An example of one instance of the `postingsDict` will have the following format: 
`'scale': {8123: 8.98370619265935, 3692: 4.491853096329675, 'DocFreq': 2, 'IDF': 4.491853096329675} `

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






