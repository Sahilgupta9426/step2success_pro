
import boto3


def fromimage(documentName):
    # Document
    documentName=documentName

    # Read document content
    with open(documentName, 'rb') as document:
        imageBytes = bytearray(document.read())

    # Amazon Textract client
    textract = boto3.client('textract')

    # Call Amazon Textract
    response = textract.detect_document_text(Document={'Bytes': imageBytes})

    #print(response)
    res=[]
    # Print detected text
    a=''
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            # print ('\033[94m' +  item["Text"] + '\033[0m')
            # new=f'\033[94m' +  item["Text"] + '\033[0m'
            # print(new)
            a+=item["Text"] 
            # res.append(a)
            # print(a) 
    return a
if __name__ == "__main__":
    documentName = "images/image_Page1_1.png"

    r=fromimage(documentName)
    print(r)
    # listToStr = ' '.join([str(elem) for elem in r])
    
    # print(listToStr) 