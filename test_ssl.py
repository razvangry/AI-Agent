import requests
import certifi

r = requests.get("https://www.google.com", verify=certifi.where())
print("Succes!" if r.status_code == 200 else "Eroare SSL")