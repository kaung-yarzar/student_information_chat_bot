import streamlit as st
from connect_db import connect_user_collection


collection = connect_user_collection()

    
def insert_new_question(username,new_question ,new_answer):
    collection.update_one({"username": username}, {"$set": {"security_answer": new_answer, "security_question": new_question}})


def change_security_question():
    username = st.session_state['role']
    if st.button('Change Security Question', use_container_width=True):
        st.session_state.changequestion = True
    

    if st.session_state.changequestion:
        with st.form('change question', clear_on_submit = True):
            st.subheader("Change Security Question")

            password = st.text_input("Enter password :", type="password")
            new_question = st.selectbox(
            "Security question :",
            ("Who is your favourite teacher?",
            "What is the name of your first pet?",
            "What is your favourite book?",
            "Waht is your favorite movie?",
            "What is your favorite song?",
            "Who is your first love?",
            "Where is your home town?",
            "What is your dream?",
            "Who is your favourite star?"), )

            new_answer = st.text_input("New answer :")


            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Change", use_container_width=True, type="primary"):
                    
                    check_password = collection.find_one({"username": username, "password": password})
                    if check_password:
                        if new_answer:
                                insert_new_question(username, new_question, new_answer)
                                st.toast("Changed Successfully!", icon ='✅')
                                #st.session_state.pop("changeusername")
                        else:
                            st.toast('Answer Should Not be empty', icon= '❌')
                    else:
                        st.toast("Incorrect Password", icon = '❌')

            def hide():
                st.session_state.pop("changequestion")

            with col2:
                st.form_submit_button("Cancel   ", use_container_width=True,on_click=hide)

                # st.session_state.pop("changequestion")