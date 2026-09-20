\# Sales Intelligence Hub



Sales Intelligence Hub is a Sales Analytics \& Financial Tracking System built using Python, MySQL, Pandas, and Streamlit.



\## Project Overview



This project provides a branch-based sales management system to:



\- Manage branch-wise customer sales

\- Track gross, received, and pending amounts

\- Support split payments

\- Automatically update received payments using MySQL triggers

\- Calculate pending amounts using generated columns

\- Provide role-based Admin and Super Admin access

\- Display sales and financial analytics through a Streamlit dashboard

\- Run predefined SQL analysis queries



\## Key Features



\- 🔐 User Login \& Role-Based Access

\- 🏢 Branch Management

\- 🛒 Customer Sales Management

\- 💳 Split Payment Tracking

\- 📊 Sales Dashboard

\- 💰 Received \& Pending Payment Tracking

\- 📈 Branch-wise Sales Analysis

\- 🧠 SQL Analysis Queries

\- 🔄 MySQL Trigger for Payment Updates

\- 📋 Financial Summary and Reports



\## Technology Stack



\- Python

\- MySQL

\- Pandas

\- Streamlit

\- MySQL Connector

\- SQL



\## Database Tables



The project uses four main tables:



1\. `branches`

2\. `customer\_sales`

3\. `users`

4\. `payment\_splits`



\## Database Features



\- Primary Keys

\- Foreign Keys

\- Unique Constraints

\- ENUM Status

\- Generated Column for Pending Amount

\- MySQL Trigger for Payment Updates

\- Split Payment Support



\## SQL Analysis



The dashboard includes predefined SQL analysis queries covering:



\- Customer sales

\- Branch information

\- Payment records

\- Open sales

\- Total gross sales

\- Total received amount

\- Total pending amount

\- Branch-wise sales count

\- Average gross sales

\- Sales with branch details

\- Payment summaries

\- Branch-wise gross sales

\- Payment method analysis

\- Branch administrator details

\- Pending payments above a specified amount

\- Top 3 gross sales



\## Project Structure



```text

Sales Analytics \& Financial Tracking System/

│

├── app.py

├── .gitignore

└── README.md

