#------------------------
# Building a Streamlit app to analyse text input & visualise word frequency
#------------------------

import pandas as pd
import streamlit as st
from collections import Counter

# Set name that appears on the browser tab (page title)
st.set_page_config(page_title="Analyst Text Tool")

# Create a text box on the screen for user input
text_input = st.text_area("Enter your text here:", height=200)

# If text box is not empty, run the code below
if text_input:

    # Preprocess the text, create a list of wordss
    words = text_input.lower().split()

    # Count the frequency of each word in that list
    word_count = Counter(words)

    # Create a DataFrame from the word count dictionary
    df = pd.DataFrame(word_count.items(), columns=['Word', 'Count'])

    # Sort the table by 'Count' (highest to lowest) and get the top 10 rows
    top_10 = df.sort_values(by='Count', ascending=False).head(10)

    # Split the screen into two equal side by sides columns
    col1, col2 = st.columns(2)

    # The Left Side: 
    with col1:
        # Add title
        st.subheader("Data Table")
        # Show table
        st.dataframe(top_10) # --> display dataframe as an interactive table

    # The Right Side:
    with col2:
        # Add title
        st.subheader("Visualisation")
        # Show bar chart with 'Word' on x-axis & 'Count' on y-axis
        st.bar_chart(top_10.set_index('Word')) # --> display bar chart

#------------------------
# Fin
# streamlit run app.py
#------------------------