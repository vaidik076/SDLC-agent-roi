import os
import glob
import json
from typing import List, Dict, Any

import streamlit as st
import pandas as pd


@st.cache_data
def load_records(folder: str) -> List[Dict[str, Any]]:
    records = []
    pattern = os.path.join(folder, "*.json")
    for p in glob.glob(pattern):
        try:
            with open(p, "r", encoding="utf-8") as f:
                records.append(json.load(f))
        except Exception as e:
            st.warning(f"Failed to load {p}: {e}")
    return records


def to_summary_df(records: List[Dict[str, Any]]) -> pd.DataFrame:
    rows = []
    for r in records:
        scores = r.get("scores", {})
        roi = r.get("roi", {})
        rca = r.get("rca", {})
        owner = r.get("owner", {})
        rows.append(
            {
                "task_id": r.get("task_id"),
                "overall_score": scores.get("overall_score"),
                "reliability": scores.get("reliability"),
                "retry_penalty": scores.get("retry_penalty"),
                "cost_efficiency": scores.get("cost_efficiency"),
                "human_effort": scores.get("human_effort"),
                "roi_percent": roi.get("roi_percent"),
                "net_benefit": roi.get("net_annual_benefit_usd"),
                "root_cause": rca.get("root_cause"),
                "rca_confidence": rca.get("confidence"),
                "owner": owner.get("owner"),
                "owner_contact": owner.get("contact"),
            }
        )
    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values(by="overall_score", ascending=False)
    return df


def main():
    st.set_page_config(page_title="AI Engineering ROI Dashboard", layout="wide")

    st.title("AI-Native SDLC ROI — Demo Dashboard")
    st.markdown(
        "This dashboard reads pipeline JSON outputs (default: output/demo) and displays an interactive table with drill-down for each task."
    )

    folder = st.text_input("Pipeline output folder", value=os.path.join("output", "demo"))

    if not os.path.isdir(folder):
        st.error(f"Folder not found: {os.path.abspath(folder)}")
        return

    records = load_records(folder)
    if not records:
        st.info(f"No JSON records found in {os.path.abspath(folder)}. Run the demo (python run_demo.py) first.")
        return

    df = to_summary_df(records)

    st.subheader("Summary table")
    st.dataframe(df, height=300)

    st.sidebar.header("Filters")
    min_score = st.sidebar.slider("Min overall score", 0, 100, 0)
    owner_filter = st.sidebar.text_input("Owner contains (leave blank for all)")

    filtered = df[df["overall_score"] >= min_score]
    if owner_filter.strip():
        filtered = filtered[filtered["owner"].str.contains(owner_filter, case=False, na=False)]

    st.subheader("Filtered tasks")
    st.dataframe(filtered, height=200)

    st.subheader("Task details")
    task_ids = filtered["task_id"].tolist()
    sel = st.selectbox("Select task", options=task_ids)

    if sel:
        rec = next((r for r in records if r.get("task_id") == sel), None)
        if rec:
            st.markdown("**Trace summary**")
            st.json(rec.get("trace", {}))

            st.markdown("**Scores**")
            st.json(rec.get("scores", {}))

            st.markdown("**ROI**")
            st.json(rec.get("roi", {}))

            st.markdown("**Root Cause Analysis**")
            st.json(rec.get("rca", {}))

            st.markdown("**Ownership**")
            st.json(rec.get("owner", {}))

            st.markdown("**Raw record**")
            st.json(rec)
        else:
            st.warning("Selected task record could not be found")


if __name__ == "__main__":
    main()
