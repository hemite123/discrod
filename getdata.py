import requests
import json
import os

for i in range(1,500):
    response = requests.get("https://pokeapi.glitch.me/v1/pokemon/"+str(i))
    data = response.json()
    filepath = 'pokemon.json'
    print(i)

    try:
        if os.stat(filepath).st_size == 1:
            with open('pokemon.json','w') as d:
                json.dump(data,d)   
        else:
            with open('pokemon.json') as f:
                jsonload = json.load(f)
            jsonload.append(data)
    
            with open('pokemon.json','w') as d:
                json.dump(jsonload,d)
    except Exception as e:
        print(e)
        
