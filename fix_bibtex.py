# -*- coding: utf-8 -*-
__version__ = '0.252'

'''
This is a program to modify bibtext files. Where there are entries for both the DOI and URL, then the
URL field is removed. If there is just only entry, or none then the entry is left untouched.

Version History:
2019.07.03 - First version created.
'''

def find_all(haystack, needle):   
    import re
    return[m.start() for m in re.finditer(needle, haystack)]
    
    
input_file_name='C:\\Users\\re\\Dropbox\\Cologne University\\Thesis\\resources\\library.bib'
#input_file_name='C:\\Users\\re\\Dropbox\\Cologne University\\Thesis\\resources\\all_documents.bib'


output_file_name='C:\\Users\\re\\Dropbox\\Cologne University\\Thesis\\resources\\library_fixed.bib'

with open(input_file_name, 'r', encoding="utf-8") as in_file:
    content=in_file.read()

entry_indexes=find_all(content, '\n@') #find the positions of each entry

fixed_entries=content[0:entry_indexes[0]] #keep the original file header before the entries start

num_indexes=len(entry_indexes) #get the number of entries

identifier_list=[]
duplicate_ids=[]
duplicate_entries=''
no_ids=[]
no_id_entries=''


for entry_number in range(0,num_indexes-1):

    entry_start=entry_indexes[entry_number] #get the start position for this entry
    
    if entry_start == num_indexes-1: #if we have the last entry, then use the end of the file
        entry_end = len(content)-1   #as the end of the entry
    else:
        entry_end=entry_indexes[entry_number+1] #otherwise use the start position of the next entry
                                                #as the end position
    
    this_entry=content[entry_start:entry_end] #get the text from the section for this entry
    
    identifier=this_entry[this_entry.find('{')+1 : this_entry.find(',')] #get the reference name 
                                                                         #for this entry (for display
                                                                         #purposes only)
    identifier=identifier.lower()
    print('\n Processing ' + identifier)
    
    #if identifier == 'engineeringtoolboxammonia':
    #    import pdb; pdb.set_trace()
        
    #if 'mauky2016' in identifier:
    #    import pdb; pdb.set_trace()
    
    skip_entry=False
    dont_change=False
    doi_present=True
    url_present=True
    
    #import pdb; pdb.set_trace()
    
    if len(identifier)==0:
        skip_entry=True
        print('\tWARNING: ENTRY WITH NO ID!')
        no_ids.append(identifier)
        no_id_entries=no_id_entries+this_entry
    
    #import pdb; pdb.set_trace()
        
    if identifier not in identifier_list: #check if this identifier is new
        identifier_list.append(identifier)
    
    else:
        skip_entry=True
        print('\tWARNING: DUPLICATE ENTRY!')
        duplicate_ids.append(identifier)
        duplicate_entries=duplicate_entries+this_entry
    #import pdb; pdb.set_trace()
    
    
    if 'doi = ' not in this_entry: #is the doi element missing? If so, don't change the entry
        dont_change=True
        doi_present=False
        print('No DOI.')
        
    #import pdb; pdb.set_trace()
            
    if 'url = ' not in this_entry: #if there a url element missing? If so, don't change the entry
        dont_change=True
        url_present=False
        print('No url.')

        

    if url_present==True and doi_present==False: #then we will insert the URL, so we should fix it.
        #import pdb; pdb.set_trace()
        this_entry_lines=this_entry.split('\n')
        new_entry=[] #start a new entry to copy what we want into
        
        for line in this_entry_lines:
        
            if 'url = ' in line: #check each line and if it doesn't have the url then copy
                                     #it to the new entry.
                #import pdb; pdb.set_trace()
                line=line.replace('{\\_}', '_')
                new_entry.append(line)
            else:
                new_entry.append(line)
                
        this_entry='\n'.join(new_entry) #join the entry back together and overwrite this_entry
                                        #with the modified entry.
        print('URL Deleted.')
    
    #import pdb; pdb.set_trace()
    
    if dont_change == False:
        this_entry_lines=this_entry.split('\n') #then split the entry by lines
        
        new_entry=[] #start a new entry to copy what we want into
        
        for line in this_entry_lines:
        
            if 'url = ' not in line: #check each line and if it doesn't have the url then copy
                                     #it to the new entry.
                new_entry.append(line)
                
        this_entry='\n'.join(new_entry) #join the entry back together and overwrite this_entry
                                        #with the modified entry.
        print('URL Deleted.')
    #import pdb; pdb.set_trace()
    
    if skip_entry==False:
        fixed_entries=fixed_entries+this_entry #add this entry to the output
    
#write out to a file
with open(output_file_name, 'w', encoding="utf-8") as out_file:
    out_file.write(fixed_entries)

import codecs
file = codecs.open(output_file_name, "w", "utf-8")
file.write(fixed_entries)
file.close()


file = codecs.open('duplicates.txt', "w", "utf-8")
file.write(duplicate_entries)
file.close()
    
file = codecs.open('no_ids.txt', "w", "utf-8")
file.write(no_id_entries)
file.close()
print('Done.\n\n')


print('Duplicate Entries:')
for entry in duplicate_ids:
    print(entry)