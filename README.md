
# Amazon FC ANDON Analytics Dashboard

**Python | Pandas | Streamlit | Plotly | Operational Analytics**

An interactive data analytics application for analyzing fulfillment center ANDON incidents, identifying recurring operational issues, and generating Problem Solver performance reports.

##  Live Dashboard

[**Launch the Streamlit Web Application**](https://amazon-yyz9-web-app-fc-andon-by-honarmah.streamlit.app)

## 📊 Project Overview

The **Amazon FC ANDON Analytics Dashboard** is a Python-based web application designed to transform operational CSV data into actionable insights through automated data cleaning, aggregation, reporting, and interactive visualization.

The application analyzes ANDON incidents across five fulfillment center areas:

- P-1-V
- P-3-M
- P-2-M
- P-1-P
- P-1-R

It provides insights into incident distributions, recurring operational issues, and Problem Solver activities.

This project demonstrates practical skills in **Python programming, data preprocessing, exploratory data analysis (EDA), business intelligence, reporting automation, and interactive dashboard development**.

## ✨ Key Features

### 1. Data Cleaning and Preparation

- Import operational data from CSV files.
- Validate required columns and data formats.
- Standardize date and location fields.
- Handle missing and invalid records.
- Prepare structured datasets for analysis and reporting.

### 2. ANDON Incident Analytics

- Analyze incident frequency by location and issue type.
- Monitor incident trends over selected time periods.
- Compare issue distributions across operational areas.
- Identify frequently occurring ANDON categories.
- Explore data through interactive visualizations.

**Visualizations include:**

- Bar charts
- Line charts
- Area charts
- Donut charts
- Treemaps

### 3. Problem Solver Performance Reports

- Generate individual and group Problem Solver reports.
- Summarize incident records by assigned Problem Solver.
- Compare Problem Solver activity.
- Analyze incident types handled by each Problem Solver.
- Review daily activities through interactive tables and charts.

### 4. Hot Bin Analysis

- Identify bins associated with repeated ANDON incidents.
- Calculate incident frequencies by bin location.
- Highlight bins with multiple reported issues.
- Examine detailed incident records for selected locations.
- Support investigations into recurring operational problems.

### 5. Interactive Data Exploration

Users can filter operational data by:

- Date range
- Fulfillment center area
- ANDON incident type
- Individual Problem Solver
- Number of repeated bin incidents

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Core application development |
| Pandas | Data cleaning, transformation, and aggregation |
| Streamlit | Interactive web application |
| Plotly Express | Interactive charts and visualizations |
| Git & GitHub | Version control and project management |
| Streamlit Community Cloud | Web application deployment |

## 🔄 Data Analytics Pipeline

The application follows a structured analytical workflow:

**CSV Data Input → Data Validation → Data Cleaning → Data Transformation → Data Aggregation → Interactive Visualization → Operational Reporting**

This workflow converts raw operational records into structured information that supports analytical exploration and evidence-based operational decision-making.

## 💻 Installation and Usage

### 1. Clone the Repository

```bash
git clone https://github.com/Aryo80/Amazon-Web-App-FC-andon.git
cd Amazon-Web-App-FC-andon
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
streamlit run Amazon.py
```

### 4. Explore the Dashboard

Upload a compatible CSV file or explore the application using the synthetic demonstration dataset.

**Required CSV columns:**

- `Location`
- `Type`
- `Last updated date`

**Additional columns for extended reporting:**

- `Root Cause`
- `Assigned to`

## 📈 Practical Applications

The dashboard demonstrates how operational analytics can support:

- **Issue Monitoring:** Tracking ANDON incidents across multiple operational areas.
- **Root-Cause Investigation:** Identifying recurring incident categories and locations.
- **Performance Reporting:** Summarizing Problem Solver activities.
- **Process Improvement:** Highlighting operational patterns worth investigating.
- **Reporting Automation:** Reducing repetitive manual data aggregation and reporting tasks.

## 🎯 Skills Demonstrated

- Python programming
- Data cleaning and preprocessing
- Exploratory data analysis (EDA)
- Data aggregation using Pandas
- Data quality validation
- Interactive dashboard development
- Operational KPI reporting
- Data visualization and storytelling
- Reporting automation
- GitHub version control
- Web application deployment

## 🔮 Future Enhancements

Potential improvements include:

- Automated data-quality monitoring
- Advanced operational KPIs
- Statistical anomaly detection
- Time-series analysis
- Historical performance comparisons
- Automated unit testing
- Continuous integration and deployment (CI/CD)
- Improved dependency management

## 🔒 Data Privacy and Disclaimer

This is an independent data analytics portfolio project and is not an official Amazon application.

The application includes synthetic demonstration data. Confidential operational records and employee-identifying information should not be published or uploaded to unauthorized services.





---

*Developed as a practical application of Python, data analytics, and interactive reporting to fulfillment center operational challenges.*

*Data Source: CSV files extracted from the FC Andon app*
