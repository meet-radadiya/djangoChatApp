# NeoFI - ChatApp

### Features:
#### 1. User authentication
* User registration with validation
* User login with validation of credentials
#### 2. Real-time chat functionality
* Retrieving list of online users
* Initiating chat with an online user
* Sending and receiving messages in real-time
#### 3. Friends recommendation
* API to recommend friends based on user interests
#### 4. Error handling
* Return appropriate errors for validation, authentication failures etc.
#### 5. Token-based authentication
* Login generates token, logout invalidates token
#### 6. High performance Redis caching backend
* Track online users in Redis set instead of database
* Signals to update Redis on login/logout
* API to fetch online users from Redis
* Improved performance compared to database lookups
### Installation:
#### 1. Clone this repository:
* `git clone https://github.com/meet-radadiya/djangoChatApp.git`
#### 2. Create virtual environment:
* `sudo apt install virtualenv`
* `virtualenv --python='/usr/bin/python3.6' venv`
* `source venv/bin/activate`
* `cd django_assignment/`
#### 3. Install dependencies:
* `pip install -r requirements.txt`
#### 4. Install postgresql:
* `wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -`
* `sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -sc)-pgdg main" > /etc/apt/sources.list.d/PostgreSQL.list'`
* `sudo apt update`
* `sudo apt-get install postgresql-10`
#### 5. Create database:
* `sudo su - postgres`
* `postgres@xxx:~$ psql`
  * `create database <db_name>;`
  * `create user <admin_name> password ;`
  * `grant all privileges on database <db_name> to <admin_name>;`
  * `postgres=# \q`
  * `postgres@xxx:~$ exit`
#### 6. Install redis:
* `sudo apt-get install redis-server`
#### 7. Create local.py in djangoChatApp/:
* local.py content:
```python
import redis
DEBUG = True
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': '<database_name>',
    'USER': '<admin_name>',
    'PASSWORD': '<password>',
    'HOST': '<hostname>',
    'PORT': '<port>',
  }
}
SECRET_KEY = '<secret_key>'

REDIS_HOST = '<hostname>'
REDIS_PORT = '<port>'

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

CHANNEL_LAYERS = {
  'default': {
   'BACKEND': 'channels_redis.core.RedisChannelLayer',
   'CONFIG': {'hosts': [(REDIS_HOST, REDIS_PORT)]},
  }
}
```
#### 8. Run migrations:
```
python3 manage.py migrate
```
#### 9. Create superuser:
```
python3 manage.py createsuperuser
```
#### 10. Run the server:
```
python3 manage.py runserver
```
#### 11. Start redis server:
```
redis-server
```
#### 12. Browse below urls:
* Documentation: - http://localhost:8000/swagger/
* Alternate Documentation: - http://localhost:8000/redoc/
* Admin Panel: - http://localhost:8000/admin/