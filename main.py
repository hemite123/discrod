import discord
from discord.ext import commands
import requests
import db
import pymysql

pokemonname = [] 
pokeserverspawn = []
bot = commands.Bot(command_prefix='poke')

class Pokemon(commands.Cog):

    def __init__ (self,bot):
        self.bot = bot

    async def getbalance(self,ctx,author):
        balance = db.GetBalance(self,author.id)
        embed = discord.Embed(title="Balance " + author.name,description="Your Balance is " + str(balance))
        await ctx.send(embed=embed)

    async def startgame(self,ctx,author):
        checkuser = db.CheckUser(self,author.id,"rcount")
        if checkuser.rowcount > 0:
            embed = discord.Embed(title="PickPokemon " + author.name,description="Pick Your Starter Pokemon Using " + bot.get_prefix + "pick <pokemon>")
            embed.add_field(name="Starter Pokemon",value="Charmander|Squirtle|Bulbasaur",inline=True)
            await ctx.send(embed=embed)
        else:
            db.InputUser(self,author.id,author.name)
            embed = discord.Embed(title="PickPokemon " + author.name,description="Pick Your Starter Pokemon Using " + bot.get_prefix + "pick <pokemon>")
            embed.add_field(name="Starter Pokemon",value="Charmander|Squirtle|Bulbasaur",inline=True)
            await ctx.send(embed=embed)

    async def pickpokemon(self,ctx,author,pokemonname):
        checkuser = db.CheckUser(self,author.id,"")
        if checkuser["3"] is None:
            db.UpdateUserPokemon(self,author.id,pokemonname)
            embed = discord.Embed(title="Pokemon Select" + author.name,description="Your Starter Pokemon Is" + pokemonname)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Pokemon Select" + author.name,description="Your Have Already Pokemon Starter")
            await ctx.send(embed=embed)



        


@bot.command(name="balance",help="See Your Balance")
async def balance(ctx):
    pokemon = bot.get_cog("Pokemon")
    await pokemon.getbalance(ctx,ctx.author)

@bot.command(name="start",help="To Start Your Game")
async def start(ctx):
    pokemon = bot.get_cog("Pokemon")
    await pokemon.startgame(ctx,ctx.author)

@bot.command(name="pick",help="Pick Pokemon Starter")
async def pick(ctx,pokemon):
    pokemon = bot.get_cog("Pokemon")
    await pokemon.pickpokemon(ctx,ctx.author,pokemon)
    
        

def pokemondata():
     response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=964")
     data_json = response.json()
     for namepokemon in data_json['results']:
         pokemonname.append(namepokemon['name'])

pokemondata()
bot.add_cog(Pokemon(bot))
bot.run('NzE2Mjk5NzU0MTg2NzM1NjM4.XtNVgQ.DxqZ-MM-fP7VOR1n0FATHB7XwhU')

