import requests
import json


def GetBalance(self, id):
    getdata = requests.get("https://projectdiscord.000webhostapp.com/userdata/"+str(id),headers="Content-Type:application/json")
    response = getdata.json()
    balance = response["balance"]
    return balance
def InputUser(self,id,name):
    data = {"user_id":id,"name":name,"balance":0,"datapost":"insert"}
    senddata = requests.post(url="https://projectdiscord.000webhostapp.com/userdata",data=data)

def CheckUser(self,id,act):
    getdata = requests.get("https://projectdiscord.000webhostapp.com/userdata/"+str(id),headers="Content-Type:application/json")
    response = getdata.json()
    if act == "rcount":
        return len(response)
    else:
        return response

def UpdateUserPokemon(self,id,pokename):
    data = {"user_id":id,"pokestart":pokename,"datapost":"update"}
    senddata = requests.post(url="https://projectdiscord.000webhostapp.com/userdata",data=data,headers="Content-Type:application/json")
    

