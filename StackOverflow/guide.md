# Installation
We first need to install Scrapy and PyMongo libraries along with MongoDB.
```
$ pip install Scrapy
```
```
$ pip install PyMongo
```
Visit <a href="https://www.mongodb.com/docs/manual/installation/">MongoDB</a> for installation help.

# Scrapy Project
```
$ scrapy startproject stack [<folder_path>]
```
This creates a number of files and folders that includes a basic boilerplate to get started with a new Scrapy project.

## Specify Data
Update the StackItem class inside "items.py" file to collect the title and url for each question.

## Create the Spider
Create a file called stack_spider.py in the "spiders" directory which will be used to find the exact data we're looking for.
Define a class that inherits from Scrapy's Spider and add the required attributes such as:
<ul>
<li>name</li>
<li>allowed_domains</li>
<li>start_urls</li>
</ul>

## XPath Selectors
Get the XPath for grabbing all questions by using Inspect Element on any question on the StackOverflow website. Test out all the XPaths in the Javascript Console.

## Extract the Data
Iterate through the 'questions' and assign the 'title' and 'url' values from the scraped data. In the "stack" directory, run the following command to render the output to a JSON file:
```
$ scrapy crawl stack -o items.json -t json
```

# Storing Data in MongoDB
Connect to localhost:27017 using MongoDB Compass and create a new databse "stackoverflow" with a collection "questions". Edit the settings.py file accordingly.

## Pipeline Management
Connect the spider and the database through a pipeline. Edit the pipelines.py file to establish a connection the database, unpack the data and save it to the databse.

# Test
Run the following command within the "stack" directory:
```
$ scrapy crawl stack
```
Open the collection in MongoDB Compass, you will be able to see the crawled data and you can export the data as per your requirements.
