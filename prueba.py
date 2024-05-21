import requests

url = "https://muscle-group-image-generator.p.rapidapi.com/getBaseImage"

querystring = {"transparentBackground":"0"}

headers = {
	"X-RapidAPI-Key": "3bf76f5e74msheec6108cdb84cc4p18f7c9jsne64f7c000350",
	"X-RapidAPI-Host": "muscle-group-image-generator.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())