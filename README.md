# Priolo Inventory - Web App

tbd

## Run the application

To run the application it is necessary docker and docker-compose installed on your machine. Moreover you need Grunt installed globally

First of all, clone this repository. After that run the following command in the root folder:

```
npm install
```

```
npm start
```

It will ask you your gmail credentials. It is necessary to send invitation email. In this case you should do an addictional step in gmail to allow your account to send email. You could skip this step. If the credentials are empty, the invitation is created at db level, but the email will not be sent.

Moreover, you should provide a valid Google Maps API Key to use the place section.

Finally, create the client_secret.json file with the information to allow Google Authentication inside the folder ```server/src```

After that you can access the application at:

http://localhost

## Docker structure

There are 4 services defined in docker compose:

1. client: carbon image that hosts the client of the application based on VUE.js
2. server: carbon image that hosts the API served via express.js
3. server-database: mangoDb image
4. proxy: nginx image that works as proxy between client and server