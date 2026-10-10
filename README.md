# Jaffle Shop Analytics Engineering Project

An end-to-end analytics engineering project using **Snowflake, dbt Core, and Streamlit** to transform raw customer, order, and payment data into analytics-ready models and an interactive dashboard.

## Project Overview

This project demonstrates a data transformation workflow, from raw source tables to business-facing analytics.

The project uses dbt to organise SQL transformations into staging, intermediate, and mart layers. A Streamlit dashboard connects to Snowflake to display key metrics and visualisations.

## Architecture

```text
Raw Data in Snowflake
        |
        v
   dbt Staging
        |
        v
 dbt Intermediate
        |
        v
     dbt Marts
        |
        v
  Analytics in Snowflake
        |
        v
 Streamlit Dashboard
```

## Technology Stack

- **Snowflake** — cloud data warehouse
- **dbt Core** — SQL transformations, model dependencies, and data testing
- **Python** — dashboard application and Snowflake connectivity
- **Streamlit** — interactive analytics dashboard
- **Git and GitHub** — version control and project documentation

## Data Models

### Staging

- `stg_jaffle_shop__customers` — standardises customer records.
- `stg_jaffle_shop__orders` — standardises order records.
- `stg_stripe__payment` — standardises payment records.

### Intermediate

- `int_orders` — combines orders with customer information.
- `int_order_payments` — aggregates payment outcomes and amounts by order.

### Marts

- `fct_orders` — provides an order-level view with payment metrics.
- `dim_customers` — provides customer-level order and payment metrics.

## Data Quality

dbt tests are used to validate key identifiers and important fields, including uniqueness and not-null constraints.

The transformed data was reconciled against the source payment records to check aggregate payment amounts and payment outcomes.

## Streamlit Dashboard

The dashboard connects to Snowflake and presents:

- Total customers
- Total orders
- Successful payment amount
- Failed payment attempts
- Top customers by successful payment amount
- Order status breakdown
- Payment outcomes

The dashboard includes a refresh control and caches query results to reduce repeated database requests.

> **Note:** The successful payment amount is shown in the source data's numeric units. No currency is assumed.

## Project Structure

```text
jaffle_shop/
├── dashboard/
│   └── app.py
├── models/
│   ├── staging/
│   ├── intermediate/
│   └── marts/
├── macros/
├── analyses/
├── seeds/
├── snapshots/
├── tests/
├── dbt_project.yml
├── requirements.txt
├── .gitignore
└── README.md
```

## Running the Dashboard Locally

1. Clone this repository.
2. Create and activate a Python virtual environment.
3. Install the dashboard dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Create `dashboard/.streamlit/secrets.toml` with your Snowflake connection settings:

   ```toml
   [snowflake]
   account = "YOUR_ACCOUNT_IDENTIFIER"
   user = "YOUR_USERNAME"
   password = "YOUR_PASSWORD"
   warehouse = "YOUR_WAREHOUSE"
   database = "ANALYTICS"
   schema = "DBT_NPUSPANATHAN"
   role = "YOUR_READ_ONLY_ROLE"
   ```

5. Start the dashboard:

   ```bash
   streamlit run dashboard/app.py
   ```

Keep `secrets.toml` private. Never commit passwords or other credentials to GitHub.

## Running dbt

Configure your Snowflake connection in your local dbt profile, then run:

```bash
dbt debug
dbt run
dbt test
```

## Future Improvements

- Deploy the dashboard using Streamlit Community Cloud.
- Use a dedicated read-only Snowflake role for dashboard access.
- Add automated testing and CI/CD.
- Expand the dashboard with additional business metrics.

