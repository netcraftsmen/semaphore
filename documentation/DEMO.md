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

```shell
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

```shell
docker save --output Downloads\semaphore.tgz joelwking/semaphore:1.0
```

## Copy and Load the file on your demo server


### Author

Joel W. King @joelwking