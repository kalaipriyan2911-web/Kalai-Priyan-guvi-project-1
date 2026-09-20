import streamlit as st
import mysql.connector
import pandas as pd


# =========================================================
# MySQL DATABASE CONNECTION
# =========================================================

def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        port=3307,
        user="root",
        password="",
        database="Sales Analytics & Financial Tracking System"
    )


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Sales Analytics & Financial Tracking System",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

if "branch_id" not in st.session_state:
    st.session_state.branch_id = None


# =========================================================
# LOGIN FUNCTION
# =========================================================

def login_user(username, password):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            user_id,
            username,
            role,
            branch_id,
            email
        FROM users
        WHERE username = %s
        AND password = %s
    """

    cursor.execute(query, (username, password))

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    return user


# =========================================================
# LOGIN PAGE
# =========================================================

if not st.session_state.logged_in:

    st.title("📊 Sales Analytics & Financial Tracking System")

    st.subheader("Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if username == "" or password == "":
            st.warning("Please enter username and password.")

        else:

            try:

                user = login_user(username, password)

                if user:

                    st.session_state.logged_in = True
                    st.session_state.username = user["username"]
                    st.session_state.role = user["role"]
                    st.session_state.branch_id = user["branch_id"]

                    st.success("Login successful!")

                    st.rerun()

                else:

                    st.error("Invalid username or password.")

            except Exception as e:

                st.error("Database connection error.")
                st.write(e)

    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📊 Sales Management")

st.sidebar.write(
    f"Welcome, **{st.session_state.username}**"
)

st.sidebar.write(
    f"Role: **{st.session_state.role}**"
)


# =========================================================
# LOGOUT
# =========================================================

if st.sidebar.button("Logout"):

    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.branch_id = None

    st.rerun()


# =========================================================
# DASHBOARD TITLE
# =========================================================

st.title("📊 Sales Analytics Dashboard")

st.write(
    f"Logged in as: **{st.session_state.role}**"
)


# =========================================================
# LOAD BRANCHES
# =========================================================

connection = get_connection()

branches_df = pd.read_sql(
    "SELECT branch_id, branch_name FROM branches",
    connection
)

connection.close()

# =========================================================
# ADD NEW SALE
# =========================================================

st.subheader("➕ Add New Sale")

with st.expander("Create a New Sales Entry"):

    with st.form("new_sale_form"):

        col1, col2 = st.columns(2)

        with col1:

            branch_name = st.selectbox(
                "Branch",
                branches_df["branch_name"].tolist()
            )

            sale_date = st.date_input(
                "Sale Date"
            )

            customer_name = st.text_input(
                "Customer Name"
            )

            mobile_number = st.text_input(
                "Mobile Number"
            )

        with col2:

            product_name = st.selectbox(
                "Product Name",
                [
                    "Laptop",
                    "Smartphone",
                    "Smart TV",
                    "Tablet",
                    "Monitor",
                    "Smartwatch",
                    "Bluetooth Speaker",
                    "Wireless Earbuds",
                    "Keyboard",
                    "Mouse"
                ]
            )

            gross_sales = st.number_input(
                "Gross Sales",
                min_value=0.0,
                step=500.0
            )

            status = st.selectbox(
                "Status",
                ["Open", "Close"]
            )

        submit_sale = st.form_submit_button(
            "Add Sale"
        )

        if submit_sale:
            

            if customer_name == "" or mobile_number == "":
                st.warning(
                    "Please enter customer name and mobile number."
                )

            else:

                try:

                    connection = get_connection()
                    cursor = connection.cursor()

                    # Get branch ID
                    cursor.execute(
                        """
                        SELECT branch_id
                        FROM branches
                        WHERE branch_name = %s
                        """,
                        (branch_name,)
                    )

                    branch = cursor.fetchone()

                    # Insert new sale
                    cursor.execute(
                        """
                        INSERT INTO customer_sales
                        (
                            branch_id,
                            date,
                            name,
                            mobile_number,
                            product_name,
                            gross_sales,
                            received_amount,
                            status
                        )
                        VALUES
                        (
                            %s, %s, %s, %s,
                            %s, %s, %s, %s
                        )
                        """,
                        (
                            branch[0],
                            sale_date,
                            customer_name,
                            mobile_number,
                            product_name,
                            gross_sales,
                            0.00,
                            status
                        )
                    )

                    connection.commit()

                    cursor.close()
                    connection.close()

                    st.success(
                        "New sale added successfully!"
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        "Error while adding sale."
                    )

                    st.write(e)
# =========================================================
# ADD PAYMENT
# =========================================================

st.subheader("💳 Add Payment")

with st.expander("Create a New Payment Entry"):

    # Get sales for payment
    connection = get_connection()

    payment_sales_df = pd.read_sql(
        """
        SELECT
            sale_id,
            name,
            product_name,
            gross_sales,
            received_amount,
            pending_amount
        FROM customer_sales
        WHERE pending_amount > 0
        ORDER BY sale_id
        """,
        connection
    )

    connection.close()

    if payment_sales_df.empty:

        st.info("No pending sales available for payment.")

    else:

        with st.form("payment_form"):

            sale_options = payment_sales_df["sale_id"].astype(int).tolist()

            selected_sale = st.selectbox(
                "Sale ID",
                 sale_options,
                 index=0,
                 key="payment_sale_id"
            

            )
            selected_sale_data = payment_sales_df[
                payment_sales_df["sale_id"] == selected_sale
            ].iloc[0]

            st.write(f"Customer: **{selected_sale_data['name']}**")
          
            st.write(f"Product: **{selected_sale_data['product_name']}**")

            st.write(f"Pending Amount: **₹{selected_sale_data['pending_amount']:.2f}**")

            payment_date = st.date_input(
                "Payment Date"
            )

            amount_paid = st.number_input(
               "Amount Paid",
               min_value=0.01,
               step=1.0,
              value=500.0,
             key="payment_amount"

            )
            

            payment_method = st.selectbox(
                "Payment Method",
                [
                    "Cash",
                    "UPI",
                    "Card"
                ]
            )

            submit_payment = st.form_submit_button(
                "Add Payment"
            )

            if submit_payment:

                try:

                    connection = get_connection()
                    cursor = connection.cursor()

                    cursor.execute(
                        """
                        INSERT INTO payment_splits
                        (
                            sale_id,
                            payment_date,
                            amount_paid,
                            payment_method
                        )
                        VALUES
                        (%s, %s, %s, %s)
                        """,
                        (
                            selected_sale,
                            payment_date,
                            amount_paid,
                            payment_method
                        )
                    )

                    connection.commit()

                    cursor.close()
                    connection.close()

                    st.success(
                        "Payment added successfully!"
                    )

                    st.rerun()

                except Exception as e:

                    st.error(
                        "Error while adding payment."
                    )

                    st.write(e)
# =========================================================
# FILTERS
# =========================================================

st.subheader("🔍 Sales Filters")

col1, col2, col3, col4 = st.columns(4)


# Branch filter

with col1:

    branch_options = ["All"] + branches_df["branch_name"].tolist()

    selected_branch = st.selectbox(
        "Branch",
        branch_options
    )


# Product filter

with col2:

    product_options_query = """
        SELECT DISTINCT product_name
        FROM customer_sales
        ORDER BY product_name
    """

    connection = get_connection()

    product_df = pd.read_sql(
        product_options_query,
        connection
    )

    connection.close()

    product_options = (
        ["All"] +
        product_df["product_name"].tolist()
    )

    selected_product = st.selectbox(
        "Product",
        product_options
    )


# Start date

with col3:

    start_date = st.date_input(
        "Start Date"
    )


# End date

with col4:

    end_date = st.date_input(
        "End Date"
    )


# =========================================================
# SALES QUERY
# =========================================================

query = """
    SELECT
        cs.sale_id,
        b.branch_name,
        cs.date,
        cs.name,
        cs.mobile_number,
        cs.product_name,
        cs.gross_sales,
        cs.received_amount,
        cs.pending_amount,
        cs.status
    FROM customer_sales cs
    JOIN branches b
        ON cs.branch_id = b.branch_id
    WHERE 1 = 1
"""

params = []


# Branch filter

if selected_branch != "All":

    query += """
        AND b.branch_name = %s
    """

    params.append(selected_branch)


# Product filter

if selected_product != "All":

    query += """
        AND cs.product_name = %s
    """

    params.append(selected_product)


# Date filters

query += """
    AND cs.date >= %s
    AND cs.date <= %s
"""

params.append(start_date)
params.append(end_date)


query += """
    ORDER BY cs.date DESC
"""


# =========================================================
# LOAD SALES DATA
# =========================================================

connection = get_connection()

sales_df = pd.read_sql(
    query,
    connection,
    params=params
)

connection.close()


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_sales = sales_df["gross_sales"].sum()

total_received = sales_df["received_amount"].sum()

total_pending = sales_df["pending_amount"].sum()

total_transactions = len(sales_df)


# =========================================================
# KPI DISPLAY
# =========================================================

st.subheader("💰 Financial Summary")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)


with kpi1:

    st.metric(
        "Total Sales",
        f"₹{total_sales:,.2f}"
    )


with kpi2:

    st.metric(
        "Total Received",
        f"₹{total_received:,.2f}"
    )


with kpi3:

    st.metric(
        "Total Pending",
        f"₹{total_pending:,.2f}"
    )


with kpi4:

    st.metric(
        "Total Transactions",
        total_transactions
    )


# =========================================================
# SALES TABLE
# =========================================================

st.subheader("🧾 Customer Sales")

if sales_df.empty:

    st.info("No sales records found for the selected filters.")

else:

    st.dataframe(
        sales_df,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# BRANCH-WISE SALES
# =========================================================

st.subheader("🏢 Branch-wise Sales")

if not sales_df.empty:

    branch_summary = (
        sales_df
        .groupby("branch_name")["gross_sales"]
        .sum()
        .reset_index()
    )

    branch_summary.columns = [
        "Branch",
        "Total Sales"
    ]

    st.dataframe(
        branch_summary,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# PAYMENT STATUS
# =========================================================

st.subheader("💳 Payment Status")

if not sales_df.empty:

    status_summary = (
        sales_df
        .groupby("status")
        .size()
        .reset_index(name="Number of Sales")
    )

    st.dataframe(
        status_summary,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# SQL ANALYSIS - PROJECT QUERIES
# =========================================================

st.subheader("🧠 SQL Analysis")
st.write("Select a project SQL query to view its live MySQL output.")

sql_queries = {
    "Query 1 - All Customer Sales": """
        SELECT * FROM customer_sales;
    """,
    "Query 2 - All Branches": """
        SELECT * FROM branches;
    """,
    "Query 3 - All Users": """
        SELECT * FROM users;
    """,
    "Query 4 - All Payment Splits": """
        SELECT * FROM payment_splits;
    """,
    "Query 5 - Open Sales": """
        SELECT *
        FROM customer_sales
        WHERE status = 'Open';
    """,
    "Query 6 - Total Gross Sales": """
        SELECT SUM(gross_sales) AS total_gross_sales
        FROM customer_sales;
    """,
    "Query 7 - Total Received Amount": """
        SELECT SUM(received_amount) AS total_received_amount
        FROM customer_sales;
    """,
    "Query 8 - Total Pending Amount": """
        SELECT SUM(pending_amount) AS total_pending_amount
        FROM customer_sales;
    """,
    "Query 9 - Number of Sales Per Branch": """
        SELECT
            b.branch_name,
            COUNT(cs.sale_id) AS total_sales
        FROM branches b
        LEFT JOIN customer_sales cs
            ON b.branch_id = cs.branch_id
        GROUP BY b.branch_id, b.branch_name;
    """,
    "Query 10 - Average Gross Sales": """
        SELECT AVG(gross_sales) AS average_gross_sales
        FROM customer_sales;
    """,
    "Query 11 - Sales With Branch Name": """
        SELECT
            cs.sale_id,
            cs.name,
            cs.product_name,
            cs.gross_sales,
            b.branch_name
        FROM customer_sales cs
        JOIN branches b
            ON cs.branch_id = b.branch_id;
    """,
    "Query 12 - Sales With Total Payment Received": """
        SELECT
            cs.sale_id,
            cs.name,
            cs.product_name,
            cs.gross_sales,
            COALESCE(SUM(ps.amount_paid), 0) AS total_payment_received
        FROM customer_sales cs
        LEFT JOIN payment_splits ps
            ON cs.sale_id = ps.sale_id
        GROUP BY
            cs.sale_id,
            cs.name,
            cs.product_name,
            cs.gross_sales;
    """,
    "Query 13 - Branch-wise Gross Sales": """
        SELECT
            b.branch_name,
            SUM(cs.gross_sales) AS total_gross_sales
        FROM branches b
        JOIN customer_sales cs
            ON b.branch_id = cs.branch_id
        GROUP BY b.branch_id, b.branch_name;
    """,
    "Query 14 - Sales With Payment Method": """
        SELECT
            cs.sale_id,
            cs.name,
            cs.product_name,
            ps.amount_paid,
            ps.payment_method
        FROM customer_sales cs
        JOIN payment_splits ps
            ON cs.sale_id = ps.sale_id;
    """,
    "Query 15 - Sales With Branch Admin Name": """
        SELECT
            cs.sale_id,
            cs.name,
            cs.product_name,
            cs.gross_sales,
            b.branch_name,
            b.branch_admin_name
        FROM customer_sales cs
        JOIN branches b
            ON cs.branch_id = b.branch_id;
    """,
    "Query 16 - Pending Amount Above ₹5,000": """
        SELECT
            sale_id,
            name,
            product_name,
            gross_sales,
            received_amount,
            pending_amount
        FROM customer_sales
        WHERE pending_amount > 5000;
    """,
    "Query 17 - Top 3 Gross Sales": """
        SELECT
            sale_id,
            name,
            product_name,
            gross_sales
        FROM customer_sales
        ORDER BY gross_sales DESC
        LIMIT 3;
    """
}

selected_sql_query = st.selectbox(
    "Select SQL Query",
    list(sql_queries.keys()),
    key="sql_analysis_query"
)

selected_query = sql_queries[selected_sql_query]

with st.expander("View SQL Query"):
    st.code(selected_query, language="sql")

try:
    connection = get_connection()
    sql_result_df = pd.read_sql(selected_query, connection)
    connection.close()

    st.dataframe(
        sql_result_df,
        use_container_width=True,
        hide_index=True
    )

except Exception as e:
    st.error("Error while running SQL analysis query.")
    st.write(e)
