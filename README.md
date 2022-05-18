[![codecov](https://codecov.io/gh/Spotifiuby/backend-users/branch/main/graph/badge.svg?token=nGGJVRVXdi)](https://codecov.io/gh/Spotifiuby/backend-users)

# Table of Contents
- [Table of Contents](#table-of-contents)
- [Setup](#setup)
- [Database Versions](#database-versions)
- [Environment Variables](#environment-variables)
- [Tests](#tests)
- [Deploy](#deploy)
  - [Setup](#setup-1)
  - [Manual Deploy](#manual-deploy)
- [Docs](#docs)

# Setup
First, create a new python environment.
```
$ python3 -m venv venv
$ source ./venv/bin/activate
```

Now install all the requirements.
```
$ pip install -r requirements.txt
```

Finally, run the app. Read [Environment Variables](##environment-variables) section before running this command.
```
$ uvicorn app.main:app --reload
```

If during development you add any dependencies, remember to run:
``` 
pip freeze > requirements.txt
```

# Database Versions
If there is a change on the alembic/versions directory, you should run the following command to update your db to the last state:
```
alembic upgrade head
```
If you already have some data in it, and there are changes adding columns not nullable, maybe you will have to delete those records to avoid errors.

# Environment Variables
To set custom environment variables, ou should add them in the run command.
```
$ API_KEY=apikey ENV=development DB_USER=dbuser DB_PWD=dbpwd DB_HOST=dbhost DB_PORT=dbport DB_NAME=dbname uvicorn app.main:app --reload
```
Filling each environment variable with your desired values.

For test purposes you will see that the ENV variable is set to Test by default. And if it's test, the DB will be a file.

# Tests
For tests and coverage run the following command:
```
$ coverage run -m pytest
$ coverage report
```

# Deploy
## Setup
Create heroku remote
```
heroku git:remote -a spotifiuby-backend-users
```

## Manual Deploy
After any change, run:
```
git push heroku main
```
For this to run successfully, you should push the changes to the main branch of your repo.

To open your default browser with the app:
```
heroku open
```

# Docs
To read the interactive docs to
http://yourAPIdomain/docs