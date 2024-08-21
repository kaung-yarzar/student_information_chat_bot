import streamlit as st
st.set_page_config(page_title = 'Student Information Chatbot', page_icon = '🕯️',initial_sidebar_state='collapsed')



if "role" not in st.session_state:
    st.session_state.role = ''

if 'user' not in st.session_state:
    st.session_state.user = ''

if "issuccess" not in st.session_state:
    st.session_state.issuccess = ''

if "changepassword" not in st.session_state:
    st.session_state.changepassword = None

if "changequestion" not in st.session_state:
    st.session_state.changequestion = None

if "messages" not in st.session_state:
      st.session_state.messages = []


from connect_db import connect_user_collection
from chatbot_model import chatbot
from signup import sign_up
from forgetpassword import forget
from changepassword import change_password
from changesecurityquestion import change_security_question
from streamlit_option_menu import option_menu



## Session Initialization


## Login Authenticate
#@st.cache_resource
def authenticate(username, password):
    collection = connect_user_collection()
    admin = collection.find_one({"username": username, "password": password})
    return admin is not None



## Loggin Form
def login():
    # st.session_state.role = st.session_state._role
    with st.form("login form"):

        st.subheader("Login")
        username = st.text_input("Username :")
        password = st.text_input("Password :", type="password")

        if st.form_submit_button("Login", type='primary'):
            if authenticate(username, password):
                st.session_state['role'] = username  # Mark the user as logged in
                st.rerun()
                st.success(f"Login Successful! Welcome, {username}")
                st.balloons()
            else:
                st.error("Invalid Username or Password. Please Try again")
        return username



## Main Function
def main():
    #st.markdown(st.session_state['role'])
    # Check if the user is already logged in
    if st.session_state['role']:
        
        chatbot()
        username = st.session_state['role']
        st.sidebar.header(f"WELCOME   :blue[{username.upper()}]") 
        st.sidebar.divider()
        
        with st.sidebar:
            change_password()
        with st.sidebar:
            change_security_question()
        st.sidebar.divider()

        def logout_button():
            st.session_state.pop("role")
            st.session_state.pop("changepassword") 
            st.session_state.pop("changequestion") 
            st.session_state.pop("messages")

        st.sidebar.button("Logout", use_container_width=True, on_click=logout_button, type='primary')   # Clear the login status

        #st.toast('Welcome', icon='😍')


            
    else:
        st.markdown("<h1 style='text-align: center;'>TU Meiktila Student Information Chatbot</h1>", unsafe_allow_html=True)
        #st.title('Student Information Chatbot')
        st.markdown(' ')
        st.markdown(' ')

        st.markdown("""
        <style>
        div[data-testid="stHeadingWithActionElements"]{
        text-align: center;
        display: block;
        margin-left: 2%;
        margin-right: auto%;
        width: 100%;}
        </style>""", unsafe_allow_html=True,)

        
        selected = option_menu(menu_title = None, options = ['Signup', 'Login', 'Forget Password'], 
            icons=[ 'person', 'person-add', 'key'], menu_icon="cast", default_index=1, orientation = "horizontal")
        st.markdown('   ')
        
        if selected == "Signup":
            sign_up()

            
        if selected == "Login":
            login()

        
        if selected == "Forget Password":
            forget()




if __name__ == "__main__":
    #st.markdown(st.session_state)
    main()

### CSS Style Inject

#     st.markdown(
#     """
#     <style>
#     div[data-testid="stButton"]{
#          text-align: center;
#             display: block;
#             margin-left: auto;
#             margin-right: auto;
#             width: 100%;
 
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )
    
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
    unsafe_allow_html=True,
)
    
#     st.markdown(
#     """
#     <style>
#     div[data-testid="stHeadingWithActionElements"]{
#          text-align: center;
#             display: block;
#             margin-left: 2%;
#             margin-right: auto%;
#             width: 100%;
 
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

  #####  


# import base64
# import plotly.express as px

# df = px.data.iris()

# # @st.experimental_memo
# def get_img_as_base64(file):
#     with open(file, "rb") as f:
#         data = f.read()
#     return base64.b64encode(data).decode()

# img = get_img_as_base64("image.jpg")
# page_bg_img = f"""
# <style>
# [data-testid="stAppViewContainer"] > .main {{
# background-image: url("https://images.unsplash.com/photo-1501426026826-31c667bdf23d");
# background-size: 180%;
# background-position: top left;
# background-repeat: no-repeat;
# background-attachment: local;
# }}

# [data-testid="stSidebar"] > div:first-child {{
# background: rgba(0,0,0,0);
# }}


# [data-testid="stBottom"] > div:first-child{{
# background: rgba(0,0,0,0);
# }}


# [data-testid="stTextInput-RootElement"] > div:first-child {{
# background: rgba(0,0,0,0);
# }}



# ["data-testid="stTextInput-RootElement"] {{
# background: rgba(0,0,0,0);
# }}

# [data-testid="baseButton-secondaryFormSubmit"] {{
# background: rgba(0,0,0,0);
# }}



# [data-testid="stHeader"] {{
# background: rgba(0,0,0,0);
# }}

# [data-testid="stToolbar"] {{
# right: 2rem;
# }}
# </style>
# """

# st.markdown(page_bg_img, unsafe_allow_html=True)