# 📊 AI Excel Analyst

An AI-powered Excel data analysis application that allows users to upload `.xlsx` or `.xls` files and automatically generate meaningful insights using Python, Pandas, Streamlit, and Groq-powered LLMs.

The application combines traditional data analysis with Generative AI to help users understand their Excel datasets without manually performing every analysis step.

---

## 🚀 Features

### 📂 Excel File Upload
- Upload `.xlsx` and `.xls` files directly through the Streamlit interface.
- Supports workbooks containing multiple sheets.
- Select the sheet you want to analyze.

### 📊 Dataset Overview
The application automatically displays:

- Total number of rows
- Total number of columns
- Missing cells
- Duplicate rows
- Column names
- Data types
- Numerical statistics

### 🧹 Data Quality Analysis

The application checks the dataset for:

- Missing values
- Missing-value percentage
- Duplicate records
- Column data types
- Unique values

### 📈 Quick Data Visualization

Users can create quick charts by selecting:

- Numeric metric
- Category/group column
- Aggregation method

Supported aggregations:

- Sum
- Mean
- Median
- Count

### 🤖 AI-Powered Analysis

The application uses a Groq-hosted LLM to analyze the uploaded dataset and generate structured insights.

The AI provides:

1. Dataset Summary
2. Important Insights
3. Missing-Value Observations
4. Anomalies
5. Possible Trends
6. Recommended Analysis
7. Best Performance Regions

### ⚙️ AI Configuration

Users can configure:

- Groq model
- Number of sample rows sent to the AI
- Temperature
- Whether numerical statistics should be included

### 📥 Downloadable Report

After analysis, users can download the generated insights as a Markdown (`.md`) report.

---

## 🧠 How It Works

```text
        Excel File
            │
            ▼
    ┌─────────────────┐
    │ Streamlit UI    │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Read Excel      │
    │ using Pandas    │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Data Profiling  │
    │                 │
    │ • Rows          │
    │ • Columns       │
    │ • Missing Data  │
    │ • Data Types    │
    │ • Statistics    │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Sample Data +   │
    │ Dataset Schema  │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ Groq LLM        │
    │ AI Analysis     │
    └────────┬────────┘
             │
             ▼
    ┌─────────────────────────────┐
    │ Structured AI Insights      │
    │                             │
    │ • Summary                  │
    │ • Insights                 │
    │ • Anomalies                │
    │ • Trends                   │
    │ • Recommendations          │
    │ • Performance Regions      │
    └─────────────┬───────────────┘
                  │
                  ▼
          Downloadable Report
