# Demo Instructions

Notes and instructions for building and running an image for demonstration during the **#Meetup**.

## Build the image

Build the image by executing the following:

```shell
docker build -t joelwking/semaphore:1.0 -f Docerfile.deploy .
```

while substituting the username version in the tag `-t` value above.

## Test the image

I used Windows 10 to develop and run this code in the VS Code development environment. Now run the image manually.

```shell
docker run -it -d joelwking/semaphore:1.0
```

In the Windoes 10 environment, to connect to the running container to execute the code, you must invoke the `docker exec` command from PowerShell. If you issue the command in the Git bash shell you will encounter the error `docker error on windows : the input device is not a TTY. If you are using mintty, try prefixing the command with 'winpty'`.

```text
powershell
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\Users\jwking> docker exec -it 72 /bin/bash
```

When satisfied with the configuration of the container image, exit from the terminal session using  `CTL + SHIFT P Q`.

Stop the container using `docker stop <container_id>`.

## Save the image

Using Windows 10 as an example, save the image to a tar file:

```shell
docker save --output Downloads\semaphore.tgz joelwking/semaphore:1.0
```

## Copy and Load the file on your demo server

In this demonstration, we have created a Digital Ocean Droplet `ubuntu-s-1vcpu-1gb-nyc3-01 / 1 GB Memory / 25 GB Disk / NYC3 - Ubuntu 22.04 (LTS) x64` after connecting to the Droplet, create a user `semaphore`, install docker and add the user to the `Docker` group.

```shell
apt install docker.io
apt install net-tools
adduser semaphore
sudo usermod -aG docker semaphore
```

Using `scp` we have uploaded the image to the Droplet, enter the directory where the `tar` file was staged, and load it.

```shell
docker load < semaphore.tgz
```

## Run multiple instances of the container

For the demonstration, run an instance of the container to publish and to consume. The environment variables providing the API keys for both the Meraki dashboard and the Confluent Cloud cluster are defined in `.env/vars`. Edit this file on the Ubuntu Droplet with the correct credentials. Then run as the publisher and consumer.

```shell
mkdir .env
semaphore@ubuntu-s-1vcpu-1gb-nyc3-01:~$ chmod 700 .env
```

Provide the appropriate credentials in the file `.env/vars`.

Now run an instance of the publisher container.

```shell
docker run -it --name publisher --env-file .env/vars -d joelwking/semaphore:1.0 
docker exec -it publisher /bin/bash
```

And run an instance of the consumer container.

```shell
docker run -it --name consumer --env-file .env/vars -d joelwking/semaphore:1.0 
docker exec -it consumer /bin/bash
```

After you have connected to the TTY of the running containers, change directory to the `library` and execute the publisher `python latency_loss_logging.py -h` and the consumer `python consumer.py -h` to publish and consume latency and loss messages from Meraki to Kafka.

### Author

Joel W. King @joelwking