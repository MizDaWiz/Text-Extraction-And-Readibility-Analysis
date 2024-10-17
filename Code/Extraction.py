# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 14:27:09 2024

@author: Fizza
"""

# %% Imports
import requests
from bs4 import BeautifulSoup
import os
import re
import pandas as pd

# %% Functionality to extract Text and Saving into .txt files


def extract_article(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the title
    title = soup.find('h1', class_='entry-title').text.strip()
    
    # Extract the main content
    content = soup.find('div', class_='td-post-content')
    
    # Remove any script or style elements
    for script in content(["script", "style"]):
        script.decompose()
    
    # Get the text content
    text = content.get_text(separator='\n\n')
    
    # Remove extra whitespace
    text = re.sub(r'\n+', '\n\n', text).strip()
    
    return f"{title}\n\n{text}"

def save_article(url_id, content):
    # Create a directory for the articles if it doesn't exist
    if not os.path.exists('articles'):
        os.makedirs('articles')
    
    # Save the content to a file
    with open(f'articles/{url_id}.txt', 'w', encoding='utf-8') as f:
        f.write(content)

def extract_url_id(url):
    # Extract the URL ID from the URL
    match = re.search(r'/([^/]+)/$', url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Could not extract URL ID from the given URL")

def process_excel_urls(excel_path):
    # Read the Excel file
    df = pd.read_csv(excel_path, encoding='utf-8')
    
    # Ensure the DataFrame has 'URL' and 'URL_ID' columns
    if 'URL' not in df.columns or 'URL_ID' not in df.columns:
        raise ValueError("Excel file must contain 'URL' and 'URL_ID' columns")
    
    # Process each URL
    for index, row in df.iterrows():
        url = row['URL']
        url_id = row['URL_ID']
        
        try:
            # Extract the article content
            content = extract_article(url)
            
            # Save the article
            save_article(url_id, content)
            
            print(f"Article saved successfully: {url_id}.txt")
        except Exception as e:
            print(f"An error occurred processing URL {url}: {str(e)}")
# %% Run to extract Text (Change folder paths)
excel_path = "C:/Users/Fizza/Desktop/20211030 Test Assignment/Input.csv"
process_excel_urls(excel_path)
# %% Functionality to clean the data from StopWords

#Load Custom Stopwords from folder
def load_stopwords(stopwords_folder):
    stopwords = set()
    for filename in os.listdir(stopwords_folder):
        if filename.endswith('.txt'):
            with open(os.path.join(stopwords_folder, filename), 'r', encoding='latin-1') as f:
                stopwords.update(word.strip().lower() for word in f)
    return stopwords


def clean_text_file(file_path, stopwords):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Split the text into words
    words = text.split()
    
    # # Remove stopwords
    cleaned_words = [word for word in words if word.lower() not in stopwords]
    

    # Join the words back into text
    cleaned_text = ' '.join(cleaned_words)
    
    # Write the cleaned text back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_text)

def clean_all_articles(articles_folder, stopwords_folder):
    stopwords = load_stopwords(stopwords_folder)
    
    for filename in os.listdir(articles_folder):
        if filename.endswith('.txt'):
            file_path = os.path.join(articles_folder, filename)
            clean_text_file(file_path, stopwords)
            print(f"Cleaned: {filename}")

# %% Run to Clean Text (Change folder paths)
articles_folder = 'C:/Users/Fizza/Desktop/20211030 Test Assignment/articles'
stopwords_folder = 'C:/Users/Fizza/Desktop/20211030 Test Assignment/StopWords'
clean_all_articles(articles_folder, stopwords_folder)
