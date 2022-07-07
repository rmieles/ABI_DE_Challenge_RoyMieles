import snscrape.modules.twitter as sntwitter
import pandas as pd
from unicodedata import normalize

query = ["BcoBolivariano until:2022-06-10 since:2022-06-02 -filter:links"]

column = ['Id','Fecha','UserName','Institucion','Texto']


def get_tweets(query):
    data = []
    n = 0
    for banco in query:
        print(banco)
        for tweet in sntwitter.TwitterSearchScraper(banco).get_items():
            
            if(tweet.user.username != 'BcoBolivariano' and tweet.user.username != 'superbancosEC' and tweet.user.username != 'BancoGuayaquil' and tweet.user.username != 'BancoPacificoEC' ):
                
                data.append([n, tweet.date, tweet.user.username, banco.split()[0], normalize( 'NFC', tweet.content)])

                n += 1

                TweetsDf = pd.DataFrame(data, columns=column)
    
    return TweetsDf


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
