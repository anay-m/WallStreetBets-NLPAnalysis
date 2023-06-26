import spacy
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json
import csv
import requests
import os
# Load the spaCy English language model with the pre-trained NER component
nlp = spacy.load('en_core_web_sm')
CSV_URL = os.environ["CSV_URL"]
# Fetch Company Stock Abbreviation and Name
def fetch_company_data():
    # Replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    
    company_symb_dict = {}
    company_name_dict = {}
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            company_symb_dict[row[0].upper()] = row[1]
            company_name_dict[row[1]] = row[0].upper()
            
    with open("stocks_symb.json", 'w') as file:
        json.dump(company_symb_dict, file)
        
    with open("stocks_name.json", 'w') as file:
        json.dump(company_name_dict, file)

# Function to analyze text and extract the topic (company name) and stock abbreviation
def analyze_topic(text, company_symb_dict, company_name_dict):
    doc = nlp(text)
    company = ''
    stock_abbreviation = ''
    max1 = 0
    old_pos = ''
    for token in doc:
        token_text = token.text
        pos = token.pos_
        if company_symb_dict.get(token.text):
            pos = 'NOUN'
        elif old_pos == 'SYM':
            pos = 'NOUN'
            token_text = token.text.upper()
            
        if pos == 'NOUN' or pos == 'PROPN':
            closest_name_match = process.extractOne(token_text, list(company_symb_dict.values()))
            closest_symb_match = process.extractOne(token_text, list(company_symb_dict.keys()))
            if closest_name_match[1] > closest_symb_match[1] or len(closest_symb_match[0]) < len(token_text):
                if closest_name_match[1] > max1:
                    company = closest_name_match[0]
                    stock_abbreviation = company_name_dict.get(company)
                    max1 = closest_name_match[1]
            else:
                if closest_symb_match[1] > max1:
                    stock_abbreviation = closest_symb_match[0] 
                    company = company_symb_dict.get(stock_abbreviation)
                    max1 = closest_symb_match[1]
        old_pos = pos
    
    if max1 < 70:
        company = "Unfound"
        stock_abbreviation = "Unfound"

    try:
        return company, stock_abbreviation
    except UnboundLocalError:
        return "Unfound", "Unfound"

def main(title):
    with open("stocks_name.json", 'r') as file:
        company_name_dict = json.load(file)
    with open("stocks_symb.json", 'r') as file:
        company_symb_dict = json.load(file)
    # Example usage
    company, stock_abbreviation = analyze_topic(title, company_symb_dict, company_name_dict)
    print("Company:", company)
    print("Stock Abbreviation:", stock_abbreviation)
    return f"{company}, {stock_abbreviation}"
