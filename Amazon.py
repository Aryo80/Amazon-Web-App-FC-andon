
"""Amazon FC ANDON dashboard.

Streamlit/Plotly dashboard for uploaded FC ANDON CSV files, with synthetic
sample data when no file is uploaded.
"""

from datetime import datetime, timedelta
import random

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="Amazon FC ANDON Reports", layout="wide")


# -----------------------------------------------------------
# Data loading and validation
# -----------------------------------------------------------

def generate_simulated_data(num_rows=1000):
    """Generate demonstration records; they are NOT real Amazon data."""
    locations = ["P-1-P", "P-1-R", "P-1-V", "P-2-M", "P-3-M"]
    types = [
        "Ambiguous Asin", "Broken Set", "Damaged Item",
        "Multiple Scannable Barcodes", "No Bin Divider",
        "No Scannable Barcode", "Unsafe to Count", "Incorrect Title",
        "Bin does not Exist", "Incorrect Binding", "Misstickered FBA Item",
        "No Scannable Bin Label", "Suspect Theft",
    ]
    start_date = datetime(2023, 11, 11)
    end_date = datetime(2023, 12, 31)
    rows = []
    for _ in range(num_rows):
        date = start_date + timedelta(
            days=random.randint(0, (end_date - start_date).days)
        )
        rows.append({
            "Location": random.choice(locations),
            "Type": random.choice(types),
            "Last updated date": date.strftime("%Y-%m-%d"),
        })
    return pd.DataFrame(rows)


def prepare_data(raw_data):
    """Validate core fields and preserve both full bin IDs and 5-char regions."""
    required = {"Location", "Type", "Last updated date"}
    missing = sorted(required.difference(raw_data.columns))
    if missing:
        raise ValueError("Missing required CSV columns: " + ", ".join(missing))

    df = raw_data.copy()
    df["Locations"] = df["Location"].astype("string").str.strip()
    df["Location"] = df["Locations"].str[:5]
    df["Type"] = df["Type"].astype("string").str.strip()
    df["Last updated date"] = pd.to_datetime(
        df["Last updated date"], errors="coerce"
    ).dt.date

    for col in ("Root Cause", "Assigned to"):
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()
            df[col] = df[col].replace("", pd.NA)

    before = len(df)
    df = df.dropna(subset=["Location", "Locations", "Type", "Last updated date"])
    df = df[(df["Location"] != "") & (df["Type"] != "")].copy()
    if len(df) < before:
        st.warning(f"Skipped {before - len(df):,} rows with missing or invalid required fields.")
    return df


def custom_pie_chart(frame, values_col, names_col, width=500, height=500):
    if frame.empty:
        st.info("No data available for this chart.")
        return
    fig = px.pie(frame, values=values_col, names=names_col, hole=0.7)
    fig.update_layout(width=width, height=height, legend=dict(orientation="v"))
    st.plotly_chart(fig, use_container_width=True)


# -----------------------------------------------------------
# Problem Solvers group and individual reports
# -----------------------------------------------------------

def ps_report(filtered):
    st.header("ICQA Problem Solvers Group Report")

    if "Assigned to" not in filtered.columns:
        st.warning("The uploaded CSV does not contain the 'Assigned to' column.")
        return

    df = filtered.dropna(subset=["Assigned to", "Type"]).copy()
    if df.empty:
        st.info("No assigned Problem Solver records match these filters.")
        return

    ps_data = (
        df.groupby(["Assigned to", "Type"])
        .size().reset_index(name="counts")
    )
    ps_pivot = pd.crosstab(df["Type"], df["Assigned to"], margins=True,
                           margins_name="Total")
    ps_pivot.index.name = "Type"
    st.dataframe(ps_pivot, use_container_width=True)

    totals = (
        df.groupby("Assigned to").size()
        .reset_index(name="Resolved Andon Num")
        .sort_values("Resolved Andon Num", ascending=True)
    )
    fig = px.bar(totals, x="Resolved Andon Num", y="Assigned to",
                 orientation="h", text="Resolved Andon Num",
                 title="Resolved Andons by Problem Solver")
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

    fig = px.treemap(ps_data, path=["Assigned to", "Type"], values="counts",
                     title="Types of Andons Resolved by Each Problem Solver")
    st.plotly_chart(fig, use_container_width=True)

    st.header("ICQA Problem Solvers Individual Report")
    left, right = st.columns([1, 4])
    names = sorted(df["Assigned to"].unique().tolist())
    with left:
        report_ps = st.radio("Select Problem Solver", names)

    individual = df[df["Assigned to"] == report_ps]
    ps_ind_data = (
        individual.groupby("Type").size()
        .reset_index(name="counts")
        .sort_values("counts", ascending=False)
    )
    with right:
        custom_pie_chart(ps_ind_data, "counts", "Type", 400, 400)

    st.subheader(str(report_ps))
    left, right = st.columns([3, 2])
    with left:
        st.dataframe(ps_ind_data, hide_index=True, use_container_width=True)
    with right:
        st.metric("Andons resolved", f"{len(individual):,}")
        dates = sorted(individual["Last updated date"].dropna().unique().tolist())
        chosen_date = st.selectbox("Schedule in detail", dates)

    st.subheader(f"Activity on {chosen_date}")
    daily = (
        individual[individual["Last updated date"] == chosen_date]
        .groupby("Type").size().reset_index(name="counts")
    )
    st.dataframe(daily, hide_index=True, use_container_width=True)


# -----------------------------------------------------------
# Hot Bins report
# -----------------------------------------------------------

def hot_bin_report(filtered):
    st.header("Hot Bins Report")
    st.subheader("Location Details Based on Repeated Counts")

    df = filtered.copy()
    if "Root Cause" in df.columns:
        df = df[df["Root Cause"].fillna("").str.casefold() != "duplicate"].copy()

    if df.empty:
        st.info("No non-duplicate records match the selected filters.")
        return

    bin_df = (
        df.groupby("Locations").size()
        .reset_index(name="Count")
        .rename(columns={"Locations": "Bin ID"})
        .sort_values(["Count", "Bin ID"], ascending=[False, True])
    )

    hot_bin = (
        bin_df.groupby("Count")["Bin ID"]
        .agg(["count", lambda s: ", ".join(s.astype(str))])
        .reset_index()
        .rename(columns={
            "Count": "Update Num",
            "count": "Bin Found",
            "<lambda_0>": "Bin IDs",
        })
        .sort_values("Update Num", ascending=False)
    )
    st.dataframe(hot_bin, hide_index=True, use_container_width=True)

    st.subheader("Hot Bins (more than 2 updates)")
    repeat_counts = sorted(bin_df.loc[bin_df["Count"] > 2, "Count"].unique(),
                           reverse=True)
    if not repeat_counts:
        st.info("No bins with more than two updates were found for these filters.")
        return

    left, right = st.columns(2)
    with left:
        selected_count = st.radio(
            "Select number of updates",
            repeat_counts,
            format_func=lambda n: f"Bin IDs with {n} updates",
        )

    matching_bins = bin_df[bin_df["Count"] == selected_count]
    with right:
        st.subheader(f"Bins with {selected_count} updates")
        selected_bin = st.radio("Select a Bin ID to see details",
                                matching_bins["Bin ID"].tolist())

    st.subheader(f"Records for {selected_bin}")
    bin_records = df[df["Locations"] == selected_bin].copy()
    st.dataframe(bin_records, hide_index=True, use_container_width=True)


# -----------------------------------------------------------
# General Andon charts
# -----------------------------------------------------------

def andons_report(filtered, report_status, date1, date2):
    st.header(f"Amazon YYZ9 Andon Report: {report_status}")
    st.subheader(f"{report_status} Andon Counts by Area")

    if st.checkbox("Show source data"):
        st.dataframe(filtered, use_container_width=True)
        st.write(f"Rows: {len(filtered):,}, Columns: {len(filtered.columns)}")

    if filtered.empty:
        st.info("There are no records matching the selected filters.")
        return

    area = filtered["Location"].value_counts().reset_index()
    area.columns = ["Location", "Count"]
    st.metric(f"Total {report_status} Andons", f"{len(filtered):,}")
    st.dataframe(area, hide_index=True, use_container_width=True)

    colors = ["#e32b34", "#f76775", "#447d73", "#46c9b8", "#dcffff"]
    fig = px.pie(area, values="Count", names="Location", hole=0.7,
                 title="Andon Distribution by Area",
                 color_discrete_sequence=colors)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(f"Counts of {report_status} Andons Across the Days")
    daily = (
        filtered.groupby("Last updated date").size()
        .reset_index(name="Count")
        .sort_values("Last updated date")
    )
    fig = px.line(daily, x="Last updated date", y="Count",
                  title="Andon Counts Over Time", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(f"Counts of {report_status} Andons Across Areas")
    by_area = (
        filtered.groupby(["Last updated date", "Location"]).size()
        .reset_index(name="Count")
    )
    chart_type = st.radio("Select Chart Type", ["Area", "Bar", "Line"],
                          horizontal=True)
    chart_args = dict(data_frame=by_area, x="Last updated date", y="Count",
                      color="Location", title="Counts per Area Over Time")
    if chart_type == "Area":
        fig = px.area(**chart_args)
    elif chart_type == "Bar":
        fig = px.bar(**chart_args)
    else:
        fig = px.line(**chart_args)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(f"Counts of {report_status} Andon Types Across the Days")
    by_type = (
        filtered.groupby(["Last updated date", "Type"]).size()
        .reset_index(name="Count")
    )
    fig = px.bar(by_type, x="Last updated date", y="Count", color="Type",
                 title="Andon Types Over Time")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(f"Cumulative {report_status} Andon Types")
    if date1 < date2:
        start_time, end_time = st.slider(
            "Select Time Range", min_value=date1, max_value=date2,
            value=(date1, date2),
        )
    else:
        start_time = end_time = date1
        st.caption(f"Selected date: {date1}")

    in_range = filtered[
        (filtered["Last updated date"] >= start_time)
        & (filtered["Last updated date"] <= end_time)
    ]
    type_counts = in_range["Type"].value_counts().reset_index()
    type_counts.columns = ["Type", "Count"]
    if not type_counts.empty:
        fig = px.bar(type_counts, x="Count", y="Type", orientation="h",
                     text="Count", color="Count",
                     color_continuous_scale="Viridis",
                     title="Count Type Distribution")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No Andons in this time range.")

    pivot_df = (
        filtered.groupby(["Location", "Type"]).size()
        .reset_index(name="Count")
    )
    if not pivot_df.empty:
        st.subheader(f"Treemap: {report_status} Andon Types by Location")
        fig = px.treemap(pivot_df, path=["Location", "Type"], values="Count",
                         title="Andon Types Within Each Area")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader(f"Treemap: Locations Within {report_status} Andon Types")
        fig = px.treemap(pivot_df, path=["Type", "Location"], values="Count",
                         title="Areas Within Each Type of Andon")
        st.plotly_chart(fig, use_container_width=True)


# -----------------------------------------------------------
# Main app
# -----------------------------------------------------------

def main():
    st.title("Amazon FC ANDON Data Reports")
    uploaded = st.file_uploader("Upload / Drag and Drop FC ANDON CSV", type=["csv"])
    if uploaded is None:
        st.info("No CSV uploaded. Showing synthetic demonstration data.")
        raw_data = generate_simulated_data()
        if st.checkbox("Show demonstration data"):
            st.dataframe(raw_data.head(), hide_index=True)
    else:
        try:
            raw_data = pd.read_csv(uploaded)
        except Exception as exc:
            st.error(f"Could not read CSV: {exc}")
            st.stop()
        st.success("FC ANDON CSV loaded successfully.")

    try:
        data = prepare_data(raw_data)
    except ValueError as exc:
        st.error(str(exc))
        st.stop()

    if data.empty:
        st.warning("No valid records are available.")
        st.stop()

    has_root_cause = "Root Cause" in data.columns
    resolved = (has_root_cause and
                data["Root Cause"].isna().sum() <= 0.5 * len(data))
    status = "Resolved" if resolved else "Non-Resolved"
    report_list = ["Andons report"]
    if resolved:
        if "Assigned to" in data.columns:
            report_list.append("Problem Solvers Report")
        report_list.append("Hot Bins Report")

    st.sidebar.header("Choose your filters")
    min_date = data["Last updated date"].min()
    max_date = data["Last updated date"].max()
    date1 = st.sidebar.date_input("Start Date", min_date,
                                  min_value=min_date, max_value=max_date)
    date2 = st.sidebar.date_input("End Date", max_date,
                                  min_value=min_date, max_value=max_date)
    if date1 > date2:
        st.warning("Start Date cannot be after End Date.")
        st.stop()

    dated = data[
        (data["Last updated date"] >= date1)
        & (data["Last updated date"] <= date2)
    ].copy()
    selected_area = st.sidebar.multiselect(
        "Region", sorted(dated["Location"].dropna().unique().tolist())
    )
    selected_type = st.sidebar.multiselect(
        "Type of Andons", sorted(dated["Type"].dropna().unique().tolist())
    )

    filtered = dated
    if selected_area:
        filtered = filtered[filtered["Location"].isin(selected_area)]
    if selected_type:
        filtered = filtered[filtered["Type"].isin(selected_type)]
    filtered = filtered.copy()

    area_text = ", ".join(selected_area) if selected_area else "all regions"
    type_text = ", ".join(selected_type) if selected_type else "all types"
    st.caption(f"Report from {date1} to {date2} | {area_text} | {type_text}")

    st.sidebar.title("Select Report")
    choice = st.sidebar.radio("Select Report", report_list)
    if choice == "Problem Solvers Report":
        ps_report(filtered)
    elif choice == "Hot Bins Report":
        hot_bin_report(filtered)
    else:
        andons_report(filtered, status, date1, date2)


if __name__ == "__main__":
    main()
