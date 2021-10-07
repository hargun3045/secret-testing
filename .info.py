import streamlit as st
import os
import pandas as pd
from collections import defaultdict
from sqlalchemy import create_engine    

database = f"mysql+mysqlconnector://{st.secrets['database']['user']}:{st.secrets['database']['password']}@{st.secrets['database']['host']}/{st.secrets['database']['dbname']}"
engine = create_engine(database,echo=False)

pd.read_sql_query('SELECT * FROM users',con=engine).to_csv('info.csv',index=False)

mycols = ['name','age','height']

def app():
    st.title('Info tracker')
    st.session_state.df = pd.read_csv('info.csv')

    col1,col2,col3 = st.columns([1,1,1])
    info = defaultdict(int)
    info['name'] = col1.text_input('What is your name?')
    info['age'] = col2.text_input('What is your age?')
    info['height'] = col3.text_input('What is your height?')
    add = st.button('Add')
    if add:
        st.session_state.df.append(pd.DataFrame(info,index=range(0,1))).to_csv('info.csv',index=False)

    delete_entry = st.button('Delete')
    index_selector = st.columns([1,1,1])[0].text_input('Enter row number to delete')

    if delete_entry:
        st.session_state.df.drop(int(index_selector),inplace=True)
        st.session_state.df.to_csv('info.csv',index=False)
    with st.expander('See data'):
        st.write('Collected data')
        st.table(pd.read_csv('info.csv'))

    confirm = st.button('Confirm')
    if confirm:
        engine.execute('DROP TABLE IF EXISTS users')
        pd.read_csv('info.csv').to_sql('users',con=engine,index=False,if_exists='append')    

