# Project Movie Reviews

### Introduction
Enables users to get information about movies, when they were released, who directed them
and which actors form cast of the movie.
Users can search for movie titles based on genre they like, word in title, or actor who is part of the cast.
Users can signup and login to their accounts.
Authenticated users can leave ratings and reviews of movies.
They can also create groups to exchange recommendations of movies they like. These posts are
visible only to group members.

### Installation

#### Create virtual environment
##### PyCharm
```bash
venv ./venv
```
##### Windows
Open Command Prompt or PowerShell, navigate to project folder and run
```bash
python -m venv ./venv
```
##### Linux/MacOS
Open terminal, navigate to project directory and run
```bash
python -m venv ./venv
```
In case that previous command didn't work, install virtualenv
```bash
pip install virtualenv
```
Run command in project directory to create virtual env
```bash
virtualenv venv
```
#### Activate Virtual environment
Open terminal and navigate to project directory, than run

| Platform | Shell      | Command to activate virtual environment |
|----------|------------|-----------------------------------------|
| POSIX    | bash/zsh   | $ source venv/bin/activate              |
|          | fish       | $ source venv/bin/activate.fish         |
|          | csh/tcsh   | $ source venv/bin/activate.csh          |
|          | PowerShell | $ venv/bin/Activate.ps1                 |
| Windows  | cmd.exe    | C:\> venv\Scripts\activate.bat          |
|          | PowerShell | PS C:\> venv\Scripts\Activate.ps1       |

#### Dependencies
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.
```bash
pip install -r requirements.txt
```
#### Database
Start MySQL server and execute all commands in **_init_db/init_db.sql_** and **_init_db/init_data.sql_**

#### Environment variables
1. Create new file **_.env_**
2. Copy all consts from **env-template** to **_.env_**
3. Assign values to const in .env file

### Login for super_user
    user_name : superuser
    password : superpass
