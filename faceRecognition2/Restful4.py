# Uploads an image file to AWS Rekognition lambda
# Collection name is sent in a custom header
# https://docs.aws.amazon.com/rekognition/latest/dg/API_SearchFacesByImage.html

import requests
import base64
import json
import time
import sys

# read target file to be searched for a known face
file_name = 'kamal3.png'
collection_id = 'face_collection3'

if (len(sys.argv) > 1):
    file_name = sys.argv[1]
print ("Input file: ", file_name) 
if (len(sys.argv) > 2):
    collection_id = sys.argv[2]
print ("Model collection ID: ", collection_id) 

with open(file_name, 'rb') as img:
    raw_img = img.read()
    b64_img = base64.b64encode(raw_img)
    print(type(raw_img))
    print(len(raw_img))
    print(type(b64_img))
    print(len(b64_img))
 
# Both the following approaches work, provided you set the content type correspondingly 
payload = raw_img 
#payload = b64_img
 
url = 'https://xxxxxxxx.execute-api.us-east-2.amazonaws.com/default/face_lambda4'
#jheader = {"content-type":"text/plain"}        # this works for b64 encoded image 
#jheader = {"content-type":"application/json"}  # this also works for b64 encoded image
#jheader = {"content-type":"application/x-www-form-urlencoded"} # this works for raw image only
#jheader = {"content-type":"application/octet-stream"} # this also works for raw image  
#jheader = {"content-type":"image/png"} # this also works for raw images, even for jpg files ! 
#jheader = {"content-type":"image/jpg"} # this also works for raw images, even for png files ! 

jheader = {"content-type":"application/octet-stream", "x-collection-id":collection_id}
print (jheader)

try:
    print('About to post to lambda...')
    response = requests.post(url, data=payload, headers=jheader)
    print('Posted to lambda.')
    code = response.status_code
    print (code)
    if (code >= 200 and code < 300):
        print (response.headers)
        print (response.text)    
    else:
        print ("HTTP error! code: ", code)  
except Exception as e:
    print (e)    
print ("\nBye !")

'''---------------------------------------------------------------------------------------------------
https://aws.amazon.com/blogs/developer/handling-arbitrary-http-requests-in-amazon-api-gateway/
https://www.youtube.com/watch?v=ETb2eVJs5UE   ***
https://medium.com/swlh/upload-binary-files-to-s3-using-aws-api-gateway-with-aws-lambda-2b4ba8c70b8e

curl https://xxxxxxxx.execute-api.us-east-2.amazonaws.com/default/face_lambda2

curl --data-binary "@one_pixel.jpg" https://xxxxxxxx.execute-api.us-east-2.amazonaws.com/default/face_lambda3

This fails:
response = client.search_faces_by_image (CollectionId=collection_id, Image={"Bytes":event['body']}) 

This works:
response = client.search_faces_by_image (CollectionId=collection_id, 
                                        Image = {"S3Object": { 
         				"Bucket": "image1-bucket",
         				"Name": "kamal1.jpg"
         				}}) 
NOTE: In S3 bucket, select the image file and click actions/make public.
Otherwise access permission will not be given to the lambda.
'''