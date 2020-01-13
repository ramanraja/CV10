# face recognition in a group photo - tutorial redacted from:
# https://towardsdatascience.com/building-k-pop-idol-identifier-with-amazon-rekognition-92302442d763

# pip install pillow

import io
import sys
import csv
import boto3
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont 
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
  
print ('Usage: python recognizer.py  test_file_name, [collection_name]')
  
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

# read target file to be searched for a known face
file_name = 'pop_group.jpg'
if len(sys.argv) > 1 :
    file_name = sys.argv[1] 
print ("Input file: ", file_name) 

collection_id = 'face_collection1'
if len(sys.argv) > 2 :
    collection_id = sys.argv[2] 
print ("Face collection name: ", collection_id) 
   
img = Image.open (file_name)    
imgdraw = ImageDraw.Draw(img)  # we will need these later to render it
font = ImageFont.truetype('fonts/Arial.ttf', 15)

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

print ('Detecting all faces in the image...')
response = client.detect_faces (Image=jimage) #  ,Attributes=['ALL']) is not needed
#print(response)
faces = response['FaceDetails']
print('Number of faces found: ', len(faces), '\n')
#print (faces)
#print('-'*20)

# cut out each face rectangle, and try if the face has a match in the collection
for face in faces:
    face_box = to_world_coords (img.size, face['BoundingBox'])
    # Image.crop takes a single tuple as parameter
    face_crop = img.crop ((face_box['TL'][0],face_box['TL'][1], face_box['BR'][0],face_box['BR'][1]))
    stream = io.BytesIO()
    face_crop.save(stream, format="JPEG") 
    bytes = stream.getvalue()
    jimage = {"Bytes": bytes}
    # match each face with our collection
    response = client.search_faces_by_image (CollectionId = collection_id, Image=jimage)
    matches = response['FaceMatches']
    # matches is an array of all matches found, ordered by similarity score
    if len(matches) > 0:
        print ('\n>>>>>> MATCH FOUND ! <<<<<<')
        #print(matches)
        name = matches[0]['Face']['ExternalImageId']
        print ('The face belongs to: ', name)
        print ('Similarity: ', matches[0]['Similarity']) 
        print ('Confidence: ', matches[0]['Face']['Confidence'], ' %\n') 
        # close the path with top left point again
        points = (face_box['TL'], face_box['TR'], face_box['BR'], face_box['BL'], face_box['TL'])  
        imgdraw.line(points, fill='#d40000', width=2)      
        imgdraw.text((face_box['BL'][0]+2,face_box['BL'][1]+2), name, font=font, fill=(255,255,255))
        imgdraw.text((face_box['BL'][0]+1,face_box['BL'][1]+1), name, font=font, fill=(255,255,255))  
        imgdraw.text(face_box['BL'], name, font=font, fill=(200,0,0))
    print (response)
    print('-'*30)

img.show() 
 


