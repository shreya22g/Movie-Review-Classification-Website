from django.shortcuts import render,HttpResponse
from home.models import Review
from django.contrib import messages
from .models import Review
import pandas as pd
from django.core.paginator import Paginator
import pymongo
import re
from django.forms.models import modelform_factory, modelformset_factory
#creating connection with mongodb
client=pymongo.MongoClient("mongodb://127.0.0.1:27017/")
mydb=client.MovieDataBase
info=mydb.home_review
information=mydb.avgcollection

#loading models using joblib

import sklearn.externals
import joblib
import_one=joblib.load('./models/vectorizer.sav')
import_two=joblib.load('./models/model.sav')

from nltk.tokenize import RegexpTokenizer    #each word is a token when a sentence is “tokenized” into words
from nltk.corpus import stopwords            #Used to remove common words such as (As, The, a ,etc)
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer   
from nltk.corpus import wordnet              #find the meanings of words, synonyms, antonyms,
import nltk
#nltk.download('wordnet')
#nltk.download('averaged_perceptron_tagger')
reg_token=RegexpTokenizer('[a-zA-Z]+')       #input:['I love python']  output:[‘I’, ‘love’, ‘Python’]
wnl=WordNetLemmatizer()                      #converts the word to its meaningful base form ex- ‘caring’ to ‘care’



#preprocessing user input
def simple_pos(p):
     if p.startswith('J'):
          return wordnet.ADJ
     elif p.startswith('V'):
          return wordnet.VERB
     elif p.startswith('N'):
          return wordnet.NOUN
     elif p.startswith('R'):
          return wordnet.ADV
     else:
          return wordnet.NOUN

def clean_data(k):
     d=reg_token.tokenize(k)
     cleaned_words=[]
     for w in d:
          p=pos_tag([w])
          word=wnl.lemmatize(w,pos=simple_pos(p[0][1]))
          cleaned_words.append(word.lower())                 #converting all to lower case
     return " ".join(cleaned_words)                          #joins all words together after preprocessing



# Create your views here.
def index(request):
    return render(request,'index.html')
    #return HttpResponse("THIS IS HOMEPAGE")

def services(request):
     return render(request,'services.html')
     #return HttpResponse("THIS IS SERVICEPAE")


def review(request):
     num=0
     if request.method == "POST":
          username=request.POST.get('username')             #critic_name
          name =request.POST.get('name')                    #movie_name
          desc =request.POST.get('desc')                    #review_content
          
          #checks if all entries are correctly filled
          if username =="" or name =="" or desc=="":
               messages.warning(request,"there is one or more fields are empty!")
               return render(request,'review.html')               
          
          a=clean_data(desc)
          #using joblib to calculate review_score
          num=import_two.predict(import_one.transform([desc]))
          #saving info in database
          flag=0
          for i in num:
               flag=int(i)
          review = Review(critic_name=username,movie_name=name,review_content=desc,review_Score=num)
          review.save()   
          cursortwo = information.find({'moviename': re.compile(name, re.IGNORECASE)})
          count=0
          temp=0
          for r in cursortwo:
               temp=r['averagerating']
               count=count+1

          if(count==0):
               record={
                         'moviename': name,
                         'averagerating': flag
                         }
               information.insert_one(record)

          else:
               average=(temp+flag)/2
               information.delete_one({'moviename': re.compile(name, re.IGNORECASE)})
               record={
                         'moviename': name,
                         'averagerating': average
                         }
               information.insert_one(record)
          messages.success(request, 'Review has been sent.')
     arr=['critic_name','review_content']
     formset=modelformset_factory(Review,fields=(arr))
     form=formset()
          
     return render(request,'review.html',{'num': num,'form':form })
     #return HttpResponse("THIS IS CONTACTPAGE")


def list(request):

     li=information.find().sort("averagerating",-1)
   
     p = Paginator(li,10)
     page=request.GET.get('page')
     venues=p.get_page(page)
     for i in li:
          print(i)
     return render(request,'list.html',
          {'li': li , 'venues': venues})
     

def view(request):
     if 'search' in request.GET:
          search=request.GET['search']
          
          if Review.objects.filter(movie_name__icontains=search):
               posts=Review.objects.filter(movie_name__icontains=search)
          else:     
               messages.warning(request,"Review of the following movie is not present.Sorry!")
               return render(request,'view.html')
          
     else:
          posts=Review.objects.all()
     


     p = Paginator(posts,10)
     page=request.GET.get('page')
     venues=p.get_page(page)
     return render(request,'view.html',{'posts' : posts, 'venues': venues})
