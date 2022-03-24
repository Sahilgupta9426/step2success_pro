from typing import List
import fitz
# import pandas as pd 
import re
from PIL import Image
# import pytesseract
# import numpy as np
import boto3

imagetext=[]
textfile=[]



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


def gettext(file):
    for pageNumber,page in enumerate(file.pages(),start=1):
        for imgNumber,img in enumerate(page.get_images(),start=1):
            xref=img[0]
            pix=fitz.Pixmap(file,xref)
            if pix.n > 4:
                pix=fitz.Pixmap(fitz.csRGB,pix)
            pix.save(f'images/image_Page{pageNumber}_{imgNumber}.png')
                
            filename = f'images/image_Page{pageNumber}_{imgNumber}.png'
            documentName=filename
            text=fromimage(documentName)
                # img1 = np.array(Image.open(filename))
                # text = pytesseract.image_to_string(img1)
            text=text.lower()
            text=text
            # print(text)
            imagetext.append(text)
                # print(text)
        text2=page.get_text()
        text2=text2.lower()

        # text2=text2
        textfile.append(text2)


def gettest():
    namedate=[]
    list1=' '.join(imagetext)
    # print('list--1---------------',list1)
    list2=' '.join(textfile)
    print('list2________',list2)
    list1=list1+list2

    
    print(list1)
    # def search(n):
    #     # print(n)
    #     a=re.search(n,list1)

    #     # print(a)
    #     if a!=None:

    #         return a.group()

    # test_name=['cbc','lft','kft','iron study','thyroid profile','lipid','hba1c','know all about your health']
    # datas=list(map(search,test_name))

    def search(test_name):
        
        childlist=[]
        print(test_name)
        
        for n_list2 in test_name:
            a=re.search(n_list2,list1)
            if a!=None:
                childlist.append(a.group())
        
        return childlist
    # test_name=['cbc','lft','kft','iron study','thyroid profile','lipid','hba1c']
    test_name=[['cbc','haemoglobin','rbc count'],['lft','bilirubin','sgot','sgpt'],['kft','bun','blood urea'],['complete haemogram','tlc','pcv','rbc','mcv','mch','mchc'],
    ['absolute leucocyte count','absolue Neutrophil count','absolute monocyte count','absolute basophil count','absolute eosinphil count'],
    ['thyroid profile','t3','t4','tsh'],['iron study','iron studies','uibc','tibc']]
    datas=list(map(search,test_name))


    # datas=datas.remove(None)
    # print(datas)

    # find name and date
    name=re.search(r"(?:mr\.|mrs\.|ms\.) [a-zA-Z]+ [a-zA-Z]+",list1)
    
    # p_name=re.compile(r'patient name\s*:\s*(.*)')
    p_name=re.compile(r'patient name\s*:\s*[a-zA-Z]+ [a-zA-Z]+')
    
    p_name= p_name.search(list1)
    if name:
        # testdata['name']=name.group()
        namedate.append(name.group())
    elif p_name:
        namedate.append(p_name.group())
            
    yy = re.search(r"[\d]{1,2}/[\d]{1,2}/[\d]{2,4}", list1)
    y_y = re.search(r"[\d]{1,2}-[\d]{1,2}-[\d]{2,4}", list1)
    mmm = re.search(r"[\d]{2} [a-zA-Z]{3} [\d]{2,4}", list1)
    m_m_m = re.search(r"[\d]{2}-[a-zA-Z]{3}-[\d]{2,4}", list1)
    slash_date = re.search(r"[\d]{2}/[a-zA-Z]{3}/[\d]{2,4}", list1)
    if yy:
            
        date=yy.group()
        namedate.append(date)
    elif y_y:
            
        date=y_y.group()
        namedate.append(date)     
    elif mmm:
            
        date=mmm.group()
        namedate.append(date)
                
    elif m_m_m:
        date=m_m_m.group()
        namedate.append(date)
    elif slash_date:
        date=slash_date.group()
        namedate.append(date)
    
    # end name and date
    return datas,namedate

if __name__=="__main__":
    # file=fitz.open('jyoti.pdf')
    # file=fitz.open('lalita.pdf')
    file=fitz.open('imagetest.pdf')
    gettext(file)
    if gettext:
        print(gettest())

# print('text file',textfile)
# print('imagetext',imagetext)
