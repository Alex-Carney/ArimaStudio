import streamlit as st
import pandas as pd
import common.arima_functions as arf
from resources.script_strings import explanations as ex

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


def visualize_order_plot(type: str):
    # Determine order of p, d, or q by generating the necessary plot
    pdq_fig = arf.find_pdq_plot(st.session_state.df, st.session_state.value_col_name, type)
    with col2:
        st.pyplot(pdq_fig)


def tag_and_process_data(date_col_name: str, value_col_name: str, starting_date: str):
    # Save index column and response variable column name for later
    st.session_state.value_col_name = value_col_name
    st.session_state.date_col_name = date_col_name

    # Process Step 1: Convert Date column to a datetime object, only grab DF past start year
    df = st.session_state.df

    df[date_col_name] = pd.to_datetime(df[date_col_name])
    df.set_index(date_col_name, inplace=True)
    df = df.loc[df.index > pd.Timestamp(starting_date)]

    # Process Step 2: Reindex DF based on business days
    business_days = pd.bdate_range(start=df.index.min(), end=df.index.max())
    df = df.reindex(business_days)
    # interpolate missing values
    df = df.interpolate()

    # Signal that data processing can begin
    st.session_state.df = df
    st.session_state.data_processing_flag = True


def build_and_forecast_model(model_spec: tuple, seasonal_model_spec: tuple, train_test_date, num_prediction_days: int):
    final_plot, model_summary_df = arf.build_and_forecast(st.session_state.df,
                                        st.session_state.value_col_name,
                                        model_spec,
                                        seasonal_model_spec,
                                        train_test_date,
                                        num_prediction_days)
    with col2:
        st.pyplot(final_plot)
        st.dataframe(model_summary_df)


def build_and_forecast_optimal_model(seasonal_frequency, train_test_date, num_prediction_days):
    optimal_model = arf.determine_optimal_sarima(st.session_state.df,
                                                 st.session_state.value_col_name,
                                                 seasonal_frequency)
    final_plot, model_summary_df = arf.build_and_forecast(st.session_state.df,
                                        st.session_state.value_col_name,
                                        optimal_model.order,
                                        optimal_model.seasonal_order,
                                        train_test_date,
                                        num_prediction_days)
    with col2:
        st.pyplot(final_plot)
        st.dataframe(model_summary_df)


# ------------------- WIDGETS -------------------------- #

col1, col2 = st.columns([1, 1])

# Column 1 is for data
st.session_state.col1 = col1

# Column 2 is for plots
st.session_state.col2 = col2

col1.header("Interact with Data")
col2.header("Data Visualization")

if st.session_state.df is None:
    col1.write(ex['pre_upload'])
    col1.markdown("**If anything goes wrong just refresh the page and start again, sorry for any "
                  "inconveniences in advance**")


# Only render this options pane once data has been uploaded
if st.session_state.df is not None:
    if st.session_state.data_processing_flag is None or st.session_state.data_processing_flag is False:
        col1.write(ex['data_selection'])
    # Setup Options Expander
    data_options_expander = col1.expander(label='Data Selection')
    with data_options_expander:
        data_naming_form = st.form(key="data_naming_form", clear_on_submit=False)
        with data_naming_form:
            date_col_n = st.text_input("Name of Date Column", value="Date")
            value_col_n = st.text_input("Name of Response Column", value="Close")
            start_date = st.date_input("Start Date")
            data_name_submit = data_naming_form.form_submit_button("Process Data")
            if date_col_n is not None and \
                    value_col_n is not None and \
                    start_date is not None and \
                    data_name_submit is True:
                try:
                    tag_and_process_data(date_col_n, value_col_n, start_date)
                except ValueError as ve:
                    print(ve)
                    st.warning("A Value Error occurred. Does your start date make sense for your data?")
                    st.warning("Please refresh the page and try again with a correct date. Your data may have been "
                               "corrupted")

# Only render once data has been properly tagged and pre-processed
if st.session_state.data_processing_flag:
    col1.write(ex['exploration'])
    # Setup Exploration Expander
    exploration_expander = col1.expander(label="Explore Your Data")
    with exploration_expander:
        st.write(ex['decomposition'])
        decompose_data_button = st.button("Decompose Time Series",
                                          on_click=decompose_time_series)

if st.session_state.data_processing_flag:
    # Setup PDQ Expander
    pdq_expander = col1.expander(label="Determine P,D,Q")
    with pdq_expander:
        st.write(ex['pdq'])
        st.button("Determine D Order", on_click=visualize_order_plot, args='d')
        st.button("Determine P Order", on_click=visualize_order_plot, args='p')
        st.button("Determine Q Order", on_click=visualize_order_plot, args='q')

if st.session_state.data_processing_flag:
    # Setup build model expander
    model_expander = col1.expander(label="Build Model and Forecast")
    with model_expander:
        st.write(ex['build_forecast'])
        model_build_form = st.form(key="model_build_form", clear_on_submit=False)
        with model_build_form:
            p_order = st.number_input("P Order", value=0)
            d_order = st.number_input("D Order", value=0)
            q_order = st.number_input("Q Order", value=0)
            train_test_date = st.date_input("Forecast Start Date")
            num_prediction_days = st.number_input("Number of days to predict")
            model_run_submit = st.form_submit_button("Build And Forecast")
            if p_order is not None and \
                    d_order is not None and \
                    q_order is not None and \
                    train_test_date is not None and \
                    num_prediction_days is not None and \
                    model_run_submit is True:
                try:
                    build_and_forecast_model((p_order, d_order, q_order), (), train_test_date, int(num_prediction_days))
                except ValueError as ve:
                    print(ve)
                    st.warning("A Value Error occurred. Does your start date make sense for your data?")

if st.session_state.data_processing_flag:
    # Setup do it for me expander
    smodel_expander = col1.expander(label="Build Automatically")
    with smodel_expander:
        st.write(ex['automatically'])
        smodel_form = st.form(key="smodel_build_form", clear_on_submit=False)
        with smodel_form:
            seasonal_frequency = st.number_input("Seasonal Frequency", value=7)
            smodel_train_test_date = st.date_input("Forecast Start Date")
            smodel_num_prediction_days = st.number_input("Number of days to predict", value=7)
            smodel_run_submit = st.form_submit_button("Build And Forecast")
            if seasonal_frequency is not None \
                    and smodel_run_submit is True:
                try:
                    build_and_forecast_optimal_model(int(seasonal_frequency), smodel_train_test_date, int(smodel_num_prediction_days))
                except ValueError as ve:
                    print(ve)
                    st.warning("A Value Error occurred. Does your start date make sense for your data?")

# Render the data only if it exists
if st.session_state.df is not None:
    col1.dataframe(st.session_state.df)

# DEFAULT SCREEN - SEE THIS ON STARTUP
col1.file_uploader("Upload CSV", type=["csv"], key="uploaded_data", on_change=upload_csv_callback)
col1.button("Use Our MSFT Data", key="default_data", on_click=upload_default_csv_callback)
