import streamlit as st
import json
import pymongo

# Add custom CSS and animation
st.markdown("""
<style>
/* Main content background */
.stApp {
    background: #9796f0;
    background: -webkit-linear-gradient(to bottom, #fbc7d4, #9796f0);
    background: linear-gradient(to bottom, #fbc7d4, #9796f0);
    color: #2c3e50;
}

/* Sidebar background */
[data-testid="stSidebar"] {
    background: #ff6e7f;
    background: -webkit-linear-gradient(to bottom, #bfe9ff, #ff6e7f);
    background: linear-gradient(to bottom, #bfe9ff, #ff6e7f);
    padding: 20px !important;
    color: #2c3e50;
}

/* Animated header */
h1 {
    color: #2c3e50;
    animation: fadeIn 2s ease-in-out;
    padding: 0.5rem 0;
}

/* FadeIn animation */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Button styling */
.stButton > button {
    background-color: #2ecc71 !important;
    color: white !important;
    border: none !important;
    border-radius: 5px !important;
    padding: 10px 24px !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
}

/* Form elements */
.stTextInput input, 
.stNumberInput input,
.stTextArea textarea {
    color: white !important;  /* Changed to white text */
    border-radius: 5px !important;
    border: 1px solid #ddd !important;
     /* Added for better contrast */
}

/* Specific fix for number input */
.stNumberInput input {
    color: white !important;
}

/* Expander styling */
.stExpander {
    background: rgba(200, 200, 200, 0.9) !important;
    border-radius: 10px !important;
    margin: 0.5rem 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
}

.stExpander .stMarkdown {
    color: #2c3e50 !important;
}

/* Metric cards */
.stMetric {
     background: #9796f0;
    background: -webkit-linear-gradient(to bottom, #fbc7d4, #9796f0);
    background: linear-gradient(to bottom, #fbc7d4, #9796f0);
    color: #2c3e50;
    padding: 15px !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
}

/* Radio buttons */
.stRadio > div {
    color: white !important;        
    background: rgba(255, 255, 255, 0.9) !important;
    border-radius: 10px !important;
    padding: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# Session State and load library 
if 'library' not in st.session_state:
    try:
        with open('library.txt', 'r') as f:
            st.session_state.library = json.load(f)
    except FileNotFoundError:
        st.session_state.library = []  # Using a list to store books

# SideBar and Menu Options with emojis
st.sidebar.title('Library Management System 📚')
menu_option = st.sidebar.selectbox('Menu', [
    'Add Book 📖',
    'Delete Book ❌',
    'Search Book 🔍',
    'List All Books 📚',
    "Statistics 📊",
    "Save Library 💾",
    "Save to MongoDB 🗄️"
])

# Main Page Header with emoji
st.title('Personal Library Management System 📚')

if menu_option.startswith('Add Book'):
    st.header('Add Book 📖')
    with st.form("add_book_form"):
        book_title = st.text_input('Book Title')
        author = st.text_input('Author')
        publication_year = st.number_input('Publication Year', min_value=0, max_value=2100, step=1)
        genre = st.text_input('Genres')
        read_status = st.checkbox('Read Status')
        submitted = st.form_submit_button('Add Book')
        
        if submitted:
            title = book_title.strip()
            author_str = author.strip()
            genre_str = genre.strip()
            if title and author_str and genre_str:
                # Check for existing book
                is_duplicate = any(
                    book['title'].lower() == title.lower() and 
                    book['author'].lower() == author_str.lower() and
                    book['publication_year'] == int(publication_year)
                    for book in st.session_state.library
                )
                
                if is_duplicate:
                    st.error('This book already exists in the library! ❌')
                else:
                    new_book = {
                        'title': title,
                        'author': author_str,
                        'publication_year': int(publication_year),
                        'genre': genre_str,
                        'read_status': read_status
                    }
                    st.session_state.library.append(new_book)
                    st.success('Book added successfully! 🎉')
            else:
                st.error('Please fill all the fields ⚠️')


elif menu_option.startswith('Delete Book'):
    st.header('Delete Book ❌')
    if not st.session_state.library:
        st.warning('No books found in the library. 😞')
    else:
        book_list = [f"{book['title']} by {book['author']} ({book['publication_year']})"
                     for book in st.session_state.library]     
        selected_book = st.selectbox('Select a book to delete', book_list)

        if st.button('Delete Book'):
            index = book_list.index(selected_book)
            del st.session_state.library[index]
            st.success('Book deleted successfully! 🎉')

elif menu_option.startswith('Search Book'):
    st.header('Search Book 🔍')
    search_term = st.text_input('Enter a book title or author name to search')
    search_by = st.radio('Search by', ['Title', 'Author'])

    if search_term:
        search_term = search_term.lower()
        results = []
        for book in st.session_state.library:
            target = book['title'].lower() if search_by == 'Title' else book['author'].lower()
            if search_term in target:
                results.append(book)

        if results:
            st.write(f'Found {len(results)} books:')
            for book in results:
                st.subheader(f"{book['title']} 📖")
                st.write(f"**Author:** {book['author']}")
                st.write(f"**Publication Year:** {book['publication_year']}")
                st.write(f"**Genre:** {book['genre']}")
                st.write(f"**Read Status:** {'Read 😊' if book['read_status'] else 'Not Read 😔'}")
        else:
            st.warning('No books found. 😞')

elif menu_option.startswith('List All Books'):
    st.header('List All Books 📚')
    if not st.session_state.library:
        st.warning('No books found in the library. 😞')
    else:
        st.write(f'Total Books: {len(st.session_state.library)}')
        for idx, book in enumerate(st.session_state.library, 1):
            with st.expander(f"{idx}. {book['title']} by {book['author']}"):
                st.write(f"**Publication Year:** {book['publication_year']}")
                st.write(f"**Genre:** {book['genre']}")
                st.write(f"**Read Status:** {'Read 😊' if book['read_status'] else 'Not Read 😔'}")

elif menu_option.startswith("Statistics"):
    st.header('Statistics 📊')
    total_books = len(st.session_state.library)
    read_books = sum(1 for book in st.session_state.library if book['read_status'])
    unread_books = total_books - read_books

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric('Total Books', total_books)
    with col2:
        st.metric('Read Books', read_books)
    with col3:
        st.metric('Unread Books', unread_books)
    with col4:
        read_percentage = (read_books / total_books) * 100 if total_books > 0 else 0
        st.metric('Read Percentage', f"{read_percentage:.1f}%")

elif menu_option.startswith("Save Library"):
    st.header('Save Library 💾')
    with open('library.txt', 'w') as f:
        json.dump(st.session_state.library, f)
    st.success('Library saved successfully! 🎉')

elif menu_option.startswith("Save to MongoDB"):
    st.header('Save to MongoDB 🗄️')
    try:
        # Connect to MongoDB (adjust connection string as needed)
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client['library_db']
        collection = db['books']

        if st.button("Save to MongoDB"):
            if st.session_state.library:
                result = collection.insert_many(st.session_state.library)
                st.success(f"{len(result.inserted_ids)} books saved to MongoDB successfully! 🎉")
            else:
                st.warning("No books in library to save! ⚠️")
                
        # Button to view current records in the database
        if st.button("View MongoDB Records"):
            records = list(collection.find({}, {'_id': 0}))  # Exclude the MongoDB _id for clarity
            if records:
                st.write("Books in MongoDB:")
                for rec in records:
                    st.write(rec)
            else:
                st.info("No records found in MongoDB. 😞")
    except Exception as e:
        st.error(f"Error connecting to MongoDB: {e} ❌")
