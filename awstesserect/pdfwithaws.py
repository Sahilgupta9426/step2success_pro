
import fitz
import re
import time
from PIL import Image
# import pytesseract
import numpy as np
import boto3
# from aws import fromimage
list1=[] #get data only from list 1

# for test by default value

# end test by default value
list2=[] # to get final testdata of dictionery in list2

def pdftotext(file):
    file=file
    for pageNumber,page in enumerate(file.pages(),start=1):
        text1=page.get_text()
        text=text1.lower()
        ret=test(text)
        
    if not list1:
        print('list1',list1)
        return ''
    else:   
        return list1 ,set(list2)


def imgtotxt(file):
    file=file
    
    for pageNumber,page in enumerate(file.pages(),start=1):

        for imgNumber,img in enumerate(page.get_images(),start=1):
            xref=img[0]
            pix=fitz.Pixmap(file,xref)
            if pix.n > 4:
                pix=fitz.Pixmap(fitz.csRGB,pix)
                
                
                
            pix.save(f'images/image_Page{pageNumber}_{imgNumber}.png')
            
            
            documentName = f'images/image_Page{pageNumber}_{imgNumber}.png'
            # img1 = np.array(Image.open(filename))
            # text = pytesseract.image_to_string(img1)
            # text=text.lower()
            # print(text)
            # test(text)
            



            text = fromimage(documentName)
             
            text=text.lower()
            print(text)
            test(text)
    if not list1 and not list2:
        return ''
    else:
        return set(list1),set(list2)

def test(text):
    
    if text:
        if 'vitamin d' in text:
            list2.append('vitamin_d')
        
            
            # get test
        #for cbc test
        if 'cbc' in text or 'complete blood count'  in text:
                
            print('the cbc value True')
            # testdata['cbc']=True
            list2.append('cbc')

            
            #end cbc test
            
            #for urine test

        if 'urine' in text: 
            print('the urine value True')
            # testdata['urine']=True
            list2.append('urine')
            
            #end urine test

            #for Haemoglobin test
        if 'hba1c' in text or 'glycated hemoglobin'  in text:
                
            print('the lft value True')
        # testdata['lft']=True
            list2.append('hba1c')
            
            #end Haemoglobin test
        # bllod sugar
        if 'blood sugar' in text:
            list2.append('blood_sugar')
        #end blood sugar
        # absolute leucocyte count
        if 'absolute leucocyte count' in text:
            list2.append('alc')
        #absolute leucocyte count 
            #for LFT test
        if 'liver function test' in text or 'lft'  in text:
                
            print('the lft value True')
            # testdata['lft']=True
            list2.append('lft')
            
            #end LFT test
            
            #for KFT test
        if 'kidney function test' in text or 'renal function test' in text or 'kft' in text or 'rft' in text:
                
            print('the kft value True')
            # testdata['kft']=True
            list2.append('kft')
            
            #end KFT test
            
            #for Iron  test
        if 'iron studies' in text or 'iron study' in text:
            list2.append('iron_study')    
            print('the Iron value True')
            # testdata['iron_study']=True

            
            #end Iron test
            
            #for Lipid test
        if 'lipid' in text:
                
            print('the lipid value True')
            # testdata['lipid']=True
            list2.append('lipid')
            
            #end Lipid test
            
        if 'thyroid profile' in text:
                
            # testdata['thyroid_profile']=True
            list2.append('thyroid profile')

            
            # end test
        
    else:
        
        print('empty data or something wrong')
    
    
    
    name=re.search(r"(?:mr\.|mrs\.|ms\.) [a-zA-Z]+ [a-zA-Z]+",text)
    
    # p_name=re.compile(r'patient name\s*:\s*(.*)')
    p_name=re.compile(r'patient name\s*:\s*[a-zA-Z]+ [a-zA-Z]+')
    
    p_name= p_name.search(text)
    if name:
        # testdata['name']=name.group()
        list1.append(name.group())
    elif p_name:
        list1.append(p_name.group())
            
    yy = re.search(r"[\d]{1,2}/[\d]{1,2}/[\d]{2,4}", text)
    y_y = re.search(r"[\d]{1,2}-[\d]{1,2}-[\d]{2,4}", text)
    mmm = re.search(r"[\d]{2} [a-zA-Z]{3} [\d]{2,4}", text)
    m_m_m = re.search(r"[\d]{2}-[a-zA-Z]{3}-[\d]{2,4}", text)
    slash_date = re.search(r"[\d]{2}/[a-zA-Z]{3}/[\d]{2,4}", text)
    if yy:
            
        date=yy.group()
        list1.append(date)
    elif y_y:
            
        date=yy.group()
        list1.append(date)     
    elif mmm:
            
        date=yy.group()
        list1.append(date)
                
    elif m_m_m:
        date=yy.group()
        list1.append(date)
    elif slash_date:
        date=slash_date.group()
        list1.append(date)
    

    
    return 1


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
    start_time = time.time()
    # file=fitz.open('share_preview2.pdf')
    # file=fitz.open('c676422960523ad28beb131038335370.pdf')
    
    # file=fitz.open('lalita.pdf')
    # file=fitz.open('prem.pdf')
    # file=fitz.open('imagetest.pdf')
    file=fitz.open('jyoti.pdf')
    # file wil go in pdftotext
    p2t_value=pdftotext(file)# get value from pdftotext.either it will have text or empty value
    print('pdftotext',p2t_value)
    
    if not p2t_value:# it will send imgtotxt function, if pdftotext do not get value
        img2t_value=imgtotxt(file)#get text from imgtotxt
        print(img2t_value)
        if not img2t_value:# if img2t_value also get empty it will show no 'no data in pdf'
            print('no data in pdf')

print("--- %s seconds ---" % (time.time() - start_time))
