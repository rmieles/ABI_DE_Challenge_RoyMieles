#Import all the libraries that will be used by the pipeline
from asyncio import gather
from datetime import datetime
from urllib import response
import snscrape.modules.twitter as sntwitter
import pandas as pd
from unicodedata import normalize
import boto3


#Create a query to search tweets about BcoBolivariano
query = ["BcoBolivariano until:2022-06-10 since:2022-06-02 -filter:links"]

#Set the columns names for the dataSet
column = ['Id','Fecha','UserName','Institucion','Texto']

#Set function to get tweets from the query 
def get_tweets(query):
    
    #Set array to store the downloaded tweets
    data = []

    #Create id column
    n = 0

    #in case we have more than just one query we create a for loop to search tweets with every query
    for banco in query:

        #Print the actual query that will be executed
        print(banco)

        #Create a for loop to search tweets with the sncraper library using the twitter query
        for tweet in sntwitter.TwitterSearchScraper(banco).get_items():
            
            #We remove all the tweets made by the same banking entities to obtain only the opinion of the clients
            if(tweet.user.username != 'BcoBolivariano' and tweet.user.username != 'superbancosEC' and tweet.user.username != 'BancoGuayaquil' and tweet.user.username != 'BancoPacificoEC' ):
                

                data.append([n, tweet.date, tweet.user.username, banco.split()[0], normalize( 'NFC', tweet.content)])

                n += 1

                TweetsDf = pd.DataFrame(data, columns=column)
    
    return TweetsDf


def gather_data():
    s3_resource = boto3.resource('s3')
    date = datetime.now()
    filename = f'{date.year}/{date.month}/{date.day}/OpinionesBancarias_df_prueba.csv'
    response = s3_resource.Object(Bucket = 'PruebaAbInBev', key = filename).upload_file('/tmp/OpinionesBancarias_df_prueba.csv')
    
    return response

def lambda_handler(event, context):
    gather_data()


#--------------------------------------------------------------------------------
#Define a main function, the entry point of the program
if __name__ == '__main__':
    #This object handles Twitter authetification and the connection to Twitter Streaming API
    print("INICIO DE SCRIPT\n")
    TweetsDf = pd.DataFrame()
    TweetsDf = get_tweets(query)
    print(TweetsDf)
    TweetsDf.to_csv('OpinionesBancarias_df_prueba.csv', sep = ";", encoding= 'UTF-8')
#---------------------------------------------------------
