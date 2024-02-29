import os
import requests
from pynytimes import NYTAPI
from bs4 import BeautifulSoup
import yaml
import argparse

parser = argparse.ArgumentParser(description='Program takes a yml file and pulls articles of interest.')
parser.add_argument('-yml', help='path to yml file.')
args = parser.parse_args()

# loading yml file and setting the variables
with open(args.yml) as stream:
  yml_file = yaml.safe_load(stream)


# TODO: incorporate the following data structure
'''
web_url    string        
source    string        
headline            
    main    string    
    kicker    string    
    content_kicker    string    
    print_headline    string    
    name    string    
    seo    string    
    sub    string    
pub_date    string        Timestamp (YYYY-MM-DD)
byline            Author
news_desk            (OpEd,  Editorial, letters …)
section_name    Single token        Frontpage or not
Body            
source    ("The New York Times")    
'''

API_KEY = yml_file['API_KEY']


def get_articles(API_KEY) -> list:
  nyt = NYTAPI(API_KEY, parse_dates=True)

  articles = nyt.article_search(
      results = 10,
      
      options = {
      "sort": "newest",
      "fq": "Gaza AND Palestine AND Israel AND Palestinian AND Israeli",
      })


  # New list to hold the extracted info
  extracted_info = []

  # Loop through each article in the list
  for article in articles:
    # Extract info from the json
    web_url = article.get('web_url', None) 
    source = article.get('source', None)  
    headline_main = article.get('headline', {}).get('main', None)
    byline = article.get('byline', {}).get('original', None)

    # Append the extracted information to the new list as a dictionary
    extracted_info.append({'headline': headline_main, 'byline': byline, 'source': source, 'web_url': web_url})
  

  return extracted_info

def get_article_content(article_url: str) -> str:
  if not article_url:
    print("No article URL provided")
    return "No article URL provided"

  print(f"Fetching article content for {article_url}")

  # Check if the article is available on the Wayback Machine
  url = "http://archive.org/wayback/available?url=" + article_url

  payload = {}
  headers = {}

  response = requests.request("GET", url, headers=headers, data=payload)

  data = response.json()

  # Check if the article is available on the Wayback Machine

  if data.get('archived_snapshots'):
    # Get the closest snapshot
    snapshot = data['archived_snapshots'].get('closest', None)

    if snapshot:
      # Get the snapshot URL
      snapshot_url = snapshot.get('url', None)

      if snapshot_url:
        # Get the article content
        r = requests.get(snapshot_url)
        soup = BeautifulSoup(r.text, 'html.parser')
        target_div = soup.find('section', class_='meteredContent css-1r7ky0e')

        if target_div:
          paragraphs = target_div.get_text(strip=True, separator='\n')
          print("Success: Article content extracted successfully!")
          return paragraphs
        else:
          print("failed: article content not found - div is missing")
          return "No div found"
      else:
        print("failed: snapshot URL not found - article content not available on the Wayback Machine")
        return "No snapshot URL found"
    else:
      print("failed: snapshot not found - article has not been archived")
      return "No snapshot found"

'''
def save_to_db(article: dict):

  try: 
    # Connect to the database
    db = mysql.connector.connect(
      host=DB_HOST,
      user=DB_USER,
      password=DB_PASS,
      database=DB_NAME
    )
    print("Connection established")
  except mysql.connector.Error as err:
    print(f"Failed to connect: {err}")

  # Create a cursor
  cursor = db.cursor()

  # Create a new table
  create_table = """
  CREATE TABLE IF NOT EXISTS articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    headline VARCHAR(255),
    byline VARCHAR(255),
    source VARCHAR(255),
    web_url TEXT,
    body TEXT
  )
  """
  cursor.execute(create_table)

  # Prepare the SQL query
  sql = "INSERT INTO articles (headline, byline, source, web_url, body) VALUES (%s, %s, %s, %s, %s)"
  values = (article.get('headline'), article.get('byline'), article.get('source'), article.get('web_url'), article.get('body'))

  # Execute the SQL query
  cursor.execute(sql, values)

  # Commit the changes
  db.commit()

  # Close the connection
  db.close()

  print(f"Article {article.get('headline')} saved to the database")
'''



if __name__ == "__main__":

  # Get the articles metadata
  articles = get_articles(API_KEY)

  for article in articles:
    # Get the article content
    article["body"] = get_article_content(article.get('web_url'))

    # Save the article to the database


