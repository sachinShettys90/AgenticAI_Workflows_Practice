import streamlit as st
import numpy as np
import pandas as pd

# Text and headers
st.header("This is a header")
st.subheader("Subheader")
st.text("Plain text")

# Button
if st.button("Click me!"):
    st.write("Button clicked! 🎉")

# Slider
age = st.slider("How old are you?", 0, 130, 25)
st.write(f"You are {age} years old.")

# Selectbox
option = st.selectbox("Choose a color", ["Red", "Blue", "Green"])
st.write(f"You selected: {option}")

# Text input
name = st.text_input("Enter your name")
if name:
    st.write(f"Hello, {name}!")

# Checkbox
if st.checkbox("Show dataframe"):
    df = pd.DataFrame(np.random.randn(10, 5), columns=(
        "col %d" % i for i in range(5)))
    st.dataframe(df)

# Sidebar (great for controls)
st.sidebar.title("Sidebar Controls")
sidebar_slider = st.sidebar.slider("Sidebar slider", 0, 100, 50)
st.write(f"Sidebar value: {sidebar_slider}")


# *************************************************************************************************
df = pd.DataFrame(np.random.randn(20, 3), columns=["A", "B", "C"])

st.title("Built-in Streamlit Charts")

st.line_chart(df)       # Line chart
st.area_chart(df)       # Area chart
st.bar_chart(df)        # Bar chart
st.scatter_chart(df)    # Scatter chart (newer versions)


# *************************************************************************************************

st.sidebar.header("Filters")
selected_cols = st.sidebar.multiselect(
    "Columns", df.columns, default=df.columns.tolist())
year = st.sidebar.slider("Simulated Year", 2000, 2025, 2023)

# Filtered/dynamic data
filtered_df = df[selected_cols] * year  # Dummy example

st.write("### Filtered Data View")
st.dataframe(filtered_df)

st.write("### Dynamic Chart")
st.line_chart(filtered_df)
