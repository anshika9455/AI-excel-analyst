import io
import json
import re
from datetime import datetime

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# ------------------------------------------------------------------ #
# Page config & styling
# ------------------------------------------------------------------ #
st.set_page_config(
    page_title="AI Excel Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem;}
    .hero {
        padding: 1.6rem 1.8rem; border-radius: 16px; margin-bottom: 1.2rem;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 55%, #db2777 100%);
        color: white;
    }
    .hero h1 {margin: 0; font-size: 2rem; color: white;}
    .hero p {margin: .3rem 0 0 0; opacity: .9;}
    .insight-card {
        border: 1px solid rgba(128,128,128,.25); border-radius: 12px;
        padding: .8rem 1rem; margin-bottom: .6rem;
        background: rgba(128,128,128,.06);
    }
    div[data-testid="stMetric"] {
        background: rgba(128,128,128,.07); border: 1px solid rgba(128,128,128,.2);
        padding: 12px 16px; border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>📊 AI Excel Analyst</h1>
        <p>Upload an Excel file and get a structured analysis: summary, insights,
        missing values, anomalies, trends, recommendations and top regions.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------ #
# Sidebar
# ------------------------------------------------------------------ #
with st.sidebar:
    st.header("⚙️ Settings")
    model_name = st.text_input("Groq model", value="openai/gpt-oss-120b")
    sample_rows = st.slider("Sample rows sent to AI", 5, 100, 30, step=5)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.2, step=0.1)
    include_stats = st.toggle(
        "Send numeric statistics too", value=True,
        help="Adds describe() output so the AI can spot anomalies better.",
    )
    st.divider()
    st.caption(
        "Only the schema, statistics and a small sample are sent to the model — "
        "never the whole file."
    )

# ------------------------------------------------------------------ #
# Helpers
# ------------------------------------------------------------------ #
SECTIONS = [
    ("dataset_summary", "1️⃣ Dataset Summary", "text"),
    ("important_insights", "2️⃣ Important Insights", "list"),
    ("missing_value_observations", "3️⃣ Missing-Value Observations", "list"),
    ("anomalies", "4️⃣ Anomalies", "list"),
    ("possible_trends", "5️⃣ Possible Trends", "list"),
    ("recommended_analysis", "6️⃣ Recommended Analysis", "list"),
    ("best_performance_regions", "7️⃣ Best Performance Regions", "list"),
]


@st.cache_data(show_spinner=False)
def load_excel(file_bytes: bytes, sheet):
    return pd.read_excel(io.BytesIO(file_bytes), sheet_name=sheet)


@st.cache_data(show_spinner=False)
def sheet_names(file_bytes: bytes):
    return pd.ExcelFile(io.BytesIO(file_bytes)).sheet_names


def build_summary(df: pd.DataFrame) -> dict:
    return {
        "rows": len(df),
        "columns": list(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "data_types": df.dtypes.astype(str).to_dict(),
    }


def build_prompt(df, summary, n_rows, with_stats) -> str:
    sample_data = df.head(n_rows).to_string(index=False)
    stats = ""
    if with_stats and not df.select_dtypes("number").empty:
        stats = "\nNumeric statistics:\n" + df.describe().round(2).to_string()

    return f"""
You are an AI Data Analyst.

Analyze this Excel dataset.

Dataset information:
Rows: {summary['rows']}
Columns: {summary['columns']}
Missing values: {summary['missing_values']}
Data types: {summary['data_types']}
{stats}

Sample of the dataset:
{sample_data}

Respond with ONLY a valid JSON object (no markdown fences, no extra text)
using exactly these keys:
{{
  "dataset_summary": "a short paragraph",
  "important_insights": ["..."],
  "missing_value_observations": ["..."],
  "anomalies": ["..."],
  "possible_trends": ["..."],
  "recommended_analysis": ["..."],
  "best_performance_regions": ["..."]
}}
Each list should have 3-6 concise, specific items that reference real column
names or values. If something cannot be determined from the data, say so
in one item instead of guessing.
"""


def parse_json(text: str):
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.S)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                return None
    return None


def run_ai(prompt: str, model: str, temp: float) -> str:
    llm = ChatGroq(model=model, temperature=temp)
    return llm.invoke(prompt).content


def to_markdown(result: dict, filename: str) -> str:
    out = [f"# AI Analysis Report — {filename}",
           f"_Generated {datetime.now():%Y-%m-%d %H:%M}_\n"]
    for key, title, kind in SECTIONS:
        out.append(f"## {title}")
        val = result.get(key, "")
        if kind == "list" and isinstance(val, list):
            out.extend(f"- {v}" for v in val)
        else:
            out.append(str(val))
        out.append("")
    return "\n".join(out)


# ------------------------------------------------------------------ #
# Upload
# ------------------------------------------------------------------ #
uploaded = st.file_uploader(
    "Drop your Excel file here", type=["xlsx", "xls"], help="Max ~200 MB"
)

if not uploaded:
    st.info("👆 Upload an `.xlsx` file to get started.")
    st.stop()

file_bytes = uploaded.getvalue()

try:
    sheets = sheet_names(file_bytes)
    sheet = st.selectbox("Sheet", sheets) if len(sheets) > 1 else sheets[0]
    df = load_excel(file_bytes, sheet)
except Exception as e:
    st.error(f"Could not read the file: {e}")
    st.stop()

if df.empty:
    st.warning("This sheet is empty.")
    st.stop()

summary = build_summary(df)

# ------------------------------------------------------------------ #
# Top metrics
# ------------------------------------------------------------------ #
total_missing = int(df.isnull().sum().sum())
c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows", f"{summary['rows']:,}")
c2.metric("Columns", len(df.columns))
c3.metric("Missing cells", f"{total_missing:,}")
c4.metric("Duplicate rows", f"{int(df.duplicated().sum()):,}")

tab_ai, tab_data, tab_quality, tab_charts = st.tabs(
    ["🤖 AI Insights", "📄 Data Preview", "🧹 Data Quality", "📈 Quick Charts"]
)

# ------------------------------------------------------------------ #
# Tab: Data preview
# ------------------------------------------------------------------ #
with tab_data:
    st.dataframe(df, use_container_width=True, height=420)
    if not df.select_dtypes("number").empty:
        st.subheader("Numeric statistics")
        st.dataframe(df.describe().round(2), use_container_width=True)

# ------------------------------------------------------------------ #
# Tab: Data quality
# ------------------------------------------------------------------ #
with tab_quality:
    q1, q2 = st.columns(2)
    with q1:
        st.subheader("Missing values by column")
        miss = df.isnull().sum()
        miss = miss[miss > 0].sort_values(ascending=False)
        if miss.empty:
            st.success("No missing values 🎉")
        else:
            miss_df = pd.DataFrame(
                {"label": miss.index.astype(str), "value": miss.values}
            )
            st.bar_chart(miss_df, x="label", y="value", sort="-value")
    with q2:
        st.subheader("Column types")
        types_df = pd.DataFrame(
            {
                "Column": df.columns,
                "Type": df.dtypes.astype(str).values,
                "Missing": df.isnull().sum().values,
                "Missing %": (df.isnull().mean() * 100).round(1).values,
                "Unique": df.nunique().values,
            }
        )
        st.dataframe(
            types_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Missing %": st.column_config.ProgressColumn(
                    "Missing %", min_value=0, max_value=100, format="%.1f%%"
                )
            },
        )

# ------------------------------------------------------------------ #
# Tab: Quick charts
# ------------------------------------------------------------------ #
with tab_charts:
    num_cols = df.select_dtypes("number").columns.tolist()
    cat_cols = df.select_dtypes(exclude="number").columns.tolist()

    if not num_cols:
        st.info("No numeric columns to chart.")
    else:
        a, b, c = st.columns(3)
        metric = a.selectbox("Metric (numeric)", num_cols)
        group = b.selectbox("Group by", ["— none —"] + cat_cols)
        agg = c.selectbox("Aggregation", ["sum", "mean", "median", "count"])

        if group == "— none —":
            vals = pd.DataFrame(
                {"row": range(len(df[metric].dropna())),
                 "value": df[metric].dropna().values}
            )
            st.bar_chart(vals, x="row", y="value")
        else:
            grouped = (
                df.groupby(group)[metric].agg(agg).sort_values(ascending=False).head(20)
            )
            grouped_df = pd.DataFrame(
                {"label": grouped.index.astype(str), "value": grouped.values}
            )
            st.bar_chart(grouped_df, x="label", y="value", sort="-value")
            st.caption(f"Top 20 `{group}` by {agg} of `{metric}`")

# ------------------------------------------------------------------ #
# Tab: AI insights
# ------------------------------------------------------------------ #
with tab_ai:
    st.write("Click the button to generate the structured analysis.")
    run = st.button("✨ Analyze with AI", type="primary", use_container_width=True)

    cache_key = f"result_{uploaded.name}_{sheet}"

    if run:
        prompt = build_prompt(df, summary, sample_rows, include_stats)
        with st.spinner("Analyzing your data..."):
            try:
                raw = run_ai(prompt, model_name, temperature)
                parsed = parse_json(raw)
                st.session_state[cache_key] = parsed if parsed else {"_raw": raw}
            except Exception as e:
                st.error(f"AI request failed: {e}")

    result = st.session_state.get(cache_key)

    if result:
        if "_raw" in result:
            st.warning("The model didn't return valid JSON — showing raw output.")
            st.markdown(result["_raw"])
        else:
            st.success("Analysis complete")

            for key, title, kind in SECTIONS:
                val = result.get(key)
                if not val:
                    continue
                with st.expander(title, expanded=True):
                    if kind == "list" and isinstance(val, list):
                        for item in val:
                            st.markdown(
                                f'<div class="insight-card">{item}</div>',
                                unsafe_allow_html=True,
                            )
                    else:
                        st.write(val)

            st.download_button(
                "⬇️ Download report (.md)",
                data=to_markdown(result, uploaded.name),
                file_name=f"analysis_{uploaded.name.rsplit('.', 1)[0]}.md",
                mime="text/markdown",
                use_container_width=True,
            )