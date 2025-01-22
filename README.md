# Project3
**BizCardX: Extracting Business Card Data with OCR**

**Project Overview**
This project involves building a Streamlit application that allows users to upload images of business cards and extract relevant information using easyOCR. The extracted details include:

Company name
Card holder's name
Designation
Mobile number
Email address
Website URL
Area, City, State, and Pin code
The extracted information is displayed in a clean, user-friendly interface and is stored in a SQLite/MySQL database. The application also allows users to manage the extracted data through CRUD operations (Create, Read, Update, Delete), enabling efficient organization of business card details.

**Features**
Image Upload: Users can upload a business card image for processing.
OCR Extraction: The application uses easyOCR to extract details like company name, card holder's name, and contact information from the uploaded image.
Display Extracted Information: The extracted data is displayed in a structured format on the UI.
Database Management: Store extracted information alongside the uploaded image in a database (SQLite/MySQL).
CRUD Operations: Users can view, update, and delete records from the database through the Streamlit UI.
Simple User Interface: Intuitive and easy-to-use interface guiding the user through the process.

**Technologies Used**
Python: Primary programming language for building the application.
Streamlit: Framework for building the web interface.
easyOCR: Optical Character Recognition (OCR) library for extracting text from images.
SQLite/MySQL: Database systems for storing the business card data.
Pillow: Python Imaging Library for basic image processing.
Pandas: Data manipulation for handling the extracted information.

**How It Works**
Upload Image: Users can upload a business card image through the Streamlit interface.
OCR Processing: The image is processed using the easyOCR library to extract the text and details.
Display Data: Extracted details like company name, mobile number, email, etc., are displayed in an organized manner on the dashboard.
Store in Database: The data is stored in a database for future retrieval.
CRUD Operations: Users can view, update, or delete records stored in the database through the Streamlit UI.

**Conclusion**
This application is a powerful tool for automating the extraction and management of business card information. By leveraging OCR technology and an intuitive interface, it simplifies the process of capturing and storing contact information from business cards, making it easier to manage and retrieve.

