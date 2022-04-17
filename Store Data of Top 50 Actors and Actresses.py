#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

actors_table = pd.DataFrame({'id':range(1,51), 'name':range(0, 50), 'web_page':range(0, 50), 'awards_page':range(0,50)}, index=range(0,50))

url = 'http://www.imdb.com/list/ls053501318/'

page = requests.get(url) #get the web page ready for web scrapping
soup = BeautifulSoup(page.text, 'html.parser')
    
names_info = []
count = 0
names_info = soup.find_all('img', height='209') 
#get all the actors available using 'image' tag, since they all have same same image size and has the actor's name in 'alt' attribution
for i in names_info:
    actors_table.loc[(actors_table.name == count), 'name'] = i.get('alt') 
    #already initialized from 0 to 49, using this can find where to save 'name'
    count=count+1

movies_table = pd.DataFrame({'id':[], 'title':[], 'rating':[], 'year':[], 'genre':[]}) #initialize columns name

infos = []
infos = soup.find_all('h3', class_='lister-item-header') #get all names' tag of the actors. 
count=0
for i in infos:
    a_url = infos[count].find('a') #get the name tag for the specific actor. 
    actor_url = 'https://www.imdb.com'+a_url.get('href') #get the actor's personal url in the title. 
    actors_table.loc[(actors_table.web_page == count), 'web_page'] = actor_url #save the actor's url in actors_table
    
    actor_page = requests.get(actor_url) #move to the actor's web page. 
    actor_soup = BeautifulSoup(actor_page.text, 'html.parser')
    
    awards = actor_soup.find('a', class_='btn-full') #get the awards' page url
    awards_url = 'https://www.imdb.com'+awards.get('href')
    actors_table.loc[(actors_table.awards_page==count), 'awards_page'] = awards_url #save the awards' url in actors_table
    
    movies = []
    movies = actor_soup.find('div', class_='filmo-category-section').find_all('div', {'class':['filmo-row even', 'filmo-row odd']})
    #find all movies only roled as actor
    mcount=0
    for j in movies:
        movie_url = 'https://www.imdb.com'+movies[mcount].find('a').get('href') #get the movie's page url
        movie_page = requests.get(movie_url) #move to the movie's page
        movie_soup = BeautifulSoup(movie_page.text, 'html.parser')
        
        rating_data = 'NaN'
        year_data = 'NaN'
        genre_data = 'NaN'
        
        movie_rating = movie_soup.find('span', class_='AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV') #get rating
        if movie_rating != None :
            rating_data = movie_rating.get_text()
        
        movie_year = movie_soup.find('a', class_='ipc-link ipc-link--baseAlt ipc-link--inherit-color TitleBlockMetaData__StyledTextLink-sc-12ein40-1 rgaOW') #get year
        if movie_year != None:
            year_data = movie_year.get_text()
            
        movie_genre = movie_soup.find('span', class_='ipc-chip__text')
        if movie_genre != None:
            genre_data = movie_genre.get_text() #get genre
                
        insert_movie_data = {'id':count+1, 'title': movie_soup.find('h1').get_text(), 'rating': rating_data, 'year': year_data, 'genre': genre_data} #save info as a list 
        movies_table = movies_table.append(insert_movie_data, ignore_index=True) #append the movie data to movies_data DataFrame

        mcount = mcount+1
        
    count=count+1


writer = pd.ExcelWriter('IMDB Data.xlsx', engine='xlsxwriter') #save as excel file 

actors_table.to_excel(writer, sheet_name='actors table') #save each Dataframe as different sheet
movies_table.to_excel(writer, sheet_name='movies table')

writer.save() #save the Dataframe


# In[ ]:




