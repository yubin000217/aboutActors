#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

actors_table = pd.read_excel('IMDB Data.xlsx', sheet_name='actors table')
movies_table = pd.read_excel('IMDB Data.xlsx', sheet_name='movies table') #NaN은 문자열 'NaN'이다. None타입이랑 헷갈리지 말기
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option("expand_frame_repr", False)

def actor_info(actor_id) :
    
    from bs4 import BeautifulSoup
    
    actor_url = actors_table.iloc[actor_id-1].values[3] #
    #get the actor's web page
    actor_page = requests.get(actor_url) 
    actor_soup = BeautifulSoup(actor_page.text, 'html.parser')
            
    bio_url = 'https://www.imdb.com'+ actor_soup.find('span', class_='see-more inline nobr-only').find('a').get('href')
    #get the actor's biography page
    bio_page = requests.get(bio_url) 
    bio_soup = BeautifulSoup(bio_page.text, 'html.parser')
            
    #print the biography of the actor
    print(bio_soup.find('div', class_='soda odd').find('p').get_text()) 

    
def actor_awards(actor_id) :
    
    from bs4 import BeautifulSoup
    
    awards_url = actors_table.iloc[actor_id-1].values[4]
    awards_page = requests.get(awards_url) #move to awards page
    awards_soup = BeautifulSoup(awards_page.text, 'html.parser')
    
    award_outcome = []
    award_category = []
    award_description = []
    award_movie = []
    
    outcome_text = " "
    category_text = " "
    every_table = []
    every_table = awards_soup.find_all('tr')
    acount = 0
    for i in every_table :
        temp = i.find('td', class_='award_outcome')
        
        #it can be none if he/she is nominated in more than one awards
        if temp != None : 
            outcome_text = temp.find('b').get_text()
        award_outcome.append(outcome_text)
        temp2 = i.find('td', class_='award_outcome')
        
        #it can be none if he/she is nominated in more than one awards
        if temp2 != None : 
            category_text = temp2.find('span').get_text()
        award_category.append(category_text)
        
        description_text = " "
        temp3 = i.find('td', class_='award_description') 
        
        #it can be none if there is no information
        if temp3 != None : 
            #with get_text() texts in lower tags are included, needs split and get the text i want
            split_list = temp3.get_text().split('\n') 
            description_text = split_list[1]
        award_description.append(description_text)
        
        movie_text = " "
        temp4 = temp3.find('a')
        
        #it can be none if the award is given to the actor/actress not due to a certain movie
        if temp4 != None : 
            movie_text = temp4.get_text()
        award_movie.append(movie_text)
        
        acount = acount+1
        

    awards_table = pd.DataFrame({'outcome':range(0,acount), 'Category':range(0,acount), 'Description':range(0,acount), 'Movie':range(0,acount)}) #create dataframe for awards
    
    #insert outcome list to award table
    awards_table['outcome'] = award_outcome 
    awards_table['Category'] = award_category
    awards_table['Description'] = award_description
    awards_table['Movie'] = award_movie
    
    
    #print only won awards' data
    print(awards_table.loc[awards_table.outcome=='Winner', ['Category', 'Description', 'Movie']]) 
    
    
def genre_wordcloud(actor_id) :
            
    #get only the actor's movies
    actor_movies = movies_table.loc[movies_table['id']==actor_id, :] 
    #count frequency by the genres
    genre_freq = actor_movies.groupby('genre').count() 
    #change dataframe to genre:frequency dictionary
    frequencies_dic = genre_freq['id'].to_dict() 
    
    #basic setting of the wordcloud
    wordcloud = WordCloud(background_color='white',
                          width=1500,
                          height=1000) 
    
    #generating wordcloud
    print_text = wordcloud.generate_from_frequencies(frequencies_dic) 
    #generating array to show the wordcloud
    arr = print_text.to_array() 
            
    plt.figure(figsize = (8, 8)) #print word cloud
    plt.imshow(arr)
    plt.axis('off')
    plt.show()

            
def movies_ratings(actor_id) :
    
    #get only the actor's movies' rating and year
    actor_movies = movies_table.loc[movies_table['id']==actor_id, ['rating', 'year']] 
    
    #new dataframe with average rating of each year
    rating_mean = actor_movies.groupby(['year']).mean() 
    
    #copy the rating dataframe
    avg = rating_mean.copy() 
    #replace each year average to total average
    avg.loc[:, 'rating'] = actor_movies.loc[:, 'rating'].mean() 
    #change column name to 'average rating'
    avg.rename(columns={'rating':'average rating'}, inplace=True) 
    
    #to show the two graphs into one graph
    fig, ax1 = plt.subplots() 
    ax2 = ax1.twinx()
    
    #bar graph
    rating_mean.plot(kind='bar', ax=ax1, color='c', width=0.8, ylim=[0,10], figsize=(15,5), rot=45, alpha=0.5, align='edge') 
    
    #line graph
    avg.plot(kind='line', linestyle='--', linewidth=3, ax=ax2, secondary_y=False, color='g', ylim=[0,10], figsize=(15,5)) 
    
    ax2.legend(loc='upper left')
    ax1.legend(loc='upper right')
    
    plt.title('Ratings of Each Year & Average Rating', fontsize=15)
    plt.show()
    
    
def movies_recommendations(actor_id) :
    
    #get only the actor's movies
    actor_movies = movies_table.loc[movies_table['id']==actor_id, ['title', 'rating', 'year', 'genre']] 
            
    print('\n', "These are top 5 rating movies: ", '\n')
    print(actor_movies.nlargest(5, 'rating')) #printing top 5 movies
    
    
    
    
while True:
    print('\n',"<< ABOUT IMDB ACTORS/ACTRESSES >>",'\n',"Please choose a number you want!",'\n',"1. List of the top 50 actors/actresses in IMDB",'\n',"2. All about an actor/actress",'\n',"3. End the program",'\n')
    first_input=input()
    
    if first_input=='1':
        print(actors_table['name'])
    elif first_input=='2':
        the_actor = input("Whom do you want to know about? ")
        
        try: 
            #find the actor's id with the name input
            actor_= actors_table[actors_table['name'].str.contains(the_actor)] 
            actor_id = actor_['id'].values[0]
        
        except IndexError : 
            #Exception handling when can't find the actor
            print('\n', "Don't know the actor! Please type precise name. ")
            
        else: 
        
            print("What do you want to know about", actors_table.loc[actor_id-1, 'name'],"?", '\n')
            
            while True: 
                print("1. About the actor/actress", '\n', "2. All time movies and raitings/years", '\n', "3. The actor/actresse's movie genre", '\n', "4. Average rating of the actor/actress's movies", '\n', "5. Recommendations of movies", '\n', "6. Actor/Actress's awards", '\n')
                second_input = input()
        
                #'about the actor/actress
                if second_input == '1': 
                    actor_info(actor_id)#call function
                    break
            
                #all time movies
                elif second_input == '2': 
                    print(movies_table.loc[movies_table['id']==actor_id, ['title', 'rating', 'year']]) #printing all movies' title, rating and year
                    break
        
                #actor's genre in wordcloud    
                elif second_input == '3':         
                    genre_wordcloud(actor_id) #call function
                    break
                 
                #average ratings and ratings of each year
                elif second_input == '4': 
                    movies_ratings(actor_id) #call function
                    break
    
                #Recommendations of movies according to ratings 
                elif second_input == '5':             
                    movies_recommendations(actor_id) #call function
                    break
                    
                #Actor/Actress's awards
                elif second_input == '6': 
                    actor_awards(actor_id) #call function
                    break
            
                else :
                    print('\n', "Please choose between 1~5", '\n')
                    
              
        
    elif first_input=='3':
        print('\n', "Ending the program!")
        break
        
    else :
        print('\n', "Please choose between 1~3")
        


# In[ ]:




