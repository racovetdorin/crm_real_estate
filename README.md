# CRMRMX

``````
Runs on Python 3.8, Django 3.1 and Django REST Framework 3.11
# after cloning the project
install docker
install docker-compose
make docker/docker-compose run without sudo (check tutorials)
install nvm (check tutorials)
nvm install 14
npm install -g gulp-cli
install yarn (check tutorials)

1. create a .env folder in root, ask someone in the team for the env variables
2. in root: docker-compose up --build
3. offers/api.py comment line 59 and 60
4. in root: docker-compose exec web ./manage.py migrate
5. offers/api.py uncomment line 59 and 60
6. in ui/static: cp node_modules/bootstrap-maxlength/dist/bootstrap-maxlength.min.js node_modules/bootstrap-maxlength
7. in ui/static: yarn install
8. in ui/static: gulp build
9. in root: docker cp ui/static/dist/. impaktcrm-web-1:/app/ui/static/dist/
10. in ui/static: docker-compose exec web ./manage.py collectstatic
11. in root: docker-compose exec web ./manage.py createsuperuser```
```
```
For windows:

install docker
install docker-compose
install npm in ui/static/ (check for documentation on web -> https://phoenixnap.com/kb/install-node-js-npm-on-windows)
npm install -g gulp-cli
install nvm 14 (check for documentation on web  -> https://docs.microsoft.com/en-us/windows/dev-environment/javascript/nodejs-on-windows)
install dox2unix -> https://sourceforge.net/projects/dos2unix/

1. create a .env folder in root, ask someone in the team for the env variables
2. in root: docker-compose up --build
3. offers/api.py comment line 59 and 60
4. in root: docker-compose exec web ./manage.py migrate . If "/usr/bin/env: "python3\r": No such file or directory" error is raised:
    -> 4.1 - dos2unix.exe ./manage.py. Continue the installation otherwise.
5. offers/api.py uncomment line 59 and 60
6. in ui/static: gulp build
7. in ui/static: docker-compose exec web ./manage.py collectstatic
8. in root: docker-compose exec web ./manage.py createsuperuser


```

```
After the completion of steps, the following commands should be run:

docker-compose up
docker-compose exec web rsync -arv ui/templates_default/ ui/templates
docker-compose exec web rsync -arv ui/templates_rmm/ ui/templates
docker-compose exec web ./manage.py showmigrations
docker-compose exec web ./manage.py migrate
docker-compose exec web ./manage.py makemessages --all
docker-compose exec web ./manage.py compilemessages
docker-compose exec web ./manage.py collectstatic --noinput (This can be also ignored.)
docker-compose restart web

```



DEBUG=True

SECRET_KEY=anything # dummy

PSQL_DB_NAME=impakt # dummy
PSQL_DB_USER=user # dummy
PSQL_DB_HOST=db # dummy
PSQL_DB_PORT=5432
PSQL_DB_PASSWORD=passowrd # dummy

BASE_DOMAIN='localhost'
 
EMAIL_HOST_USER= # check with server admin
EMAIL_HOST_PASSWORD= # check with server admin
```

```
How to dump database from a backup file:

1) Place your 'backup.sql' file in the root of the project, next to loaddb.sh script.
2) Run: docker-compose exec web (or service container from docker yml) bash
3) Run: chmod 777 loaddb.sh | ./loadd.sh (from bash) OR ./loaddb.sh if you granted 777 permissions
```

- ```docker-compose up --build```

- before ```./manage.py migrate```, in ```properties/filters.py``` and ```offers/api.py``` comment this:
```python
features = Feature.objects.filter(is_filtered=True)

for feature in features:
    filtered_features['_'.join(feature.name.lower().split())] = django_filters.CharFilter(label=_(feature.name),
                                                                                       field_name='features')

locals().update(filtered_features)
```

- ```docker-compose exec web bash```

    -   ```>> ./manage.py migrate```

    -   ```>> ./manage.py fixture_script```

    -   ```>> ./manage.py compilemessages```
  

- uncomment previously mentioned snippets

***
- Possible problems with node.js: if binding errors, change node.js version to 14.x

- Possible problems with gulp: if gulp-cli/gulp module not found, try ```export PATH=/usr/share/nodejs/gulp/bin/:$PATH``` (or where gulp.js is located on your system)
***

xxx
