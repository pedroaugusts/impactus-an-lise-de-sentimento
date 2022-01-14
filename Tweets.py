#importar as bibliotecas

from nltk import word_tokenize
import nltk
import re
import pandas as pd
from tweepy.streaming import Stream
from tweepy.auth import OAuthHandler
import tweepy as tw
from textblob import TextBlob as tb
from googletrans import Translator



#chaves de acesso
api_key = 'km5KInWgcQADOZW6PbWeyoxdG'
api_key_secret = 'oEEhZwEQakFGNuOVWM6BjDfQQ6HDLzD1MGd6hon9CwZuEqWP5E'
acess_token = '1240425057890992130-9dlaCrTp8FDTupcafVno9HDNA8ryLL'
acess_token_secret = '4fkm975M2PlXngog76G462SVhPiSGsTppipJbhFUNuQAS'

# objeto de autorização de acesso
auth = tw.OAuthHandler(api_key,api_key_secret)


palavras_procuradas = ["Petz" ,"petz", "PETZ"]
#criacao do obj tipo api
api = tw.API(auth)

# Open/create a file to append data to



lista_de_tweets = []

for tweet in tw.Cursor(api.search_tweets, q= palavras_procuradas , lang = "pt-br", result_type = "recent").items(500):
    lista_de_tweets.append(tweet.text)



df = pd.DataFrame(columns = ['Textos'], data = lista_de_tweets)
translator = Translator()

df['tradução'] = df['Textos'].apply(lambda x: translator.translate(x, dest='en').text)

print()
