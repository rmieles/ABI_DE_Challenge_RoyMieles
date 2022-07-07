import snscrape.modules.twitter as sntwitter
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from unicodedata import normalize
from sentiment_analysis_spanish import sentiment_analysis

#Instanciamos el objeto de procesamiento de lenguaje natural
sentiment = sentiment_analysis.SentimentAnalysisSpanish()

pd.set_option('display.max_colwidth', 1)

#query = ["BcoBolivariano until:2022-06-10 since:2020-06-10 -filter:links",
#         "BancoGuayaquil until:2022-06-10 since:2020-06-10 -filter:links",
#         "BancoPacificoEC until:2022-06-10 since:2020-06-10 -filter:links"]

query = ["BcoBolivariano until:2022-06-10 since:2022-06-02 -filter:links"]

column = ['Id','Fecha','UserName','Institucion','Texto']

data = []

n = 0

for banco in query:
    print(banco)
    for tweet in sntwitter.TwitterSearchScraper(banco).get_items():
        
        if(tweet.user.username != 'BcoBolivariano' and tweet.user.username != 'superbancosEC' and tweet.user.username != 'BancoGuayaquil' and tweet.user.username != 'BancoPacificoEC' ):
            
            data.append([n, tweet.date, tweet.user.username, banco.split()[0], normalize( 'NFC', tweet.content)])

            n += 1

            TweetsDf = pd.DataFrame(data, columns=column)
    


print(TweetsDf)

cleanTxt(TweetsDf.query("UserName == 'Ruiz12Evelyn'")['Texto'][0])


TweetsDf.to_csv('OpinionesBancarias_df.csv', sep = ";", encoding= 'UTF-8')

def deep_search(needles, haystack):
    found = {}
    if type(needles) != type([]):
        needles = [needles]

    if type(haystack) == type(dict()):
        for needle in needles:
            if needle in haystack.keys():
                found[needle] = haystack[needle]
            elif len(haystack.keys()) > 0:
                for key in haystack.keys():
                    result = deep_search(needle, haystack[key])
                    if result:
                        for k, v in result.items():
                            found[k] = v
    elif type(haystack) == type([]):
        for node in haystack:
            result = deep_search(needles, node)
            if result:
                for k, v in result.items():
                    found[k] = v
    return found

    # Definimos una función que realice un preprocesamiento de los tweets recibidos
def cleanTxt(text):

    
    try:
        a = deep_search(["full_text"], text)
        print(a)
        text['full_text'] = a['full_text']
    except:
        text['full_text'] = text['text']
    
    text['text_with_stopwords'] = re.sub(r'@[A-Za-z0-9]+', '', text['text'])
    text['text_with_stopwords'] = re.sub(r'#', '', text['text_with_stopwords'])
    text['text_with_stopwords'] = re.sub(r'RT[\s]+','',text['text_with_stopwords'])
    text['text_with_stopwords'] = re.sub(r'https?:\/\/\S+','', text['text_with_stopwords'])
    text['text_with_stopwords'] = re.sub(r':','',text['text_with_stopwords'])
    #print('Texto original: ',text['text'])
    text['text_with_stopwords'] = re.sub(r'[^a-zA-Zá-ú]',' ', text['text_with_stopwords'])
    text['text_with_stopwords'] = text['text_with_stopwords'].lower()
    
    #text_split = text['text_with_stopwords'].split()
    #ps = PorterStemmer()
    #text_split = [ps.stem(word) for word in text_split if not word in set(stopwords.words('spanish'))] 
    
    #print('Texto limpiado: ',' '.join(text_split))
    #text['text_with_stopwords'] = ' '.join(text_split)
    text['score_with_stopwords'] = sentiment.sentiment(text['text_with_stopwords'])
    
    text['text_without_stopwords'] = re.sub(r'@[A-Za-z0-9]+', '', text['text'])
    text['text_without_stopwords'] = re.sub(r'#', '', text['text_without_stopwords'])
    text['text_without_stopwords'] = re.sub(r'RT[\s]+','',text['text_without_stopwords'])
    text['text_without_stopwords'] = re.sub(r'https?:\/\/\S+','', text['text_without_stopwords'])
    text['text_without_stopwords'] = re.sub(r':','',text['text_without_stopwords'])
    text['text_without_stopwords'] = re.sub(r'[^a-zA-Zá-ú]',' ', text['text_without_stopwords'])
    text['text_without_stopwords'] = text['text_without_stopwords'].lower()
    text['score_without_stopwords'] = sentiment.sentiment(text['text_without_stopwords'])
    
    return text