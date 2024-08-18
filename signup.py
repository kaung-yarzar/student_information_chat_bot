import streamlit as st
import re
from connect_db import connect_user_collection


collection = connect_user_collection()


##insert data into database
def insert_user(e, u, p, q, sq):
    document ={'email': e, 'username': u, 'password' : p, 'security_question' : q, 'security_answer': sq}
    insert_document = collection.insert_one(document)
    print(insert_document.inserted_id)



## checking email is already exists in database
def validate_email(e):
    email_check = collection.find_one({'email' : e}, {'_id' : 0, 'username' :0, 'password' : 0})
    if email_check == None:
        return True   # True means user can create account



## checking username is already exists in database
def validate_username(u):
    username_check = collection.find_one({'username' : u}, {'_id' : 0, 'email' :0, 'password' : 0})
    if username_check == None:
        return True   # True means user can create account



## Checking email is in true format
def check_email(e):
    pattern = "^[a-z0-9_]+@[a-z0-9]+\.[a-z]{1,3}$"
    if re.match(pattern, e):
        return True



## Checking username is in true format
def check_username(u):
    pattern = "^[a-zA-Z0-9]*$"
    if re.match(pattern, u):
        return True



## Sign Up Function 
def sign_up():
    with st.form(key = 'signup', clear_on_submit = True):    

        st.subheader('Create Account')
        

        email = st.text_input(':red[*]Email :')
        username = st.text_input(':red[*]Username :')
        password = st.text_input(':red[*]Password :',type = 'password')
        confirm_password = st.text_input(':red[*]Confirm Password :',type='password')
        option = st.selectbox(
            ":red[*]Security Question :",
            ("Who is your favourite teacher?",
            "What is the name of your first pet?",
            "What is your favourite book?",
            "Waht is your favorite movie?",
            "What is your favorite song?",
            "Who is your first love?",
            "Where is your home town?",
            "What is your dream?",
            "Who is your favourite star?"), )
        answer = st.text_input( label =':red[*]Answer :')


        ## condition စစ်
        if st.form_submit_button('Sign Up', type='primary'):
            if email and username and password and confirm_password and answer:
                if check_email(email) == True:
                    if validate_email(email) == True:
                        if username:
                            if check_username(username) ==True:
                                if validate_username(username) == True:
                                    if len(username) > 3:
                                        if len(password) > 7:
                                                if password == confirm_password:
                                                    if len(answer) > 2:
                                                        #hashed_password = stauth.Hasher([confirm_password]).generate()
                                                        #insert_user(email, username, hashed_password[0]) # hashed password က array အနေနဲ့ထွက်လာလို့ 0 index ထောက်
                                                        insert_user(email,username,password,option, answer)
                                                        st.success('Account Created Successfully. Please Login...')
                                                    else:
                                                        st.error("Please Answer Security Question")
                                                else:
                                                    st.error('Password Does Not Match')
                                        else:
                                            st.error('Password Should Have at Least 8 Characters')
                                    else:
                                        st.error('Username Should Have At Least 4 Characters')
                                else:
                                    st.error('Username Already Exists')
                            else:
                                st.error('Username Should be Alphabets or Numbers')
                        else:
                            st.error('Please Enter A Username')
                    else:
                        st.error('Your Account Is Already Exist. Please Try to Login Instead')
                else:
                    st.error('Enter a Correct Email Address')
            else:
                st.error('Please fill out all **Required** fields')
        
 #######
