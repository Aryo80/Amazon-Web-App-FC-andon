import pandas as pd
import streamlit as st
import plotly.express as px
import random
from datetime import datetime, timedelta
# Your Streamlit app code

try:
    # Code that may raise an error
    # For example, @st.cache_data usage or any other potentially error-prone code
    pass  # Replace 'pass' with the code that might cause an error
except Exception as e:
    st.warning("An error occurred: {}".format(e))  # Display a warning message
    # You can also choose to ignore the error silently without displaying a message
    pass  # Replace 'pass' with what you want to do if the error occurs

# Rest of your Streamlit app code
st.set_page_config(page_title="YYZ9", page_icon=":bar_chart:",layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
st.header('Amazon YYZ9     Andon Report Based on Area and Types')

# Function to generate simulated data (with caching)
@st.cache
def generate_simulated_data(num_rows=1000):
    # Simulating data for Location, Type, and Date
    locations = ['P-1-P', 'P-1-R', 'P-1-V', 'P-2-M', 'P-3-M']
    types     = ['Ambiguous Asin', 'Broken Set', 'Damaged Item', 'Multiple Scannable Barcodes', 'No Bin Divider',
                'No Scannable Barcode', 'Unsafe to Count', 'Incorrect Title', 'Bin does not Exist', 'Broken Set',
                'Damaged Item', 'Incorrect Binding', 'Incorrect Title', 'Misstickered FBA Item', 'Multiple Scannable Barcodes',
                'No Bin Divider', 'No Scannable Barcode', 'No Scannable Bin Label', 'Suspect Theft', 'Unsafe to Count', 'Ambiguous Asin', 
                'Bin does not Exist', 'Broken Set', 'Damaged Item', 'Incorrect Binding', 'Incorrect Title', 'Multiple Scannable Barcodes', 
                'No Bin Divider', 'No Scannable Barcode', 'No Scannable Bin Label', 'Suspect Theft', 'Unsafe to Count', 'Ambiguous Asin', 
                'Bin does not Exist', 'Broken Set', 'Damaged Item', 'Incorrect Title', 'Multiple Scannable Barcodes', 'No Bin Divider', 
                'No Scannable Barcode', 'No Scannable Bin Label', 'Suspect Theft', 'Unsafe to Count']
    start_date = datetime(2023, 11, 11)
    end_date = datetime(2023, 12, 31)

    data = []
    for _ in range(1000):  # Generating 100 rows of simulated data
        data.append({
            'Location': random.choice(locations),
            'Type': random.choice(types),
            'Last updated date': (start_date + timedelta(days=random.randint(0, (end_date - start_date).days)) + timedelta(hours=random.randint(0, 23))).strftime('%Y-%m-%d')
    })
    df = pd.DataFrame(data)
    return df

file = st.file_uploader("Upload /Drag and Drop CSV file from FC ANDON", type=['csv'])
if file is not None:
    # Read the uploaded file with Pandas
    data= pd.read_csv(file) 
    # Display DataFrame in Streamlit
    show_data = st.checkbox('Show Data')
    if show_data:
        st.write("Uploaded DataFrame:")
        st.write(data.head(100))
        st.write("Row col",data.shape)
else:
        # Generate or retrieve simulated data using st.cache_data    
        data = generate_simulated_data(num_rows=1000) # Adjust the number of rows as needed
        st.write("Drag and Drop CSV file from FC ANDON")
        st.write("Simulated data generated to run the demo :")
        show_data = st.checkbox('Show Data')
        if show_data:
            st.write(data.head(20))
            

st.subheader('Andon counts on different areas')
#data=pd.read_csv(r"C:\Users\Honar\Downloads\data.csv")
data['Location'] = data['Location'].str[0:5]
col1, col2 = st.columns((2))
# Cleaning Data
# Getting the min and max date for date input
data['Last updated date'] = pd.to_datetime(data['Last updated date']).dt.date
startDate = data['Last updated date'].min()
endDate = data['Last updated date'].max()
# Create Sidebar for Areas
st.sidebar.header("Choose your filter: ")
date1 =st.sidebar.date_input("Start Date", startDate)
date2 = st.sidebar.date_input("End Date", endDate)
data = data[(data['Last updated date'] >= date1) & (data['Last updated date'] <= date2)].copy()
selected_area = st.sidebar.multiselect("Region", data['Location'].unique())


if not selected_area:
    filtered_area=data.copy()
else:
    filtered_area=data[data['Location'].isin(selected_area)]
# Create Sidebar for Types of Andon
selected_type = st.sidebar.multiselect("Type of Andons", data['Type'].unique())
if not selected_type:
    filtered_type=data.copy()
else:
    filtered_type=data[data['Type'].isin(selected_type)]

if not selected_type and not selected_area:
    filter_data=data
elif not selected_type and selected_area:
    filter_data=filtered_area
elif  selected_type and not selected_area:
    filter_data=filtered_type
else:
    filter_data=filtered_type[filtered_type['Location'].isin(selected_area)]

## Cleaning data for Area
area=filter_data['Location'].value_counts().reset_index()
area.columns = ['Location', 'Count']

# Donut plot for Areas
fig = px.pie(area, values='Count', names='Location', hole=0.7)
color_scale = [
     # Define a custom color scale with varying shades from yellow to red
    'rgb(227, 43, 52)' , # Medium gray
    'rgb(247, 103, 117)',  # Light gray
    'rgb(68, 125, 115)',  # Medium gray
    'rgb(70, 201, 184)',  # Yellow 
    'rgb(220, 255, 255)'   # Dark gray       
]
fig.update_layout(
    autosize=True,
    width=500,
    height=500
)

fig.update_traces(marker=dict(colors=color_scale))
# Defining First row in two parts of columns

col1, col2 = st.columns((2))
with col1:
    st.plotly_chart(fig,use_container_width=True)
with col2:
    st.subheader('Total number of Andons =  ' +str(len(data) ) )
    st.table(area)
    
# Line chart using Plotly Express
st.subheader("Counts of Andon Across the Days") 
pivot_df = filter_data.groupby(['Last updated date', 'Location']).size().reset_index(name='Count')
fig = px.area(pivot_df, x='Last updated date', y='Count', color='Location',  title='Count per Location Over Time')
fig.update_layout(xaxis_title='Date', yaxis_title='Count',width=900,height=500)
st.plotly_chart(fig)


st.subheader("Counts of Andon Based on the Types")
# Type of issues
type_counts = filter_data['Type'].value_counts().reset_index()
type_counts.columns = ['Type', 'Count']
# Create a horizontal bar chart with a custom color scale
fig = px.bar(
    type_counts,
    x='Count',
    y='Type',
    orientation='h',
    text='Count',
    color='Count',  # Use the 'Count' column to define colors
    color_continuous_scale='viridis',  # Set a color scale (you can use other predefined scales)
    labels={'Count': 'Count'},  # Label for the color bar
)

# Update layout and axis titles if necessary
fig.update_layout(
    title='Count Type Distribution',
    xaxis_title='Count',
    yaxis_title='Type',
    width=850,
    height=500
)
st.plotly_chart(fig)
# Display the plot

st.subheader(" Tree Map of Andon Issue Counts by Location  ")
# Create a pivot table to aggregate counts based on Location and Type
pivot_df = filter_data.groupby(['Location', 'Type']).size().reset_index(name='Count')
pivot_df = pd.DataFrame(pivot_df)

# Create a treemap using Plotly Express
fig = px.treemap(pivot_df, path=['Location', 'Type'],values='Count',
                 height=900,width=1000)
st.plotly_chart(fig)
# Add annotations for each tile with count values
# Create a treemap using Plotly Express
st.subheader(" Tree Map of Count Types of Andons in Respective Areas ")
fig = px.treemap(pivot_df, path=[ 'Type','Location'], values='Count',
                 height=900,width=1000)

# Update layout and hover template to display custom data

# Update layout

st.plotly_chart(fig)
