from datetime import datetime

from app.googlesearch import GoogleSearch
from app.psql import MiddleLayer
from app.config import DISCORD_TOKEN
import os
import discord
import logging

client = discord.Client()

logger = logging.getLogger(os.path.basename(__file__))


@client.event
async def on_ready():
    logger.info(f'{client.user.name} ready!')


@client.event
async def on_message(message):
    try:
        # if not from normal user, ignore.
        if message.author == client.user:
            return

        # respond to hi with hey
        if message.content.lower() == 'hi':
            response = "hey"
        else:
            body = message.content.split()
            #only !google and !recent supported
            if len(body) > 1:

                # get query
                query = ' '.join(body[1:])
                #establish DB connection
                connection = MiddleLayer()

                # google search.
                if '!google' == body[0]:
                    
                    logger.info("Google Search: {} by : {}".format(query, message.author.name))
                    
                    try:
                        connection.add_record((query,message.author.name,str(datetime.now())))
                        data = GoogleSearch.search(query)
                        response = "Google search results:\n" + data
                        
                    except Exception as e:
                        response = "Error : {}".format(str(e))
                        logger.info(response)
                
                #recent search
                elif '!recent' == body[0]:
                    
                    try:
                    
                        logger.info("Recent Search: {} by : {}".format(query, message.author.name))
                        data = connection.search_query(query=query)

                        if len(data)>0:

                            response = "Recent results:\n"

                            for ind,datas in enumerate(data):

                                response += str(ind+1) + ". Recent Search : {} done By: {}\n".format(datas[0], datas[1])

                        else:
                            response = "No Related Recent."
                            
                    except Exception as e:
                        response = "Error : {}".format(str(e))
                        logger.info(response)
                else:
                    response = "Not supported"
            else:
                response = "Not supported"
                
        await message.channel.send(response)
        
    except Exception as e:
        msg = "Some Error occurred: {}".format(str(e))
        logger.info(msg)
        await message.channel.send(msg)
        
client.run(DISCORD_TOKEN)