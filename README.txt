## README
Excel file will be created after running 'Store_Data.py', however created excel file is also included in the zip file in case the program takes too much time. With the excel file, 'Project_Yubin.py' will work even without running the 'Store_Data.py'. 

> Project Description
>> The project is to provide user-friendly software that offers information about top 50 actors/actresses in Hollywood. 

> How To Use
>> Before running the project, the data should be stored in the local space by running 'Store_Data'. This software automatically stores the data needed for the project in local space in excel. 
>> When the project started, user will be asked to input a number between 1~3 (1: List of the available actors/actresses, 2: About an actor/actress, 3: End the program). 
>>> Typing 3 will end the program immediately, which means that the program will be running repeatedly untill the user enters 3. 
>>> Typing 1 will show all 50 actors/actresses. 
>>> Typing 2 will allow user to get to know about an actor/actress. User will be asked to type in the name of an actor/actress. Only a few alphabets of the actor/actress is fine, the program will find the actor/actress's name. If user put wrong or unavailable name, the program will say it doesn't know the actor and go back to the beginning. 
>>>> After recognizing the actor/actress, user will be asked to choose a number between 1~5 (1: About the actor/actress, 2: All movies, 3: Genre, 4: Average ratings, 5: Movie recommendations). 
>> Every time user puts a number out of range, the program will say that it is a wrong number and waits user to put an available number. 

> Install Requirments
>> Before running 'Store_Data.py' : install request, bs4, xlsxwriter
>> Before running 'Project_Yubin.py' : install pandas, wordcloud, matplotlib, openpyxl