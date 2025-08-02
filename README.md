# 📚 Personal Library Management System

A Streamlit-powered web app for tracking, managing, and analyzing your personal book collection. Featuring an eye-catching gradient UI, animated headers, and intuitive controls, this lightweight system demonstrates how to build a polished, stateful application in pure Python.

---

## 🚀 Features

- **Add, Delete & Search Books**  
  - Fill out a simple form to add a new book (title, author, year, genre, read status).  
  - Prevents duplicate entries by matching title, author, and year.  
  - Remove books with a single click.  
  - Search by title or author and instantly display matching results.

- **List & Explore Your Collection**  
  - Expandable panels show full book details at a glance.  
  - Counts total books; shows metadata like author, genre, and whether you’ve read it.

- **Reading Statistics Dashboard**  
  - Dynamic Streamlit metrics for total books, number read vs. unread, and percentage completed.  
  - Instantly visualize your reading progress.

- **Persistent Storage**  
  - Uses Streamlit’s session state for live interaction.  
  - Saves and loads your library to `library.txt` in JSON format so data persists across sessions.

- **Custom Theming & Animations**  
  - Gradient backgrounds for main content and sidebar.  
  - Fade-in header and hover-scaled buttons for a modern feel.  
  - Styled inputs, expanders, and metric cards for consistent branding.

---

## ⚙️ Prerequisites

- Python 3.8+  
- [Streamlit](https://streamlit.io): `pip install streamlit`

---

## 🛠 Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/library-management.git
   cd library-management


2. **Install dependencies**

   ```bash
   pip install streamlit
   ```

3. **Run the app**

   ```bash
   streamlit run app.py
   ```

   Replace `app.py` with your script filename if different.

---

## 📝 Usage

1. **Add Book**

   * Select “Add Book 📖” from the sidebar.
   * Fill in Title, Author, Publication Year, and Genre.
   * Check “Read Status” if you’ve already read it.
   * Click **Add Book**.

2. **Delete Book**

   * Choose “Delete Book ❌”.
   * Select the book from the dropdown and click **Delete Book**.

3. **Search Book**

   * Go to “Search Book 🔍”.
   * Enter a keyword and choose whether to search Title or Author.
   * Results appear instantly.

4. **List All Books**

   * Click “List All Books 📚” to see every entry.
   * Expand each book to view details.

5. **Statistics**

   * Click “Statistics 📊” to view total vs. read/unread counts and percentage read.

6. **Save Library**

   * Choose “Save Library 💾” to write `library.txt` with your current collection.

---

## 📁 Project Structure

```
├── app.py                 # Main Streamlit application
├── library.txt            # Persistent JSON storage (auto-created)
├── requirements.txt       # (Optional) pinned dependencies
├── utils/                 
│   └── (if you modularize any helpers)
└── README.md              # This documentation
```

---

## 🛡 License

Distributed under the MIT License. See [`LICENSE`](./LICENSE) for more information.

---
