import streamlit as st
import requests
import pandas as pd


# --------------------------------------------------
# Page title
# --------------------------------------------------

st.title("ReviewStream")
st.subheader("Real-Time Review Intelligence")


# --------------------------------------------------
# Get review analytics
# --------------------------------------------------

analytics_response = requests.get(
    "http://127.0.0.1:8001/analytics"
)

analytics = analytics_response.json()


# --------------------------------------------------
# KPI cards
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Reviews",
        analytics["total_reviews"]
    )

with col2:
    st.metric(
        "Average Rating",
        f"{analytics['average_rating']} ⭐"
    )

with col3:
    st.metric(
        "Positive Reviews",
        analytics["positive_reviews"]
    )

with col4:
    st.metric(
        "Negative Reviews",
        analytics["negative_reviews"]
    )


st.write("---")


# --------------------------------------------------
# Sentiment distribution
# --------------------------------------------------

st.subheader("📊 Review Sentiment Distribution")

sentiment_data = pd.DataFrame(
    {
        "Reviews": [
            analytics["positive_reviews"],
            analytics["neutral_reviews"],
            analytics["negative_reviews"]
        ]
    },
    index=[
        "Positive",
        "Neutral",
        "Negative"
    ]
)

st.bar_chart(sentiment_data)


st.write("---")


# --------------------------------------------------
# Recent reviews
# --------------------------------------------------

st.subheader("📝 Recent Reviews")

reviews_response = requests.get(
    "http://127.0.0.1:8001/reviews"
)

reviews_data = reviews_response.json()

for review in reviews_data["reviews"]:

    st.write(
        f"### ⭐ Rating: {review['rating']}"
    )

    st.write(
        review["review_text"]
    )

    st.write(
        f"Sentiment: **{review['rating_category']}**"
    )

    st.write("---")


# --------------------------------------------------
# Semantic search
# --------------------------------------------------

st.subheader("🔎 Semantic Review Search")

st.write(
    "Search customer reviews using natural language."
)

query = st.text_input(
    "Enter your search",
    placeholder="Example: customers complaining about delivery"
)


if st.button("Search"):

    response = requests.post(
        "http://127.0.0.1:8001/search",
        json={"query": query}
    )

    data = response.json()

    st.write("### Search Results")

    for result in data["results"]:

        st.write(
            f"### ⭐ Rating: {result['rating']}"
        )

        st.write(
            result["review_text"]
        )

        similarity = 1 - result["distance"]

        st.write(
            f"Similarity: {similarity * 100:.1f}%"
        )

        st.write("---")