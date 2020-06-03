import discord
from discord.ext import commands
import requests
import db
import pymysql
import random


pstart = []
plegend = [] 
pmythical = []
palolan = [] 
pevo2 = []
pevo3 = []
pevo1 = []
pokeserverspawntimer = []
pokeserverpokemonname = []
defaultpref = ['poke']
bot = commands.Bot(command_prefix= defaultpref[0])

class Pokemon(commands.Cog):

    def __init__ (self,bot):
        self.bot = bot

    async def getbalance(self,ctx,author):
        balance = db.GetBalance(self,author.id)
        embed = discord.Embed(title="Balance " + author.name,description="Your Balance is " + str(balance[0]))
        await ctx.send(embed=embed)

    async def startgame(self,ctx,author):
        checkuser = db.CheckUser(self,author.id,"rcount")
        if checkuser > 0:
            embed = discord.Embed(title="Pick Pokemon " + author.name,description="Pick Your Starter Pokemon Using " + defaultpref[0] + "pick <pokemon>")
            embed.add_field(name="Starter Pokemon",value="Charmander|Squirtle|Bulbasaur",inline=True)
            await ctx.send(embed=embed)
        else:
            db.InputUser(self,author.id,author.name)
            embed = discord.Embed(title="Pick Pokemon " + author.name,description="Pick Your Starter Pokemon Using " + defaultpref[0] + "pick <pokemon>")
            embed.add_field(name="Starter Pokemon",value="Charmander|Squirtle|Bulbasaur",inline=True)
            await ctx.send(embed=embed)

    async def pickpokemon(self,ctx,author,pokemonname):
        checkuser = db.CheckUser(self,author.id,"")
        for cuser in checkuser:
            if cuser[3] is None:
                db.UpdateUserPokemon(self,author.id,pokemonname)
                embed = discord.Embed(title="Pokemon Select " + author.name,description=" Your Starter Pokemon Is " + pokemonname)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Pokemon Select " + author.name,description="Your Have Already Pokemon Starter")
                await ctx.send(embed=embed)

    async def catchpokemon(self,ctx,author,pokemonname):
        checkuser = db.CheckUser(self,author.id,"rcount")
        if checkuser > 0:
            for i in range(len(pokeserverpokemonname)):
                    if pokeserverpokemonname[i][0] == ctx.channel.id:
                        if pokeserverpokemonname[i][1] == pokemonname: 
                            await ctx.send("<@" + str(author.id) + "> You Got " + str(pokeserverpokemonname[i][1])   + " Level " + str(pokeserverpokemonname[i][2]) )
                            number = db.GetPokedex(self,author.id,"num") + 1
                            db.InsertPokeDex(self,number,author.id,str(pokeserverpokemonname[i][2]),10)
                            pokeserverpokemonname[i][1] = None
                            pokeserverpokemonname[i][2] = 0
                            pokeserverspawntimer[i][1] = random.randrange(1,20)
                        else:
                             await ctx.send("<@" + str(author.id) + "> Wrong Pokemon Name Try Another Name") 


        else:
            await ctx.send("<@" + str(author.id) + "> You Dont Start The Game Please Type " +defaultpref[0] + "start To Start The Game")



@bot.event
async def on_message(message):
    if message.content is not None:
        print(message.content)
        index = 0
        for i in range(len(pokeserverspawntimer)):
                if pokeserverspawntimer[i][0] == message.channel.id:
                    if pokeserverspawntimer[i][1] > 0:
                        pokeserverspawntimer[i][1] = pokeserverspawntimer[i][1] - 1
                        break
                    else:
                        for j in range(len(pokeserverpokemonname)):
                            if pokeserverpokemonname[j][0] == message.channel.id:
                                if pokeserverpokemonname[j][1] is None:
                                    droprate = random.randrange(0.1,100.0)
                                    if droprate >= 48.9:
                                        pokename = pevo1[random.randrange(len(pevo1))]
                                    elif droprate >= 30.0:
                                        pokename = pevo2[random.randrange(len(pevo2))]
                                    elif droprate >= 15.0:
                                        pokename = pevo3[random.randrange(len(pevo3))]
                                    elif droprate >= 5.0:
                                        pokename = palolan[random.randrange(len(palolan))]
                                    elif droprate >= 1.0:
                                        pokename = pmythical[random.randrange(len(pmythical))]
                                    elif droprate >= 0.1:
                                        pokename = plegend[random.randrange(len(plegend))]
                                    pokeserverpokemonname[j][1] = pokename
                                    pokeserverpokemonname[j][2] = random.randrange(1,50)
                                    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokename}")
                                    data_json = response.json()
                                    embed = discord.Embed(title="Wild Pokemon Has Appeared", description="Catch Your Pokemon Using " + defaultpref[0] +"catch <pokemonname>")
                                    if data_json["sprites"]["front_default"] is not None:
                                        embed.set_image(url=data_json["sprites"]["front_default"])
                                    await message.channel.send(embed=embed)
                                    print(f"Pokemon {pokename} Spawn In Channel Id{pokeserverpokemonname[j][0]}")
                                    break
                            
                else:
                    index += 1
                        
        if index == len(pokeserverspawntimer):
            pokeserverspawntimer.append([message.channel.id,random.randrange(1,20)])
            pokeserverpokemonname.append([message.channel.id,None,0])
            index = 0

        
        
            
    
    await bot.process_commands(message)

@bot.event
async def on_ready():
    c = discord.Client()
    chanell = c.get_all_channels()
    for chn in chanell:
        print(chn)   


@bot.command(name="balance",help="See Your Balance")
async def balance(ctx):
    pokemon = bot.get_cog("Pokemon")
    await pokemon.getbalance(ctx,ctx.author)

@bot.command(name="start",help="To Start Your Game")
async def start(ctx):
    pokemon = bot.get_cog("Pokemon")
    await pokemon.startgame(ctx,ctx.author)

@bot.command(name="pick",help="Pick Pokemon Starter")
async def pick(ctx,pokemons):
    pokemon = bot.get_cog("Pokemon")
    await pokemon.pickpokemon(ctx,ctx.author,pokemons)

@bot.command(name="catch",help="Catch Wild Pokemon Spawn In Chat")
async def catch(ctx,pokename):
    pokemon = bot.get_cog("Pokemon")
    await pokemon.catchpokemon(ctx,ctx.author,pokename)
        

def pokemondata():
    r1 = requests.get("https://pokeapi.glitch.me/v1/pokemon/counts")
    request = r1.json()
    count = request["total"]
    for i in range(count):
        print(i)
        responseapi = requests.get("https://pokeapi.glitch.me/v1/pokemon/" + str(i))
        datajson = responseapi.json()
        try:
            print(datajson[0]["name"])
            if datajson[0]["starter"]:
                pstart.append(datajson[0]['name'])
            elif datajson[0]["legendary"]:
                plegend.append(datajson[0]['name'])
            elif datajson[0]["mythical"]:
                pmythical.append(datajson[0]['name'])
            for einfo in datajson[0]["family"]["evolutionLine"]:
                if len(einfo) == 2:
                    pevo1.append(einfo[0])
                    pevo2.append(einfo[1])
                elif len(einfo) == 3:
                    pevo1.append(einfo[0])
                    pevo2.append(einfo[1])
                    pevo3.append(einfo[2])
                else:
                    pevo1.append(einfo[0])
        except:
            print("error unknown data")

pokemondata()
bot.add_cog(Pokemon(bot))
bot.run('NzE2Mjk5NzU0MTg2NzM1NjM4.XtNVgQ.DxqZ-MM-fP7VOR1n0FATHB7XwhU')
