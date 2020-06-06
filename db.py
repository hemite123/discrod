import requests
import json


def GetBalance(self, id):
    getdata = requests.get("https://projectdiscord.000webhostapp.com/userdata.php/?user_id="+str(id)+"&action=data",headers={"Content-Type":"application/json"})
    response = getdata.json()
    balance = response["balance"]
    return balance
def InputUser(self,id,name):
    senddata = requests.post(url="https://projectdiscord.000webhostapp.com/userdata.php",json={"user_id":id,"name":name,"datapost":"insert"},headers={"Content-Type":"application/json",'Accept': 'text/plain'})
    print(senddata.text)
    
def CheckUser(self,id,act):
    getdata = requests.get("https://projectdiscord.000webhostapp.com/userdata.php/?user_id="+str(id)+"&action=data",headers={"Content-Type":"application/json"})
    response = getdata.json()
    print(response)
    if act == "rcount":
        return response["data"]
    else:
        return response

def UpdateUserPokemon(self,id,pokename):
    senddata = requests.post(url="https://projectdiscord.000webhostapp.com/userdata.php",json={"user_id":id,"pokemon":pokename,"datapost":"update","select":1},headers={"Content-Type":"application/json",'Accept': 'text/plain'})
    print(senddata.text)

def InsertPokemon(self,id,pokename,level,nomor):
    senddata = requests.post(url="https://projectdiscord.000webhostapp.com/userdata.php",json={"user_id":id,"pokemon":pokename,"datapost":"newpokemon","nomor":nomor,"level":level},headers={"Content-Type":"application/json",'Accept': 'text/plain'})
    print(senddata.text)

def ManyPokemon(self,id):
    getdata = requests.get("https://projectdiscord.000webhostapp.com/userdata.php/?user_id="+str(id)+"&action=manypoke",headers={"Content-Type":"application/json"})
    response = getdata.json()
    return response["many"]

def GetAllPokemon(self,id):
    getdata = requests.get("https://projectdiscord.000webhostapp.com/userdata.php/?user_id="+str(id)+"&action=listpokemon",headers={"Content-Type":"application/json"})
    response = getdata.json()
    return response

def GetPokemonSelect(self,id):
    getdata = requests.get("https://projectdiscord.000webhostapp.com/userdata.php/?user_id="+str(id)+"&action=pokemons",headers={"Content-Type":"application/json"})
    response = getdata.json()
    return response

def UpdatePokemonInfo(self,id,nomor,level,curexp):
    senddata = requests.post(url="https://projectdiscord.000webhostapp.com/userdata.php",json={"user_id":id,"datapost":"updatepokeinfo","nomor":nomor,"level":level,"curexp":curexp},headers={"Content-Type":"application/json",'Accept': 'text/plain'})
    print(senddata.text)

def SelectPokemon(self,id,nomor):
    senddata = requests.post(url="https://projectdiscord.000webhostapp.com/userdata.php",json={"user_id":id,"datapost":"selectpokemon","nomor":nomor},headers={"Content-Type":"application/json",'Accept': 'text/plain'})
    print(senddata.text)
