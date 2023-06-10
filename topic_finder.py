import spacy
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Load the spaCy English language model with the pre-trained NER component
nlp = spacy.load('en_core_web_sm')

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
                break

    # Find the main verb phrase as the topic
    for token in doc:
        if token.pos_ == 'VERB':
            topic = token.text
            break

    return topic, company, stock_abbreviation

# List of known company names with their stock abbreviations


# Example usage
sentence = "Microsodt Corporation is launching a new product."
topic, company, stock_abbreviation = analyze_sentiment(sentence, company_list)
print("Topic:", topic)
print("Company:", company)
print("Stock Abbreviation:", stock_abbreviation)

