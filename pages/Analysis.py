import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from pages.Home import homepage, home_placeholder

#---- UPLOAD FILE ----
def uploaded(key):
    uploaded_file = st.sidebar.file_uploader(label="Upload your file(CSV or Excel)",
        type=['csv','xlsx'],key=key,)
    return uploaded_file 

#---- READ EXCEL FILE ----
uploaded_file = uploaded("two")

def get_data_from_excel():
    if uploaded_file is not None:
        try:
            df = pd.read_excel(
                io = uploaded_file,
                engine = 'openpyxl',
                sheet_name = 'Sales',
                skiprows = 3,
                usecols = 'B:R',
                nrows = 1000,
            )
            df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
            return df
        except Exception:
            try:
                df = pd.read_csv(
                    io = uploaded_file,
                    engine = 'openpyxl',
                    sheet_name = 'Sales',
                    skiprows = 3,
                    usecols = 'B:R',
                    nrows = 1000,
                )
                df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
                return df
            except Exception as e:
                st.error(e)

def analysis():
    #---- HIDE STREAMLIT STYLE ----
    hide_st_style = """ 
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    header {visibility: hidden;}
                    </style>
                    """

    if get_data_from_excel() is not None:
        df = get_data_from_excel()

        #----SIDEBAR----
        st.sidebar.header("Filter:")
        city = st.sidebar.multiselect(
            "Select City:",
            options=df["City"].unique(),
            default=df["City"].unique(),
        )

        customer_type = st.sidebar.multiselect(
            "Select Customer Type:",
            options=df["Customer_type"].unique(),
            default=df["Customer_type"].unique(),
        )

        gender = st.sidebar.multiselect(
            "Select Gender:",
            options=df["Gender"].unique(),
            default=df["Gender"].unique(),
        )

        df_selection = df.query(
            "City == @city & Customer_type == @customer_type & Gender == @gender"
        )

        #----MAIN PAGE----
        st.title(":bar_chart: Sales Dashboard")
        st.markdown("##")

        # TOP KPI's
        total_sales = int(df_selection["Total"].sum())
        average_rating = round(df_selection["Rating"].mean(),1)
        star_rating = ":star:" * int(round(average_rating,0))
        average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

        left_column, middle_column, right_column = st.columns(3)
        with left_column:
            st.subheader("Total Sales:")
            st.subheader(f"US $ {total_sales:,}")
        with middle_column:
            st.subheader("Average rating:")
            st.subheader(f"{average_rating} {star_rating}")
        with right_column:
            st.subheader("Average Sales Per Transaction:")
            st.subheader(f"US $ {average_sale_by_transaction}")

        st.markdown("---")

        # SALES BY PRODUCT LINE [BAR CHART]
        sales_by_product_line = (
            df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
        )

        fig_product_sales = px.bar(
            sales_by_product_line,
            x="Total",
            y=sales_by_product_line.index,
            orientation='h',
            title= "<b> Sales by Product Line</b>",
            color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
            template = "plotly_white",
        )

        fig_product_sales.update_layout(
            plot_bgcolor = "rgba(0,0,0,0)",
            xaxis = (dict(showgrid=False)),
        )

        # SALES BY HOUR [BAR CHART]
        sales_by_hour = (
            df_selection.groupby(by=["hour"]).sum()[["Total"]]
        )

        fig_hourly_sales = px.bar(
            sales_by_hour,
            y="Total",
            x=sales_by_hour.index,
            title= "<b> Sales by Hour</b>",
            color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
            template = "plotly_white",
        )

        fig_hourly_sales.update_layout(
            plot_bgcolor = "rgba(0,0,0,0)",
            xaxis = dict(tickmode="linear"),
            yaxis = (dict(showgrid=False)),
        )

        left_column, right_column = st.columns(2)
        left_column.plotly_chart(fig_hourly_sales,use_container_width=True)
        right_column.plotly_chart(fig_product_sales,use_container_width=True)

        st.markdown(hide_st_style,unsafe_allow_html=True)

    elif get_data_from_excel() is None:
        home_placeholder("Please upload a CSV or Excel file to analyse.")

#---- CREATE PAGE ----
if __name__ == '__main__':
    global df # df is in try blocks

    try:
        if st.session_state["login"]:
            analysis()
        else:
            switch_page("SignUp or Login")
    except Exception as e:
        st.error(e)
        switch_page("SignUp or Login")
