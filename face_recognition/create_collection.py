# create a new image collection  
# tutorial redacted from:
# https://towardsdatascience.com/building-k-pop-idol-identifier-with-amazon-rekognition-92302442d763

# pip install pillow

import io
import sys
import csv
import boto3

if len(sys.argv) < 2:  # the first argv is the program name
    print ("Usage: python  create_collection.py  COLLECTION_NAME")
    sys.exit(0)
    
collection_id = sys.argv[1] 
print ("new collection name: " +collection_id) 
 
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

# execute this block only once to create a new collection:
print ('Creating collection...')
try:
    response = client.create_collection (CollectionId=collection_id)
except Exception as e:
    print ('Error: cannot create the new collection')
    print(e)
    sys.exit(1)
    
print(response)

# verify if an empty collection is there
print ('\nCollection ID : ', collection_id)
response = client.describe_collection(CollectionId=collection_id)
print(response)
print ('\nCollection successfully created.') 
