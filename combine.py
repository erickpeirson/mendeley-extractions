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
        
#pickle.dump(data, open('./combined_data.pkl', 'wb'))

sif_file = open('./data/combined_data.sif', 'wb')
node_type_file = open('./data/node_type.noa', 'wb')
node_type_file.write("node_type\n")
edge_year_file = open('./data/edge_year.eda', 'wb')
for datum in data:
    for author in datum['authors']:
        node_type_file.write(author.encode("ascii", "ignore").replace(" ","_") + " = person\n")
        for keyword in datum['keywords']:
            node_type_file.write(keyword.encode("ascii", "ignore").replace(" ","_") + " = keyword\n")
            sif_file.write( author.encode("ascii", "ignore").replace(" ","_") + " uses " + keyword.encode("ascii", "ignore").replace(" ","_") + "\n")
            edge_year_file.write(author.encode("ascii", "ignore").replace(" ","_") + " (uses) " + keyword.encode("ascii", "ignore").replace(" ","_") + " = "+ datum['pub_year'] + "\n")


 
documents = [[keyword.encode("ascii", "ignore") for keyword in datum['keywords']] for datum in data ]
doc_file = open('./data/documents.pkl', 'wb')
pickle.dump(documents, doc_file)