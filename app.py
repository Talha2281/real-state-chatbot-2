import streamlit as st

# Dummy data for properties
dummy_properties = [
    {"title": "2 BHK Apartment in Zurich", "price": "$250,000", "location": "Zurich", "type": "Apartment"},
    {"title": "3 BHK Villa in Geneva", "price": "$1,000,000", "location": "Geneva", "type": "Villa"},
    {"title": "1 BHK Studio in Basel", "price": "$150,000", "location": "Basel", "type": "Studio"},
    {"title": "Office Space in Zurich", "price": "$500,000", "location": "Zurich", "type": "Commercial"},
]

def main():
    # Page settings
    st.set_page_config(page_title="Immo Green AI Chatbot", layout="wide")

    # Ask user if they are logged in
    st.title("Welcome to Immo Green AI!")
    st.info("Before we begin, let's confirm your login status.")
    logged_in = st.radio(
        "Have you logged in or registered on the official website?",
        ("Yes", "No"),
        index=1
    )

    if logged_in == "No":
        st.warning("Please log in or register on the official website to use this service.")
        st.write("[Go to Official Website](https://www.doclingo.ai)")
        return

    # Welcome message
    st.success("Thank you for confirming! How can we assist you today?")
    st.write("Use the chat below to ask questions or search for properties.")

    # Chat functionality
    st.subheader("Chat with Immo Green AI")
    query = st.text_input("Ask your question or search for properties:")
    if query:
        if "company" in query.lower():
            st.write("We are Immo Green AI, specializing in real estate solutions, including buying, selling, and renting properties. Our services also focus on green energy and sustainable living!")
        elif "services" in query.lower():
            st.write("We provide services like property consultations, rental management, and premium insights for green energy initiatives.")
        else:
            st.write("Thank you for your question. Please use the filters below to refine your search or ask more specific questions.")

    # Search filters
    st.subheader("Search for Properties")
    col1, col2, col3 = st.columns(3)

    with col1:
        location = st.selectbox("Location", ["All", "Zurich", "Geneva", "Basel"])
    with col2:
        price_range = st.selectbox("Price Range", ["All", "$100,000-$200,000", "$200,000-$500,000", "$500,000+"])
    with col3:
        property_type = st.selectbox("Property Type", ["All", "Apartment", "Villa", "Studio", "Commercial"])

    # Filter results
    st.subheader("Search Results")
    filtered_properties = [
        prop for prop in dummy_properties
        if (location == "All" or prop["location"] == location) and
           (price_range == "All" or (
               price_range == "$100,000-$200,000" and "$100,000" <= prop["price"] <= "$200,000") or
               (price_range == "$200,000-$500,000" and "$200,000" <= prop["price"] <= "$500,000") or
               (price_range == "$500,000+" and "$500,000" <= prop["price"])
           ) and
           (property_type == "All" or prop["type"] == property_type)
    ]

    if filtered_properties:
        for prop in filtered_properties:
            st.write(f"**{prop['title']}** - {prop['price']} - {prop['location']} - {prop['type']}")
    else:
        st.write("No properties match your search criteria. Please adjust the filters and try again.")

if __name__ == "__main__":
    main()

      
