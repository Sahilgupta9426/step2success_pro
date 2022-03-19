
import fitz
import re
import time
from PIL import Image
import pytesseract
import numpy as np
import glob
import os
import math, random
import shutil

list1=[] #get data only from list 1
testdata={}#for Patient test details in pair of key and value
# for test by default value
testdata={'cbc':False,'urine':False,'lft':False,'kft':False,'iron_study':False,'lipid':False,'thyroid_profile':False,'date':'','name':''}
# end test by default value
list2=[] # to get final testdata of dictionery in list2

def pdftotext(file):
    file=file
    for pageNumber,page in enumerate(file.pages(),start=1):
        text1=page.get_text()
        text=text1.lower()
        if text:
            # print(text)
            
            # print('empty text1',text)
            if not list1 :
                list1.append(text)
            
                # get test
            #for cbc test
            if 'cbc' in text or 'complete blood count'  in text:
                
                print('the cbc value True')
                testdata['cbc']=True
            
            #end cbc test
            
            #for urine test

            if 'urine' in text: 
                print('the urine value True')
                testdata['urine']=True
            
            #end urine test

            #for Haemoglobin test
            
            
            #end Haemoglobin test

            #for LFT test
            if 'liver function test' in text or 'lft'  in text:
                
                print('the lft value True')
                testdata['lft']=True
            
            #end LFT test
            
            #for KFT test
            if 'kidney function test' in text or 'renal function test' in text or 'kft' in text or 'rft' in text:
                
                print('the kft value True')
                testdata['kft']=True
            
            #end KFT test
            
            #for Iron  test
            if 'iron studies' in text or 'iron study' in text:
                
                print('the Iron value True')
                testdata['iron_study']=True
            
            #end Iron test
            
            #for Lipid test
            if 'lipid' in text:
                
                print('the lipid value True')
                testdata['lipid']=True
            
            #end Lipid test
            
            if 'thyroid profile' in text:
                
                testdata['thyroid_profile']=True

            
            # end test
            list2.append([testdata])
        else:
            list2.append([])
            print('empty data or something wrong')
    
    
    if text:
        name=re.search(r"(?:mr\.|mrs\.|ms\.) [a-zA-Z]+ [a-zA-Z]+",text)
        print(name.group())
        
        if name:
            testdata['name']=name.group()
        # in order to get date
        for l1 in list1:
            # print(l1)
            l1=l1
        yy = re.search(r"[\d]{1,2}/[\d]{1,2}/[\d]{2,4}", l1)
        y_y = re.search(r"[\d]{1,2}-[\d]{1,2}-[\d]{2,4}", l1)
        mmm = re.search(r"[\d]{2} [a-zA-Z]{3} [\d]{2,4}", l1)
        m_m_m = re.search(r"[\d]{2}-[a-zA-Z]{3}-[\d]{2,4}", l1)

        if yy:
            
            testdata['date']=yy.group()
        elif y_y:
            
            testdata['date']=y_y.group()      
        elif mmm:
            
            testdata['date']=mmm.group()
                
        elif m_m_m:
            testdata['date']=m_m_m.group()
    else:
        print('something is wrong with')

    return list2[-1]



def imgtotxt(file):
    file=file
    # random
    
    string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    randomfile = ""
    
    length = 6
    for i in range(6) :
        randomfile += string[math.floor(random.random() * length)]
    print(randomfile)
    # random end
    # create folder
    # Directory
    directory = randomfile
    
    # Parent Directory path
    parent_dir = "images/"
    
    # Path
    path = os.path.join(parent_dir, directory)
    
    # Create the directory
    # 'GeeksForGeeks' in
    # '/home / User / Documents'
    os.mkdir(path)
    # create folder end
    for pageNumber,page in enumerate(file.pages(),start=1):

        for imgNumber,img in enumerate(page.get_images(),start=1):
            xref=img[0]
            pix=fitz.Pixmap(file,xref)
            if pix.n > 4:
                pix=fitz.Pixmap(fitz.csRGB,pix)
                
                
                
            pix.save(f'images/{randomfile}/image_Page{pageNumber}_{imgNumber}.png')
            
            
            filename = f'images/{randomfile}/image_Page{pageNumber}_{imgNumber}.png'
            img1 = np.array(Image.open(filename))
            text = pytesseract.image_to_string(img1)
            text=text.lower()
            if text:
                # print(text)
                
                # print('empty text1',text)
                if not list1 :
                    list1.append(text)
                
                    # get test
                #for cbc test
                if 'cbc' in text or 'complete blood count'  in text:
                    print('the cbc value True')
                    testdata['cbc']=True
                        
                
                #end cbc test
                
                #for urine test

                if 'urine'in text: 
                    print('the urine value True')
                    testdata['urine']=True
                
                #end urine test

                #for Haemoglobin test
                
                
                #end Haemoglobin test

                #for LFT test
                if 'liver function test' in text or 'lft'  in text:
                    
                    print('the lft value True')
                    testdata['lft']=True
                
                #end LFT test
                
                #for KFT test
                if 'kidney function test' in text or 'renal function test' in text or 'kft' in text or 'rft' in text:
                    
                    print('the kft value True')
                    testdata['kft']=True
                
                #end KFT test
                
                #for Iron  test
                if 'iron studies' in text or 'iron study' in text:
                    
                    print('the Iron value True')
                    testdata['iron_study']=True
                
                #end Iron test
                
                #for Lipid test
                if 'lipid' in text:
                    
                    print('the lipid value True')
                    testdata['lipid']=True
                
                #end Lipid test
                
                if 'thyroid profile' in text:
                    
                    testdata['thyroid_profile']=True

                
                # end test
                list2.append([testdata])
            else:
                list2.append([])
                print('empty data or something wrong')
            
    
    
    if text:
        name=re.search(r"(?:mr\.|mrs\.|ms\.) [a-zA-Z]+ [a-zA-Z]+",text)
        print(name.group())
        
        if name:
            testdata['name']=name.group()
        # in order to get date
        for l1 in list1:
            # print(l1)
            l1=l1
        yy = re.search(r"[\d]{1,2}/[\d]{1,2}/[\d]{2,4}", l1)
        y_y = re.search(r"[\d]{1,2}-[\d]{1,2}-[\d]{2,4}", l1)
        mmm = re.search(r"[\d]{2} [a-zA-Z]{3} [\d]{2,4}", l1)
        m_m_m = re.search(r"[\d]{2}-[a-zA-Z]{3}-[\d]{2,4}", l1)
        # print(yy.group(),y_y.group(),mmm.group(),m_m_m.group())
        if yy:
            
            testdata['date']=yy.group()
        elif y_y:
            
            testdata['date']=y_y.group()      
        elif mmm:
            
            testdata['date']=mmm.group()
                
        elif m_m_m:
            
            
            testdata['date']=m_m_m.group()
        
    else:
        print('something is wrong with')
                
    # print(text)
    shutil.rmtree(path)
    return list2[-1]



if __name__ == "__main__":
    start_time = time.time()
    # file=fitz.open('share_preview2.pdf')
    # file=fitz.open('c676422960523ad28beb131038335370.pdf')
    # file=fitz.open('lalitaimg.pdf')
    # file=fitz.open('lalita.pdf')
    file=fitz.open('imagetest.pdf')
    a=pdftotext(file)
    print(a)
    if not a:
        b=imgtotxt(file)
        print(b)
        if not b:
            print('no data in pdf')

print("--- %s seconds ---" % (time.time() - start_time))
