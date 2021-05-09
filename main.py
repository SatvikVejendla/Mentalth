import warnings
warnings.filterwarnings("ignore")

import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Conv1D, Dense, Input, LSTM, Embedding, Dropout, Activation, MaxPooling1D
import numpy as np
from gensim.models import KeyedVectors
from keras.models import Model, Sequential
import tensorflowjs as tfjs
import pickle

import os
import discord
import json
from dotenv import load_dotenv
import time
import sys


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
tokenizer = 0
word2vec = 0


with open('state/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

with open('state/word2vec.pickle', 'rb') as handle:
    word2vec = pickle.load(handle)

model = keras.models.load_model("state/depression/keras/model.h5")


word_index = tokenizer.word_index


users = {}

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return


    

    global users
    if (users.get(str(message.author.id))):
        n = 0
    else:

        d = {
            "score": 0,
            "messages": []
        }
        users[str(message.author.id)] = d
    
    

    txt = message.content


    sequences_d = tokenizer.texts_to_sequences([txt])
    data_d = pad_sequences(sequences_d, maxlen=140)

    output = model.predict(data_d)
    print(output)
    if(output > 0.7):

        messages = users[str(message.author.id)]["messages"]
        for i in messages:
            if (round(time.time() * 1000) - i["timeStamp"] > 259200000):
                users[str(message.author.id)]["messages"].remove(i)

        users[str(message.author.id)]["messages"].append({
            "content": txt,
            "timeStamp": round(time.time() * 1000),
        })

        users[str(message.author.id)]["score"]+=1

        for i, val in users.items():

            if (val["score"] > 2):
                embed=discord.Embed(title="Thinking about suicide?", description="There's plenty of reasons not to commit suicide. Here are some resources:", color=0xFF5733)
                embed.add_field(name="Suicide Prevention Lifeline", value="Call 800-273-8255 to talk to people about your situation. There are plenty of people willing to help make it better.", inline=False)
                embed.add_field(name="For people outside the US", value="[International Association for Suicide Prevention](http://www.iasp.info/)", inline=False)
                embed.add_field(name="Suicide Prevention Extra Resources", value="[American Foundation for Suicide Prevention](https://afsp.org/suicide-prevention-resources)\n[Suicide Prevention Resource Guide](https://www.healthline.com/health/mental-health/suicide-resource-guide)\n[Suicide Prevention Resource Center](https://www.sprc.org/)\n[NJ Department of Mental Health and Addiction Services](https://www.state.nj.us/humanservices/dmhas/resources/services/prevention/suicide.html)", inline=False)
                embed.set_thumbnail(url="https://www.georgetownbehavioral.com/sites/default/files/georgetown-suicide-awareness.jpg")
                
                await message.channel.send(embed=embed)



    
client.run(TOKEN)

