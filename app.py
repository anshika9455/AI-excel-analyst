from dotenv import load_dotenv
from langchain_groq import ChatGroq
import pandas as pd

load_dotenv()

model = ChatGroq(model="openai/gpt-oss-120b")


def analyze_xlsx(file_path):

    # Load Excel
    df = pd.read_excel(file_path)

    # Basic information instead of sending entire Excel
    summary = {
        "rows": len(df),
        "columns": list(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "data_types": df.dtypes.astype(str).to_dict()
    }

    # Send only a limited number of rows
    sample_data = df.head(30).to_string(index=False)

    prompt = f"""
You are an AI Data Analyst.

Analyze this Excel dataset.

Dataset information:
Rows: {summary['rows']}
Columns: {summary['columns']}
Missing values: {summary['missing_values']}
Data types: {summary['data_types']}

Sample of the dataset:
{sample_data}

Provide:
1. Dataset summary
2. Important insights
3. Missing-value observations
4. anomalies
5. Possible trends
6. Recommended analysis
7. best performance regions
"""

    response = model.invoke(prompt)

    return response.content


file_path = "data.xlsx"

result = analyze_xlsx(file_path)

print(result)