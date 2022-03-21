
# import re


# my_list = ['Jack', 'Mack', 'Jay', 'Mark']
# a=[]
# a.append("hello my name is hack fack")
# a.append("hello my name is fack")
# i=0
# print(a)



#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3

def detect_text(photo, ):
    image=open(photo,'rb')
    client = boto3.client('rekognition',aws_access_key_id="AKIAUW2ODFNIMRNUGSX2",aws_secret_access_key="3Wtf0x7LuB+0+4wxYNj1mjsWQDJec+YMre7MPcGu",region_name='ap-south-1')

    response=client.detect_text(Image={'Bytes': image.read()})
                        
    textDetections=response['TextDetections']
    print(textDetections)
    print ('Detected text\n----------')
    for text in textDetections:
            print ('Detected text:' + text['DetectedText'])
            print ('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
            print ('Id: {}'.format(text['Id']))
            if 'ParentId' in text:
                print ('Parent Id: {}'.format(text['ParentId']))
            print ('Type:' + text['Type'])
            print()
    return len(textDetections)

def main():

    # bucket='bucket'
    # photo='image_Page5_1.png'
    photo='text.png'
    text_count=detect_text(photo)
    print("Text detected: " + str(text_count))


if __name__ == "__main__":
    main()