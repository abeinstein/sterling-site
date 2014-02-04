Sterling
=============
### **IMPORTANT: API is currently down as we are dealing with Facebook ToS issues**

~~To get started with sterling, visit our webiste at www.sterlingshare.com. Right now, we have an iOS frontend and an API.~~

## API Documentation
To start using the API, you need to have a Facebook app. The API only works on users that have signed up for your Facebook app.
Refer to the Facebook documentation to get started with the Facebook API.

Once you have a Facebook App with some users, register for an account on our website. You will need your app's Facebook ID 
to register.

After you have registered, make the following calls to access the API:


1) **POST**: `www.sterlingshare.com/api/register/`
This registers your request, and starts running the algorithms for the particular user. It takes the following parameters:
* `app_facebook_id`: Your app's Facebook ID
* `facebook_id`: The user's Facebook ID
* `oauth_token`: The OAuth Token for the particular user

It returns an 201 upon success.

2) **GET**: `www.sterlingshare.com/api/friends/`
This fetches the suggestion list for the given user. It takes the following parameters:
* `app_facebook_id`: Your app's Facebook ID
* `facebook_id`: The user's Facebook ID

On success, it returns:
* `friends`: An ordered list of the user's best friends.
* `list_id`: A unique ID for the list. Save this if you wish to send invites to the users.

3) **POST**: `www.sterlingshare.com/api/friends/`
This sends a Facebook message to the selected friends. It also collects statistics that you can see on the website.
It takes the following parameters:
* `list_id`: The ID of the suggestion list returned by the GET request.
* `friends_seen`: A list of the friends that the user saw (i.e. were on the front page). If you don't know, feel free to include 
all of the users friends. 
* `friends_invited`: A list of the friends that the user selected to invite. WARNING: A private facebook message will be sent to each of these users.

It returns a 200 on success.


