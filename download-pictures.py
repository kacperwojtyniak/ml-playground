import requests
from pathlib import Path
import shutil
import configparser

config = configparser.ConfigParser()
config.read('local_settings.ini')

subscription_key = config['DEFAULT']['subscription_key']
headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
search_url = "https://api.bing.microsoft.com/v7.0/images/search"


search_terms = {'undamaged':'Common european Cars'}

path = Path('cars')
if not path.exists():
   path.mkdir()

for k in search_terms:

   term = search_terms[k]
   dest = (path/k)
   dest.mkdir(exist_ok=True)

   i = 0
   offset = 0
   for iteration in range(2):

      print(f'searching {term}')
      
      params = {'q':term, 'count':150, 'min_height':128, 'min_width':128, "offset": offset}
      response = requests.get(search_url, headers=headers, params=params)
      response.raise_for_status()
      search_results = response.json()
      offset = search_results["nextOffset"]
      results = search_results["value"]

      print(f'Next offset is {offset}')

      urls = [img["contentUrl"] for img in results]

      print(len(urls))

     
      for u in urls:
         filename = f'{dest}/{i}.jpg'
         try:
            r = requests.get(u, stream = True)
            if r.status_code == 200:
               r.raw.decode_content = True
               with open(filename,'wb') as f:
                  shutil.copyfileobj(r.raw, f)
                  print(f'Downloaded. Count = {i}')
            else:
               print(f'Failed to download {u}')
         except:
            print(f'Exception downloading {u}')
         i += 1