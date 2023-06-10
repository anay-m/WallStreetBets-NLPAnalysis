import requests
import os
VANTAGE_API_KEY = os.environ["VANTAGE_API_KEY"]
api_key = VANTAGE_API_KEY  # Replace with your Alpha Vantage API key

# Endpoint URL for listing status
url = f'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={api_key}'

# Send a GET request to the API
response = requests.get(url)

# Process the response
companies = []

if response.status_code == 200:
    data = response.json()
    companies_data = data['data']
   
    for company in companies_data:
        symbol = company['symbol']
        name = company['name']
        exchange = company['exchange']
       
        company_info = {
            'symbol': symbol,
            'name': name,
            'exchange': exchange
        }
       
        companies.append(company_info)
else:
    print('Error occurred while retrieving company list.')

# Print the company information
for company in companies:
    print(f"Symbol: {company['symbol']}, Name: {company['name']}, Exchange: {company['exchange']}")