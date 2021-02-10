# Email.Cloud IOC API Management
This repo contains the source code for the Email.Cloud API (ECAPI) docker container. Email.Cloud allows the use of Indicators Of Compromise (IOC) to manage in- and outbound email based on given criteria.

## Running the docker container
Please issue the following command on a docker host to run the docker container:
```shell
docker run --name ecapi -d -p 8000:5000 -v /docker/db:/home/ecapi/db coolhva/ecapi:latest
```
This will start a docker container listening on port 8000 on the docker host and binds the folder ```/docker/db``` to the folder where the docker container stores its (SQLite) database. The ```-v /docker/db:/home/ecapi/db``` parameter is optional, without the parameter it will use the db inside the container.

1. Go to http://dockerhost:8000/

   Register yourself a new user and enter your ClientNet credentials for the API (it is recommended to create a seperate API user in the ClientNet portal).
   
   ![register_user](https://raw.githubusercontent.com/coolhva/ecapi/main/docs/register.png)
   
2. ***(optional)*** After logging in add your domains if you have domain specific IOC configuration.
3. Now you can start using the application by showing the current IOC's, use the + sign to add new IOC's or use the bulk upload functionality.

![main_interface](https://raw.githubusercontent.com/coolhva/ecapi/main/docs/ecapi_main.png)

## Run code in your development environment

1. Download/clone this repository
2. In the root directory issue the ``` python -m venv venv``` command to create a virtual environment
3. Activate the virtual environment, e.g. in linux ``` source venv/bin/activate```
4. Install requirements via ```pip install -r requirements.txt```
5. Create database with ```flask db upgrade```
5. Start flask ```flask run```
6. Visit the web application at http://localhost:5000/
