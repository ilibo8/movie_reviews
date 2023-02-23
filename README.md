# Project Movie Reviews

### Introduction
Enables users to get information about movies, when they were released, who directed them
and which actors are part of the cast.
Users can search for movie titles based on genre they like, word in title, or actor who is part of the cast. 
There is also information about top movies by current user ratings.
Authenticated users can leave ratings and reviews of movies.
They can also create groups to exchange recommendations of movies they like. 
These posts are visible only to group members.

### Installation

##### Create and activate virtual environment
[help](venv_activate.md)

##### Dependencies
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.
```bash
pip install -r requirements.txt
```

#### Troubleshooting with PyCharm
Edit Run/Debug configurations.   
**_Script path_**   ..\movie_reviews\app\main.py   
**_Working directory_**..\movie_reviews    

#### Database
Start MySQL server and execute all commands in:   
__init_db/init_db.sql__   
__init_db/init_data.sql__   

### Login for super_user
    user_name : superuser
    password : superpass

### Login for classic_user from database
    user_name : {name}
    password : {name}123
