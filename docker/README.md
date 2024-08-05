
# Docker

## Frequent Use Docker command

-  Build Image

    <pre>  docker build -t {module_name}:{tag_id} . </pre>

-  Run Image

    <pre> docker run {module_name}:{tag_id} </pre>

-  List Image

    <pre> docker image list </pre>    

-  Remove Image

    <pre> docker rmi {module_name}:{tag_id} </pre>    

- Remove Images with none:none

    <pre> docker image prune </pre>


-  List Container    

    <pre> docker ps -a </pre>

-  Stop Container

    <pre> docker stop {container_id} </pre>

-  Remove Container

    <pre> docker rm {container_id} </pre>

 - Attached to a Container

    <pre> docker exec -it {container_id} /bin/sh

## Docker File Sample

## VOLUME

In DockerFile, add the following :

    # VOLUME {path INSIDE container}
    VOLUME ./resources/  

then, run the image with command :

    docker run -v {host folder}:{container folder} -t {image_tag}


## Networking

First of all, in Dockerfile, should expose the service port as the following:

    #EXPOSE {port num}
    EXPOSE 5000

[TO BE CONFIRM]
later in docker command, run image with option -p as following:

    docker run -p


<br><br>

# Docker-Compose

## docker-compose.yml sample



    version: "3.81"

    services:

    homebot:
        restart: always
        build: homebot
        container_name: homebot
        ports:
        - 9999:9999
        volumes:
        - type: bind
            source: /home/brandicast/bot/homebot/resources/
            target: /opt/homebot/resources/

    gemini_agent:
        restart: always
        container_name: gemini_agent
        build: gemini_agent
        ports:
        - 5000:5000
        volumes:
        - type: bind
            source: /home/brandicast/bot/gemini_agent/resources
            target: /code/resources
        - type: bind
            source: /home/brandicast/bot/gemini_agent/history
            target: /code/history

    volumes:
    config:
    data:
    log:

## docker-compose commands

- build all

    ```
    docker-compose -f docker-compose.yml build
- build one of the service
    ```
    docker-compose build {service name}
- run
    ```
    docker-compose -f docker-compose.yml up
- stop 
    ```
    docker-compose -f docker-compose down

