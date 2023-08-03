import pandas as pd

# Load the entire CSV file
data = pd.read_csv('input.csv')

# Select only the "title" and "score" columns
selected_columns = data[['text', 'sentiment']]
new_data = selected_columns.head(5000)

# Save the new version of the CSV file
new_data.to_csv('reddit.csv', index=False)