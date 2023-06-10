import spacy
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import csv
import requests

# Load the spaCy English language model with the pre-trained NER component
nlp = spacy.load('en_core_web_sm')

# Fetch Company Stock Abbreviation and Name
def fetch_company_data():
    # Replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    CSV_URL = 'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=A4C7A6Z2GY0I40TS'
    company_list = []
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            data = f"{row[1]}, {row[0]}"
            company_list.append(data)
    return company_list

# Function to analyze sentiment and extract the topic, company name, and stock abbreviation
def analyze_sentiment(text, company_list):
    doc = nlp(text)
    topic = ''
    company = ''
    stock_abbreviation = ''

    # Extract named entities and their labels
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    # Find the most relevant entity as the company name
    for entity, label in entities:
        if label == 'ORG' or label == 'PRODUCT':
            closest_match = process.extractOne(entity, company_list)
            if closest_match[1] >= 80:
                company = closest_match[0]
            else:
                # Perform autocompletion on company names
                closest_match = process.extractOne(entity, company_list, scorer=fuzz.token_sort_ratio)
                if closest_match[1] >= 80:
                    company = closest_match[0]
            break

    # Find the stock abbreviation for the company
    if company:
        for entry in company_list:
            if company in entry:

                stock_abbreviation = entry.split(',')[1].strip()
                company_name = entry.split(',')[0].strip()

                break


    # Find the main verb phrase as the topic
    for token in doc:
        if token.pos_ == 'VERB':
            topic = token.text
            break
    try:
        return topic, company_name, stock_abbreviation
    except UnboundLocalError:
        return "Unfound Search", "Unfound", "Unfound"
# List of known company names with their stock abbreviations
def main(title):
    company_list = fetch_company_data()

    # Example usage
    topic, company, stock_abbreviation = analyze_sentiment(title, company_list)
    print("Topic:", topic)
    print("Company:", company)
    print("Stock Abbreviation:", stock_abbreviation)
    return f"{company}, {stock_abbreviation}"


