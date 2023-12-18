
import pandas as pd
import streamlit as stps
import plotly.express as px
import random
from datetime import datetime, timedelta
# Load your data or use sample data
# Assuming 'df_sorted' contains your data
# Replace this with your actual data

# Your Streamlit app code
try:
    # Code that may raise an error
    # For example, @st.cache_data usage or any other potentially error-prone code
    pass  # Replace 'pass' with the code that might cause an error
except Exception as e:
    st.warning("An error occurred: {}".format(e))  # Display a warning message
    # You can also choose to ignore the error silently without displaying a message
    pass  # Replace 'pass' with what you want to do if the error occurs

def custom_pie_chart(data, values_col, names_col,w=500,h=500):
    # Create a pie chart using Plotly Express
    fig = px.pie(data, values=values_col, names=names_col, hole=0.7)

    # Update the layout of the pie chart
    fig.update_layout(
        autosize=True,
        width=w,
        height=h
    )

    # Assign the custom color scale to the pie chart
    fig.update_layout(
        legend=dict(
            orientation='v'  # Horizontal orientation for the legend
                     # Positioning the legend in the center horizontally
                       # Positioning the legend in the center vertically
        )
    )

    # Display the pie chart using Streamlit
    st.plotly_chart(fig, use_container_width=True)


# Function to generate simulated data (with caching)

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
            'Last updated date': (start_date + timedelta(days=random.randint(0, 
            (end_date - start_date).days)) + timedelta(hours=random.randint(0, 23))).strftime('%Y-%m-%d')
    })
    df = pd.DataFrame(data)
    return df

file = st.file_uploader("Upload /Drag and Drop CSV file from FC ANDON", type=['csv'])
if file is not None:
    # Read the uploaded file with Pandas
    data= pd.read_csv(file) 
    # Display DataFrame in Streamlit
    st.write("Data Loaded")
else:
        # Generate or retrieve simulated data using st.cache_data    
        data = generate_simulated_data(num_rows=1000) # Adjust the number of rows as needed
        st.write("Drag and Drop CSV file from FC ANDON")
        st.write("Simulated data generated to run the demo :")
        show_data1 = st.checkbox('Show The Data')
        if show_data1:
            st.write(data.head())
            


#data=pd.read_csv(r"C:\Users\Honar\Downloads\data.csv")
data['Locations'] = data['Location']
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

msg_filter = f"Report from {startDate} to {endDate} at {selected_area} based on {selected_type}"
st.write(msg_filter)
def ps_report():
    st.header('ICQA Problem Solvers Report')
    #filter_data = data[data['Root Cause'] != 'Duplicate']
    df_sorted = pd.DataFrame(filter_data)
    # Grouping by 'Location' and getting counts
    ps_data = df_sorted.groupby('Assigned to').size().reset_index(name='counts')
    ps_data = df_sorted.groupby(['Assigned to','Type']).size().reset_index(name='counts')
    ps_pivot = ps_data.pivot_table(values='counts', columns='Assigned to', index='Type'
                                , margins=True, margins_name='Total', aggfunc='sum')


    fig = px.pie(ps_data, values='counts', names='Assigned to', hole=0.7)

    fig.update_layout(
        autosize=True,
        width=500,
        height=500
    )
    # Assign the custom color scale to the pie chart
    fig.update_layout(
        legend=dict(
            orientation='v',     # Horizontal orientation for the legend
            x=-0.4,              # Positioning the legend in the center horizontally
            y=0.5                # Positioning the legend in the center vertically
            
        )
    )

    st.plotly_chart(fig,use_container_width=True)
     # pivot table for ps 
    st.dataframe(round(ps_pivot,0),height=550,width=900)
   
    



    col1, col2= st.columns([1, 4])

    # Display content in the defined columns
    with col1:
         
         report_ps = st.radio('Select Report',df_sorted['Assigned to'].dropna().unique())
         ps_indvidual = df_sorted[df_sorted['Assigned to'] == report_ps].iloc[:,2:]
    with col2:
        # Prepare data for individual reports of PS
        ps_ind_data = df_sorted[df_sorted['Assigned to'] == report_ps].groupby('Type').size().reset_index(name='counts')
        #st.write(ps_ind_data)
        custom_pie_chart(ps_ind_data, 'counts', 'Type',400,400)
         #


    col1, col2= st.columns([4, 1])

    # Display content in the defined columns
    with col1:
         st.write(ps_ind_data)
    with col2:
         st.write(report_ps)
             

    fig = px.treemap(ps_data, path=['Assigned to','Type'], values='counts', 
                    title='Types of Andon Within each Area',
                    custom_data=['counts'],
                    hover_data={'counts': True},
                    height=700,width=900
                    )
    # Update layout and hover template to display custom data
    # Update layout
    st.plotly_chart(fig)

        # Display content for Report A

def hot_bin_report():
    st.header('hot_bin_report')
    # Load your data or use sample data
    # Assuming 'df_sorted' contains your data
    # Replace this with your actual data
    df = data[data['Root Cause'] != 'Duplicate']
    df_sorted = pd.DataFrame(df)
    # Grouping by 'Location' and getting counts
    bins = df_sorted.groupby('Locations').size()
    bin_df = pd.DataFrame(bins)
    bin_df.reset_index(inplace=True)  # Resetting index

    # Assigning column names
    bin_df.columns = ['Location', 'Count']

    # Sorting by the 'Count' column in descending order
    bin_df_sorted = bin_df.sort_values(by='Count', ascending=False)
    # Get unique counts of repetitions
    unique_counts = bin_df_sorted['Count'].unique()

    # Streamlit app
    st.title('Location Details Based on Repeated Counts')
    # Hot Bin List
    hot_bin=bin_df_sorted.groupby('Count').size().reset_index()
    hot_bin.columns=['Update Num','Bin Found']
    hot_bin=hot_bin.sort_values(by='Update Num',ascending=False)
    newlist=[]
    for bin_list in  unique_counts:
        newlist.append(bin_df_sorted[bin_df_sorted['Count']==bin_list]['Location'].to_list()) 
    hot_bin['bin Id']=newlist

    st.write(hot_bin,index=False)

    with st.container():
        st.title('.          Hot Bins')
        col1, col2 = st.columns(2)

            # Adding content to the first column
        with col1:
            
            # Preparing List for Radio Button
            radio_list=[]
            for item in unique_counts[unique_counts>2]: 
                radio_list.append( " Bin IDs with Update Num of  " + str(item) ) 
            st.subheader("List the Bin IDs based on the number of updates:")
            selected_count = st.radio("List the Bin IDs based on the number of updates:",radio_list)
    # Add other content to the first column as needed

    # Adding content to the second column
        with col2:
            selected_hot = int(selected_count.replace( " Bin IDs with Update Num of  ", '' ))
            locations_with_selected_count = bin_df_sorted[bin_df_sorted['Count'] == selected_hot ]
            #st.write(locations_with_selected_count)
            st.subheader(f"Bin IDs Found for Update Num of   {selected_hot} :")
            selected_bin = st.radio("Select a Bin ID to see the Details :", locations_with_selected_count['Location'])
    # Radio buttons for selecting counts
    # Filter data based on selected count
    locations_with_selected_count = bin_df_sorted[bin_df_sorted['Count'] == selected_count]

    # Display selected count locations
    if  selected_bin:
        
        st.write(f" **{selected_bin} Records:**")
        bin_rec=df_sorted[df_sorted['Locations']== selected_bin].iloc[:,2:]
        bin_rec['Locations'], bin_rec['Location'] = bin_rec['Location'], bin_rec['Locations']
        st.write(bin_rec)
    else:
        st.write("No locations with the selected count.")
        # Display content for Report B
def Andons_report():
    st.header('Amazon YYZ9     Andon Report Based on Area and Types')
    st.subheader('Andon counts on different areas')
    show_data = st.checkbox('Show Data')
    if show_data:
        st.write("Uploaded DataFrame:")
        st.write(data)
        st.write("Row col",data.shape)
    # Display content for Report C
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
    # Assign the custom color scale to the pie chart
    fig.update_traces(marker=dict(colors=color_scale))
    fig.update_layout(
        legend=dict(
            orientation='v',  # Horizontal orientation for the legend
            x=-0.4,  # Positioning the legend in the center horizontally
            y=0.5  # Positioning the legend in the center vertically
            
        )
    )

    # Defining First row in two parts of columns
    st.write('Total number of Andons =' + str(len(data) ) )
    st.write(area)
    #if area.iloc[0,0] : st.write(f'**Total number of Andons at { area.iloc[0,0] } =  { area.iloc[0,1] }**'  )
    #if area.iloc[1,0] : st.write(f'**Total number of Andons at { area.iloc[1,0] } =  { area.iloc[1,1] }**'  )
    #if area.iloc[2,0] : st.write(f'**Total number of Andons at { area.iloc[2,0] } =  { area.iloc[2,1] }**'  )
    #if area.iloc[3,0] : st.write(f'**Total number of Andons at { area.iloc[3,0] } =  { area.iloc[3,1] }**'  )
    #if area.iloc[4,0] : st.write(f'**Total number of Andons at { area.iloc[4,0] } =  { area.iloc[4,1] }**'  )
    #if area.iloc[5,0] : st.write(f'**Total number of Andons at { area.iloc[5,0] } =  { area.iloc[5,1] }**'  )
    
    st.plotly_chart(fig,use_container_width=True)
    col1, col2 = st.columns((2))
    #####with col1:
        
        #st.dataframe(area)
        
    #####with col2:
        #st.write('Total number of Andons =' + str(len(data) ) )
        #st.plotly_chart(fig,use_container_width=True)
    
    # Line chart using Plotly Express
    st.subheader("Counts of Andon Across the Days") 
    pivot_df = filter_data.groupby('Last updated date').size().reset_index(name='Count')
    fig = px.line(pivot_df, x='Last updated date', y='Count',  title='Count per Location Over Time')
    fig.update_layout(xaxis_title='Date', yaxis_title='Count',width=900,height=500)
    st.plotly_chart(fig)

    # Function to create the chart based on the selected type
    def create_chart(chart_type):
        pivot_df = filter_data.groupby(['Last updated date', 'Location']).size().reset_index(name='Count')

        if chart_type == 'Bar':
            fig = px.bar(pivot_df, x='Last updated date', y='Count', color='Location',
                        title='Count per Location Over Time')
        elif chart_type == 'Area':
            fig = px.area(pivot_df, x='Last updated date', y='Count', color='Location',
                        title='Count per Location Over Time')
        elif chart_type == 'Line':
            fig = px.line(pivot_df, x='Last updated date', y='Count', color='Location',
                        title='Count per Location Over Time')

        fig.update_layout(xaxis_title='Date', yaxis_title='Count', width=900, height=500)
        st.plotly_chart(fig)

    # Streamlit app
    st.subheader("Counts of Andon Across the Days in different Areas")
    # Radio box to select the chart type
    chart_types = ['Bar', 'Area', 'Line']
    selected_chart = st.radio("Select Chart Type", chart_types)
    # Create chart based on the selected type
    create_chart(selected_chart)
        
    

    # Line chart using Plotly Express
    st.subheader("Counts of Andon Typed Across the Days") 

    pivot_df = filter_data.groupby(['Last updated date', 'Type']).size().reset_index(name='Count')
    fig = px.bar(pivot_df, x='Last updated date', y='Count', color='Type',  title='Count/Type Over Time')
    fig.update_layout(xaxis_title='Date', yaxis_title='Count',width=900,height=500)
    st.plotly_chart(fig)


    st.subheader(f"Cumulative counts of Andon Types based on their respective types from  {startDate} to {endDate}") 
    # Type of issues
###################################################
    start_time, end_time = st.slider(
    "Select Time Range",
    min_value=date1,
    max_value=date2,
    value=(date1, date2))
    st.write(start_time, end_time)
    
    
##################################################
    type_counts = filter_data[(filter_data['Last updated date'] >= start_time) &
     (filter_data['Last updated date'] <= end_time)]['Type'].value_counts().reset_index()
  
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


    # Create a treemap using Plotly Express
    fig = px.treemap(pivot_df, path=['Location', 'Type'], values='Count', 
                    title='Types of Andon Within each Area',
                    custom_data=['Count'],
                    hover_data={'Count': True},
                    height=700,width=900
                    )

    # Update layout and hover template to display custom data
    # Update layout

    st.plotly_chart(fig)
    # Add annotations for each tile with count values
    # Create a treemap using Plotly Express
    st.subheader(" Tree Map of Count Types of Andons in Respective Areas ")
    fig = px.treemap(pivot_df, path=[ 'Type','Location'], values='Count', 
                    title='Zone Within each Type of Andons',
                    custom_data=['Count'],
                    hover_data={'Count': True},
                    height=700,width=900)
    # Update layout and hover template to display custom data

    # Update layout

    st.plotly_chart(fig)

def main():
    st.sidebar.title('Select Report')
    report_choice = st.sidebar.radio('Select Report', ['Andons report','Problem Solvers Report', 'Hot Bins Report' ])

    if report_choice == 'Problem Solvers Report':
        ps_report()
    elif report_choice == 'Hot Bins Report':
        hot_bin_report()
    elif report_choice == 'Andons report':
        Andons_report()

if __name__ == '__main__':
    main()




