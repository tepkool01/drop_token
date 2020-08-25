# Drop Token back-end implementation
This infrastructure and code will allow for game sessions to validate moves and state conditions throughout the duration of multiple games.

### Pre-requisites
- An active AWS account with write access to API Gateway, DynamoDB, Lambda, CloudFormation, and IAM
- This repo cloned or downloaded to your local machine
- Some basic knowledge of AWS (s3 and cloudformation preferred)

### Installation Steps (GUI / AWS Console way)
#### TLDR
- Login to AWS, go to CloudFormation, and deploy this template as any name
- The outputs tab (when it finished) will give you the BASE URL for the API
- An example endpoint would be GET BASE_URL/drop_token

#### Long Description
1. Login to AWS and Navigate to the "CloudFormation" service via links: "Services"->"CloudFormation"
2. Click link "Create stack"->"With new resources"
3. Under 'Specify template' section, select 'Upload a template file' and select the file in this repo: ```infrastructure/master.yml```
4. Click "Next"
5. Input valid parameter values (or keep defaults and move on)
6. Click "Next"
7. Click "Next" again
8. Click "Create stack" and visually confirm that your stack is in the status **CREATE_COMPLETE** 
9. Check the outputs tab for the BASE URL of the API
10. Invoke endpoints using postman/curl/etc (just can't be a CORS service)

### Cleanup
I apologize I didn't create a better clean-up process.
1. Navigate to the S3 bucket created by CloudFormation
2. Delete the s3 key: lambda.zip
3. Delete the s3 bucket
4. Delete the stack from CloudFormation

## Notes / Tips
- All the code for the business logic is located in `./services/drop_token`
- Placing the open api yml file into **https://editor.swagger.io/** will give developers a GUI to view the file