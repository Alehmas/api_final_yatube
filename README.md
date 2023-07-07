# REST API for YaTube social network.

##  Description
Add-on for working through the API to the [Yatube](https://github.com/Oleg-2006/yatube_project) social network project. 
The Yatube project is a social network. It will allow users to create an account,
post entries, subscribe to their favorite authors, and tag their favorites.

##  Technologies used
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

### Available functionality
* JWT tokens are used for authentication.
* Unauthenticated users have read-only access to the API.
* The /follow/ endpoint has an additional restriction. It can only be accessed by authenticated users.
* Authenticated users are allowed to modify and delete their content, otherwise access is read-only.
* Subscriptions to users.
* View, create, edit and delete entries.
* View and create groups.
* Ability to add, edit, delete your own comments and view others.
* Filtering by fields.

##  Run the project locally
- Clone the repository
```
git clone git@github.com:Alehmas/api_final_yatube.git
```
- Move to a new directory
```
cd api_final_yatube
```
- Initialize the virtual environment
```
python -m venv venv
```
- Activate the virtual environment
```
source venv/Scripts/activate
```
- Update pip and set project dependencies
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
- From the directory with the file `manage.py` run the migrations
```
python manage.py migrate
```
- Create a superuser
```
python manage.py createsuperuser
```
- Collect statics
```
python manage.py collectstatic
```
- To disable debug mode, change `yatube.settings.py' to
```
DEBUG = False
```
- Project launch
```
python manage.py runserver
```
- Fill out the database

##  Programs for sending requests

### Program options for sending requests
* API testing via httpie - API console client.
If you like this console API client, [you can find installation instructions there, on the developers' website.](https://httpie.io/docs/cli/installation)

* API Testing with VS Code Extension
The extension [REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) allows you to send HTTP requests directly from VS Code and view responses to them in the same interface.

* API Testing with Postman
Postman is a popular and convenient API client that can send requests and show responses, save request history and authentication data, and allow you to design and test API.
[Download Postman from the download page](https://www.postman.com/downloads/) project and install it on your work machine.


## Document examples:

`api/v1/posts/` (POST)create a new post
```
{
  "text": "string",
  "image": "string",
  "group": 0
}
```
`api/v1/posts/{post_id}/` (GET, PUT, PATCH, DELETE): get, edit or delete a post by id
```
{
  "text": "string",
  "image": "string",
  "group": 0
}
```
`api/v1/posts/{post_id}/comments/` (POST):create a new one, specifying the id of the post we want to comment on.
```
{
  "text": "string"
}
```
More detailed documentation on queries can be found in the running project at http://127.0.0.1:8000/redoc/

## Authors
- [Aleh Maslau](https://github.com/Alehmas)