import streamlit as st
from connect_db import connect_user_collection



collection = connect_user_collection()

    
def insert_password(username, new_password):
    collection.update_one({"username": username}, {"$set": {"password": new_password}})



def change_password():
    username = st.session_state['role']
    #st.markdown(st.session_state['role'])
    #st.write(username)
    st.header(f"WELCOME {username.upper()}  (●'◡'●)") 
    st.sidebar.divider()
    with st.form('change password'):

        st.subheader("Change Password")
        
        current_password = st.text_input("Current Password :", type="password")
        new_password = st.text_input("New Password :", type="password")
        new_password_retype = st.text_input("Confirm New Password : ", type="password")


        if st.form_submit_button("Change", use_container_width=True):
            
            user = collection.find_one({"username": username, "password": current_password})
            if user:
                if len(new_password) > 7:
                    if new_password == new_password_retype:
                        insert_password(username, new_password)
                        st.success("Password Changed Successfully!")
                    else:
                        st.error("Password Doesn't Match")
                else:
                    st.error('Password too Short')
            else:
                st.error("Current Password is not Correct")