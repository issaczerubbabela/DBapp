
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
    like_term = f"%{search_term}%"
    c.execute("""
        SELECT * FROM people
        WHERE name LIKE ? OR
              age LIKE ? OR
              email LIKE ?
    """, (like_term, like_term, like_term))
    return c.fetchall()

# ---------- Streamlit UI ----------
st.set_page_config(page_title="People DB App", page_icon=":busts_in_silhouette:", layout="centered")
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>People Database App</h1>", unsafe_allow_html=True)

menu = ["Add", "View", "Update", "Delete", "Search"]
choice = st.sidebar.radio("Menu", menu)

if choice == "Add":
    st.markdown("## ➕ Add Person")
    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name")
        with col2:
            age = st.number_input("Age", 0, 120, step=1)
        email = st.text_input("Email")
        submitted = st.form_submit_button("Add")
        if submitted:
            if name and email:
                add_person(name, age, email)
                st.success(f"✅ {name} added to database!")
            else:
                st.error("Please fill in all required fields.")

elif choice == "View":
    st.markdown("## 📄 View All People")
    people = get_all_people()
    if people:
        st.dataframe(people, use_container_width=True, hide_index=True)
    else:
        st.info("No records found.")

elif choice == "Update":
    st.markdown("## ✏️ Update Person")
    people = get_all_people()
    ids = [p[0] for p in people]
    if ids:
        selected_id = st.selectbox("Select ID to Update", ids)
        selected_person = next((p for p in people if p[0] == selected_id), None)

        if selected_person:
            with st.form("update_form"):
                col1, col2 = st.columns(2)
                with col1:
                    new_name = st.text_input("Name", value=selected_person[1])
                with col2:
                    new_age = st.number_input("Age", 0, 120, value=selected_person[2], step=1)
                new_email = st.text_input("Email", value=selected_person[3])
                update_btn = st.form_submit_button("Update")
                if update_btn:
                    if new_name and new_email:
                        update_person(selected_id, new_name, new_age, new_email)
                        st.success("✅ Record updated successfully!")
                    else:
                        st.error("Please fill in all required fields.")
    else:
        st.info("No records to update.")

elif choice == "Delete":
    st.markdown("## 🗑️ Delete Person")
    people = get_all_people()
    ids = [p[0] for p in people]
    if ids:
        selected_id = st.selectbox("Select ID to Delete", ids)
        if st.button("Delete"):
            delete_person(selected_id)
            st.warning("⚠️ Record deleted successfully!")
    else:
        st.info("No records to delete.")

elif choice == "Search":
    st.markdown("## 🔎 Search People")
    search_term = st.text_input("Enter search term (name, age, email):")
    if st.button("Search"):
        results = search_people(search_term)
        if results:
            st.success(f"✅ Found {len(results)} matching record(s).")
            st.dataframe(results, use_container_width=True, hide_index=True)
        else:
            st.warning("No matching records found.")

# ---------- End ----------
