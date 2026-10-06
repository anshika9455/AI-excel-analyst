# 📊 AI Excel Analyst

An AI-powered Excel data analysis application that helps users understand and analyze Excel datasets using Python, Pandas, Streamlit, and Generative AI.

The application allows users to upload Excel files, explore data quality, generate visualizations, and receive AI-powered insights and recommendations.

## 🚀 Live Demo

🔗 **Try the application live:**  
https://ai-excel-analyst-d32p.onrender.com/

> The application is deployed on Render. If the service has been inactive, the first request may take a little longer while the server starts.

---

## 📌 Project Overview

AI Excel Analyst combines traditional data analysis with Generative AI to simplify exploratory data analysis.

Instead of manually checking an Excel dataset for missing values, duplicates, statistics, trends, and important observations, users can upload their Excel file and let the application perform the initial analysis automatically.

### The application can help answer questions such as:

- How large is my dataset?
- Are there missing values?
- Are there duplicate records?
- What are the important numerical statistics?
- What patterns or trends exist in the data?
- Which regions or categories are performing better?
- What further analysis should be performed?

---

## ✨ Features

### 📂 Excel File Upload

- Upload `.xlsx` and `.xls` files.
- Select the worksheet you want to analyze.
- Preview uploaded data.

### 📊 Dataset Overview

Automatically displays:

- Number of rows
- Number of columns
- Missing cells
- Duplicate records
- Column names
- Data types
- Numerical statistics

### 🧹 Data Quality Analysis

The application checks:

- Missing values
- Missing-value percentage
- Duplicate rows
- Column data types
- Unique values

### 📈 Quick Data Visualization

Create quick visualizations by selecting:

- Category column
- Numeric metric
- Aggregation method

Supported aggregations include:

- Sum
- Mean
- Median
- Count

### 🤖 AI-Powered Insights

The application uses a Groq-powered Large Language Model to generate structured insights from the dataset.

The AI analysis includes:

- Dataset Summary
- Important Insights
- Missing-Value Observations
- Anomalies
- Possible Trends
- Recommended Analysis
- Best Performance Regions

### ⚙️ AI Configuration

Users can configure:

- AI model
- Sample size
- Temperature
- Numerical statistics inclusion

### 📥 Downloadable Report

Generated AI insights can be downloaded as a Markdown report for further use.

---

## 🧠 How It Works

```text
                    Excel File
                        │
                        ▼
              ┌──────────────────┐
              │  Streamlit UI    │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Read Excel File  │
              │     Pandas       │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Data Profiling   │
              │                  │
              │ • Rows           │
              │ • Columns        │
              │ • Missing Data   │
              │ • Duplicates     │
              │ • Statistics     │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Sample Data +    │
              │ Dataset Context  │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │    Groq LLM      │
              │   AI Analysis    │
              └────────┬─────────┘
                       │
                       ▼
          ┌──────────────────────────┐
          │    AI-Generated Insights │
          │                          │
          │ • Summary                │
          │ • Insights               │
          │ • Anomalies              │
          │ • Trends                 │
          │ • Recommendations        │
          │ • Performance Regions    │
          └────────────┬─────────────┘
                       │
                       ▼
                Download Report
