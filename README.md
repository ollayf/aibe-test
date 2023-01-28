# aibe-test

## Setup instructions

### 1. Create a google service account
This service account grants access to google sheets and google cloud buckets

https://cloud.google.com/iam/docs/creating-managing-service-accounts

Grant the account role 'Storage Access Admin'

Export the account key as a JSON ([instructions](https://stackoverflow.com/questions/46287267/how-can-i-get-the-file-service-account-json-for-google-translate-api))

Rename the JSON to `credentials.json` and store it in the root of this project.

### 2. Create a google sheet

Create a google sheet from the [following template](https://docs.google.com/spreadsheets/d/1T5P6UVy6jnTe_S9nnvUQ-P17xrCBq_rtQDOx1SttcD4/edit?usp=sharing) ['File' -> 'Make a copy']

Grant edit access to the service account.

### 3. 