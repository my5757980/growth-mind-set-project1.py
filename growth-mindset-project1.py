import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="📂file converter" , layout="wide")
st.title("📂file converter & cleaner")
st.write("upload csv or excel files , clean data & convert formates🚀")

files = st.file_uploader("upload csv or excel files" , type=["csv" , "xlsx"], accept_multiple_files=True)

if files:
   for file in files:
       ext = file.name.split(".")[-1]
       df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

   st.subheader(f"🔍{file.name} - preview")
   st.dataframe(df.head())




   if st.checkbox(f"Remove Duplicates - {file.name}"):
      df = df.drop_duplicates()
      st.success("Duplicates Removed")
      st.dataframe(df.head())
    




   if st.checkbox(f"fill missing value - {file.name}"):
      df.fillna(df.select_dtypes(include="number").mean(), inplace=True)
      st.success("missing value filled with mean")
      st.dataframe(df.head())



      selected_columns = st.multiselect(f"select columns - {file.name}" , df.columns , default=df.columns)
      df = df[selected_columns]
      st.dataframe(df.head())



   if st.checkbox(f"📊show chart - {file.name}") and not df.select_dtypes(include="number").empty:
      st. bar_chart(df.select_dtypes(include="number").iloc[:,:2])
      format_choice = st.radio(f"convert {file.name}to:",["csv" , "excel"], key=file.name)


      if st.button(f"⬇️ download {file.name} as {format_choice}"):
         output = BytesIO()
         if format_choice == "csv":
            df.to_csv(output,index=False)
            mime = "text/csv"
            new_name = file.name.replace(ext, "csv")
         else:
             df.to_excel(output,index=False)
             mime = "application/vnd.openxmlformates-officedocument.spreadsheetml.sheet"
             new_name = file.name.replace(ext, "xlsx")
             st.download_button("⬇️ download file" , file_name=new_name , data=output , mime=mime)
             st.success("processing completed 🎉")







