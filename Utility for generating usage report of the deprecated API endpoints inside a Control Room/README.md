# Utility for generating usage report of the deprecated API endpoints inside a Control Room
From A360.33, the POST v1/authentication, POST v1/authentication/token, and v1/usermanagement API endpoints are discontinued and will stop working. Update your applications to use the v2 versions of these endpoints. 

Steps to follow : 

#### STEP 1: 
Download the exported bot (.zip file) from the following GitHub repository https://github.com/partnersolutiondesk/RPA/tree/main/Utility%20for%20generating%20usage%20report%20of%20the%20deprecated%20API%20endpoints%20inside%20a%20Control%20Room
 
#### STEP 2:  
Import it to your control room. 
#### STEP 3: 
Open command prompt and run the below given 'pip' commands to install the required python modules to run the script. 

##### External Libraries (Require pip install):
* requests: pip install requests
* requests_toolbelt: pip install requests-toolbelt

##### Standard Library Modules (No pip install needed):
These modules come with Python, and you can use them directly without installing anything.
* csv: 
* os:
* json: 
* shutil:
* inspect: 
* logging: 
* re
* datetime
* pathlib
* traceback
 

#### STEP 4: 
Run the bot by giving the input as shown below


![image](https://github.com/user-attachments/assets/ec3df72e-003f-4c25-94a8-abb73c6ac80e)

![image](https://github.com/user-attachments/assets/08b063d3-0547-4052-b612-10adf586a4dd)



### Sample Report :

![image](https://github.com/user-attachments/assets/7feb9f25-db83-4660-89da-efaffc388156)

