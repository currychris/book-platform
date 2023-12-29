import streamlit as st
import requests

if "page" not in st.session_state:
    st.session_state.page = "search_books"

if "search_results" not in st.session_state:
    st.session_state.search_results = None

if "search_param" not in st.session_state:
    st.session_state.search_param = {"title": None,
                                     "description": None,
                                     "author": None}

if "login_param" not in st.session_state:
    st.session_state.login_param = {"username": None,
                                    "password": None}
    
if "register_param" not in st.session_state:
    st.session_state.register_param = {"pseudonym": None,
                                       "email": None,
                                       "username": None,
                                       "password": None}
    
if "update_acc_param" not in st.session_state:
    st.session_state.update_acc_param = {"new_password": None}
    
if "user_session" not in st.session_state:
    st.session_state.user_session = {"username": None,
                                     "jwt_token": None}
    
if "create_book_param" not in st.session_state:
    st.session_state.create_book_param = {"title": None,
                                          "description": None,
                                          "isbn": None,
                                          "price": None}
    

def search_books():
    response = requests.get("http://0.0.0.0:8000/books/show",
                             params=st.session_state.search_param)
    st.session_state.search_results = response.json()["books"]


def login():
    response = requests.post("http://0.0.0.0:8000/user/login",
                             params=st.session_state.login_param)
    if response.status_code == 200 and "JWT Token" in response.json():
        st.success("Login successful")
        st.session_state.user_session["username"] = st.session_state.login_param["username"]
        st.session_state.user_session["jwt_token"] = response.json()['JWT Token']
    else:
        st.error(f"Login failed: {response.json()['message']}")
    
    st.session_state.login_param["username"] = None
    st.session_state.login_param["password"] = None

def delete_account():
    response = requests.delete("http://0.0.0.0:8000/user/delete",
                               params=st.session_state.user_session)
    if response.status_code == 200 and response.json()["message"].endswith("deleted"):
        st.success("Account deleted")
        st.session_state.user_session["username"] = None
        st.session_state.user_session["jwt_token"] = None
    else:
        st.error(f"Account deletion failed: {response.json()['message']}")

def register():
    response = requests.post("http://0.0.0.0:8000/user/create",
                             params=st.session_state.register_param)
    if response.status_code == 200 and response.json()["message"].endswith("created"):
        st.success("Account created")
    else:
        st.error(f"Account creation failed: {response.json()['message']}")


def logout():
    response = requests.delete("http://0.0.0.0:8000/user/logout",
                               params={"username": st.session_state.user_session["username"]})
    if response.status_code == 200 and response.json()["message"].endswith("logged out"):
        st.success("Logout successful")
        st.session_state.user_session["username"] = None
        st.session_state.user_session["jwt_token"] = None
    else:
        st.error(f"Logout failed: {response.json()['message']}")

def change_password():
    response = requests.post("http://0.0.0.0:8000/user/update",
                             params={**st.session_state.user_session,
                                     **st.session_state.update_acc_param})
    if response.status_code == 200 and response.json()["message"].endswith("password changed"):
        st.success("Password changed")
        st.session_state.update_acc_param["new_password"] = None
    else:
        st.error(f"Password change failed: {response.json()['message']}")

def create_book():
    response = requests.post("http://0.0.0.0:8000/books/create",
                             params={**st.session_state.user_session,
                                     **st.session_state.create_book_param})
    if response.status_code == 200 and response.json()["message"].endswith("created"):
        st.success("Book created")
        st.session_state.create_book_param = {"title": None,
                                              "description": None,
                                              "isbn": None,
                                              "price": None}
    else:
        st.error(f"Book creation failed: {response.json()['message']}")


if st.session_state.page == "search_books":
    st.title("Book search")
    st.write("Search for a book in Emilia's Buchplattform")

    with st.form(key="search"):
        st.session_state.search_param['title'] = st.text_input("Title")
        st.session_state.search_param['description'] = st.text_input("Description")
        st.session_state.search_param['author'] = st.text_input("Author")
        st.form_submit_button("Search", on_click=search_books)

    if st.session_state.search_results:
        st.dataframe(st.session_state.search_results)

elif st.session_state.page == "create_book":
    st.title("Create a book")
    if st.session_state.user_session["username"] is None:
        st.error("You need to be logged in to create a book")
    else:
        with st.form(key="create_book"):
            st.session_state.create_book_param = {"title": st.text_input("Title"),
                                                "description": st.text_input("Description"),
                                                "isbn": st.text_input("ISBN"),
                                                "price": st.number_input("Price")}
            st.form_submit_button("Create book", on_click=create_book)

elif st.session_state.page == "manage_books":
    st.title("Manage Books")

elif st.session_state.page == "account":
    st.title("Account")

    if st.session_state.user_session["username"] is None:

        with st.form(key="login"):
            st.subheader("Login")
            st.session_state.login_param["username"] = st.text_input("Username")
            st.session_state.login_param["password"] = st.text_input("Password",
                                                                     type="password")
            st.form_submit_button("Login", on_click=login)

        st.divider()

        with st.form(key="register"):
            st.subheader("Register")
            st.session_state.register_param["pseudonym"] = st.text_input("Pseudonym")
            st.session_state.register_param["email"] = st.text_input("E-Mail")
            st.session_state.register_param["username"] = st.text_input("Username")
            st.session_state.register_param["password"] = st.text_input("Password",
                                                                        type="password")
            st.form_submit_button("Register", on_click=register)

    else:
        st.write(f"Logged in as {st.session_state.user_session['username']}")

        with st.form(key="change_password"):
            st.session_state.update_acc_param["new_password"] = st.text_input("New Password",
                                                                              type="password")
            st.form_submit_button("Change password", on_click=change_password)
        
        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.button("Logout", on_click=logout, use_container_width=True)
        with col2:
            st.button("Delete account", on_click=delete_account, type="primary",
                      use_container_width=True)

def navigate(page_name):
    st.session_state.page = page_name

with st.sidebar:
    st.header("Emilia's Buchplattform")

    st.button("Book search", key="book_search", on_click=navigate,
              kwargs={"page_name": "search_books"}, use_container_width=True)
    st.button("Create a book", key="create_book", on_click=navigate,
              kwargs={"page_name": "create_book"}, use_container_width=True)
    st.button("Manage Books", key="manage_books", on_click=navigate,
              kwargs={"page_name": "manage_books"}, use_container_width=True)
    st.button("Account", key="account", type="primary", on_click=navigate,
              kwargs={"page_name": "account"}, use_container_width=True)
