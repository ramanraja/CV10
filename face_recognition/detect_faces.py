# face detection
# https://towardsdatascience.com/building-k-pop-idol-identifier-with-amazon-rekognition-92302442d763

# pip install pillow

import io
import sys
import csv
import boto3
from PIL import Image
from PIL import ImageDraw

#------------------------------------------------------------------------------------
'''
 converts face bounding boxes found by rekognition into world coordinates
 input: 
    img_size: tuple; overall size of the image in the order (width, height)
    box: dictionary; bounding box given by rekognition:  
    its entries are 'Left', 'Top', 'Width', 'Height' in relative coordinates
 return value: 
    dictionary; 'TL', 'TR', 'BR', 'BL' in world coordinates
'''
def to_world_coords (img_size, box):
    # the bounding box units from rekognition are: fractions of the overall image size
    world_box = {'TL':0, 'TR':0, 'BR':0, 'BL':0}
    total_width, total_height = img_size
    left   = total_width  * box['Left']
    top    = total_height * box['Top']
    width  = total_width  * box['Width']
    height = total_height * box['Height']
    world_box['TL'] = (left, top)
    world_box['TR'] = (left+width, top)
    world_box['BR'] = (left+width, top+height)
    world_box['BL'] = (left, top+height)
    return world_box
#------------------------------------------------------------------------------------   

print ('Usage: python detect_faces.py  image_file_name') 

with open ('../../credentials/aws.csv' ,'r') as f:
    next(f)  # skip the header row
    reader = csv.reader(f)
    for line in reader:
        #print(line)
        key = line[1]    # first column is user name, skip it
        secret = line[2]
        region = line[3]
          
# file from local storage
file_name = 'pop_group.jpg'   
if len(sys.argv) > 1 :
    file_name = sys.argv[1] 
print ("Input file: " +file_name) 
   
img = Image.open (file_name)    
stream = io.BytesIO()
img.save(stream, format="JPEG")
bytes = stream.getvalue()
jimage = {"Bytes": bytes}

'''
Aliter:
with open(file_name, 'rb') as img:
    bytes = img.read()
    jimage = {"Bytes": bytes}
'''

# Ensure that the S3 bucket is in the same region where you are creating your rekognition client ***
client = boto3.client('rekognition', aws_access_key_id = key, aws_secret_access_key = secret, region_name = region)
#print (type(client))

response = client.detect_faces(Image=jimage, Attributes=['ALL'])
#print(response)

faces = response['FaceDetails']
print('Number of faces found: ', len(faces))
print (faces)

# draw a box around every face
for face in faces:
    face_box = to_world_coords (img.size, face['BoundingBox'])
    # close the path with top left point again
    points = (face_box['TL'], face_box['TR'], face_box['BR'], face_box['BL'], face_box['TL'])  
    imgdraw = ImageDraw.Draw(img)
    imgdraw.line(points, fill='#00d400', width=3)

img.show() 