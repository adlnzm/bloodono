#working final
import streamlit as st
import pymysql
from streamlit_extras.let_it_rain import rain
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from datetime import datetime, timedelta
import numpy as np
from geopy.distance import geodesic

try:
        # Connect to MySQL server (without selecting a database yet)
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',  # Replace with your actual MySQL password
        cursorclass=pymysql.cursors.DictCursor
    )

    # Create a cursor object
    cursor = connection.cursor()

    # Name of the database
    database_name = 'blood_donation'

    # Create database if it does not exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    print(f"Database '{database_name}' checked/created successfully.")

    # Close the first connection
    cursor.close()
    connection.close()

except pymysql.MySQLError as e:
    print("Error while connecting to MySQL:", e)

# Now connect again, this time to the specific database
def get_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database=database_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection
def initialize_tables():    
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            # Donor table
            cursor.execute('''CREATE TABLE IF NOT EXISTS donors (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR(255),
                            phone_number VARCHAR(20),
                            village_town VARCHAR(255),
                            city VARCHAR(255),
                            state VARCHAR(255),
                            pin VARCHAR(10),
                            blood_group VARCHAR(5)
                        )''')

            # Receiver (Patient) table
            cursor.execute('''CREATE TABLE IF NOT EXISTS receivers (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR(255),
                            phone_number VARCHAR(20),
                            village_town VARCHAR(255),
                            city VARCHAR(255),
                            state VARCHAR(255),
                            pin VARCHAR(10),
                            blood_group VARCHAR(5)
                        )''')

            # Hospital table
            cursor.execute('''CREATE TABLE IF NOT EXISTS hospitals (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            hospital_name VARCHAR(255),
                            phone_number VARCHAR(20),
                            village_town VARCHAR(255),
                            city VARCHAR(255),
                            state VARCHAR(255),
                            pin VARCHAR(10)
                        )''')
            connection.commit()
    finally:
        connection.close()


# Add a donor
def add_donor(name, phone_number, village_town, city, state, pin, blood_group):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('''INSERT INTO donors (name, phone_number, village_town, city, state, pin, blood_group)
                              VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                           (name, phone_number, village_town, city, state, pin, blood_group))
        connection.commit()
    finally:
        connection.close()

# Get list of donors

def get_donors():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM donors')
            donors = cursor.fetchall()  # Returns a list of dictionaries
            
                # Convert the list of dictionaries to a pandas DataFrame
            df = pd.DataFrame(donors)
            st.write("Donor Information")
            #st.dataframe(df)  # Display the DataFrame in Streamlit
            
            return df
    except Exception as e:
        st.write(f"An error occurred: {e}")
        return []
    finally:
        connection.close()


# Delete a donor
def delete_donor(donor_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM donors WHERE id = %s', (donor_id,))
        connection.commit()
    finally:
        connection.close()

# Add a receiver
def add_receiver(name, phone_number, village_town, city, state, pin, blood_group):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('''INSERT INTO receivers (name, phone_number, village_town, city, state, pin, blood_group)
                              VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                           (name, phone_number, village_town, city, state, pin, blood_group))
        connection.commit()
    finally:
        connection.close()

# Get list of receivers
def get_receivers():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM receivers')
            receiver = cursor.fetchall()
            df = pd.DataFrame(receiver)
            st.write("Receiver Information")
            return df
    finally:
        connection.close()

# Delete a receiver
def delete_receiver(receiver_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM receivers WHERE id = %s', (receiver_id,))
        connection.commit()
    finally:
        connection.close()

# Add a hospital
def add_hospital(hospital_name, phone_number, village_town, city, state, pin):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('''INSERT INTO hospitals (hospital_name, phone_number, village_town, city, state, pin)
                              VALUES (%s, %s, %s, %s, %s, %s)''',
                           (hospital_name, phone_number, village_town, city, state, pin))
        connection.commit()
    finally:
        connection.close()

# Get list of receivers
def get_hosptials():
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM hospitals')
            hospital = cursor.fetchall()
            df = pd.DataFrame(hospital)
            st.write("Hospital Information")
            return df
    finally:
        connection.close()

# Delete a hospital
def delete_hospital(hospital_id):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM hospitals WHERE id = %s', (hospital_id,))
        connection.commit()
    finally:
        connection.close()

# Search donors by blood group and city
def search_donors_by_blood_group_and_city(blood_group, city):
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM donors WHERE blood_group = %s OR city = %s', (blood_group, city))
            return cursor.fetchall()
    finally:
        connection.close()


# Fetch Compatible Donors
def get_compatible_donors(receiver, donors_data):
    donors = pd.DataFrame(donors_data)  # Convert to DataFrame
    compatible_blood_groups = blood_compatibility(receiver['blood_group'])
    compatible_donors = donors[
        (donors['blood_group'].isin(compatible_blood_groups)) & (donors['city'] == receiver['city'])
    ]
    return compatible_donors


def train_knn_model(data):
    """
    Trains a KNN model to rank donors based on historical matches.

    Parameters:
        data (pd.DataFrame): Historical data including features like distance, blood compatibility, and frequency.

    Returns:
        NearestNeighbors: Trained KNN model.
    """
    features = data[['distance', 'blood_compatibility', 'frequency']]
    model = NearestNeighbors(n_neighbors=5, metric='euclidean')
    model.fit(features)
    return model

def predict_matches(receiver, donors, model):
    """
    Predicts the top matches for a receiver using a trained KNN model.

    Parameters:
        receiver (dict): Receiver's details.
        donors (pd.DataFrame): Donors' data.
        model (NearestNeighbors): Trained KNN model.

    Returns:
        pd.DataFrame: Top matched donors.
    """
    receiver_features = pd.DataFrame([{
        'distance': geodesic((receiver['latitude'], receiver['longitude']), 
                             (row['latitude'], row['longitude'])).km,
        'blood_compatibility': 1 if row['blood_group'] in blood_compatibility[receiver['blood_group']] else 0,
        'frequency': (datetime.now() - pd.to_datetime(row['last_donation_date'])).days
    } for _, row in donors.iterrows()])

    distances, indices = model.kneighbors(receiver_features)
    return donors.iloc[indices.flatten()]

def blood_compatibility(donor_blood_group, receiver_blood_group):
    # Define compatibility logic
    compatibility = {
        "O-": ["O-"],
        "O+": ["O-", "O+"],
        "A-": ["O-", "A-"],
        "A+": ["O-", "O+", "A-", "A+"],
        "B-": ["O-", "B-"],
        "B+": ["O-", "O+", "B-", "B+"],
        "AB-": ["O-", "A-", "B-", "AB-"],
        "AB+": ["O-", "O+", "A-", "A+", "B-", "B+", "AB-", "AB+"],
    }
    return receiver_blood_group in compatibility.get(donor_blood_group, [])

# Streamlit UI
st.title("Blood Donation")
st.header("Blood-Connect: Bridging Lives Through Blood Donation")
st.subheader("Simplifying the Connection Between Donors, Patients, and Hospitals for Lifesaving Support")


# Display Images

# import Image from pillow to open images
from PIL import Image
img = Image.open("/Users/adlnzmnzr/Downloads/blood_donate.jpeg")

# display image using streamlit
# width is used to set the width of an image
st.image(img, width=200)

initialize_tables()

menu = ["Home","Donor", "Receiver", "Hospital", "Search"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    st.subheader("About")
    # Raining Emoji 
    rain(
         emoji="🩸", 
         font_size=10,  # the size of emoji 
         falling_speed=10,  # speed of raining 
         animation_length="infinite",  # for how much time the animation will happen 
         ) 
    about='''\n\nBlood-Connect is a streamlined web-based application designed to facilitate blood donation management by connecting donors, receivers, and hospitals. With the increasing demand for efficient blood donation services, this platform simplifies the process of registering donors and receivers, while allowing hospitals to stay organized and accessible. Blood-Connect provides an easy-to-use interface for users to add, view, and manage critical data, ensuring quick and accurate access during emergencies.
            \n\nFor blood donors, the platform enables seamless registration with essential details like name, blood group, and location, allowing receivers and hospitals to identify compatible donors swiftly. Similarly, patients or their families can register themselves as receivers, making it easier to match them with available donors. Hospitals, on the other hand, can use the system to organize their blood donation campaigns, connect with donors, and schedule donations efficiently. By centralizing these features, Blood-Connect ensures that lifesaving resources are always within reach.
            \n\nThe app also includes a robust search feature that helps users find donors based on blood group and city. This is especially helpful during urgent situations when time is of the essence. Blood-Connect bridges the gap between those in need and those willing to help, fostering a community-driven approach to saving lives through blood donation. Whether you are a donor, a patient, or a hospital, Blood-Connect is here to make blood donation simple, transparent, and impactful.
            '''
    st.text(about)

elif choice == "Donor":
    donor_action = st.selectbox("Choose an action", ["Add Donor", "Donors List", "Delete Donor"])

    if donor_action == "Add Donor":
        st.subheader("Add Donor")
        with st.form("donor_form"):
            name = st.text_input("Name")
            phone_number = st.text_input("Phone Number")
            village_town = st.text_input("Village/Town")
            city = st.text_input("City")
            state = st.text_input("State")
            pin = st.text_input("PIN")
            blood_group = st.text_input("Blood Group")
            submitted = st.form_submit_button("Add Donor")
            if submitted:
                add_donor(name, phone_number, village_town, city, state, pin, blood_group)
                st.success("Donor added successfully!")

    elif donor_action == "Donors List":
        st.subheader("Donors List")
        donors = get_donors()
        st.write(donors)

    elif donor_action == "Delete Donor":
        st.subheader("Delete Donor")
        donor_id = st.text_input("Enter Donor ID")
        if st.button("Delete Donor"):
            delete_donor(donor_id)
            st.success("Donor deleted successfully!")

elif choice == "Receiver":
    receiver_action = st.selectbox("Choose an action", ["Add Receiver", "List of Receivers", "Delete Receiver"])

    if receiver_action == "Add Receiver":
        st.subheader("Add Receiver")
        with st.form("receiver_form"):
            name = st.text_input("Name")
            phone_number = st.text_input("Phone Number")
            village_town = st.text_input("Village/Town")
            city = st.text_input("City")
            state = st.text_input("State")
            pin = st.text_input("PIN")
            blood_group = st.text_input("Blood Group")
            submitted = st.form_submit_button("Add Receiver")
            if submitted:
                add_receiver(name, phone_number, village_town, city, state, pin, blood_group)
                st.success("Receiver added successfully!")

    elif receiver_action == "List of Receivers":
        st.subheader("List of Receivers")
        receivers = get_receivers()
        st.write(receivers)

    elif receiver_action == "Delete Receiver":
        st.subheader("Delete Receiver")
        receiver_id = st.text_input("Enter Receiver ID")
        if st.button("Delete Receiver"):
            delete_receiver(receiver_id)
            st.success("Receiver deleted successfully!")

elif choice == "Hospital":
    hospital_action = st.selectbox("Choose an action", ["Add Hospital","List of hopitals", "Delete Hospital"])

    if hospital_action == "Add Hospital":
        st.subheader("Add Hospital")
        with st.form("hospital_form"):
            hospital_name = st.text_input("Hospital Name")
            phone_number = st.text_input("Phone Number")
            village_town = st.text_input("Village/Town")
            city = st.text_input("City")
            state = st.text_input("State")
            pin = st.text_input("PIN")
            submitted = st.form_submit_button("Add Hospital")
            if submitted:
                add_hospital(hospital_name, phone_number, village_town, city, state, pin)
                st.success("Hospital added successfully!")

    elif hospital_action == "List of hopitals":
        st.subheader("List of hopitals")
        hospitals = get_hosptials()
        st.write(hospitals)

    elif hospital_action == "Delete Hospital":
        st.subheader("Delete Hospital")
        hospital_id = st.text_input("Enter Hospital ID")
        if st.button("Delete Hospital"):
            delete_hospital(hospital_id)
            st.success("Hospital deleted successfully!")

elif choice == "Search":
    st.subheader("Search Donors by Blood Group and City")

    # Blood group selection
    blood_group = st.selectbox("Select Blood Type", ["A+", "B+", "AB+", "O+", "A-", "B-", "AB-", "O-"])
    city = st.text_input("Enter City")

    if st.button("Search"):
        # Fetch compatible donors using the new logic
        matching_donors = search_donors_by_blood_group_and_city(blood_group, city)
        
        if matching_donors:
            st.write("Matching Donors:")
            for donor in matching_donors:
                st.write(f"Name: {donor['name']}, Blood Group: {donor['blood_group']}, City: {donor['city']}, Phone Number: {donor['phone_number']}")

            # Select donor for scheduling donation
            donor_ids = [donor['id'] for donor in matching_donors]
            selected_donor_id = st.selectbox(
                "Select Donor ID for Donation",
                donor_ids,
                format_func=lambda x: next(d for d in matching_donors if d['id'] == x)['name']
            )
  
        else:
            st.warning("No donors found for the specified criteria.")