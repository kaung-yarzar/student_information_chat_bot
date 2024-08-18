import streamlit as st
from connect_db import connect_user_collection



collection = connect_user_collection()

def insert_password(username, new_password):
    collection.update_one({"username": username}, {"$set": {"password": new_password}})



def change_password():
    username = st.session_state['role']
    #st.markdown(st.session_state['role'])
    #st.write(username)
    

    if st.button('Change Password', use_container_width=True):
        st.session_state.changepassword = True

    if st.session_state.changepassword:
        with st.form('change password', clear_on_submit = True):
            st.subheader("Change Password")
            
            current_password = st.text_input("Current password :", type="password")
            new_password = st.text_input("New password :", type="password")
            new_password_retype = st.text_input("Confirm new password : ", type="password")

            col1 , col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Change", use_container_width=True, type='primary'):
                    
                    user = collection.find_one({"username": username, "password": current_password})
                    if user:
                        if len(new_password) > 7:
                            if new_password == new_password_retype:
                                insert_password(username, new_password)
                                
                                st.toast("Password Changed Successfully!", icon='✅')
                                
                                
                            else:
                                st.toast("Passwords doesn't Match", icon='❌')
                        else:
                            st.toast('Password must contain at least 8 characters', icon='❌')
                    else:
                        st.toast("Current Password is not Correct", icon='❌')

            def hide():
                st.session_state.pop("changepassword")

            with col2:
                st.form_submit_button("Cancel   ", use_container_width=True,on_click=hide)
                


                