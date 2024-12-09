import streamlit as st
import requests
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain.chains import ConversationalRetrievalChain
import faiss
import numpy as np

# Streamlit configuration
st.set_page_config(page_title="Immo Green AI Chatbot", layout="wide")

# Welcome and introduction
def show_welcome():
    st.title("👋 Welcome to Immo Green AI!")
    st.write("""
        At Immo Green AI, we offer advanced real estate services tailored to your needs.
        Discover, buy, rent, or manage properties efficiently with our AI-powered system.
    """)

# Login and user session
def login():
    st.sidebar.title("Login")
    with st.sidebar.form("login_form"):
        email = st.text_input("Email:")
        password = st.text_input("Password:", type="password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            st.session_state["user_logged_in"] = True
            st.session_state["user_email"] = email
            st.success("Login successful! Redirecting...")
            st.experimental_set_query_params(logged_in="true")

# Chatbot functionality
def chatbot():
    # Display categories
    st.write("Welcome back! How can we assist you today?")
    option = st.selectbox("Choose a category:", [
        "Buy or sell real estate",
        "Rental and management",
        "Renovation",
        "Construction projects and planning"
    ])

    # Search functionality
    # Example property database (Replace this with actual data or API calls)
property_database = [
    {
        "name": "Luxury Apartment",
        "price": 450000,
        "size": 600,
        "condition": "New",
        "region": "Zurich",
        "type": "Apartment",
    },
    {
        "name": "Renovated House",
        "price": 800000,
        "size": 1200,
        "condition": "Renovated",
        "region": "Geneva",
        "type": "House",
    },
    {
        "name": "Commercial Space",
        "price": 300000,
        "size": 500,
        "condition": "Old",
        "region": "Zurich",
        "type": "Commercial",
    },
]

# Search functionality
query = st.text_input("Search for a property (e.g., 'Apartment in Zurich'):")
if st.button("Search"):
    if query:
        st.write(f"Searching for: {query}")

        # Filter options
        max_price = st.number_input("Price (Max):", step=1000, value=500000)
        min_size = st.number_input("Size (Min in sqft):", step=100, value=500)
        condition = st.selectbox("Condition:", ["All", "New", "Renovated", "Old"])
        region = st.text_input("Region (e.g., Zurich):")
        property_type = st.selectbox("Property Type:", ["All", "Apartment", "House", "Land", "Commercial"])

        # Filter properties from the database
        filtered_properties = [
            property for property in property_database
            if (query.lower() in property["name"].lower())
            and (property["price"] <= max_price)
            and (property["size"] >= min_size)
            and (condition == "All" or property["condition"] == condition)
            and (region == "" or region.lower() in property["region"].lower())
            and (property_type == "All" or property["type"] == property_type)
        ]

        # Display results
        if filtered_properties:
            st.write("Results:")
            for property in filtered_properties:
                st.write(f"- **{property['name']}**")
                st.write(f"  - Price: {property['price']} CHF")
                st.write(f"  - Size: {property['size']} sqft")
                st.write(f"  - Condition: {property['condition']}")
                st.write(f"  - Region: {property['region']}")
                st.write(f"  - Type: {property['type']}")
                st.write("---")
        else:
            st.warning("No matching properties found. Try adjusting your filters.")


    # Chat consultation
    user_question = st.text_input("Ask the chatbot a question:")
    if st.button("Consult"):
        if user_question.strip():
            with st.spinner("Generating response..."):
                response = generate_response(user_question)  # Call the function for interaction
                st.write(f"**Immo Green AI:** {response}")
        else:
            st.warning("Please enter a question!")

# Gimni API integration using API key
def generate_response(user_query):
    api_key = st.secrets["GIMNI_API_KEY"]
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    url = "https://api.gimni.com/chat"  # Adjust this endpoint if necessary
    data = {"query": user_query}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json().get("response", "No response available.")
        else:
            return f"Error: {response.status_code}, please try again later."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# LangChain integration for data fetching from a website
def fetch_data_from_website(url):
    loader = WebBaseLoader(url)
    data = loader.load()
    return data

# Create LangChain retriever and use it for Q&A
def langchain_retriever(query):
    url = "https://www.rekhta.org"  # Replace with the actual website you want to scrape
    data = fetch_data_from_website(url)
    
    # Use Hugging Face's Sentence Transformers for Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Use FAISS as a vector store
    vectors = embeddings.embed_documents([d.page_content for d in data])
    
    # Create FAISS index
    index = faiss.IndexFlatL2(vectors[0].shape[0])
    index.add(np.array(vectors))
    
    # Query the vector store
    _, indices = index.search(np.array(embeddings.embed_query(query)).reshape(1, -1), k=1)
    
    if indices[0][0] != -1:
        return data[indices[0][0]].page_content
    else:
        return "No relevant data found."

# Main application flow
if "user_logged_in" not in st.session_state:
    st.session_state["user_logged_in"] = False

if not st.session_state["user_logged_in"]:
    show_welcome()
    st.info("Please log in to access all features.")
    login()
else:
    chatbot()
