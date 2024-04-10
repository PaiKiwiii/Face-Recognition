import numpy as np
import pandas as pd
import cv2
import redis

# insight face
from insightface.app import FaceAnalysis
from sklearn.metrics import pairwise


# Connect to Redis Client
hostname = 'redis-15807.c15.us-east-1-2.ec2.cloud.redislabs.com'
portnumber = '15807'
password = '4t3qO54RKOJUrXJZUMfosvD1XwqbzPEn'

r = redis.StrictRedis(host = hostname,
                      port = portnumber,
                      password = password)

# configure face analysis
faceapp = FaceAnalysis(name = 'buffalo_sc', root = 'insightface_model',
                       providers = ['CPUExecutionProvider'])
faceapp.prepare(ctx_id = 0, det_size = (640, 640), det_thresh = 0.5)

#Retrive Data from database
def retrieve_data(name):
    retrieve_dict = r.hgetall(name)
    retrieve_series = pd.Series(retrieve_dict)
    # Get the index of the Series and convert byte strings to strings
    index = retrieve_series.index
    index = list(index)
    retrieve_series.index = index
    retrieve_df = retrieve_series.to_frame().reset_index()
    retrieve_df.columns = ['name_role', 'facial_features']
    # Decode byte strings to strings before splitting
    retrieve_df['name_role'] = retrieve_df['name_role'].apply(lambda x: x.decode())
    # Split the 'name_role' column into separate columns
    split_data = retrieve_df['name_role'].str.split('@', expand=True)
    # Ensure split_data has the correct number of columns
    if len(split_data.columns) == 5:
        retrieve_df[['First Name', 'Last Name', 'Department', 'ID Number', 'Course']] = split_data
    else:
        # If the split operation did not result in 5 columns, fill missing columns with NaN
        retrieve_df[['First Name', 'Last Name', 'Department', 'ID Number', 'Course']] = split_data.reindex(columns=[0, 1, 2, 3, 4])
    return retrieve_df[['First Name', 'Last Name', 'Department', 'ID Number', 'Course', 'facial_features']]


#ML Search Algorithm
def ml_search_algorithm(dataframe, feature_column, test_vector, name_role = ['Name', 'Role'], thresh = 0.5):
    """
    cosine similarity base search algorithm
    """
    # step-1 : take the the dataframe (collection of the data)
    dataframe = dataframe.copy()
    # step-2: Index face embedding form the dataframe and convert into array
    X_list = dataframe[feature_column].tolist()
    x = np.asarray(X_list)
    # step-3: Cal.cosine similarity 
    similar = pairwise.cosine_similarity(x, test_vector.reshape(1, -1))
    similar_arr = np.array(similar).flatten()
    dataframe['cosine'] = similar_arr
    # step-4: filter the data
    data_filter = dataframe.query(f'cosine >= {thresh}')
    if len(data_filter) > 0:
        # step-5: get the person name
        data_filter.reset_index(drop = True, inplace = True)
        argmax = data_filter['cosine'].argmax()
        person_name, person_role = data_filter.loc[argmax][name_role]
    else:
        person_name = 'Unknown'
        person_role = 'Unknown'

    return person_name, person_role

def face_prediction(test_image, dataframe, feature_column, name_role = ['Name', 'Role'], thresh = 0.5):
    # step-1: take  the test image and apply insight face
    results = faceapp.get(test_image)
    test_copy = test_image.copy()
    # step-2: use for loop and extract each embedding and pass to ml_search_algorithm
    for res in results:
        x1, y1, x2, y2 = res['bbox'].astype(int)
        embeddings = res['embedding']
        person_name, person_role = ml_search_algorithm(dataframe,
                                                       feature_column,
                                                       test_vector = embeddings,
                                                       name_role = name_role,
                                                       thresh = thresh)
        if person_name == 'Unknown':
            color = (0, 0, 255) #bgr
        else:
            color = (0, 255, 0)
            
        cv2.rectangle(test_copy, (x1, y1), (x2, y2), color)
        text_gen = person_name
        cv2.putText(test_copy,text_gen, (x1, y1), cv2.FONT_HERSHEY_DUPLEX, 0.7, color, 2)

    return test_copy
