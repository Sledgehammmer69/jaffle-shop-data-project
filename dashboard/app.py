import streamlit as st
import snowflake.connector

st.set_page_config(
    page_title="Jaffle Shop Analytics",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Jaffle Shop Analytics")
st.caption("Customer, order and payment performance")
if st.button("🔄 Refresh dashboard"):
    st.cache_data.clear()
    st.rerun()

@st.cache_resource
def get_connection():
    return snowflake.connector.connect(
        account=st.secrets["snowflake"]["account"],
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"],
        role=st.secrets["snowflake"]["role"],
    )

@st.cache_data(ttl=300)
def load_kpis():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT
                (SELECT COUNT(*)
                 FROM ANALYTICS.DBT_NPUSPANATHAN.DIM_CUSTOMERS)
                    AS total_customers,

                (SELECT COUNT(*)
                 FROM ANALYTICS.DBT_NPUSPANATHAN.FCT_ORDERS)
                    AS total_orders,

                (SELECT COALESCE(
                    SUM(SUCCESSFUL_PAYMENT_AMOUNT), 0
                 )
                 FROM ANALYTICS.DBT_NPUSPANATHAN.FCT_ORDERS)
                    AS successful_payment_amount,

                (SELECT COALESCE(
                    SUM(FAILED_PAYMENT_COUNT), 0
                 )
                 FROM ANALYTICS.DBT_NPUSPANATHAN.FCT_ORDERS)
                    AS failed_payment_attempts
        """)

        return cursor.fetchone()

    finally:
        cursor.close()

try:
    total_customers, total_orders, successful_amount, failed_attempts = (
        load_kpis()
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Customers", f"{total_customers:,}")
    col2.metric("Total Orders", f"{total_orders:,}")
    col3.metric("Successful Payment Amount", f"{successful_amount:,.0f}")
    col4.metric("Failed Payment Attempts", f"{failed_attempts:,}")

    st.success("Dashboard data loaded successfully from Snowflake.")




    st.divider()

    st.subheader("🏆 Top 10 Customers by Successful Payment Amount")

    @st.cache_data(ttl=300)
    def load_top_customers():
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT
                    FIRST_NAME || ' ' || LAST_NAME AS CUSTOMER_NAME,
                    TOTAL_SUCCESSFUL_PAYMENT_AMOUNT
                FROM ANALYTICS.DBT_NPUSPANATHAN.DIM_CUSTOMERS
                ORDER BY TOTAL_SUCCESSFUL_PAYMENT_AMOUNT DESC
                LIMIT 10
            """)

            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            return rows, columns

        finally:
            cursor.close()

    customer_rows, customer_columns = load_top_customers()

    import pandas as pd

    customer_df = pd.DataFrame(
        customer_rows,
        columns=customer_columns,
    )

    st.bar_chart(
        customer_df,
        x="CUSTOMER_NAME",
        y="TOTAL_SUCCESSFUL_PAYMENT_AMOUNT",
        horizontal=True,
    )



    ######Customer Analytics######

    st.divider()

    st.subheader("📦 Order Status Breakdown")

    @st.cache_data(ttl=300)
    def load_order_status():
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT
                    ORDER_STATUS,
                    COUNT(*) AS ORDER_COUNT
                FROM ANALYTICS.DBT_NPUSPANATHAN.FCT_ORDERS
                GROUP BY ORDER_STATUS
                ORDER BY ORDER_COUNT DESC
            """)

            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            return rows, columns

        finally:
            cursor.close()

    status_rows, status_columns = load_order_status()

    status_df = pd.DataFrame(
        status_rows,
        columns=status_columns,
    )

    st.bar_chart(
        status_df,
        x="ORDER_STATUS",
        y="ORDER_COUNT",
    )

    #### Payment Analytics ####
    
    st.divider()

    st.subheader("💳 Payment Outcomes")

    @st.cache_data(ttl=300)
    def load_payment_outcomes():
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT
                    'Successful' AS PAYMENT_OUTCOME,
                    SUM(SUCCESSFUL_PAYMENT_COUNT) AS ATTEMPT_COUNT
                FROM ANALYTICS.DBT_NPUSPANATHAN.FCT_ORDERS

                UNION ALL

                SELECT
                    'Failed' AS PAYMENT_OUTCOME,
                    SUM(FAILED_PAYMENT_COUNT) AS ATTEMPT_COUNT
                FROM ANALYTICS.DBT_NPUSPANATHAN.FCT_ORDERS
            """)

            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

            return rows, columns

        finally:
            cursor.close()

    payment_rows, payment_columns = load_payment_outcomes()

    payment_df = pd.DataFrame(
        payment_rows,
        columns=payment_columns,
    )

    st.bar_chart(
        payment_df,
        x="PAYMENT_OUTCOME",
        y="ATTEMPT_COUNT",
    )

    st.dataframe(payment_df, hide_index=True)



except Exception as e:
    st.error("Unable to load dashboard data from Snowflake.")
    st.exception(e)
