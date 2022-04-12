# -*- coding: utf-8 -*-
"""
Created on Sun May  2 15:49:56 2021

@author: OBIORA NNAJI
"""

# plot is duration of illness against age group 

import matplotlib.pyplot as plt 



def DOI(Age, Sex):
        
       
    if 0 < Age < 19 and Sex == "male":  
             
        return 14 
    
    elif 0 < Age < 19 and Sex == "female":
                          
          return 13 
        
    elif 20 < Age < 29 and Sex == "male":
       
        return 14
   
    elif 20 < Age < 29 and Sex == "female":
         
       return 13 
   
   
    elif 30 < Age < 39 and Sex == "male":
                   
       return 14
   
    elif 30 < Age < 39 and Sex == "female":
                
        return 16
    
    elif 40 < Age < 49 and Sex == "male":
          
       return 16
   
    elif 40 < Age < 49 and Sex == "female":
                
       return 16
    
    elif 50 < Age< 100 and Sex == "male" or "female":  
           
      return 19 
  
ymale = [DOI(15,"male"), 
         DOI(25, "male"),
         DOI(35, "male"),
         DOI(45, "male"),
         DOI(55, "male")]

xmale = ["0-19","20-29","30-39","40-49","50-100"]

yfemale = [DOI(15,"female"), 
          DOI(25, "female"),
          DOI(35, "female"),
          DOI(45, "female"),
          DOI(55, "female")]

xfemale = ["0-19","20-29","30-39","40-49","50-100"]


sd = [5,6,6,6,6]

plt.bar(xmale, ymale, align= 'edge', label = "Male" ,  color = 'cyan', yerr = sd, width = 0.3 )

plt.bar(xfemale, yfemale, align ='edge', label = 'Female' ,  color = 'red', yerr = sd, width = -0.3)

plt.legend(loc = 'upper left')

plt.title('Duration Of Illness VS Age Group ', fontsize = 23,)

plt.xlabel('Age Group', fontsize = 18)

plt.ylabel("Duration Of Illness", fontsize = 18)

plt.show()

