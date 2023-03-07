import streamlit as st
import pandas as pd
import common.arima_functions as arf

st.write("Hello World, Studio Page")

# ----------------- GLOBAL DATA AND INITIAL STATE VALUES ------------------- #
if 'data_processing_flag' not in st.session_state:
    st.session_state.data_processing_flag = False
if 'df' not in st.session_state:
    st.session_state.df = None


# ----------------- HELPER FUNCTIONS ------------------- #

def upload_csv_callback():
    if st.session_state.uploaded_data is not None:
        df_to_display = pd.read_csv(st.session_state.uploaded_data)
        st.session_state.df = df_to_display
        with col1:
            st.dataframe(df_to_display)


def upload_default_csv_callback():
    if st.session_state.default_data is not None:
        df_to_display = pd.read_csv("./resources/microsoft_stock_prices.csv")
        st.session_state.df = df_to_display

def decompose_time_series():
    # Decompose time series into Trend and Seasonality, both Add. and Mult. wise
    result_mul, result_add = arf.decompose_data(st.session_state.df, st.session_state.value_col_name)
    fig_mul = result_mul.plot()
    fig_mul.suptitle('Multiplicative Decompose', fontsize=22)
    fig_add = result_add.plot()
    fig_add.suptitle('Additive Decompose', fontsize=22)
    with col2:
        st.pyplot(fig_mul)
        st.pyplot(fig_add)





def tag_and_process_data(date_col_name: str, value_col_name: str, start_year: str):
    # Save index column and response variable column name for later
    st.session_state.value_col_name = value_col_name
    st.session_state.date_col_name = date_col_name
    st.session_state.start_year = int(start_year)

    # Process Step 1: Convert Date column to a datetime object, only grab DF past start year
    df = st.session_state.df

    df[date_col_name] = pd.to_datetime(df[date_col_name])
    mask = df[date_col_name].dt.year >= int(start_year)
    df = df.loc[mask]
    df.index = df.index - df.index[0]
    df.set_index(date_col_name, inplace=True)

    # Process Step 2: Reindex DF based on business days
    business_days = pd.bdate_range(start=df.index.min(), end=df.index.max())
    df = df.reindex(business_days)
    # interpolate missing values
    df = df.interpolate()

    # Signal that data processing can begin
    st.session_state.df = df
    st.session_state.data_processing_flag = True


# ------------------- WIDGETS -------------------------- #

col1, col2 = st.columns([1, 1])

# Column 1 is for data
st.session_state.col1 = col1

# Column 2 is for plots
st.session_state.col2 = col2

col1.header("Interact with Data")
col2.header("Data Visualization")

# Only render this options pane once data has been uploaded
if st.session_state.df is not None:
    # Setup Options Expander
    data_options_expander = col1.expander(label='Data Selection')
    with data_options_expander:
        data_naming_form = st.form(key="data_naming_form", clear_on_submit=False)
        with data_naming_form:
            date_col_n = st.text_input("Name of Date Column", value="Date")
            value_col_n = st.text_input("Name of Response Column", value="Close")
            start_year_in = st.text_input("Start Year", value="2022")
            data_name_submit = data_naming_form.form_submit_button("Process Data")
            if date_col_n is not None and \
                    value_col_n is not None and \
                    start_year_in is not None and \
                    data_name_submit is True:
                tag_and_process_data(date_col_n, value_col_n, start_year_in)

# Only render once data has been properly tagged and pre-processed
if st.session_state.data_processing_flag:
    # Setup Exploration Expander
    exploration_expander = col1.expander(label="Explore Your Data")
    with exploration_expander:
        decompose_data_button = st.button("Decompose Time Series",
                                          on_click=decompose_time_series)


if st.session_state.data_processing_flag:
    # Setup PDQ Expander
    pdq_expander = col1.expander(label="Determine P,D,Q")
    with pdq_expander:
        st.button("Determine D Order")
        st.button("Determine P Order")
        st.button("Determine Q Order")


# Render the data only if it exists
if st.session_state.df is not None:
    col1.dataframe(st.session_state.df)

# DEFAULT SCREEN - SEE THIS ON STARTUP
col1.file_uploader("Upload CSV", type=["csv"], key="uploaded_data", on_change=upload_csv_callback)
col1.button("Use Our MSFT Data", key="default_data", on_click=upload_default_csv_callback)
