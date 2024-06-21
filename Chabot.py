# Install Required Libraries
# Run the following command in your terminal or command prompt to install the necessary libraries
# pip install transformers torch pymongo

from transformers import GPT2Tokenizer, GPT2LMHeadModel
from pymongo import MongoClient

# Load Pre-trained GPT-2 Model and Tokenizer from Local Directory
model_path = "path/to/your/local/gpt2_model"
tokenizer = GPT2Tokenizer.from_pretrained(model_path)
model = GPT2LMHeadModel.from_pretrained(model_path)

def generate_mongodb_query(input_text):
    # Tokenize input
    inputs = tokenizer.encode(input_text, return_tensors='pt')
    
    # Generate output
    outputs = model.generate(inputs, max_length=100, num_return_sequences=1)
    
    # Decode output
    query = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return query

def post_process_query(query):
    # Example post-processing to convert the generated text into a valid MongoDB query
    query = query.replace('<replace_with_correct_field>', 'field_name')
    return query

def execute_query(query):
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['your_database_name']
    collection = db['your_collection_name']
    
    # Execute query (assuming it's a find query in this example)
    try:
        result = collection.find(eval(query))  # Use eval with caution, ensure query is safe
        return list(result)
    except Exception as e:
        print(f"Query execution failed: {e}")
        return []

if __name__ == "__main__":
    # Example natural language input
    input_text = "Find all documents where the age is greater than 25"
    
    # Generate MongoDB query
    raw_query = generate_mongodb_query(input_text)
    print("Raw Query:", raw_query)
    
    # Post-process the query
    query = post_process_query(raw_query)
    print("Processed Query:", query)
    
    # Execute the query
    results = execute_query(query)
    for result in results:
        print(result)
