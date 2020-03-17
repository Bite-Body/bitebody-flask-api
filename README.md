# bitebody-flask-api
Team Late's back-end API for bitebody.xyz created with Flask (Python micro-framework).

Created by **Bryan Rojas**, **Hector Mendoza**, **Malik Coleman**, **David Ibarra**

## Prerequisites

### Specifications & Tools
* 64-bit environment (Trying to make it system agnostic)
* [Git](https://git-scm.com/downloads)

### Back-end
* [Python 3.7.x](https://www.python.org/downloads/)
* [Pip](https://pip.pypa.io/en/stable/installing/)

## Downloading Application

1. Ensure git is installed on computer. You can verify by running the following command on your terminal.
```
git --version
```
2. Clone the GitHub repository.
```
git clone https://github.com/Bite-Body/bitebody-flask-api.git
```

## Prerequisites

1. Verify you have Python 3.7.x, open up terminal and run the following command.
```
python -V 
```


## Running Application locally

1. Change directory (cd) into the project folder.
```
cd bitebody-flask-api
```
2. Install Python dependencies.
```
pip install -r requirements.txt
```
3. Running the API server.
```
python manage.py
```

## Deployment Notes

1. Log into heroku CLI
```
heroku login
```
2. Login into Heroku containers
```
heroku container:login
```
3. Heroku push container
```
heroku container:push web --app gentle-inlet-25364
```
4. Heroku release container
```
heroku container:release web --app gentle-inlet-25364
```
5. Check logs to verify
```
heroku logs --tail
```
## Testing API endpoints through Individual Python Files

Before going through with the steps outlined below, please have a local instance of the application running. Documentation for running locally can be found above in the "Running Application Locally" section of the README. :)

Each of the tables stored in the database can have the API's CRUD operations tested through the command line.

A) To test the USER table follow the following instructions:

1. Open the Command Prompt on your machine.
2. Change directory to backend
```
cd bitebody-flask-api
```
3. change directory to test folder (where test files are housed)
```
cd tests
```
4. run user_Test file
```
python user_Test.py
```

B) To test the COLLABORATOR table follow the following instructions:

1. Open the Command Prompt on your machine.
2. Change directory to backend
```
cd bitebody-flask-api
```
3. change directory to test folder (where test files are housed)
```
cd tests
```
4. run user_Test file
```
python collab_Test.py
```

C) To test the YOUTUBE VIDEOS table follow the following instructions:

1. Open the Command Prompt on your machine.
2. Change directory to backend
```
cd bitebody-flask-api
```
3. change directory to test folder (where test files are housed)
```
cd tests
```
4. run youtube_video_test file
```
python youtube_video_Test.py
```

D) To test the MEAL table follow the following instructions:

1. Open the Command Prompt on your machine.
2. Change directory to backend
```
cd bitebody-flask-api
```
3. change directory to test folder (where test files are housed)
```
cd tests
```
4. run meal_test file
```
python meal_Test.py
```

E) To test the WORKOUT table follow the following instructions:

1. Open the Command Prompt on your machine.
2. Change directory to backend
```
cd bitebody-flask-api
```
3. change directory to test folder (where test files are housed)
```
cd tests
```
4. run meal_test file
```
python workout_Test.py
```
## Testing API endpoints through A SINGLE Python File

1. Open the Command Prompt on your machine.
2. Change directory to backend
```
cd bitebody-flask-api
```
3. run Test_Tables file
```
python Test_Tables.py
```
4. Once you start the file running, make sure to press any key whenever text stops appearing on screen. This is meant fo you to proceed whenever you're done reading each table's set of tests.
