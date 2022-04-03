import fitz
import re
import time
from PIL import Image
import pytesseract
import numpy as np
# import boto3



list1=[] #get data only from list 1


list2=[] # to get final testdata of dictionery in list2


# def fromimage(documentName):
    # Document
    # documentName=documentName

    # # Read document content
    # with open(documentName, 'rb') as document:
    #     imageBytes = bytearray(document.read())

    # # Amazon Textract client
    # textract = boto3.client('textract')

    # # Call Amazon Textract
    # response = textract.detect_document_text(Document={'Bytes': imageBytes})

    # #print(response)
    # res=[]
    # # Print detected text
    # a=''
    # for item in response["Blocks"]:
    #     if item["BlockType"] == "LINE":
    #         # print ('\033[94m' +  item["Text"] + '\033[0m')
    #         # new=f'\033[94m' +  item["Text"] + '\033[0m'
    #         # print(new)
    #         a+=item["Text"] 
    #         # res.append(a)
    #         # print(a) 
    # return a


def pdftotext(file):
    alltext=''
    file=file
    for pageNumber,page in enumerate(file.pages(),start=1):
        text1=page.get_text()
        text=text1.lower()
        alltext+=text
    date_get=get_date(alltext)
    print(date_get)
    name=get_name(alltext)
    # print(name)
    nametotext=name_to_all_text(name,alltext)
    if nametotext==1:
        if  name and date_get:
            testresult=gettest(alltext)
            return name,date_get,testresult
        return ''
    
    elif name and date_get:
        testresult=gettest(nametotext)
        return name,date_get,testresult
    else:
        return ''
        
def imgtotxt(file):
    alltext=''
    alltext2=''
    file=file
    for pageNumber,page in enumerate(file.pages(),start=1):
        for imgNumber,img in enumerate(page.get_images(),start=1):
            xref=img[0]
            pix=fitz.Pixmap(file,xref)
            if pix.n > 4:
                pix=fitz.Pixmap(fitz.csRGB,pix)
            pix.save(f'images/image_Page{pageNumber}_{imgNumber}.png')
            filename = f'images/image_Page{pageNumber}_{imgNumber}.png'
            # documentName=filename
            # text=fromimage(documentName).
            # pytesrect
            img1 = np.array(Image.open(filename))
            text = pytesseract.image_to_string(img1)
            # end pyt
            text=text.lower()
            alltext2+=text
            
    alltext+=alltext2
    print('__________________________',alltext)
    # print(alltext)
    date_get=get_date(alltext)
    print(date_get)
    name=get_name(alltext)
    print(name)
    nametotext=name_to_all_text(name,alltext)#GET NAME TO END OF REPORT TEXTS
    if nametotext==1:
        if name and date_get:
            testresult=gettest(alltext)
            return name,date_get,testresult
        return ''
    testresult=gettest(nametotext)
    return name,date_get,testresult

def name_to_all_text(name,alltext):
    endofreport=re.search(r'end of report',alltext)
    if endofreport:
        nametoend=re.compile(rf'({name})(.*?|\n)*(end of report)')
        nametoend=nametoend.search(alltext)
        print(nametoend)
        
        return nametoend.group()
    elif alltext:
        return 1
    return ''

def get_date(alltext):
    text=alltext
 
    
            
    yy = re.search(r"[\d]{1,2}/[\d]{1,2}/[\d]{2,4}", text)
    y_y = re.search(r"[\d]{1,2}-[\d]{1,2}-[\d]{2,4}", text)
    mmm = re.search(r"[\d]{2} [a-zA-Z]{3} [\d]{2,4}", text)
    m_m_m = re.search(r"[\d]{2}-[a-zA-Z]{3}-[\d]{2,4}", text)
    slash_date = re.search(r"[\d]{2}/[a-zA-Z]{3}/[\d]{2,4}", text)
    if yy:
            
        date=yy.group()
        return date
    elif y_y:
            
        date=y_y.group()
        return date   
    elif mmm:
            
        date=mmm.group()
        return date
                
    elif m_m_m:
        date=m_m_m.group()
        return date
    elif slash_date:
        date=slash_date.group()
        return date
    return ''

def get_name(text):
    name=re.search(r"(?:mr\.|mrs\.|ms\.) [a-zA-Z]+ [a-zA-Z]+",text)
    
    # p_name=re.compile(r'patient name\s*:\s*(.*)')
    p_name=re.compile(r'patient name\s*:\s*[a-zA-Z]+ [a-zA-Z]+')
    
    p_name= p_name.search(text)
    if name:
        
        
        return name.group()
    elif p_name:
        
        return p_name.group()
    return ''

def gettest(text):
    def sub_search(test_name):
        # print(test_name)
        a=re.search(test_name,text)
        if a is not None:

            return a.group()
    test_name=['cbc','lft','kft','iron study','thyroid profile','lipid','hba1c']
    
    datas=list(map(sub_search,test_name))#for search function



    # get test value
    
    test_name=[['mch','rbc count','platelet count','meditest full body checkup panel','tlc (total leucocyte count)'],
    ['bilirubin, total','sgot','sgpt'],['blood urea'],['hba1c'],['vitamin b12']]
    
    
    def test_value(datas):
        def sub_test_value(datas):
    
            # a=re.compile(fr'{datas} ^\d*[.,]?\d*$ ')
            
            
            
            # t_value1=re.compile(rf'{(datas)}\s*\n\s*[a-zA-Z]?\d*[0-9]*[.]?[0-9]*')
            
            # t_value2=re.compile(rf'{datas}\s*\n\d*[0-9]*[.,]?[0-9]*')
            print(datas)

            # t_value1=re.compile(rf'(?={datas})(.*?|\n)*(\d*[0-9]*[.]?[0-9])')
            t_value1=re.compile(rf'({datas})(.*?|\n)*(\d*[0-9]*[.]?[0-9])')
            t_value1=t_value1.search(text)
            
           
            if t_value1 is not None:
                print(t_value1.group())
                return t_value1.group() 
                
           
        subtestvalue=list(map(sub_test_value,datas))
        return subtestvalue



    testvalue=list(map(test_value,test_name))
    # print('test_value',testvalue)
    # end test value
    return datas, testvalue


if __name__ == "__main__":
    start_time = time.time()
    # file=fitz.open('share_preview2.pdf')
    # file=fitz.open('c676422960523ad28beb131038335370.pdf')
    
    file=fitz.open('lalita.pdf')
    # file=fitz.open('prem.pdf')
    # file=fitz.open('imagetest.pdf')
    # file=fitz.open('ajax.pdf')
    # file=fitz.open('jyoti.pdf')
    # file wil go in pdftotext
    p2t_value=pdftotext(file)# get value from pdftotext.either it will have text or empty value
    print('pdftotext',p2t_value)
    
    if not p2t_value:# it will send imgtotxt function, if pdftotext do not get value
        img2t_value=imgtotxt(file)#get text from imgtotxt
        print(img2t_value)
        if not img2t_value:# if img2t_value also get empty it will show no 'no data in pdf'
            print('no data in pdf')

print("--- %s seconds ---" % (time.time() - start_time))
