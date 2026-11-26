# AWS & Docker Setup Guide

## AWS SSH Access
To connect to an AWS EC2 instance using SSH:
```sh
ssh -i <key-pair-file-location> <username>@<ip-address>
```
**Example:**
```sh
ssh -i /Users/dhanesh/Documents/keys/EC2-mac-test.pem ec2-user@123.45.67.89
```

## Installing Docker on AWS
```sh
sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo usermod -aG docker ec2-user   # Allow EC2 user to access Docker
```

---

# Docker Commands

## Building & Running Containers
- **Build an image:**
  ```sh
  docker build -t node-image-app .
  ```
  `-t` is used to specify the image name.

- **Run a container:**
  ```sh
  docker run -it --rm -p 4000:4000 -d --name <container-name> <image-id>
  ```
  - `-p 4000:4000` → Maps port 4000 of the container to port 4000 on the host.
  - `-d` → Runs the container in detached mode.
  - `--name` → Assigns a custom name to the container.
  -it ---> opens the terminal 
  --rm --> removes when we exit the container
## Managing Containers & Images
- **List all running containers:**
  ```sh
  docker ps
  ```
- **List all containers (including stopped ones):**
  ```sh
  docker ps -a
  ```
- **List all images:**
  ```sh
  docker image ls
  ```
- **Pull an image from Docker Hub:**
  ```sh
  docker pull <image-name>
  ```
- **Stop a container:**
  ```sh
  docker stop <container-id>
  ```
- **Start a container:**
  ```sh
  docker start <container-id>
  ```
- **Remove a container:**
  ```sh
  docker rm <container-id> -f  # -f forces removal
  ```
- **Remove an image:**
  ```sh
  docker rmi <image-id>
  ```

## Running Commands Inside a Container
- **Access a running container:**
  ```sh
  docker exec -it <container-id> bash
  ```
  This allows interactive access to the container’s shell.

- **View logs from a container:**
  ```sh
  docker logs <container-name> -f
  ```
- **Inspect container details:**
  ```sh
  docker inspect <container-id>
  ```

---

# Docker Volumes & Mounts

## Bind Mounts
- **Run a container with a bind mount:**
  ```sh
  docker run -v <local-dir>:<container-dir>:<permissions> -p 4000:4000 -d <image-id>
  ```
  - `permissions`: `ro` for read-only access.

  docker run  -it --rm --mount type=bind,source="${PWD}"/my-data,destination=/my-data ubuntu:22.04

## Docker Volumes
- **List all volumes:**
  ```sh
  docker volume ls
  ```
- **Remove unused volumes:**
  ```sh
  docker volume prune
  ```
- **Remove a volume when deleting a container:**
  ```sh
  docker rm <container-id> -fv
  ```
- **Remove a specific volume:**
  ```sh
  docker volume rm <volume-name>
  ```
# Create a container and mount the volume into the container filesystem
docker run  -it --rm --mount source=my-volume,destination=/my-data/ ubuntu:22.04

---

# Docker Compose

## Basic Commands
- **Start containers:**
  ```sh
  docker-compose up
  ```
- **Stop and remove containers, networks, and volumes:**
  ```sh
  docker-compose down -v
  ```
- **Start in detached mode and force a rebuild:**
  ```sh
  docker-compose up -d --build
  ```
- **Use multiple compose files:**
  ```sh
  docker-compose -f <file1.yml> -f <file2.yml> up -d --build
  ```
- **Scale a service:**
  ```sh
  docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d --scale <service-name>=2
  ```

---

# MongoDB in Docker

## Access MongoDB Shell
```sh
mongosh -u "mongoAdmin" -p "Test@1234"
```

---

# Docker Networking

## Bridge Networks (Review Needed)
To create and use a custom bridge network:
```sh
docker network create my-bridge-network
```
Attach containers to this network:
```sh
docker run -d --name container1 --network my-bridge-network <image-name>
docker run -d --name container2 --network my-bridge-network <image-name>
```
Check network details:
```sh
docker network inspect my-bridge-network
```

---

### 🚀 Happy Coding! Let me know if you need any improvements!

