from Home import st

st.set_page_config(page_title='Logs', layout='wide')

# Create a column layout for the RFID and Face Recognition buttons
c1, c2, c3 = st.columns([0.11, 0.2, 1])

# Button for RFID
rfid_button = c1.button("RFID")

# Selectbox for RFID
rfid_selectbox = None

# Button for Face Recognition
face_recognition_button = c3.button("Face Recognition")

# If RFID button is clicked, show the selectbox for RFID
if rfid_button:
    with st.container():
        # Create a selectbox for RFID
        rfid_selectbox = c2.selectbox("", ("Entry", "Exit"))

# If Face Recognition button is clicked, hide the selectbox
if face_recognition_button:
    rfid_selectbox = None

# Separator line
st.markdown("<hr style='margin: 2px 0;'>", unsafe_allow_html=True)

# Display the report filters if RFID button is clicked
if rfid_selectbox is not None:
    # Create two columns for the report filters
    col1, col2 = st.columns([5, 1])

    # Left column
    with col1:
        st.write("Left Column")

    # Right column
    with col2:
        # Title for the report
        st.header("Report")
        
        # Filter buttons for month, day, year, and gate
        month = st.selectbox("Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
        day = st.selectbox("Day", list(range(1, 32)))
        year = st.selectbox("Year", list(range(2000, 2023)))  # Adjust the range as needed
        gate = st.selectbox("Gate", ["Gate 1", "Gate 2", "Gate 5", "Gate 6", "Gate 9"])

        # Button to apply filters
        apply_filters = st.button("Apply Filters")
        
        

if face_recognition_button:
    # Create two columns for the report filters
    col1, col2 = st.columns([5, 1])

    # Left column
    with col1:
        st.write("Face Recognition")

    # Right column
    with col2:
        # Title for the report
        st.header("Report")
        
        # Filter buttons for month, day, year, and gate
        month = st.selectbox("Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
        day = st.selectbox("Day", list(range(1, 32)))
        year = st.selectbox("Year", list(range(2000, 2023)))  # Adjust the range as needed
        gate = st.selectbox("Gate", ["Gate 1", "Gate 2", "Gate 5", "Gate 6", "Gate 9"])

        # Button to apply filters
        apply_filters = st.button("Apply Filters")

# Hide the report filters if RFID button is clicked
if rfid_button:
    pass


#----once option is picked from the dropdown button--------
# Filter based on the selected option
selected_option = None

if selected_option:
    with st.container():
        if selected_option == "Entry":
            # Place your code for filtering data when "Entry" is clicked
            pass
        elif selected_option == "Exit":
            # Place your code for filtering data when "Exit" is clicked
            pass
