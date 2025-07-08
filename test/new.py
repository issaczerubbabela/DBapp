import streamlit as st
import sqlite3

# ---------- Database setup ----------
conn = sqlite3.connect('people.db', check_same_thread=False)
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS people (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        email TEXT
    )
''')
conn.commit()

# ---------- Database functions ----------
def add_person(name, age, email):
    c.execute("INSERT INTO people (name, age, email) VALUES (?, ?, ?)", (name, age, email))
    conn.commit()

def get_all_people():
    c.execute("SELECT * FROM people")
    return c.fetchall()

def update_person(person_id, name, age, email):
    c.execute("UPDATE people SET name = ?, age = ?, email = ? WHERE id = ?", (name, age, email, person_id))
    conn.commit()

def delete_person(person_id):
    c.execute("DELETE FROM people WHERE id = ?", (person_id,))
    conn.commit()

def search_people(search_term):
    # Search in name, age, and email columns
    like_term = f"%{search_term}%"
    c.execute("""
        SELECT * FROM people
        WHERE name LIKE ? OR
              age LIKE ? OR
              email LIKE ?
    """, (like_term, like_term, like_term))
    return c.fetchall()

# ---------- Streamlit UI ----------
st.title("People Database App 🚀")

menu = ["Add", "View", "Update", "Delete", "Search"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add":
    st.subheader("Add Person")
    with st.form("add_form", clear_on_submit=True):
        name = st.text_input("Name")
        age = st.number_input("Age", 0, 120)
        email = st.text_input("Email")
        submitted = st.form_submit_button("Add")
        if submitted:
            add_person(name, age, email)
            st.success(f"Added {name} to database!")

elif choice == "View":
    st.subheader("View All People")
    people = get_all_people()
    st.dataframe(people)

elif choice == "Update":
    st.subheader("Update Person")
    people = get_all_people()
    ids = [p[0] for p in people]
    if ids:
        selected_id = st.selectbox("Select ID to Update", ids)
        selected_person = next((p for p in people if p[0] == selected_id), None)

        if selected_person:
            new_name = st.text_input("Name", value=selected_person[1])
            new_age = st.number_input("Age", 0, 120, value=selected_person[2])
            new_email = st.text_input("Email", value=selected_person[3])
            if st.button("Update"):
                update_person(selected_id, new_name, new_age, new_email)
                st.success("Updated successfully!")

else:
    if choice == "Delete":
        st.subheader("Delete Person")
        people = get_all_people()
        ids = [p[0] for p in people]
        if ids:
            selected_id = st.selectbox("Select ID to Delete", ids)
            if st.button("Delete"):
                delete_person(selected_id)
                st.warning("Deleted successfully!")
        else:
            st.info("No records to delete.")

    elif choice == "Search":
        st.subheader("Search People")
        search_term = st.text_input("Enter search term (name, age, or email):")
        if st.button("Search"):
            results = search_people(search_term)
            if results:
                st.dataframe(results)
            else:
                st.warning("No matching records found.")

# ---------- End ----------
