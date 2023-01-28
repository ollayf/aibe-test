# aibe-test

## Pending work
- integrate audio file predictor

## API usage
See [here](docs/README.md)

## Setup instructions

### 1. Create a google service account
This service account grants access to google sheets and google cloud buckets

https://cloud.google.com/iam/docs/creating-managing-service-accounts

Grant the account role 'Storage Access Admin'

Export the account key as a JSON ([instructions](https://stackoverflow.com/questions/46287267/how-can-i-get-the-file-service-account-json-for-google-translate-api))

Rename the JSON to `credentials.json` and store it in the root of this project.

### 2a. Create a storage bucket
See (here)[https://cloud.google.com/storage/docs/creating-buckets]
After creating bucket, go to (storage.py)['./services/storage.py'] and add in
### 2b. Create a google sheet
Create a google sheet from the [following template](https://docs.google.com/spreadsheets/d/1T5P6UVy6jnTe_S9nnvUQ-P17xrCBq_rtQDOx1SttcD4/edit?usp=sharing) ['File' -> 'Make a copy']

Rename the google sheet to '[SHINE] AIBE test data' (name is hardcoded in [code](services/gsheet.py))

Grant edit access to the service account.

### 3. Run project
Create docker image

```docker build --tag shine-aibe .```

Run on http://localhost:5001

```docker run -d -p 5001:80 shine-aibe```



## Further works
1. Abstract env configuration file to safely store JWT secret
2. Swagger docs
3. Add a more robust class for google sheet: difficult to add new fields and ensure columns are 'aligned'
4. Fix hardcoding of google sheet name, project id, storage bucket (ideally done when env vars are set up)
5. Use production settings for app [ref](https://flask.palletsprojects.com/en/2.2.x/tutorial/deploy/)