import streamlit as st
from connect_db import connect_user_collection



collection = connect_user_collection()



## Forget Password Function
def forget():
    with st.form('forget password'):
        st.subheader('Forget Password')
        email = st.text_input('Find your account : ', placeholder = 'Enter your email')
        
        if st.form_submit_button('Find', type='primary'):
            user = collection.find_one({"email": email})
            st.session_state['user'] = user
            st.markdown("    ")
            
            if user:
                st.success("Found Your Account. Click Link to Follow")
                col1,col2 = st.columns([1,2])
                with col1:
                    st.write('**Reset your password here :**')

                
                with col2:
                    st.page_link("pages/newpassword.py", label="Rest Here", icon="🔑",use_container_width=True)
            else:
                st.error('Account Does Not Found! Please Sign Up')

    #st.markdown(st.session_state)
