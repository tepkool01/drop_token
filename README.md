# Drop Token back-end implementation
This infrastructure and code will allow for game sessions to validate moves and state conditions throughout the duration of multiple games.

## Installation
This installation is in 2 parts: a bootstrapping phase and a infrastructure deployment phase. The bootstrapping process sets up the s3 bucket and uploads the required code/artifacts to be leveraged in the 2nd process.

### Pre-requisites
- An active AWS account with write access to API Gateway, DynamoDB, Lambda, CloudFormation, and IAM
- This repo cloned or downloaded to your local machine
- Some basic knowledge of AWS (s3 and cloudformation preferred)

### Installation Steps (GUI / AWS Console way)
1. Login to AWS and Navigate to the "CloudFormation" service via links: "Services"->"CloudFormation"
2. Click link "Create stack"->"With new resources"
3. Under 'Specify template' section, select 'Upload a template file' and select the file in this repo: ```infrastructure/bootstrap.yml```
4. Click "Next"
5. Input valid parameter values
    * **Stack Name** can be anything within the RegEx defined in the description
        * I.E. mine was *drop-token-bootstrap*
    * **ArtifactsBucketName** must be a unique name in the global namespace of S3 Buckets that conforms to S3 naming conventions.
        * I.E. mine is *drop-token-artifacts*, and yours could use that name with a random number appended to the end
6. Click "Next"
7. Click "Next" again
8. Click "Create stack" and visually confirm that your stack is in the status **CREATE_COMPLETE** 
9. Navigate to your newly created bucket name via: "Services"->"S3"->"*ArtifactsBucketName*"
    * *ArtifactsBucketName* was created in step 5
10. Upload all files in ```services/``` folder from this repo into the S3 bucket
    * Maintain the integrity of the folder structure (you may need to manually create folder names)
11. Repeat the above steps (1-4 and 6-8), swapping out the file in step 3 for ```infrastructure/master.yml```
    * Make sure to tick the checkbox on the last screen '*I acknowledge that AWS CloudFormation might create IAM resources.*'

## Notes / Tips
- Whichever region you deploy the CFT in, will be the region where all the resources are deployed
- Placing the open api yml file into **https://editor.swagger.io/** will give developers a GUI to view the file

## Legend
- Double quotes "link" indicate links to be clicked
- Single quotes 'section' indicate sections
- **bold** items are input names or identifiers
- Arrows -> indicate continued navigation or linked instructions that are dependent on one another
- ```code blocks``` indicate code, files, or filenames