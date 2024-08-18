from pymongo import MongoClient
import streamlit as st


@st.cache_resource
def connect_db():
    try:
        client = MongoClient('mongodb://admin:admin12345@cluster0-shard-00-00.g1sch.mongodb.net:27017,cluster0-shard-00-01.g1sch.mongodb.net:27017,cluster0-shard-00-02.g1sch.mongodb.net:27017/?ssl=true&replicaSet=atlas-i75tpn-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0')
    except Exception as e:
        raise ConnectionError(f"Error Connecting to MongoDB Cloud: {e}")
    return client['tumltaproject']


@st.cache_resource
def connect_training_data_collection():
    db = connect_db()
    return db['training_data']

@st.cache_resource
def connect_user_collection():
    db = connect_db()
    return db['user']


# def connection_close(client):
#     client.close()