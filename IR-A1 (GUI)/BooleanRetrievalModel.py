#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Approach for Making Boolean Retrival Model 
#1.Preprocessing -Tokenization -Removal of Stop Words -Stemming.
#2.Inverted-Positional Index - Posting Lists
#3.query Processing.


# In[2]:


# Libraries 
import nltk #used for Stemming

import tkinter as tk 
from PIL import Image, ImageTk
root = tk.Tk(className='Boolean Retrieval Model')
root.geometry('1080x500')
root.configure(bg="black")

background = ImageTk.PhotoImage(file="img1.jpg")
label1 = tk.Label(root,image=background)
label1.pack(fill=tk.BOTH,expand=True)
label = tk.Label(root,text="Boolean Retreival Model",bg="black",
fg="white",font="Courier 30 bold")
label.place(relx=0.25,rely=0.25,height=50)






# In[3]:


#Declarations - Lists & Dictionaries. 
inverted_index = {}
tokens_ = {}


# In[4]:


from nltk.stem.porter import PorterStemmer
p_stemmer = PorterStemmer() #importing Porter Stemmer from NLTK


# In[5]:


#1. Preprocessing. 

# Importing all the stop words from the given file. 
# Tokenization of the given corpus. 
# Removal of Stopwords from the tokens, lowering them and then stemming. 


# In[6]:


# Step1. Importing all the stopwords from the file for the removal. 

with open('Stopword-List.txt','r') as lines:
    stopwords = lines.readlines()
    stopwords = [x.rstrip() for x in stopwords]
    #print(stopwords)
    
# with-open automatically closes the file. 
# stop words are read and then stripped of, stored in stopwords.
    


# In[7]:


#Step2. Tokenization - Removal of Stopwords 

for x in range(1,51):
    myfile=open("ShortStories/"+str(x)+ ".txt","r",encoding='utf-8')
    #for x in tokens:
    #print(x)
    
    words=myfile.read().replace(".","").replace("n't"," not").replace("'","").replace("]"," ").replace("[","").replace(","," ").replace("?","").replace("\n"," ").replace("-"," ").replace("(","").replace(")","").replace("!","").replace("“","").replace("”","").replace(":","").replace("*","").replace("—","").replace(";","").replace("’","").split()
    
    #for i in range(len(temp)):
    #temp[i]=[p_stemmer.stem(x.lower()) for x in temp[i]]
    stem=[p_stemmer.stem(x.lower()) for x in words]
    tokens = [x for x in stem if x not in stopwords]
    inverted_index[x]=tokens
    tokens_[x]=stem
#len(tokens)
#stem[0:20]
tokens.sort()
myfile.close()
tokens[0:10]


# In[8]:


#inverted_index
#inverted_index.keys()
#len(inverted_index)


# In[9]:


#Inverted - Positional Indexes


# In[10]:


# Inverted-Index
index = {}

for i in inverted_index.keys():
    for j in set(inverted_index[i]):
        if j not in index:
            index[j]=[]
            index[j].append(i)
        else:
            index[j].append(i)
#index

try:
    file = open('InvertedIndex.txt', 'w')
    file.write(str(index))
    file.close()

except:
    print("Unable to write to file")


# In[11]:


# Positional Index 

pos_index={}
for i in tokens_.keys():
    count=0
    for j in tokens_[i]:
        count+=1
        if j in stopwords:  # entertaining the presence of stop words in the file (increment index without doing anything)
            continue
        if j not in pos_index:
            pos_index[j]={}
            pos_index[j][i]=[]
            pos_index[j][i].append(count)
        else:
            if i not in pos_index[j]:
                pos_index[j][i]=[]
            pos_index[j][i].append(count)


#pos_index

try:
    file = open('PositionalIndex.txt', 'w')
    file.write(str(pos_index))
    file.close()

except:
    print("Unable to write to file")


# In[12]:


# query Processing  
# Boolean Queries & Proximity Queries 


# In[13]:


#Step 1. 
#We have to take user input and stem that query to match the inverted-positional indexes for retrival 


# In[84]:


def counter_pos(word1, word2, prox_value,intersect): 
    result = []
    for pos1 in word1:
        for pos2 in word2:
            if (abs(pos1-pos2)-1) == prox_value:
                #print("DOC--> ",intersect,"-->pos1(",pos1,") - pos2(",pos2,")",abs(pos1-pos2)-1)
                result.append(intersect)
    return result

def proximity_query(w1, w2, prox_value, pos_index):
    word1={} 
    word2={}
    for word in pos_index.keys():
        if word == w1:
            for i in pos_index[word]:
                word1[i]=pos_index[word][i]
        elif word==w2:
            for i in pos_index[word]:
                word2[i]=pos_index[word][i]
                
    s1=set(word1.keys())
    s2=set(word2.keys())
    intersect=None
    intersect=s1.intersection(s2)
    
    finaldocs=[]
    if intersect != None:
        for intersect in intersect:
                x=counter_pos(word1[intersect],word2[intersect], prox_value,intersect)
                if len(x)>0:
                    finaldocs.append(intersect)
    else:
        print("result not found")
        
    label9 = tk.Label(root,text=f"Returned Document: {finaldocs}",bg="black",fg="white",font="Courier 10 bold")
    label9.place(relx=0.45,rely=0.67,height=35)


# In[77]:


def check_index(w,index):
#     print("in word found func ")

    for word in index.keys():
        if word == w:
            return set(index[word])
        
    return None

def boolean_query(x, index): 
    
    # For AND query we use intersection 
    if 'and' in x:
# matching if its AND query.
        val = [i for i in x if i=='and']
        #print(val)
    #The approach im using here is to determine number of AND's , as the complexity is 3 AND.
        if len(val)==1: 
            count1=check_index(x[0],index)
            count2=check_index(x[2],index)
            count=count1.intersection(count2)
            label1 = tk.Label(root,text=f"Returned Documents {count}",bg="black",
            fg="white",font="Courier 10 bold")
            label1.place(relx=0.45,rely=0.67,height=35)
            #print("\nReturned Documents -->",count)
        elif len(val)==2:
            count1=check_index(x[0],index)
            count2=check_index(x[2],index)
            count3=check_index(x[4],index)
            count=count3.intersection(count1.intersection(count2))
            label2 = tk.Label(root,text=f"Returned Documents {count}",bg="black",
            fg="white",font="Courier 10 bold")
            label2.place(relx=0.45,rely=0.67,height=35)
            #print("\nReturned Documents -->",count)
        elif len(val)==3:
            count1=check_index(x[0],index)
            count2=check_index(x[2],index)
            count3=check_index(x[4],index)
            count4=check_index(x[8],index)
            count=count4.intersection(count3.intersection(count1.intersection(count2)))
            label3 = tk.Label(root,text=f"Returned Documents {count}",bg="black",
            fg="white",font="Courier 10 bold")
            label3.place(relx=0.45,rely=0.67,height=35)

    # For OR query we use union
    if 'or' in x: # matching if its OR query.
        val = [i for i in x if i=='or']
        #print(val)
    #The approach im using here is to determine number of OR's , as the complexity is 3 AND.
        if len(val)==1: 
            count1=check_index(x[0],index)
            count2=check_index(x[2],index)
            count=count1.union(count2)
            label4 = tk.Label(root,text=f"Returned Documents {count}",bg="black",
            fg="white",font="Courier 8 bold")
            label4.place(relx=0.0,rely=1.0,height=35,anchor ='sw')
        elif len(val)==2:
            count1=check_index(x[0],index)
            count2=check_index(x[2],index)
            count3=check_index(x[4],index)
            count=count3.union(count1.union(count2))
            label5 = tk.Label(root,text=f"Returned Documents {count}",bg="black",
            fg="white",font="Courier 10 bold")
            label5.place(relx=0.0,rely=1.0,height=35,anchor ='sw')
        elif len(val)==3:
            count1=check_index(x[0],index)
            count2=check_index(x[2],index)
            count3=check_index(x[4],index)
            count4=check_index(x[8],index)
            count=count4.union(count3.union(count1.union(count2)))
            label6 = tk.Label(root,text=f"Returned Documents {count}",bg="black",
            fg="white",font="Courier 10 bold")
            label6.place(relx=0.0,rely=1.0,height=35)
                  
    if 'not' in x:
        j=set(tokens_.keys())
        val=[i for i in x if i=='not']
        if len(val)%2 == 0:
                for word in index.keys():
                    if word == x[len(val)]:
                        print(index[word])
        else:
            for word in index.keys():
                    if word == x[len(val)]:
                        found=set(index[word])
                        notfound=j.difference(found)
                        label7 = tk.Label(root,text=f"Returned Documents {notfound}",bg="black",fg="white",font="Courier 6 bold")
                        label7.place(relx=0.0,rely=1.0,height=35,anchor='sw')

def one_word_query(query,pos_index):
    if len(query)==1:
        for word in pos_index.keys():
            if word == query[0]: 
                check = []
                for i in pos_index[word]:
                    check.append(i)
                    #print(i,"-->",pos_index[word][i])  - gives the doc id and pos index.

    label10 = tk.Label(root,text=f"Returned documents {check}",bg="black",fg="white",font="Courier 9 bold")
    label10.place(relx=0.0,rely=1.0,height=35,anchor='sw')


# In[89]:
def inputval(): 
    query=query_.get()
    #query = input("ENTER query FOR SEARCHING: ")
    query=query.replace(".","").replace("n't"," not").replace("'","").replace("]"," ").replace("[","").replace(","," ").replace("?","").replace("\n"," ").replace("-"," ").replace("(","").replace(")","").replace("!","").replace("“","").replace("”","").replace(":","").replace("/"," / ").replace("*","").replace("—","").replace(";","").replace("’","").split()
    x=[p_stemmer.stem(x.lower()) for x in query]
    print(x)

    #Boolean Queries
    if 'and' in x or 'or' in x or 'not' in x: 
        boolean_query(x,index)

    #Proximity Queries
    elif '/' in x:
        proximity= int(x[x.index('/')+1])
        w1=x[0]
        w2=x[1]
        if proximity != 0:
            proximity_query(w1,w2,proximity,pos_index)

    elif 'not' not in x and 'and' not in x and 'or' not in x:
        if len(x)!=0:
            one_word_query(x,pos_index)



query_=tk.StringVar()


entry = tk.Entry(root,width=100,bd=3,textvariable=query_)
entry.place(relx=0.17,rely=0.45,height=35)

button = tk.Button(root,text="Search",bg="#000000",fg="white",
font="Courier 15 bold",command=inputval)
button.place(relx=0.73,rely=0.45,height=35)
root.mainloop()

