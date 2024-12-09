import streamlit as st

# Expanded dummy data for properties
dummy_properties = [
    {"title": "2 BHK Apartment in Zurich", "price": 250000, "location": "Zurich", "type": "Apartment"},
    {"title": "3 BHK Villa in Geneva", "price": 1000000, "location": "Geneva", "type": "Villa"},
    {"title": "1 BHK Studio in Basel", "price": 150000, "location": "Basel", "type": "Studio"},
    {"title": "Office Space in Lausanne", "price": 500000, "location": "Lausanne", "type": "Commercial"},
    {"title": "4 BHK House in Bern", "price": 750000, "location": "Bern", "type": "Villa"},
    {"title": "Luxury Penthouse in Lucerne", "price": 1200000, "location": "Lucerne", "type": "Apartment"},
    {"title": "Cozy Studio in Zurich", "price": 200000, "location": "Zurich", "type": "Studio"},
    {"title": "Retail Space in Geneva", "price": 600000, "location": "Geneva", "type": "Commercial"},
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
        location = st.selectbox("Location", ["All"] + list(set([prop["location"] for prop in dummy_properties])))
    with col2:
        price_range = st.selectbox("Price Range", [
            "All",
            "100,000 - 200,000",
            "200,000 - 500,000",
            "500,000 - 1,000,000",
            "1,000,000+"
        ])
    with col3:
        property_type = st.selectbox("Property Type", ["All"] + list(set([prop["type"] for prop in dummy_properties])))

    # Filter results based on user selection
    st.subheader("Search Results")
    filtered_properties = []
    for prop in dummy_properties:
        # Location filter
        if location != "All" and prop["location"] != location:
            continue
        # Price range filter
        if price_range != "All":
            if price_range == "100,000 - 200,000" and not (100000 <= prop["price"] <= 200000):
                continue
            if price_range == "200,000 - 500,000" and not (200000 <= prop["price"] <= 500000):
                continue
            if price_range == "500,000 - 1,000,000" and not (500000 <= prop["price"] <= 1000000):
                continue
            if price_range == "1,000,000+" and prop["price"] < 1000000:
                continue
        # Property type filter
        if property_type != "All" and prop["type"] != property_type:
            continue
        # Add property to filtered results
        filtered_properties.append(prop)

    # Display results
    if filtered_properties:
        for prop in filtered_properties:
            st.write(f"**{prop['title']}** - ${prop['price']} - {prop['location']} - {prop['type']}")
    else:
        st.write("No properties match your search criteria. Please adjust the filters and try again.")

if __name__ == "__main__":
    main()
