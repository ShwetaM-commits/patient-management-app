import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000"

st.title("Contact Management System")
st.set_page_config(layout="wide")

if "delete_id" not in st.session_state:
    st.session_state.delete_id = None

if "update_id" not in st.session_state:
    st.session_state.update_id = None

if "show_contacts" not in st.session_state:
    st.session_state.show_contacts = False


with st.form("contact_form"):
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    address = st.text_area("Address")
    email = st.text_input("Email")
    phone = st.text_input("Phone")

    import re
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    phone_valid = phone.isdigit() and len(phone) <= 10
    email_valid = re.match(email_pattern, email)

    if phone and not phone_valid:
        st.warning("Phone number must be up to 10 digits.")
    if email and not email_valid:
        st.warning("Please enter a valid email address.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        submit = st.form_submit_button("Add Contact")
    with col2:
        show_submit = st.form_submit_button("Show Saved Contacts")
    
    if show_submit:
        st.session_state.show_contacts = True
    
    if submit:
        if phone_valid and email_valid:
            data = {
                "first_name": first_name,
                "last_name": last_name,
                "address": address,
                "email": email,
                "phone": phone
            }
            response = requests.post(API_URL + "/patients", json=data)
            if response.status_code == 200:
                st.success("Contact added successfully!")
            else:
                st.error("Error adding contact")
        else:
            st.warning("Please correct the errors above before submitting.")


if st.session_state.show_contacts:
    st.header("All Contacts")
    if st.session_state.update_id:
        update_id = st.session_state.update_id

        st.divider()
        st.subheader("Update Contact")

        res = requests.get(f"{API_URL}/patients/{update_id}")
        selected = res.json()

        if selected:
            with st.form(f"update_form_{update_id}"):
                first_name = st.text_input("First Name", value=selected["first_name"])
                last_name = st.text_input("Last Name", value=selected["last_name"])
                address = st.text_area("Address", value=selected["address"])
                email = st.text_input("Email", value=selected["email"])
                phone = st.text_input("Phone", value=selected["phone"])

                import re
                email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
                phone_valid = phone.isdigit() and len(phone) <= 10
                email_valid = re.match(email_pattern, email)

                if phone and not phone_valid:
                    st.warning("Phone number must be up to 10 digits.")
                if email and not email_valid:
                    st.warning("Please enter a valid email address.")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    submit = st.form_submit_button("Update")

                with col2:
                    cancel = st.form_submit_button("Cancel")

                if submit:
                    if phone_valid and email_valid:
                        data = {
                            "first_name": first_name,
                            "last_name": last_name,
                            "address": address,
                            "email": email,
                            "phone": phone
                        }
                        update_res = requests.put(
                            f"{API_URL}/patients/{update_id}",
                            json=data
                        )
                        if update_res.status_code == 200:
                            st.success("Updated successfully!")
                            st.session_state.update_id = None
                            st.rerun()
                        else:
                            st.error("Update failed")
                    else:
                        st.warning("Please correct the errors above before updating.")

                if cancel:
                    st.session_state.update_id = None
                    st.rerun()
        
    else:
        
        response = requests.get(f"{API_URL}/patients")
        if response.status_code == 200:
            contacts = response.json()
            
            col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1,2,2,3,2,2,2,2])
            col1.write("ID")
            col2.write("First Name")
            col3.write("Last Name")
            col4.write("Email")
            col5.write("Phone")
            col6.write("Address")
            col7.write("Update")
            col8.write("Delete")

            st.divider()

            for contact in contacts:
                col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1,2,2,3,2,2,2,2])

                col1.write(contact["id"])
                col2.write(contact["first_name"])
                col3.write(contact["last_name"])
                col4.write(contact["email"])
                col5.write(contact["phone"])
                col6.write(contact["address"])

                with col7:
                    if st.button("Update", key=f"upd_{contact['id']}"):
                        st.session_state.update_id = contact["id"]
                        st.rerun()

                with col8:
                    if st.button("Delete", key=f"del_{contact['id']}"):
                        st.session_state.delete_id = contact["id"]

if st.session_state.delete_id:
    delete_id = st.session_state.delete_id
    res = requests.delete(f"{API_URL}/patients/{delete_id}")
    if res.status_code == 200:
        st.success(f"Deleted ID {delete_id}")
    else:
        st.error("Delete failed")
        
    st.session_state.delete_id = None
    st.rerun()
    
