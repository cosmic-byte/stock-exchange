# Stock Exchange API

### Setup and Installation
_Note: make sure docker and docker-compose are installed_

## Development Server

### Step 1
Build the containers
```shell script
sh scripts/docker_build.sh build
```

### Step 2
Run the containers
```shell script
sh scripts/docker_build.sh up
```

or build and run with a single command
```shell script
sh scripts/docker_build.sh up --build
```

### Step 3
Open your web browser and view the application using the following urls
```
API Docs:  localhost:8001

Kibana: localhost:5601
```
### Extras
Note: all docker-compose commands works after the script
Eg: `kill`, `stop`, `--no-cache` etc.
```shell script
sh scripts/docker_build.sh down
```
```shell script
sh scripts/docker_build.sh kill
```
```shell script
sh scripts/docker_build.sh build --no-cache
```
```shell script
sh scripts/docker_build.sh run -d
```

To run unit tests
```shell script
> docker-compose -f ./docker-compose-ci.yml build
> docker-compose -f ./docker-compose-ci.yml run app
```

# Seed Test Data
Make sure the containers are up and running, then execute
```shell script
> docker exec -it stock_api bash
/var/app#  python quick_test_seeding.py 
```