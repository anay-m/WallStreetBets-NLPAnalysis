import tensorflow as tf
import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import BertTokenizer, TFBertModel

dataset_path = "./stock_data.csv"  # Replace with the path to your dataset file
df = pd.read_csv(dataset_path)

train_data, temp_data = train_test_split(df, test_size=0.4, random_state=42)
test_data, validation_data = train_test_split(temp_data, test_size=0.5, random_state=42)

train_texts = train_data["Text"].tolist()
train_score = train_data["Sentiment"].tolist()

test_texts = test_data["Text"].tolist()
test_score = test_data["Sentiment"].tolist()

validation_texts = validation_data["Text"].tolist()
validation_score = validation_data["Sentiment"].tolist()

# Load the pre-trained BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
bert_model = TFBertModel.from_pretrained("bert-base-uncased")

# Tokenize the input texts and convert them to model inputs
train_inputs = tokenizer(train_texts, padding=True, truncation=True, return_tensors="tf")
validation_inputs = tokenizer(validation_texts, padding=True, truncation=True, return_tensors="tf")
test_inputs = tokenizer(test_texts, padding=True, truncation=True, return_tensors="tf")

# Get the BERT embeddings for the input texts
train_outputs = bert_model(train_inputs)
validation_outputs = bert_model(validation_inputs)
test_outputs = bert_model(test_inputs)

# Build the model using BERT embeddings
model = tf.keras.Sequential()
model.add(tf.keras.layers.Input(shape=(None, 768)))  # BERT embeddings have 768 dimensions
model.add(tf.keras.layers.Dense(16, activation='relu'))
model.add(tf.keras.layers.Dense(1))
model.compile(optimizer='adam',
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['accuracy'])

# Train the model (same as before)
history = model.fit(
    train_outputs[0], train_score,
    epochs=10,
    validation_data=(validation_outputs[0], validation_score),
    verbose=1
)

# Evaluate the model (same as before)
results = model.evaluate(test_outputs[0], test_score, verbose=2)
for name, value in zip(model.metrics_names, results):
    print("%s: %.3f" % (name, value))