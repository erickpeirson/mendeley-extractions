import os
import os.path
import pickle
from pprint import pprint

data = []
for file in os.listdir("."):
    if file.endswith('.data_pkl'):
        file_path = os.path.join('.',file)
        loaded = pickle.load(open(file_path, 'rb'))
        data += loaded
        
pickle.dump(data, open('./combined_data.pkl', 'wb'))