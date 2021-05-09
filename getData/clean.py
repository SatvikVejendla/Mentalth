import tensorflow as tf
import numpy as np
from tensorflow import keras
import pandas as pandas
import re
import ftfy
from nltk.corpus import stopwords
from nltk import PorterStemmer
import nltk

df = pandas.read_csv("./data.csv")

df = df.drop(["id","conversation_id","created_at","date","time","timezone","user_id","username","name","place","language","mentions","urls","photos","replies_count","retweets_count","likes_count","hashtags","cashtags","link","retweet","quote_url","video","thumbnail","near","geo","source","user_rt_id","user_rt","retweet_id","reply_to","retweet_date","translate","trans_src","trans_dest"], axis=1)

data = df.to_numpy()

def clean_tweets(tweets):
    cleaned_tweets = []
    for tweet in tweets:
        tweet = str(tweet)
        # if url links then dont append to avoid news articles
        # also check tweet length, save those > 10 (length of word "depression")
        if re.match("(\w+:\/\/\S+)", tweet) == None and len(tweet) > 10:
            #remove hashtag, @mention, emoji and image URLs
            tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|(\#[A-Za-z0-9]+)|(<Emoji:.*>)|(pic\.twitter\.com\/.*)", " ", tweet).split())
            
            #fix weirdly encoded texts
            tweet = ftfy.fix_text(tweet)
            

            #remove punctuation
            tweet = ' '.join(re.sub("([^0-9A-Za-z \t])", " ", tweet).split())

            #stop words
            stop_words = set(stopwords.words('english'))
            word_tokens = nltk.word_tokenize(tweet) 
            filtered_sentence = [w for w in word_tokens if not w in stop_words]
            tweet = ' '.join(filtered_sentence)

            #stemming words
            tweet = PorterStemmer().stem(tweet)
            
            cleaned_tweets.append(tweet)

    return cleaned_tweets

def first(i):
    return i[0]
data = list(map(first, data))

data = clean_tweets(data)


data = "\n".join(data)



f = open("data/data.txt", "w", encoding='utf-8')
f.write(data)
f.close()



def sixth(i):
    return i[5]
df2 = pandas.read_csv("./randomtweets.csv")

data2 = df2.to_numpy()

data2 = data2[:60141]

data2 = list(map(sixth, data2))

data2 = clean_tweets(data2)

data2 = "\n".join(data2)




f = open("data/data2.txt", "w", encoding='utf-8')
f.write(data2)
f.close()
