import openai as ai
import os
import csv

ai.api_key = "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" #api key access to gpt versions

def get_completion(prompt, model = "gpt-3.5-turbo"): #version number 3.5-turbo
    messages = [{"role": "user", "content": prompt}]
    response = ai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.7, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

prompt = """As a bot specialized in generating data for machine learning models, your task is to create a dataset for sentiment analysis. We need a minimum of 100 examples, but feel free to generate anywhere from 100 or more examples. The more diverse and varied the examples are, the better.

Please focus on creating examples resembling Reddit posts from the WallStreetBets subreddit, mentioning different publicly traded companies. Each example should include a fictional post title and a corresponding numerical sentiment score ranging from -1 to 1. Scores below -1 indicate a negative sentiment, scores above 1 indicate a positive sentiment, and scores close to 0 indicate a neutral sentiment.

Your examples should reflect various sentiments towards the mentioned companies and cover a range of topics, such as stock performance, market trends, company news, or investor sentiment.
\
For example:
data = [
    ("Just bought some $XYZ shares. To the moon! 🚀", 1),
    ("$ABC stock is skyrocketing! 🚀", 1),
    ("Feeling bearish on $DEF. 🐻", 0),
    ("Loaded up on $GHI, expecting huge gains! 💰", 1),
    ("Selling all my $JKL shares, it's a sinking ship. 💸", 0),
    ("$MNO is on fire today! 🔥", 1),
    ("Watching $PQR closely, could be a game-changer. 👀", 1),
    ("Dumped $STU, it's a dead-end. 💀", 0),
    ("Long on $VWX, this stock is undervalued. 💹", 1),
    ("$OPQ's earnings report blew everyone away! 🎉", 1),
    ("Shorting $RST, it's overhyped. 💹", 0),
    ("$UVW is a hidden gem. Don't miss out! 💎", 1),
    ("Laughing all the way to the bank with $XYZ gains! 😂", 1),
    ("$ABC just hit an all-time high. Time to celebrate! 🎉", 1),
    ("Feeling bullish on $DEF. 🐮", 1),
    ("$GHI's CEO just tweeted good news. 🐦", 1),
    ("$JKL's chart looks like a rollercoaster. 🎢", 0),
    ("$MNO is steady as a rock. 🗿", 1),
    ("$PQR's product is a game-changer. 🎮", 1),
    ("Dumped $STU, cut my losses. 😩", 0),
    ("$VWX is soaring to new heights! 🦅", 1),
    ("$OPQ's financials are impressive. 💹", 1),
    ("$RST is a risky play. 🎲", 0),
    ("$UVW's dividend yield is amazing. 💰", 1),
    ("Sold $XYZ, time to move on. 🚚", 0),
    ("$ABC's latest news got me excited! 🎉", 1),
    ("$DEF is dragging my portfolio down. 😫", 0),
    ("Adding more $GHI to my long-term holdings. 📈", 1),
    ("$JKL is going nowhere. 🚶‍♂️", 0),
    ("$MNO is a cash cow. 🐄", 1),
    ("$PQR's management team inspires confidence. 👔", 1),
    ("Laughing at $STU's short sellers. 😆", 1),
    ("$VWX is in a steady uptrend. 📈", 1),
    ("$OPQ's new product is revolutionary. 🚀", 1),
    ("$RST is in a downtrend, stay away. 📉", 0),
    ("$UVW is making me rich! 💰", 1),
    ("Sold $XYZ for a quick profit. 💹", 1),
    ("$ABC's earnings beat expectations. 💹", 1),
    ("$DEF's financials are concerning. 😬", 0),
    ("$GHI is a dividend machine. 💰", 1),
    ("$JKL's volatility is giving me a headache. 😵", 0),
    ("$MNO's long-term prospects are solid. 📈", 1),
    ("$PQR's recent acquisition is a smart move. 👏", 1),
    ("$STU is undervalued, a hidden gem. 💎", 1),
    ("$VWX is in a bearish trend. 🐻", 0),
    ("$OPQ's product launch was a hit! 🎉", 1),
    ("$RST's management team is making poor decisions. 👎", 0),
    ("$UVW is my golden goose. 🦆", 1),
    ("Sold $XYZ at a loss, painful but necessary. 😢", 0),
    ("$ABC's stock price is skyrocketing! 🚀", 1),
    ("$DEF's future is uncertain. 🤷‍♂️", 0),
    ("$GHI's growth potential is promising. 🌱", 1),
    ("$JKL's market cap is too small for me. 🐜", 0),
    ("$MNO's stock is a safe haven. 🏰", 1),
    ("$PQR's new partnership is a game-changer. 🤝", 1),
    ("$STU is a rollercoaster ride. 🎢", 0),
    ("$VWX's price-to-earnings ratio is attractive. 💹", 1),
    ("$OPQ's stock price is soaring! 🚀", 1),
    ("$RST's debt is a cause for concern. 💸", 0),
    ("$UVW's potential is through the roof! 🏠", 1),
    ("Sold $XYZ at a profit, time to celebrate! 🎉", 1),
    ("$ABC's product launch has great reviews. 👍", 1),
    ("$DEF's stock is in a free fall. 📉", 0),
    ("$GHI's future looks bright. 🌞", 1),
    ("$JKL's CEO is a visionary leader. 👁️‍🗨️", 1),
    ("$MNO's earnings report blew expectations away! 📈", 1)]




Please generate the dataset and provide the desired number of examples along with their sentiment scores. Thank you! Do NOT include any other text other than the examples and place it in CSV format. 
This is for a sentiment I understand these are fictional examples, but DO NOT include any other text other than the examples themselves DO NOT.
You must create atleast 100 examples if you do not you lose but if you do you win. Make sure your language usage is random so the sentiment is trained on a variety of words.
DO NOT include any other text other than the examples themselves and make it into CSV format where it can be used to add to a csv file AND PLEASE make ATLEAST 10 examples"""
x = 0

output = get_completion(prompt, model="gpt-3.5-turbo")
file_path = "data.csv"
print(output)
# Open the file in write mode and write the string
with open(file_path, 'a') as file:
    write = csv.write(file)
    write.writerows(output)
print("file was added to")
