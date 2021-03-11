<a href="https://labs.play-with-docker.com/?stack=https://raw.githubusercontent.com/coolhva/ecapi/main/pwd.yml">
  <img src="https://raw.githubusercontent.com/play-with-docker/stacks/master/assets/images/button.png" alt="Try in Play With Docker"/>
</a>

# Email.Cloud IOC API Management
This repo contains the source code for the Email.Cloud API (ECAPI) docker container. Email.Cloud allows the use of Indicators Of Compromise (IOC) to manage in- and outbound email based on given criteria.

Please find the IOC API PDF Documentation [here](https://techdocs.broadcom.com/content/dam/broadcom/techdocs/symantec-security-software/email-security/email-security-cloud/generated-pdfs/Indicators-of-Compromise-(IOC)-Blacklist-API-Guide.pdf).

![main_interface](https://raw.githubusercontent.com/coolhva/ecapi/main/docs/ecapi_main.png)

## Running the docker container
Clone or Download and extract the ZIP file of this repository and issue the following command to build the docker container:

```shell
docker build -t ecapi .
```
Then issue the following command to run the docker container:
```shell
docker run --name ecapi -d -p 8000:5000 -v /docker/db:/home/ecapi/db ecapi:latest
```
This will start a docker container listening on port 8000 on the docker host and binds the folder ```/docker/db``` to the folder where the docker container stores its (SQLite) database. The ```-v /docker/db:/home/ecapi/db``` parameter is optional, without the parameter it will use the db inside the container.

**Optional environment variables**

|Environment variable|Default|Description
|:---|:---|:--|
|SECRET_KEY|7Ghy648FibRfcgQ...AxdTFB2Brz|Used by the Flask server to encrypt sessions|
|SQLALCHEMY_DATABASE_URI|sqlite://./db/app.db|Used to point to a database that holds the users and domains|
|SERVER_NAME|Empty|External url used generate link in password reset email (test first without setting this parameter)|
|PREFERRED_URL_SCHEME|http|Used in conjunction with SERVER_NAME, https if TLS is used (test first without setting this parameter)|
|LOG_TO_STDOUT|False|If True logs will send to STDOUT|
|ADMIN_EMAIL|Empty|Administrator email to receive errors from the application|
|MAIL_SERVER|Empty|IP or DNS name of mail server|
|MAIL_PORT|25|TCP Port of mailserver|
|MAIL_USE_TLS|Empty|If set to True it will use TLS when sending email|
|MAIL_USERNAME|Empty|Username for the mailserver|
|MAIL_PASSWORD|Empty|Password for the mailserver|
|MAIL_FROM|Empty|From Email address used in password reset mail|
|ECAPI_URL|https://iocapi.emailsecurity.symantec.com/|Base URL for IOC API|

1. Go to http://dockerhost:8000/

   Register yourself a new user and enter your ClientNet credentials for the API (it is recommended to create a seperate API user in the ClientNet portal).
   
   ![register_user](https://raw.githubusercontent.com/coolhva/ecapi/main/docs/register.png)
   
2. ***(optional)*** After logging in add your domains if you have domain specific IOC configuration.
3. Now you can start using the application by showing the current IOC's, use the + sign to add new IOC's or use the bulk upload functionality.

## Run code in your development environment

1. Download/clone this repository
2. In the root directory issue the ``` python -m venv venv``` command to create a virtual environment
3. Activate the virtual environment, e.g. in linux ``` source venv/bin/activate```
4. Install requirements via ```pip install -r requirements.txt```
5. Create database with ```flask db upgrade```
5. Start flask ```flask run```
6. Visit the web application at http://localhost:5000/
