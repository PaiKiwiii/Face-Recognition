import streamlit as st

st.set_page_config(page_title='Attendance System', layout='wide')


#Retrive the data from Regis Database
import face_rec
redis_face_db = face_rec.retrieve_data(name='academy:register')
st.dataframe(redis_face_db)

#Real Time Prediction
