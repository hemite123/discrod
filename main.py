import discord
from discord.ext import tasks,commands
import requests
import db
import pymysql
import random
import time
import json
import re
import datetime
from datetime import datetime,timedelta


pstart = []
plegend = [] 
pmythical = []
pevo2 = []
pevo3 = []
pevo1 = []
palolan = []
pmega = []
pform = []
spam = []
pokeserverspawntimer = []
pokeserverpokemonname = []
defaultpref = ['poke']
pokespin = []
xpboost = []
bot = commands.Bot(command_prefix= defaultpref[0])
bot.remove_command("help")

class Pokemon(commands.Cog):

    def __init__ (self,bot):
        self.bot = bot

    async def getbalance(self,ctx,author):
        balance = db.GetBalance(self,author.id)
        embed = discord.Embed(title="Balance " + author.name,description="Your Balance is " + str(balance[0]))
        await ctx.send(embed=embed)

    async def startgame(self,ctx,author):
        checkuser = db.CheckUser(self,author.id,"rcount")
        print(checkuser)
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
        if checkuser["pokestart"] is None:
            no = 0
            for i in range(len(pstart)):
                if pstart[i].lower() == pokemonname.lower():
                    db.UpdateUserPokemon(self,author.id,pstart[i])
                    embed = discord.Embed(title="Pokemon Select " + author.name,description=" Your Starter Pokemon Is " + pokemonname)
                    await ctx.send(embed=embed)
                    break
                else :
                    no += 1
            if(no == len(pstart)):
                await ctx.send("<@" + str(author.id) + "> Thats Pokemon Is No Pokemon Starter")
        else:
            embed = discord.Embed(title="Pokemon Select " + author.name,description="Your Have Already Pokemon Starter")
            await ctx.send(embed=embed)

    async def catchpokemon(self,ctx,author,pokemonname):
        checkuser = db.CheckUser(self,author.id,"rcount")
        wrong = 0
        if checkuser > 0:
            for i in range(len(pokeserverpokemonname)):
                    if pokeserverpokemonname[i][0] == ctx.channel.id and pokeserverpokemonname[i][1] is not None:
                        print(i)
                        pname = str(pokeserverpokemonname[i][1])
                        pask = ""
                        for d in range(len(pokemonname)):
                            if len(pask) == 0 :
                                pask = pask + pokemonname[d]
                            else:
                                pask = pask + " " + pokemonname[d]
                        print(pask)
                        if pname.lower() == pask.lower():
                            if pokeserverpokemonname[i][3] is None:
                                pokeserverpokemonname[i][3] = author.id
                                number = db.ManyPokemon(self,pokeserverpokemonname[i][3]) + 1 
                                db.InsertPokemon(self,author.id,pokeserverpokemonname[i][1],pokeserverpokemonname[i][2],number)
                                await ctx.send("<@" + str(author.id) + "> You Got " + str(pokeserverpokemonname[i][1])  + " Level " + str(pokeserverpokemonname[i][2]))
                                pokeserverpokemonname[i][1] = None
                                pokeserverpokemonname[i][2] = 0
                                pokeserverpokemonname[i][3] = None
                                pokeserverspawntimer[i][1] = random.randrange(1,20)

                        else:
                            await ctx.send("<@" + str(author.id) + "> Wrong Pokemon Name Try Another Name") 


        else:
            await ctx.send("<@" + str(author.id) + "> You Dont Start The Game Please Type " +defaultpref[0] + "start To Start The Game")

    async def listpokemon(self,ctx,author,pagesmouns):
        print(pagesmouns)
        userpokemon = db.GetAllPokemon(self,author.id)
        page = []
        index = 1
        string = ""
        print(len(userpokemon))
        for i in range(len(userpokemon)):
            print(i)
            if index < 21:
                string = string + "\n "+userpokemon[i]["pokemonname"] +" Level : "+ userpokemon[i]["level"] + " Number " + userpokemon[i]["nomor"]
                index = index + 1
            else:
                page.append(string)
                index = 1
                string = ""
        if len(string) > 0:
            page.append(string)
            string = ""
        embed = None
        print(page)
        if len(page[pagesmouns-1]) > 0:
            embed = discord.Embed(title="Pokemon List " + author.name,description="List Pokemon Of "+author.name)
            embed.add_field(name="Pokemon Data",value=page[pagesmouns -1])
        else:
            embed = discord.Embed(title="Pokemon List " + author.name,description="No Pokemon On Page "+ pagesmouns + " " + author.name)   
        await ctx.send(embed=embed)
    
    async def selectpokemon(self,ctx,author,nomor):
        userpokemon = db.GetAllPokemon(self,author.id)
        data = 0 
        for i in range(len(userpokemon)):
            if userpokemon[i]["nomor"] == nomor :
                db.SelectPokemon(self,author.id,nomor)
                embed = discord.Embed(title="Pokemon Select " + author.name,description=author.name + " Has Selected " + userpokemon[i]["pokemonname"])
                await ctx.send(embed=embed)
                return
            else:
                data += 0
            
        if data == len(userpokemon):
            embed = discord.Embed(title="Pokemon Select " + author.name,description="You No Have Pokemon With Thats Number")
            await ctx.send(embed=embed)
    
    async def hint(self,ctx):
        for i in range(len(pokeserverpokemonname)):
            if pokeserverpokemonname[i][0] == ctx.channel.id :
                hint = ""
                for d in range(len(pokeserverpokemonname[i][1])):
                    range = random.randrange(0,1)
                    if range == 1:
                         hint = hint + pokeserverpokemonname[i][1][d]
                    else:
                         hint = hint + "_"
            await ctx.send(hint)
      
    async def legend(self,ctx,author):
        print(ctx.author.id)
        if str(ctx.author.id) == "577889192944599070":
            print("true")
            for j in range(len(pokeserverpokemonname)):
                 if pokeserverpokemonname[j][0] == ctx.channel.id:
                    print("Connect")
                    pokename = plegend[random.randrange(len(plegend))]
                    pokeserverpokemonname[j][1] = pokename
                    pokeserverspawntimer[j][1] = 0
                    pokeserverpokemonname[j][2] = random.randrange(1,50)
                    embed = discord.Embed(title="Wild Pokemon Has Appeared", description="Catch Your Pokemon Using " + defaultpref[0] +"catch <pokemonname>")
                    with open("pokemon.json") as pokedb:
                       dataload = json.load(pokedb)
                       for i in range(len(dataload)):
                         if dataload[i]["name"] == pokename:
                               embed.set_image(url=dataload[i]["sprite"])
                    await ctx.send(embed=embed)
                    print(f"Pokemon {pokename.lower()} Spawn In Channel Id{pokeserverpokemonname[j][0]}")
        
    async def daily(self,ctx):
        getdata = requests.get("https://projectdiscord.000webhostapp.com/daily.json")
        respone = getdata.json()
        index = 0
        for i in range(len(respone)):
            if(respone[i]["id"] == ctx.author.id):
                datec = datetime.fromtimestamp(respone[i]["time"]) + timedelta(days=1)
                if(datetime.now() == datec ):
                    await ctx.send(f"Added Balance {ctx.author.name} 50 Balance")
                    respone[i]["time"] = time.time()
                    jsondump = json.dumps(respone,indent=4)
                    db.UpdateDaily(bot,jsondump)
                else:
                    await ctx.send(f"You Already Claim You Can Claim The Reward Tommorow ")
            else:
                index += 1
        if(index == len(respone)):
            respone.append({"id":ctx.author.id,"time":time.time()})
            print(respone)
            jsondump = json.dumps(respone,indent=4)
            db.UpdateDaily(bot,jsondump)
            await ctx.send(f"Added Balance {ctx.author.name} 50 Balance")

           
            
class Command(commands.Cog):
    
    def __init__ (self,bot):
        self.bot = bot 

    async def help(self,ctx):
        embed = discord.Embed(title="PokeSenpai Help",description="Follow The Command In Help By Using " + defaultpref[0] + " Command In Help")
        embed.add_field(name=defaultpref[0]+"catch",value="Using For Catch The Pokemon While The Wild Pokemon Is Spawning On The Server",inline=True)
        embed.add_field(name=defaultpref[0]+"mon <page>",value="Using For To See The Pokemon Your Already Catch",inline=True)
        embed.add_field(name=defaultpref[0]+"sel <pokemon number>",value="Using For Change Pokemon To Leveling Or Evolution",inline=True)
        embed.add_field(name=defaultpref[0]+"start",value="To Start The Game",inline=True)
        await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    if message.content is not None:
        print(pokeserverpokemonname)
        print(pokeserverspawntimer)
        xp = random.randrange(30,70)
        for ite in range(len(spam)):
            if spam[ite][0] == message.channel.id:
                if spam[ite][3] > 0:
                    spam[ite][3] = spam[ite][3] - 1
                elif spam[ite][2] > 10:
                    spam[ite][3] = 5000
                elif spam[ite][2] < 3 and spam[ite][1] != message.author.id:
                    spam[ite][1] = message.author.id
                    spam[ite][2] = 0
                if spam[ite][1] == message.author.id and spam[ite][2] > 3:
                    xp = xp - (xp*0.25)
                    data = db.GetPokemonSelect(bot,message.author.id)
                    if data != False:
                        exp = int(data["curexp"]) + xp
                        level = data["level"]
                        name = data['pokemonname']
                        with open("level.json") as leveldb:
                            dataload = json.load(leveldb)
                            for i in range (len(dataload)):
                                if str(dataload[i]["level"]) == str(data["level"]):
                                    if int(exp) > int(dataload[i]["exp"]):
                                        level = int(level) + 1
                                        exp = 0
                                        with open("evolution.json") as evodb:
                                            dataevo = json.load(evodb)
                                            for m in range(len(dataevo)):
                                                with open("pokemon.json") as pokedb:
                                                    dataloadc = json.load(pokedb)
                                                    for l in range(len(dataload)):
                                                        if(dataevo[m]["id"] == dataloadc[l]["family"]["id"]):
                                                            if(dataloadc[l]["name"] == data["pokemonname"]):
                                                                if(dataloadc[i]["family"]["evolutionStage"] == 1):
                                                                    if(level == int(dataevo[m]["evo2"][0]["level"])):
                                                                        name = dataevo[m]["evo2"][0]["evo"]
                                                                        embed = discord.Embed(title="Level Up Evolution", description=f"{message.author.name} Your Pokemon {data['pokemonname']} Is Evolution To {name}")
                                                                        await message.channel.send(embed=embed)
                                                                        break
                                                                    else:
                                                                        embed = discord.Embed(title="Level Up", description=f"{message.author.name} Your Pokemon {data['pokemonname']} now Level {level}")
                                                                        await message.channel.send(embed=embed)
                                                                        break
                                                                elif(dataloadc[i]["family"]["evolutionStage"] == 2):
                                                                    if(level == int(dataevo[m]["evo3"][0]["level"])):
                                                                        name = dataevo[m]["evo3"][0]["evo"]
                                                                        embed = discord.Embed(title="Level Up Evolution", description=f"{message.author.name} Your Pokemon {data['pokemonname']} Is Evolution To {name}")
                                                                        await message.channel.send(embed=embed)
                                                                        break
                                                                    else:
                                                                        embed = discord.Embed(title="Level Up", description=f"{message.author.name} Your Pokemon {data['pokemonname']} now Level {level}")
                                                                        await message.channel.send(embed=embed)
                                                                        break
                                                                else:
                                                                    embed = discord.Embed(title="Level Up", description=f"{message.author.name} Your Pokemon {data['pokemonname']} now Level {level}")
                                                                    await message.channel.send(embed=embed)
                                                                    break
                        db.UpdatePokemonInfo(bot,message.author.id,data["nomor"],level,exp,name)
                        
                else:                                  
                    data = db.GetPokemonSelect(bot,message.author.id)
                    if data != False:         
                        exp = int(data["curexp"]) + xp
                        level = data["level"]
                        name = data['pokemonname']
                        with open("level.json") as leveldb:
                            dataload = json.load(leveldb)
                            for i in range (len(dataload)):
                                if str(dataload[i]["level"]) == str(data["level"]):
                                    if int(exp) > int(dataload[i]["exp"]):
                                        level = int(level) + 1
                                        exp = 0
                                        with open("evolution.json") as evodb:
                                            dataevo = json.load(evodb)
                                            for m in range(len(dataevo)):
                                                with open("pokemon.json") as pokedb:
                                                    dataloadc = json.load(pokedb)
                                                    for l in range(len(dataload)):
                                                        if(dataevo[m]["id"] == dataloadc[l]["family"]["id"]):
                                                            if(dataloadc[l]["name"] == data["pokemonname"]):
                                                                if(dataloadc[i]["family"]["evolutionStage"] == 1):
                                                                    if(level == int(dataevo[m]["evo2"][0]["level"])):
                                                                        name = dataevo[m]["evo2"][0]["evo"]
                                                                        embed = discord.Embed(title="Level Up Evolution", description=f"{message.author.name} Your Pokemon {data['pokemonname']} Is Evolution To {name}")
                                                                        await message.channel.send(embed=embed)
                                                                    else:
                                                                        embed = discord.Embed(title="Level Up", description=f"{message.author.name} Your Pokemon {data['pokemonname']} now Level {level}")
                                                                        await message.channel.send(embed=embed)
                                                                elif(dataloadc[i]["family"]["evolutionStage"] == 2):
                                                                    if(level == int(dataevo[m]["evo3"][0]["level"])):
                                                                        name = dataevo[m]["evo3"][0]["evo"]
                                                                        embed = discord.Embed(title="Level Up Evolution", description=f"{message.author.name} Your Pokemon {data['pokemonname']} Is Evolution To {name}")
                                                                        await message.channel.send(embed=embed)
                                                                    else:
                                                                        embed = discord.Embed(title="Level Up", description=f"{message.author.name} Your Pokemon {data['pokemonname']} now Level {level}")
                                                                        await message.channel.send(embed=embed)
                                        
                        db.UpdatePokemonInfo(bot,message.author.id,data["nomor"],level,exp,name)  
        index = 0
        #Leveling
        for i in range(len(pokeserverspawntimer)):
                if pokeserverspawntimer[i][0] == message.channel.id:
                    if pokeserverspawntimer[i][1] > 0:
                        pokeserverspawntimer[i][1] = pokeserverspawntimer[i][1] - 1
                        break
                    else:
                        for j in range(len(pokeserverpokemonname)):
                            if pokeserverpokemonname[j][0] == message.channel.id:
                                if pokeserverpokemonname[j][1] is None:
                                    droprate = random.uniform(0.1,100.0)
                                    if droprate >= 33.9 or droprate <= 33.9:
                                        pokename = pevo1[random.randrange(len(pevo1))]
                                    elif droprate <= 30.0:
                                        pokename = pevo2[random.randrange(len(pevo2))]
                                    elif droprate <= 10.0:
                                        pokename = pevo3[random.randrange(len(pevo3))]
                                    elif droprate <= 5.0:
                                        pokename = palolan[random.randrange(len(palolan))]
                                    elif droprate <= 1.0:
                                        pokename = pmythical[random.randrange(len(pmythical))]
                                    elif droprate >= 0.1:
                                        pokename = plegend[random.randrange(len(plegend))]
                                    pokeserverpokemonname[j][1] = pokename
                                    pokeserverpokemonname[j][2] = random.randrange(1,50)
                                    embed = discord.Embed(title="Wild Pokemon Has Appeared", description="Catch Your Pokemon Using " + defaultpref[0] +"catch <pokemonname>")
                                    with open("pokemon.json") as pokedb:
                                        dataload = json.load(pokedb)
                                    for i in range(len(dataload)):
                                        if dataload[i]["name"] == pokename:
                                            embed.set_image(url=dataload[i]["sprite"])
                                    await message.channel.send(embed=embed)
                                    print(f"Pokemon {pokename.lower()} Spawn In Channel Id{pokeserverpokemonname[j][0]}")
                                    break
                                
                else:
                    index += 1
             
        if index == len(pokeserverspawntimer):
            pokeserverspawntimer.append([message.channel.id,random.randrange(1,20)])
            pokeserverpokemonname.append([message.channel.id,None,0,None])
            spam.append([message.channel.id,None,0,0])
            index = 0
        #spawn

        
        
            
    
    await bot.process_commands(message)

@bot.event
async def on_ready():
    print(f"{bot.user.name} Has Connect To Server")
    for chan in bot.guilds:
        print(chan.id)
    
        
   
    


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
async def catch(ctx,*pokename):
    pokemon = bot.get_cog("Pokemon")
    await pokemon.catchpokemon(ctx,ctx.author,pokename)

@bot.command(name="mon",help="Check Your Catch Pokemon")
async def mon(ctx,page=1):
    pokemon = bot.get_cog("Pokemon")
    await pokemon.listpokemon(ctx,ctx.author,page)

@bot.command(name="sel",help="Select Your Pokemon")
async def monsel(ctx,nomor):
    pokemon = bot.get_cog("Pokemon")
    await pokemon.selectpokemon(ctx,ctx.author,nomor)
                                                              
@bot.command(name="hint",help="Wild Pokemon Name Hint")
async def hint(ctx):
    pokemon = bot.get_cog("Pokemon")
    await pokemon.hint(ctx)
                                                         
@bot.command(name="legend",help="Spawn Pokemon Only Author Bot")
async def legend(ctx):
    pokemon = bot.get_cog("Pokemon")
    await pokemon.legend(ctx,ctx.author)

@bot.command(name="help")
async def help(ctx):
    command = bot.get_cog("Command")
    await command.help(ctx)

@bot.command(name="daily")
async def daily(ctx):
   pokemon = bot.get_cog("Pokemon")
   await pokemon.daily(ctx)
                                                        


def pokemondata():
    with open("pokemon.json") as pokedb:
        dataload = json.load(pokedb)
        for i in range(len(dataload)):
            print(dataload[i]["name"])
            if dataload[i]["starter"]:
                pstart.append(dataload[i]["name"])
            elif dataload[i]["name"].count("Forme") > 0 or dataload[i]["name"].count("Form") > 0 or dataload[i]["name"].count("Ash") > 0 or dataload[i]["name"].count("Style") > 0 or dataload[i]["name"].count("Core") > 0 or dataload[i]["name"].count("Cloak") > 0 or dataload[i]["name"].count("Sun") > 0 or dataload[i]["name"].count("Moon") > 0 or dataload[i]["name"].count("Primal") > 0 or dataload[i]["name"].count("Dusk") > 0 or dataload[i]["name"].count("Dawn") > 0:
                pform.append(dataload[i]["name"])   
            elif dataload[i]["legendary"] and dataload[i]["mega"] == False:
                plegend.append(dataload[i]["name"]) 
            elif dataload[i]["mythical"] and dataload[i]["mega"] == False:
                pmythical.append(dataload[i]["name"])   
            elif dataload[i]["mega"]:
                pmega.append(dataload[i]["name"])
            elif dataload[i]["name"].count("Alolan") > 0:
                palolan.append(dataload[i]["name"])  
            elif dataload[i]["family"]["evolutionStage"] == 1 and dataload[i]["mega"] == False:
                pevo1.append(dataload[i]["name"])      
            elif dataload[i]["family"]["evolutionStage"] == 2 and dataload[i]["mega"] == False:
                pevo2.append(dataload[i]["name"])
            elif dataload[i]["family"]["evolutionStage"] == 3 and dataload[i]["mega"] == False:
                pevo3.append(dataload[i]["name"])
            
            
            
            
        
            

pokemondata()
print(plegend)
print(pmythical)
print(pevo1)
print(pevo2)
print(pevo3)
print(pstart)
bot.add_cog(Pokemon(bot))
bot.add_cog(Command(bot))
bot.run('NzE2Mjk5NzU0MTg2NzM1NjM4.XtNVgQ.DxqZ-MM-fP7VOR1n0FATHB7XwhU')
