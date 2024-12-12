import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
from PIL import Image
import pandas as pd
import numpy as np
import re
import io
import sqlite3

def image_to_text(path):
    input_image = Image.open(path)

    # Converting image to array format
    image_array = np.array(input_image)

    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_array, detail=0)
    return result, input_image

def extracted_text(texts):
    extracted_dict = {
        "NAME": [],
        "DESIGNATION": [],
        "COMPANY NAME": [],
        "CONTACT": [],
        "EMAIL": [],
        "WEBSITE": [],
        "ADDRESS": [],
        "PINCODES": []
    }

    extracted_dict["NAME"].append(texts[0])
    extracted_dict["DESIGNATION"].append(texts[1])

    for i in range(2, len(texts)):
        if texts[i].startswith("+") or (texts[i].replace("-", "").isdigit() and "-" in texts[i]):
            extracted_dict["CONTACT"].append(texts[i])
        elif "@" in texts[i]:
            extracted_dict["EMAIL"].append(texts[i])
        elif "www" in texts[i].lower() or ".com" in texts[i].lower():
            small = texts[i].lower()
            extracted_dict["WEBSITE"].append(small)
        elif "Tamil Nadu" in texts[i] or "TamilNadu" in texts[i] or texts[i].isdigit():
            extracted_dict["PINCODES"].append(texts[i])
        elif re.match(r'^[A-Za-z]', texts[i]):
            extracted_dict["COMPANY NAME"].append(texts[i])
        else:
            remov_colon = re.sub(r'[,;]', '', texts[i])
            extracted_dict["ADDRESS"].append(remov_colon)

    for key, value in extracted_dict.items():
        if len(value) > 0:
            concatenated = " ".join(value)
            extracted_dict[key] = [concatenated]
        else:
            extracted_dict[key] = ["NA"]
    return extracted_dict

# Streamlit part
st.set_page_config(layout="wide")
st.title("EXTRACTING BUSINESS CARD DATA WITH OCR")

with st.sidebar:
    select = option_menu("MENU", ["HOME", "UPLOAD & MODIFYING", "DELETE"])

if select == "HOME":
    pass

elif select == "UPLOAD & MODIFYING":
    img = st.file_uploader("Upload the Image", type=["png", "jpg", "jpeg"])
    if img is not None:
        st.image(img, width=300)

        text_image, input_img = image_to_text(img)
        text_dict = extracted_text(text_image)

        if text_dict:
            st.success("TEXT IS EXTRACTED SUCCESSFULLY")

        df = pd.DataFrame(text_dict)

        # Converting image to bytes
        Image_bytes = io.BytesIO()
        input_img.save(Image_bytes, format="PNG")
        image_data = Image_bytes.getvalue()

        # Creating dictionary
        data = {"IMAGE": [image_data]}
        df_1 = pd.DataFrame(data)

        concat_df = pd.concat([df, df_1], axis=1)
        st.dataframe(concat_df)

        button_1 = st.button("Save", use_container_width=True)
        if button_1:
            # Connect to SQLite database
            mydb = sqlite3.connect("bizcardx.db")
            cursor = mydb.cursor()

            # Table Creation
            create_table_query = """
            CREATE TABLE IF NOT EXISTS bizcard_details(
                name VARCHAR(255),
                designation VARCHAR(255),
                company_name VARCHAR(255),
                contact VARCHAR(255),
                email VARCHAR(225),
                website TEXT,
                address TEXT,
                pincode VARCHAR(255),
                image TEXT
            );
            """

            cursor.execute(create_table_query)
            mydb.commit()

            # Insert query
            insert_query = """
            INSERT INTO bizcard_details(name, designation, company_name, contact, email, website, address, pincode, image)
            VALUES(?,?,?,?,?,?,?,?,?)
            """
            datas = concat_df.values.tolist()[0]
            cursor.execute(insert_query, datas)
            mydb.commit()
            st.success("SAVED SUCCESSFULLY")

        method = st.radio("Select the Method", ["None", "Preview", "Modify"])

        if method == "None":
            st.write("")

        elif method == "Preview":
            mydb = sqlite3.connect("bizcardx.db")
            cursor = mydb.cursor()
            # Select query
            select_query = "SELECT * FROM bizcard_details"
            cursor.execute(select_query)
            table = cursor.fetchall()
            mydb.commit()

            table_df = pd.DataFrame(table, columns=("NAME", "DESIGNATION", "COMPANY_NAME", "CONTACT", "EMAIL",
                                                    "WEBSITE", "ADDRESS", "PINCODE", "IMAGE"))
            st.dataframe(table_df)

        elif method == "Modify":
            mydb = sqlite3.connect("bizcardx.db")
            cursor = mydb.cursor()
            # Select query
            select_query = "SELECT * FROM bizcard_details"
            cursor.execute(select_query)
            table = cursor.fetchall()
            mydb.commit()

            table_df = pd.DataFrame(table, columns=("NAME", "DESIGNATION", "COMPANY_NAME", "CONTACT", "EMAIL",
                                                    "WEBSITE", "ADDRESS", "PINCODE", "IMAGE"))

            col1, col2 = st.columns(2)
            with col1:
                selected_name = st.selectbox("Select the name", table_df["NAME"])

            df_3 = table_df[table_df["NAME"] == selected_name]
            df_4 = df_3.copy()

            col1, col2 = st.columns(2)
            with col1:
                mo_name = st.text_input("Name", df_3["NAME"].unique()[0])
                mo_desi = st.text_input("Designation", df_3["DESIGNATION"].unique()[0])
                mo_com_name = st.text_input("Company_name", df_3["COMPANY_NAME"].unique()[0])
                mo_contact = st.text_input("contact", df_3["CONTACT"].unique()[0])
                mo_email = st.text_input("email", df_3["EMAIL"].unique()[0])

                df_4["NAME"] = mo_name
                df_4["DESIGNATION"] = mo_desi
                df_4["COMPANY_NAME"] = mo_com_name
                df_4["CONTACT"] = mo_contact
                df_4["EMAIL"] = mo_email

            with col2:
                mo_website = st.text_input("website", df_3["WEBSITE"].unique()[0])
                mo_address = st.text_input("address", df_3["ADDRESS"].unique()[0])
                mo_pincode = st.text_input("pincode", df_3["PINCODE"].unique()[0])
                mo_image = st.text_input("image", df_3["IMAGE"].unique()[0])

                df_4["WEBSITE"] = mo_website
                df_4["ADDRESS"] = mo_address
                df_4["PINCODE"] = mo_pincode
                df_4["IMAGE"] = mo_image

            st.dataframe(df_4)

            col1, col2 = st.columns(2)
            with col1:
                button_3 = st.button("Modify")

            if button_3:
                mydb = sqlite3.connect("bizcardx.db")
                cursor = mydb.cursor()

                cursor.execute(f"DELETE FROM bizcard_details WHERE NAME = '{selected_name}'")
                mydb.commit()

                # Insert query
                insert_query = """
                INSERT INTO bizcard_details(name, designation, company_name, contact, email, website, address, pincode, image)
                VALUES(?,?,?,?,?,?,?,?,?)
                """
                datas = df_4.values.tolist()[0]
                cursor.execute(insert_query, datas)
                mydb.commit()
                st.success("MODIFIED SUCCESSFULLY")

elif select == "DELETE":
    mydb = sqlite3.connect("bizcardx.db")
    cursor = mydb.cursor()

    col1, col2 = st.columns(2)
    with col1:
        select_query = "SELECT NAME FROM bizcard_details"
        cursor.execute(select_query)
        table1 = cursor.fetchall()
        mydb.commit()

        names = [i[0] for i in table1]
        name_select = st.selectbox("Select the name", names)

    with col2:
        select_query = f"SELECT DESIGNATION FROM bizcard_details WHERE NAME='{name_select}'"
        cursor.execute(select_query)
        table2 = cursor.fetchall()
        mydb.commit()

        designation = [j[0] for j in table2]
        designation_select = st.selectbox("Select the designation", designation)

    if name_select and designation_select:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"Selected Name: {name_select}")
            st.write("")
            st.write("")
            st.write("")
            st.write(f"Selected Designation: {designation_select}")

        with col2:
            st.write("")
            st.write("")
            st.write("")
            st.write("")

            remove = st.button("Delete")

            if remove:
                cursor.execute(f"DELETE FROM bizcard_details WHERE NAME='{name_select}' AND DESIGNATION='{designation_select}'")
                mydb.commit()
                st.warning("DELETED")
