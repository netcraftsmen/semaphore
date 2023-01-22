# Demo Instructions

Notes and instructions for building and running an image for demostration during the **#Meetup**.

## Build the image

Execute the following:

```shell
docker build -t joelwking/semaphore:1.0 -f Docerfile.deploy .
```

## Test the image

I used Windows 10 to develop and run this code.

```shell
docker run -it -d joelwking/semaphore:1.0
```

Invoke Powershell to avoid the Git bash error `docker error on windows : the input device is not a TTY. If you are using mintty, try prefixing the command with 'winpty'`

```text
powershell
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\Users\jwking> docker exec -it 72 /bin/bash
root@72e3092ad81c:/semaphore# ls

CTL + SHIFT P Q
```

Stop the container when you are satified `docker stop <container_id>`

## Save the image

Using Windows 10 as an example:

```text
docker save --output Downloads\semaphore.tgz joelwking/semaphore:1.0
```

## Copy and Load the file on your demo server

Create a user `semaphore`, install docker and add the user to the group

ubuntu-s-1vcpu-1gb-nyc3-01 / 1 GB Memory / 25 GB Disk / NYC3 - Ubuntu 22.04 (LTS) x64



```shell
apt install docker.io
apt install net-tools
adduser semaphore

sudo usermod -aG docker semaphore

docker load < semaphore.tgz

docker run -it --name publisher --env-file .env/vars -d joelwking/semaphore:1.0 

docker exec -it publisher /bin/bash

mkdir .env
semaphore@ubuntu-s-1vcpu-1gb-nyc3-01:~$ chmod 700 .env




```

### Author

Joel W. King @joelwking