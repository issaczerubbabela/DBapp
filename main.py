import streamlit as st
import sqlite3
import pandas as pd

# ---------- Page Configuration ----------
st.set_page_config(
    page_title="People Database",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Custom CSS Styling ----------
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        margin: 2rem auto;
        max-width: 1200px;
    }
    
    /* Title styling */
    .main-title {
        text-align: center;
        color: #2c3e50;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .css-1d391kg .css-1544g2n {
        background: transparent;
        color: white;
    }
    
    .css-1d391kg .css-1544g2n:hover {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    /* Section headers */
    .section-header {
        color: #2c3e50;
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
        text-align: center;
    }
    
    /* Form styling */
    .stForm {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid #e9ecef;
    }
    
    /* Input fields */
    .stTextInput input, .stNumberInput input {
        border: 2px solid #e9ecef;
        border-radius: 10px;
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Success/Warning/Info messages */
    .stAlert {
        border-radius: 10px;
        border: none;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Data table styling */
    .stDataFrame {
        background: white;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }
    
    /* Select box styling */
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e9ecef;
    }
    
    /* Sidebar selectbox */
    .css-1d391kg .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
    }
    
    /* Card styling for stats */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 1rem;
        font-weight: 500;
        opacity: 0.9;
    }
    
    /* Animation for form submission */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
</style>
""", unsafe_allow_html=True)

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

def get_stats():
    c.execute("SELECT COUNT(*) FROM people")
    total_people = c.fetchone()[0]
    
    c.execute("SELECT AVG(age) FROM people WHERE age IS NOT NULL")
    avg_age = c.fetchone()[0]
    avg_age = round(avg_age, 1) if avg_age else 0
    
    return total_people, avg_age

# ---------- Streamlit UI ----------
st.markdown('<h1 class="main-title">👥 People Database Manager</h1>', unsafe_allow_html=True)

# Display stats
total_people, avg_age = get_stats()
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{total_people}</div>
        <div class="metric-label">Total People</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{avg_age}</div>
        <div class="metric-label">Average Age</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">✨</div>
        <div class="metric-label">Database Active</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Sidebar menu
menu = ["➕ Add Person", "👁️ View All", "✏️ Update", "🗑️ Delete", "🔍 Search"]
choice = st.sidebar.selectbox("📋 Navigation Menu", menu)

if choice == "➕ Add Person":
    st.markdown('<h2 class="section-header">Add New Person</h2>', unsafe_allow_html=True)
    
    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("👤 Full Name", placeholder="Enter full name...")
            age = st.number_input("🎂 Age", min_value=0, max_value=120, value=25)
        
        with col2:
            email = st.text_input("📧 Email Address", placeholder="example@email.com")
            st.markdown("<br>", unsafe_allow_html=True)
        
        submitted = st.form_submit_button("✅ Add Person", use_container_width=True)
        
        if submitted:
            if name and email:
                add_person(name, age, email)
                st.success(f"🎉 Successfully added {name} to the database!")
                st.balloons()
            else:
                st.error("⚠️ Please fill in all required fields (Name and Email)")

elif choice == "👁️ View All":
    st.markdown('<h2 class="section-header">All People in Database</h2>', unsafe_allow_html=True)
    
    people = get_all_people()
    if people:
        df = pd.DataFrame(people, columns=['ID', 'Name', 'Age', 'Email'])
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Download option
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name="people_database.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("📭 No people in the database yet. Add some people to get started!")

elif choice == "✏️ Update":
    st.markdown('<h2 class="section-header">Update Person Information</h2>', unsafe_allow_html=True)
    
    people = get_all_people()
    if people:
        # Create a more user-friendly display for selection
        people_display = [f"ID: {p[0]} - {p[1]} ({p[3]})" for p in people]
        selected_display = st.selectbox("👤 Select Person to Update", people_display)
        
        if selected_display:
            selected_id = int(selected_display.split(":")[1].split(" -")[0])
            selected_person = next((p for p in people if p[0] == selected_id), None)
            
            if selected_person:
                col1, col2 = st.columns(2)
                
                with col1:
                    new_name = st.text_input("👤 Name", value=selected_person[1])
                    new_age = st.number_input("🎂 Age", min_value=0, max_value=120, value=selected_person[2])
                
                with col2:
                    new_email = st.text_input("📧 Email", value=selected_person[3])
                    st.markdown("<br>", unsafe_allow_html=True)
                
                if st.button("💾 Update Person", use_container_width=True):
                    update_person(selected_id, new_name, new_age, new_email)
                    st.success("✅ Person updated successfully!")
                    st.rerun()
    else:
        st.info("📭 No people in the database to update.")

elif choice == "🗑️ Delete":
    st.markdown('<h2 class="section-header">Delete Person</h2>', unsafe_allow_html=True)
    
    people = get_all_people()
    if people:
        people_display = [f"ID: {p[0]} - {p[1]} ({p[3]})" for p in people]
        selected_display = st.selectbox("👤 Select Person to Delete", people_display)
        
        if selected_display:
            selected_id = int(selected_display.split(":")[1].split(" -")[0])
            selected_person = next((p for p in people if p[0] == selected_id), None)
            
            if selected_person:
                st.warning(f"⚠️ Are you sure you want to delete **{selected_person[1]}**?")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🗑️ Yes, Delete", use_container_width=True):
                        delete_person(selected_id)
                        st.success("✅ Person deleted successfully!")
                        st.rerun()
                
                with col2:
                    if st.button("❌ Cancel", use_container_width=True):
                        st.info("Delete operation cancelled.")
    else:
        st.info("📭 No people in the database to delete.")

elif choice == "🔍 Search":
    st.markdown('<h2 class="section-header">Search People</h2>', unsafe_allow_html=True)
    
    search_term = st.text_input("🔍 Enter search term", placeholder="Search by name, age, or email...")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        search_button = st.button("🔍 Search", use_container_width=True)
    
    if search_button and search_term:
        results = search_people(search_term)
        if results:
            st.success(f"✅ Found {len(results)} matching record(s)")
            df = pd.DataFrame(results, columns=['ID', 'Name', 'Age', 'Email'])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("🔍 No matching records found. Try a different search term.")
    elif search_button:
        st.error("⚠️ Please enter a search term.")

# ---------- Footer ----------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; font-size: 0.9rem; margin-top: 2rem;">
    <p>💡 People Database Manager - Built with Streamlit</p>
    <p>Manage your contacts with style and efficiency! ✨</p>
</div>
""", unsafe_allow_html=True)

# ---------- End ----------
