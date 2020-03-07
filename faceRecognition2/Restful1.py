# basice test of AWS lambda and custom headers

import requests
import json
import time
import sys

# This lambda simply echoes the event object:
url = 'https://xxxxxxxx.execute-api.us-east-2.amazonaws.com/default/face_lambda1'


jdata =   { "Bytes":"Thease are the image bytes" }
jheader = { 
             "content-type":"application/json",
             "x-my-custom-header":"my-own-custom-value"
          }
#  "content-type":"application/x-www-form-urlencoded"

try:
    response = requests.post(url, json=jdata, headers=jheader)
    code = response.status_code
    print ("\nResult code: ", code)
    if (code >= 200 and code < 300):
        print ("\nresponse.headers :\n")
        print (response.headers)
        print ("\nresponse.text:\n")
        print (response.text)
        print('-'*30)
        jresponse = json.loads(response.text)
        print('Version:')
        print (jresponse['version'])
        print('Path:')
        print (jresponse['path'])
        print ("Body:")
        print (jresponse['body'])
        print ("Body type:")
        print (type(jresponse['body']))
        print ("isBase64Encoded:")
        print (jresponse['isBase64Encoded'])
        jbody =  json.loads(jresponse['body'])
        print ("jbody['Bytes']:")  
        print (jbody['Bytes'])
        # Request headers received by the lambda in the event object :
        jheaders = jresponse['headers']  # this is already converted to json in the above step
        print ('\nContent type sent in the REQUEST:')
        print (jheaders['Content-Type'])
        if 'x-my-custom-header' in jheaders:
            print ('Custom header:')
            print (jheaders['x-my-custom-header'])
        else:
            print ("Custom header 'x-my-custom-header' not found")
        print('-'*30)
        print ('Request headers:')
        print (jresponse)
    else:
        print('HTTP ERROR !')
except Exception as e:
    print('Exception occured:')
    print (e)    
print ("\nBye !")

''' ----------------------------------------------------------------------------
The response.text is as follows:
{
  "version": 2, 
  "path": "/default/face_lambda1",
   ....... 
  "body":  "{\"Bytes\": \"Thease are the image bytes\"}", 
  "isBase64Encoded": false
 }

'''