# Image Processing Application

This repository contains the code required to deploy an image processing application. It is built using Svelte (front-end), Flask (Python-based API framework as the back-end) and MongoDB (persistent storage).

## Local Installation

- Build the stack: `docker-compose build`
- Run the stack: `docker-compose up`
- Remove the stack: `docker-compose down`
- Log in to the mongo shell when the container is running via `docker exec -it <container_id> mongo`
- Obtain `conainer_id` by running `docker ps`
- Application will start at `localhost:5000`
