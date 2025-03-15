import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Setup Page

st.set_page_config(page_title="📝 Data Sweeper", layout='centered')
st.title("📝 Welcome To Data Sweeper")
st.write('Transform your file between CSV and Excel formats with built-in data cleaning and visualization.')

upload_file = st.file_uploader('Upload your files (CSV or Excel):', type=['csv','xlsx'], accept_multiple_files=True)

if upload_file:
    for file in upload_file:
        file_ext = os.path.splitext(file.name)[-1].lower() # type: ignore

        if file_ext == '.csv':
            df = pd.read_csv(file)
        elif file_ext == '.xlsx':
            df =pd.read_excel(file)
        else:st.error(f'Unsupported file type only csv and Excel file accepted {file_ext}')
        continue

    # Display info about the file
    st.write(f'**File Name:** {file.name}')
    st.write(f'**File Size:** {file.size /1024} ')

    # show 5 rows of our df(data frame)
    st.write('🔎 Preview the Head of the Dataframe')
    st.dataframe(df.head())

    # option for data cleaning
    st.subheader("🛠 Data Cleaning Options")
    if st.checkbox(f'Clean data for {file.name}'):
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f'Remove Duplicate from {file.name}'):
                df.drop_duplicates(inplace=True)
                st.write('Duplicates Removed!')
        with col2:
            if st.button(f'Fill Missing values for {file.name}'):
                numeric_cols = df.select_dtypes(include=['number']).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.write('Missing Values have been filled')

# Choose specific columns to keep or convert

    st.subheader('Select Column to Convert')
    columns = st.multiselect(f'Choose Colums for {file.name}', df.columns, default=df.columns)
    df = df[columns] 

# Create Some Visualizations
    st.subheader('📊 Data Visualization ')
    if st.checkbox(f'Show Visualization for {file.name}'):
        st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

# Convert the file -> CSV to Excel or Viceversa
    st.subheader('🔄Convertion Options')
    conversion_type = st.radio(f'Convert {file.name} to:', ["CSV", "Excel"], key=file.name)
    if st.button(f'Covert {file.name}'):
        buffer =BytesIO()
        if conversion_type == 'CSV':
            df.to_csv(buffer, index=False)
            file_name = file.name.replace(file_ext, '.csv')    
            mime_type = "text/csv"

        elif conversion_type == 'Excel':
            df.to_excel(buffer, index=False)
            file_name = file.name.replace(file_ext, '.xlsx')
            mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        buffer.seek(0)

# Download Button
        st.download_button(
            label=f"⏬Download {file.name} as {conversion_type}",
            data=buffer,
            file_name= file_name,
            mime=mime_type
        )

st.success('🎉 All Files Processed!')
st.markdown('<h4 style="color:#3D8D7A; text-align: center">Made By Muhammad Rehan</h4>', unsafe_allow_html=True)