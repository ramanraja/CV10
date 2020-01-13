# create an image collection with multiple images for each person 
# tutorial redacted from:
# https://towardsdatascience.com/building-k-pop-idol-identifier-with-amazon-rekognition-92302442d763

# pip install pillow

import io
import os
import sys
import csv
import boto3
 
  
print ('Usage: python indexer.py  root_folder_name, [collection_name]')
   
with open ('../../credentials/aws.csv' ,'r') as f:
    next(f)  # skip the header row
    reader = csv.reader(f)
    for line in reader:
        #print(line)
        key = line[1]    # first column is user name, skip it
        secret = line[2]
        region = line[3]
          
client = boto3.client('rekognition', aws_access_key_id = key, aws_secret_access_key = secret, region_name = region)
#print (type(client))

# Traverse the directory tree and read face sample files 
# Each file name is of the form:  PersonName_xxxxx.jpg
# Assumption: there are no other files in the folders, except the images

root_path = 'images'
if len(sys.argv) > 1 :
    root_path = sys.argv[1] 
print ("Image files root directory: ", root_path) 

collection_id = 'face_collection'
# Before proceeding: you must have already invoked create_collection.py with the above collecion ID
if len(sys.argv) > 2 :
    collection_id = sys.argv[2] 
print ("Collection ID: ", collection_id) 

for root, dirs, files in os.walk(root_path):
    for file_name in files:
        full_name = os.path.join(root, file_name)
        print (full_name)
        img_id = file_name.split('_')[0]
        print ("Image id: ", img_id, '\n')
        with open(full_name, 'rb') as img:
            bytes = img.read()
            jimage = {"Bytes": bytes}
        response = client.index_faces (Image=jimage, ExternalImageId=img_id, CollectionId=collection_id)
        print(response)
        print('-'*25)
        
print('\n') 
print('='*40)        
print ('Collection ID : ', collection_id)
response = client.describe_collection(CollectionId=collection_id)
print(response)
 





