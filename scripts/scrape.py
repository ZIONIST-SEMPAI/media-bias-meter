import requests
from pynytimes import NYTAPI
from bs4 import BeautifulSoup
import yaml
import argparse
import datetime
import csv

parser = argparse.ArgumentParser(description='Program takes a yml file and pulls articles of interest.')
parser.add_argument('--yml', help='path to yml file.')
args = parser.parse_args()

# loading yml file and setting the variables
with open(args.yml) as stream:
  yml_file = yaml.safe_load(stream)


API_KEY = yml_file['API_KEY']
begin_date = yml_file['begin_date']
end_date = yml_file['end_date']
filter_query = yml_file['filter_query']


def get_articles(API_KEY) -> list:
  nyt = NYTAPI(API_KEY, parse_dates=True)

  articles = nyt.article_search(
    results=10,
    options={
      "sort": "newest",
      "fq": filter_query
    },
    dates={
      "begin": datetime.date(year=begin_date[0], month=begin_date[1], day=begin_date[2]),
      "end": datetime.date(year=end_date[0], month=end_date[1], day=end_date[2])
    }
  )
  # New list to hold the extracted info
  extracted_info = []
  
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
  # Loop through each article in the list
  for article in articles:
    # Extract info from the json
    web_url = article.get('web_url', None) 
    source = article.get('source', None)  
    headline_main = article.get('headline', {}).get('main', None)
    headline_kicker = article.get('headline').get('kicker')
    headline_content_kicker = article.get('headline').get('content_kicker')
    headline_print_headline = article.get('headline').get('print_headline')
    headline_name = article.get('headline').get('name')
    headline_seo = article.get('headline').get('seo')
    headline_sub = article.get('headline').get('sub')
    pub_date = article.get('pub_date')
    news_desk = article.get('news_desk')
    byline = article.get('byline', {}).get('original', None)

    # Append the extracted information to the new list as a dictionary
    extracted_info.append({'headline': headline_main,
                           'byline': byline,
                           'source': source,
                           'web_url': web_url,
                           'headline-kicker': headline_kicker,
                           'headline-content-kicker': headline_content_kicker,
                           'headline-print-headline': headline_print_headline,
                           'headline-name': headline_name,
                           'headline-seo': headline_seo,
                           'headline-sub': headline_sub,
                           'pub_date': pub_date,
                           'news-desk': news_desk})

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


if __name__ == "__main__":

  # Get the articles metadata
  articles = get_articles(API_KEY)

  for article in articles:
    # Get the article content
    article["body"] = get_article_content(article.get('web_url'))

  header = ['headline', 'byline', 'source', 'web_url', 'headline-kicker','headline-content-kicker',
            'headline-print-headline', 'headline-name', 'headline-seo', 'headline-sub', 'pub_date',
            'news-desk', 'body']

  # Save the article to a csv file
  with open('articles.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames= header)
    writer.writeheader()
    writer.writerows(articles)

