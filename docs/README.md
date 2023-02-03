# API use
## Happy path

Load [postman collection](v1.postman_collection.json) for reference

Step 1: Call `GET /prompts` to get prompts
Step 2: Call `POST /auth` to get JWT token using `username: shine, password: shine` as credentials
Step 3: Call `POST /recordings` with form-data and relevant fields to upload recording.
Step 4: View recording data in google sheet

## JWT Token Header
- Add Header: Authorization
- JWT <token>

## Adding file
- When Adding the file on Postman, make sure path is correct. Can edit in headers tab