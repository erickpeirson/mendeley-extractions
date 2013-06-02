from pprint import pprint
from mendeley_client import *
import os
import sys
import time

def ol_get(list, filter):
    for x in list:
        if filter(x):
            return x
    return False

def get_selection (options, prompt):
    """options should be a dict with id and title"""
    found = False
    while not found:
        print prompt
        for opt in options:
            print str(opt['id']) + " : " + opt['title']
        choice = raw_input("Please make a selection: ")

        selected = ol_get(options, lambda x: int(x['id']) == int(choice))
        
        if selected:                                   
            found = True
            return selected
        else:
            print "Invalid selection. Please try again."      # Dipshit

class data_methods:
    def paper_keywords(self, mendeley, id):
        data = []
        papers = []
        pages = mendeley.folder_documents(id)['total_pages']
        for page in range(0, pages):
            papers += mendeley.folder_documents(id, page=page)['document_ids']
        papers_detailed = [ mendeley.document_details(paper) for paper in papers ]

        for paper in papers_detailed:
            datum = {}
            datum['uri'] = paper['mendeley_url']
            datum['id'] = paper['id']
            datum['authors'] = [ author['forename'] + " " + author['surname'] for author in paper['authors'] ]
            try:
                datum['pub_year'] = paper['year']
            except KeyError:
                datum['pub_year'] = "None"
            datum['keywords'] = paper['keywords']
            
            data.append(datum)
        return data
                
class output_methods:
    def csv(self, data, name):
        """Commas in values are removed."""
        filename = str(name) + str(time.time()) + ".csv"
        f = open(filename, "wb")
    
        f.write(','.join(key for key in data[0].keys()) + "\n")
        for datum in data:
            line_values = []
            for key, value in datum.iteritems():
                if type(value) is list:
                    line_values.append(';'.join(str(item).replace(","," ") for item in value))
                else:
                    line_values.append(str(value).replace(","," "))
            f.write(','.join(line_values) + "\n")
        
        f.close()
        return filename
        
    def tsv(self, data, name):
        """Same as CSV, except using tab-stops, and commas are permitted in values."""
        
        filename = str(name) + str(time.time()) + ".csv"
        f = open(filename, "wb")
    
        f.write('\t'.join(key for key in data[0].keys()) + "\n")
        for datum in data:
            line_values = []
            for key, value in datum.iteritems():
                if type(value) is list:
                    line_values.append(';'.join(str(item) for item in value))
                else:
                    line_values.append(str(value))
            f.write('\t'.join(line_values) + "\n")
        
        f.close()
        return filename

def interface():
    mendeley = create_client()
    
    # User selects a folder from his/her library.
    
    folders = [ { 'id': folder['id'], 'title': folder['name'], 'size': folder['size'] } for folder in mendeley.folders() ]
    selected_folder = get_selection( folders, "Please select a folder: ")

    print "Selected folder \"" + selected_folder['title'] + "\" with " + selected_folder['size'] + " records."

    # User selects data type

    data_types = [ { 
                        'id': 0,
                        'title': 'Paper-Keywords',
                        'method': 'paper_keywords'
                        } ]
                        
    selected_data = get_selection(data_types, "Please select data: ")

    # User selects output format

    output_formats = [ {
                            'id': 0,
                            'title': 'Comma-separated values (CSV)',
                            'method': 'csv'
                        },
                        {
                            'id': 1,
                            'title': 'Tab-separated values (TSV)',
                            'method': 'tsv'
                        } ]

    selected_format = get_selection(output_formats, "Please select an output format: ")

    # Execute analysis and save to disk

    print "Extracting selected data. This may take a while, depending on your internet connection and the size of the folder."
    data_method = getattr(data_methods, selected_data['method'])
    data = data_method(data_methods(), mendeley, selected_folder['id'])

    print "Writing data to disk."
    output_method = getattr(output_methods, selected_format['method'])
    out_file = output_method(output_methods(), data, selected_folder['id'])

    print selected_data['title'] + " data saved as " + selected_format['title'] + " in file: " + out_file
    #selected_format['method']()


if __name__ == '__main__':
    interface()