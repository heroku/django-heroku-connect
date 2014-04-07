# Django Heroku Connect Client

Heroku Connect syncs data from Salesforce into a database. This is an
application which provides models and factories for the database tables Heroku
Connect creates.

**NOTE**: This app assumes you have synced all of the standard fields/objects
and only those fields/objects. If your mappings are unique, you will need to
fork this repo and modify the models and factories to suit your application.

## Example Project

A sample Django project is included in this repo, along with a settings module
which requires a the following environment variables to function properly:

 * **HEROKU\_CONNECT\_DATABASE\_URL**: URL used to connect to your Heroku
   Connect database.
 * **HEROKU\_CONNECT\_SCHEMA**: Schema name you chose when setting up Heroku
   Connect
