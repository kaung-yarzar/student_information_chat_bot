import streamlit as st
from connect_db import connect_user_collection
#from forgetpassword import check_user_exist
collection = connect_user_collection()



###kkyyzz


#st.markdown(st.session_state['user'])
try:
    username = st.session_state.user['username']
    user = st.session_state['user']
    #st.markdown(user)

    st.title('Password Reset')

    with st.form('Password Reset', clear_on_submit=True):
        st.subheader(f'Username : **{user['username']}**')
        st.write(user['security_question'])
        real_answer = user['security_answer']

        answer = st.text_input('answer :') 
        if st.form_submit_button('Submit'):

            if answer == real_answer:
                st.session_state['issuccess'] = 'success'
                st.success('Please Input a New Password')
            else:
                st.error('Incorrect Answer. Please Try Again...')


                

    is_success = st.session_state['issuccess']

    if is_success == 'success':

        with st.form("Set Password", clear_on_submit=True):

            new_password = st.text_input('Enter a new password :', type = 'password')

            if st.form_submit_button('Change'):

                if len(new_password) > 7:

                    result = collection.update_one(
                                    {"username": username},
                                    {"$set": {"password": new_password}}
                                )
                    st.success('Password Reset Successful!')

                else:
                    st.error('Password is Too Short')

    c1,c2,c3 =st.columns(3)
    with c2:
        st.page_link("app.py", label=" Go back to Home Page", icon="🏠")


except Exception as e:
    st.error('Your Session Expired! Go Back to Home Page')
    #raise ConnectionError(f"Your Session Expired...Go Back to Home Page... or... Please contact to Admin...{e}")


st.markdown(
    """
    <style>
    div[data-testid="stFormSubmitButton"]{
         text-align: center;
            display: block;
            margin-left:auto;
            margin-right: auto;
            width: 100%;
 
    }
    </style>
    """,
    unsafe_allow_html=True,)