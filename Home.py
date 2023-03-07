import streamlit as st

# Only render the background image for home page
st.markdown(
    f"""
     <style>
     .stApp {{
         background-image: url("https://tradebrains.in/features/wp-content/uploads/2021/07/stock-market-news-trade-brains.jpg");
         background-size: contain;
         background-repeat: no-repeat;
         -webkit-background-size: cover;
     }}
     </style>
     """,
    unsafe_allow_html=True
)


st.markdown("<h1 style='text-align: center; color: white; font-style: italic;'>ARIMA Studio</h1>",
            unsafe_allow_html=True)
st.markdown(
    "<h4 style='text-align: center; color: white; font-style: italic;'>Built by Alex Carney, Lauren Goyette, Edmund Aduse Poku</h4>",
    unsafe_allow_html=True)