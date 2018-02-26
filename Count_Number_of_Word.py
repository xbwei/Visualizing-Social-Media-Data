'''
Created on Feb 22, 2017

@author: Xuebin Wei
www.lbsocial.net

find the 10 most common words
and write the result to an excel file
'''
import xlwt        
from collections import Counter        
         
book = xlwt.Workbook() # create a new excel file
sheet_test = book.add_sheet('word_count') # add a new sheet
i = 0
sheet_test.write(i,0,'word') # write the header of the first column
sheet_test.write(i,1,'count') # write the header of the second column
 
with open('','r') as jmu_news: # define the location of your txt file
    count_result =  Counter(jmu_news.read().split()) 
    for result in count_result.most_common(10):
        i = i+1 
        sheet_test.write(i,0,result[0])
        sheet_test.write(i,1,result[1])
 
book.save('') # define where to save your excel file
