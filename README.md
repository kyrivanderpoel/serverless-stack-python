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

Create a note using the local server. Make sure you have `sls wsgi serve` in another terminal.

```
$ flask note create --user-id kyri --attachment theattachment --content thecontent
{
  "note": {
    "attachment": "theattachment",
    "content": "thecontent",
    "created_date": "2020-09-25T04:34:48.597903",
    "note_id": "c515cd91-d447-420b-b3e7-012a98fb1418",
    "user_id": "kyri"
  }
}
```

```
$ flask note list --user-id kyri
{
  "notes": [
    {
      "attachment": "theattachment",
      "content": "thecontent",
      "created_date": "2020-09-25T05:24:36.168837",
      "note_id": "0a0ea446-7c1b-44c7-a483-0e3499cf92d3",
      "user_id": "kyri"
    },
    {
      "attachment": "theattachment",
      "content": "thecontent",
      "created_date": "2020-09-25T04:34:48.597903",
      "note_id": "c515cd91-d447-420b-b3e7-012a98fb1418",
      "user_id": "kyri"
    }
}
```

```
$ flask note get --user-id kyri --note-id "c99b084a-a2cb-4632-85b8-4b58f95138af"
{
  "note": {
    "attachment": "theattachment",
    "content": "thecontent",
    "created_date": "2020-09-25T04:41:11.722450",
    "note_id": "c99b084a-a2cb-4632-85b8-4b58f95138af",
    "user_id": "kyri"
  }
}
```

## Deploy
```
sls deply
```

