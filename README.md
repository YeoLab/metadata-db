# metadata-db

## Currently hosted at: [pipelines.brian-yee.com](https://pipelines.brian-yee.com)

Steps for deployment using Elastic Beanstalk:

# Setting Up and Configuring Elastic Beanstalk
### 1. Install and configure the [aws cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- For this application, it shouldn't matter which version (v1 or v2) is installed. For more information, [see documentation](https://docs.aws.amazon.com/cli/latest/userguide/cliv2-migration-changes.html)
- Add access and secrete access keys to an 'eb-cli' profile: ```aws configure --profile eb-cli```. You can generate/find these keys using the [AWS console](https://console.aws.amazon.com/iam/home?region=us-west-1#security_credential).
#### Some options to consider: 
    - Default region name: select the region closest to you (e.g. us-west-1)
    - Default output format: text/JSON, not super important for this app
### 2. Install the [elastic beanstalk cli](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install-advanced.html) (eb) with pip: 
- ```pip install awsebcli --upgrade --user```
- You can do this outside of the application environment to avoid conflicts.
### 3. Set up elastic beanstalk
- ```eb init```
#### Some options to consider
    - Use CodeCommit? I'd choose "No" and stick with Github. Main difference I can see is security/access (CodeCommit is integrated with AWS IAM roles etc. whereas Github is not). 
    - Create an ssh key/pair? Choosing "Yes" creates a pub/private key pair in your ~/.ssh/. I'd recommend to create one so you can login to your instance via ```eb ssh```
### 4. Create the environment and application
- ```eb create```
#### Some options to consider
    - DNS CNAME prefix. Use something that makes sense for this application (e.g. metadata-db-prod)
    - Load balancer type: application (2). Likely doesn't make any difference with this app
### 5. Check that .elasticbeanstalk was created, and that the config files for deployment exist
- ensure that the 'global:profile' setting matches the profile from step 1. This ties the application and its environment to your AWS account.
- you can check/modify the size of the instance used as well. For this application, the smallest instance should be good enough.

### Other configurations
#### For Django-specific applications, we will also need a 'django.config' file, in '.ebextensions'. 
    - This config file allows us to run custom commands during the deployment process. 
    - Importantly, we will need to migrate changes made to the database
    - See django.config -> container_commands -> 01_migrate for an example

#### Create RDS Database before deployment
    - In the AWS console, under your environment go to 'Configuration'. Scroll down to Database and press the 'Edit' button. Choose all defaults and create a username and password (this will be used in the future in settings.py)
    
# Deployment
- Deploying the main code:
    - Commit changes to the main or master branch
    - ```eb deploy metadata-db-test```
- Deploying uncommited code in case you just want to test:
    - Add changes with ```git add```
    - ```eb deploy --staged``` (this deploys staged changes as opposed to committed ones)
    - Sometimes you may need to include the environment name as well: ```eb deploy metadata-db-test --staged```
# Issues/troubleshooting
##### "Incorrect application version found on all instances. Expected version..." 
[stackoverflow response](https://stackoverflow.com/questions/37104699/aws-eb-error-incorrect-application-version-found-on-all-instances)

TLDR: fix deployment using either the log files or by poking around with ```eb ssh```
##### Relevant log files (inside eb instance):
- ```/var/log/cp_log``` (tracks issues related to the Django application)
- ```/var/log/cfn-init-cmd.log``` (tracks issues related to eb deployment)

# Steps for adding a SSL-protected domain:

- In Route53, lookup and select a valid domain name and purchase one.
- In elastic beanstalk console under 'environments', copy the URL (*.elasticbeanstalk.com)

- Once you have a valid domain, you will need to point the domain to your EB instance. 
    - Under Route53 -> Hosted zones -> DOMAIN, create a CNAME record (name = your domain name, value = elastic beanstalk URL)

- Now, add SSL protection (HTTPS)
    - Go to the AWS Certificate Manager (ACM) and request a new (public) certificate
    - Add your domain and select a validation method. If you choose [DNS validation](https://docs.aws.amazon.com/acm/latest/userguide/dns-validation.html), you will need to add another CNAME record. This proves that you own the domain.
    - Once verified, a certificate will be granted. Then, go to your elastic beanstalk environment console, and under
    
        Elastic Beanstalk -> Environments -> Your Environment -> Configuration -> Load Balancer:
        
        Add a new HTTPS listener. 
        
        Attach the appropriate certificate corresponding to your domain. 
        
        443 is typically the default port to use.
        
        And as of 09/22 the recommended ELB Policy 
        is [ELBSecurityPolicy-2016-08](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/elb-security-policy-table.html)
