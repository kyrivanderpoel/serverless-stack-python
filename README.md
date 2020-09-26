# notes-app-api
serverless-stack notes app built using Python and Flask.

## Getting Started
This is my workflow for setting up this project. Please replace any steps with your personal preference when applicable.


After you pull the repo and change to the repo directory you can start installing some depend
```
npm install -g serverless
npm install
virtualenv venv --python=python3
source venv/bin/activate
pip install
sls deploy -v
```

Anytime you start a new terminal & enter the project you should execute the following.

```
source venv/bin/activate
export FLASK_APP=./notes/app.py
```

Start the development server.
```
sls wsgi serve
```

## Examples
```
$ flask auth create-user --email kyri@coolperson.com --password 'coolpasswordT!1'
{
  "user": {
    "user_id": "kyri@coolperson.com"
  }
}

$ flask auth create-user --email kyri@coolperson.com --password 'coolpasswordT!1'
{
  "message": "An account with the given email already exists.",
  "status_code": 400
}

$ flask note create --user-id kyri@coolperson.com --attachment "whateverforever123.jpg" --content "someothercontent" --password 'mypasswordT!1'
{
  "message": "User is not confirmed.",
  "status_code": 400
}
{
  "message": "User is not authenticated.",
  "status_code": 400
}
{
  "message": "User is not authenticated.",
  "status_code": 400
}

$ flask auth confirm --email kyri@coolperson.com
{
  "message": "Confirmed account for kyri@coolperson.com."
}

$ flask note create --user-id kyri@coolperson.com --attachment "whateverforever123.jpg" --content "someothercontent" --password 'mypasswordT!1'
{
  "message": "Login successful for kyri@coolperson.com."
}
{
  "note": {
    "attachment": "whateverforever123.jpg",
    "content": "someothercontent",
    "created_date": "2020-09-26T09:24:28.706624",
    "note_id": "9a8845fa-35d4-463d-b9ec-dcd3d8a75653",
    "user_id": "kyri@coolperson.com"
  }
}
{
  "message": "Logout successful for kyri@coolperson.com."
}

$ flask note list --user-id kyri@coolperson.com --password 'mypasswordT!1'
{
  "message": "Login successful for kyri@coolperson.com."
}
{
  "notes": [
    {
      "attachment": "whateverforever123.jpg",
      "content": "someothercontent",
      "created_date": "2020-09-26T09:24:28.706624",
      "note_id": "9a8845fa-35d4-463d-b9ec-dcd3d8a75653",
      "user_id": "kyri@coolperson.com"
    }
  ]
}
{
  "message": "Logout successful for kyri@coolperson.com."
}

$ flask note get --user-id kyri@coolperson.com --password 'mypasswordT!1' --note-id 9a8845fa-35d4-463d-b9ec-dcd3d8a75653
{
  "message": "Login successful for kyri@coolperson.com."
}
{
  "note": {
    "attachment": "whateverforever123.jpg",
    "content": "someothercontent",
    "created_date": "2020-09-26T09:24:28.706624",
    "note_id": "9a8845fa-35d4-463d-b9ec-dcd3d8a75653",
    "user_id": "kyri@coolperson.com"
  }
}
{
  "message": "Logout successful for kyri@coolperson.com."
}
```
