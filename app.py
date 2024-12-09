import streamlit as st

# Dummy property data for cities in Switzerland
dummy_properties = [
    {"title": "2 BHK Apartment", "price": 250000, "location": "Zurich", "type": "Apartment"},
    {"title": "3 BHK Villa", "price": 1000000, "location": "Geneva", "type": "Villa"},
    {"title": "1 BHK Studio", "price": 150000, "location": "Basel", "type": "Studio"},
    {"title": "Office Space", "price": 500000, "location": "Lausanne", "type": "Commercial"},
    {"title": "4 BHK House", "price": 750000, "location": "Bern", "type": "Villa"},
    {"title": "Luxury Penthouse", "price": 1200000, "location": "Lucerne", "type": "Apartment"},
    {"title": "Cozy Studio", "price": 200000, "location": "Winterthur", "type": "Studio"},
    {"title": "Retail Space", "price": 600000, "location": "Lugano", "type": "Commercial"},
    {"title": "Modern Apartment", "price": 400000, "location": "St. Gallen", "type": "Apartment"},
    {"title": "Classic Villa", "price": 900000, "location": "Thun", "type": "Villa"},
]

# Initialize session state for filters
if "location" not in st.session_state:
    st.session_state["location"] = "All"
if "price_range" not in st.session_state:
    st.session_state["price_range"] = "All"
if "property_type" not in st.session_state:
    st.session_state["property_type"] = "All"
if "show_results" not in st.session_state:
    st.session_state["show_results"] = False


def main():
    # Page settings
    st.set_page_config(page_title="Immo Green AI Chatbot", page_icon="🏡", layout="wide")

    # Ask user if they are logged in
    st.title("👋 Welcome to Immo Green AI!")
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
    query = st.text_input("Ask your question:")
    if query:
        st.write(f"**Answer**: {get_chat_response(query)}")

    # Search functionality
    st.subheader("Search for Properties")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.session_state["location"] = st.selectbox(
            "Location", ["All"] + list(set([prop["location"] for prop in dummy_properties])),
            key="location_selector"
        )
    with col2:
        st.session_state["price_range"] = st.selectbox(
            "Price Range",
            ["All", "100,000 - 200,000", "200,000 - 500,000", "500,000 - 1,000,000", "1,000,000+"],
            key="price_selector"
        )
    with col3:
        st.session_state["property_type"] = st.selectbox(
            "Property Type",
            ["All"] + list(set([prop["type"] for prop in dummy_properties])),
            key="type_selector"
        )

    # Apply filters
    if st.button("Apply Filters"):
        st.session_state["show_results"] = True

    # Show results
    if st.session_state["show_results"]:
        display_filtered_properties()


def get_chat_response(query):
    """Dummy knowledge base responses."""
    knowledge_base = {
        "what is real estate": "Real estate involves the buying, selling, and renting of land, buildings, and homes.",
        "what services do you offer": "We offer services like property consultations, buying and selling assistance, rental management, and green energy solutions.",
        "how to sell a property": "To sell a property, you can list it on our platform by registering and providing the necessary details.",
        "what is the price range in zurich": "Property prices in Zurich typically range from $200,000 to $1,200,000, depending on the type and location.",
        "what is green energy": "Green energy refers to energy sources that are renewable and environmentally friendly, like solar, wind, and hydropower.",
    }
    return knowledge_base.get(query.lower(), "I'm sorry, I don't have information on that topic. Please ask something else.")


def display_filtered_properties():
    """Filter and display property results based on user selection."""
    filtered_properties = []
    for prop in dummy_properties:
        # Location filter
        if st.session_state["location"] != "All" and prop["location"] != st.session_state["location"]:
            continue
        # Price range filter
        if st.session_state["price_range"] != "All":
            if st.session_state["price_range"] == "100,000 - 200,000" and not (100000 <= prop["price"] <= 200000):
                continue
            if st.session_state["price_range"] == "200,000 - 500,000" and not (200000 <= prop["price"] <= 500000):
                continue
            if st.session_state["price_range"] == "500,000 - 1,000,000" and not (500000 <= prop["price"] <= 1000000):
                continue
            if st.session_state["price_range"] == "1,000,000+" and prop["price"] < 1000000:
                continue
        # Property type filter
        if st.session_state["property_type"] != "All" and prop["type"] != st.session_state["property_type"]:
            continue
        # Add property to filtered results
        filtered_properties.append(prop)

    # Display results
    st.subheader("Search Results")
    if filtered_properties:
        for prop in filtered_properties:
            st.write(f"**{prop['title']}** - ${prop['price']} - {prop['location']} - {prop['type']}")
    else:
        st.write("No properties match your search criteria. Please adjust the filters and try again.")


if __name__ == "__main__":
    main()
