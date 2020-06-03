import discord
from discord.ext import commands
import requests
import db
import pymysql
import random
import google_images_search

pokemonname = [] 
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
                            print("correct")
        else:
            await ctx.send("You Dont Start The Game Please Type " +defaultpref[0] + "start To Start The Game")



@bot.event
async def on_message(message):
    if message.content is not None:
        print(message.content)
        print(pokeserverspawntimer)
        print(pokeserverpokemonname)
        index = 0
        indexpokemon = 0
        for i in range(len(pokeserverspawntimer)):
                if pokeserverspawntimer[i][0] == message.channel.id:
                    if pokeserverspawntimer[i][1] > 0:
                        pokeserverspawntimer[i][1] = pokeserverspawntimer[i][1] - 1
                        break
                    else:
                        for j in range(len(pokeserverpokemonname)):
                            if pokeserverpokemonname[j][0] == message.channel.id:
                                if pokeserverpokemonname[j][1] is None:
                                    pokename = pokemonname[random.randrange(len(pokemonname))]
                                    pokeserverpokemonname.append([str(message.channel.id),pokename])
                                    response = requests.get("https://pokeapi.co/api/v2/pokemon/"+pokename)
                                    data_json = response.json()
                                    for namepokemon in data_json['sprites']:
                                        print(namepokemon['front_default'])
                                    print(pokeserverpokemonname[0][1])
                                    embed = discord.Embed(title="Wild Pokemon Has Appeared", description="Catch Your Pokemon Using " + defaultpref[0] +"catch <pokemonname>")
                                    embed.set_image()
                                    await message.channel.send(embed=embed)
                                    await message.channel.send("pokemon name " + pokeserverpokemonname[0][1] )
                                    break
                            else:
                                indexpokemon += 1
                else:
                    index += 1
                        
        if index == len(pokeserverspawntimer):
            pokeserverspawntimer.append([message.channel.id,random.randrange(1,20)])
            
        if indexpokemon == len(pokeserverpokemonname):
            pokeserverpokemonname.append([message.channel.id,pokemonname[random.randrange(len(pokemonname))]])
            print(pokeserverpokemonname[0][1])
            embed = discord.Embed(title="Wild Pokemon Has Appeared", description="Catch Your Pokemon Using " + defaultpref[0] +"catch <pokemonname>")
            await message.channel.send(embed=embed)
            await message.channel.send("pokemon name " + pokeserverpokemonname[0][1] )
                
                
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
     response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=964")
     data_json = response.json()
     for namepokemon in data_json['results']:
         pokemonname.append(namepokemon['name'])

pokemondata()
bot.add_cog(Pokemon(bot))
bot.run('NzE2Mjk5NzU0MTg2NzM1NjM4.XtNVgQ.DxqZ-MM-fP7VOR1n0FATHB7XwhU')

