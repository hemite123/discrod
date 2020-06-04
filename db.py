import requests
import json


def GetBalance(self, id):
    getdata = requests.get("https://projectdiscord.000webhostapp.com/userdata.php/?user_id="+str(id),headers={"Content-Type":"application/json"})
    response = getdata.json()
    balance = response["balance"]
    return balance
def InputUser(self,id,name):
    datas = {"user_id":id,"name":name,"balance":0,"datapost":"insert"}
    senddata = requests.post(url="https://projectdiscord.000webhostapp.com/userdata.php",data=datas,headers={"Content-Type":"application/json",'Accept': 'text/plain'})
    print(senddata.text)
    
def CheckUser(self,id,act):
    getdata = requests.get("https://projectdiscord.000webhostapp.com/userdata.php/?user_id="+str(id),headers={"Content-Type":"application/json"})
    response = getdata.json()
    print(response)
    if act == "rcount":
        return response["data"]
    else:
        return response

def UpdateUserPokemon(self,id,pokename):
    datas = {"user_id":id,"pokestart":pokename,"datapost":"update"}
    senddata = requests.post(url="https://projectdiscord.000webhostapp.com/userdata.php",data=datas,headers={"Content-Type":"application/json",'Accept': 'text/plain'})
    

