import discord
from discord.ext import commands
import requests
import db
import pymysql
import random

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
        for serverpokemon in pokeserverpokemonname:
            for pns in pokeserverpokemonname[serverpokemon]:
                if pns[0] == ctx.channel.id:
                    if pns[1] == pokemonname:
                        print("correct")
        else:
            await ctx.send("<@"+author.id+"> You Dont Start The Game Please Type " +defaultpref[0] + "start To Start The Game")



@bot.event
async def on_message(message):
    if len(pokeserverspawntimer == 0):
        pokeserverspawntimer.append((message.channel.id,random.randrange(500,1000)))
    else:
        for cserver in pokeserverspawntimer:
            for channeldata in pokeserverspawntimer[cserver]:
                if(channeldata[0] == message.channel.id):
                    if(channeldata[1] > 0 ){
                        channeldata[1] = channeldata[1] - 1
                    }else{
                        pokeserverpokemonname.append((message.channel.id,pokemonname[random.randrange(len(pokemonname))]))
                        print(pokeserverpokemonname[0][1])
                    }
                elif message.channel.id not in channeldata[0]:
                    pokeserverspawntimer.append((message.channel.id,random.randrange(500,1000)))
                
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
    await pokemon.pickpokemon(ctx,ctx.author,pokename)
        

def pokemondata():
     response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=964")
     data_json = response.json()
     for namepokemon in data_json['results']:
         pokemonname.append(namepokemon['name'])

pokemondata()
bot.add_cog(Pokemon(bot))
bot.run('NzE2Mjk5NzU0MTg2NzM1NjM4.XtNVgQ.DxqZ-MM-fP7VOR1n0FATHB7XwhU')

