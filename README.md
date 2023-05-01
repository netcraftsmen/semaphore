# semaphore

Project name, **Semaphore**: a system of sending messages by holding the arms or two flags or poles in certain positions according to an alphabetic code.

[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/netcraftsmen/semaphore)

## Title
Introduction to network telemetry using Apache Kafka in Confluent Cloud.

## Abstract

The use of telemetry is an increased focus in IT operations providing raw data to the Machine Learning / Artificial Intelligence (ML/AI) algorithms for AIOps (Artificial Intelligence for IT Operations).

Network operators have relied upon [SNMP](https://www.ietf.org/rfc/rfc9232.html#RFC3416) and [Syslog](https://www.ietf.org/rfc/rfc9232.html#RFC5424) to monitor the network. Network telemetry (streaming data pushed to a collector) is replacing the polling of network devices. The push approach is less burden to the CPU of the device, can be delivered promptly, and is initiated by the device when a state change is detected.

There are open source tools to receive telemetry data, store it, visualize and alert; how should the network operator provide access to infrastructure telemetry data, in real-time, at scale across all technology stakeholders?

This session illustrates publishing telemetry data from the Meraki SDK to Apache Kafka deployed in Confluent Cloud. Kafka is a distributed event store and stream-processing platform designed for big data and high throughput. Using the developer instance of Confluent Cloud and the Python SDK, we examine the ease at which a network operator can publish and consume telemetry data to implement its own AIOps approach.

## Presentation

The live stream and recorded [presentation](https://www.youtube.com/watch?v=ABMcflO1ix8) (following the event on January 25th 2023) is available at https://www.youtube.com/@infrastructureautomation Programmability and Automation Meetup youtube channel.

## Telemetry Source

To illustrate the concepts of publishing telemetry to Kafka, the telemetry source is the Meraki dashboard API [Loss and Latency](https://developer.cisco.com/meraki/api-v1/#!get-device-loss-and-latency-history) via the Meraki SDK is used in the demonstration code.

## Installation

Installation instructions are documented in `documentation/INSTALLATION.md`.  After cloning the repository,

```shell
git clone https://github.com/netcraftsmen/semaphore.git
```

with Docker installed, follow the `documentation/INSTALLATION.md` to build an image and execute on your target cloud platform.

## Usage

The `documentation/INSTALLATION.md` instructions detail updating the environment variables.

### Publisher

The use case demonstrated during the Meetup presentation publishes latency and loss information from the Meraki API

#### latency_loss_logging.py

Execute the Kafka publisher.

```shell
# python latency_loss_logging.py -h
please create and specify the API key, e.g. "export MERAKI_DASHBOARD_API_KEY=12345"
usage: latency_loss_logging.py [-h] [-a {syslog,kafka,both}]

Demonstration of telemetry logging and publishing

optional arguments:
  -h, --help            show this help message and exit
  -a {syslog,kafka,both}, --action {syslog,kafka,both}
                        action
```

#### publish_clients.py

An additional use case is to publish all clients observed on the networks within the organizations. It uses the `getNetworkClients` SDK method.

```shell
# python publish_clients.py -h
usage: publish_clients.py [-h] [-d DEBUG]

Publish clients

optional arguments:
  -h, --help            show this help message and exit
  -d DEBUG, --debug DEBUG
                        debug
```
This use case was developed to demonstrate the Event-Driven Ansible client.

### Consumer

Execute the Kafka consumer.

```shell
# python consumer.py -h
usage: consumer.py [-h] [-g GROUP] [-o {latest,earliest}] [-t TIMEOUT] [-r RANGE] [-v VERBOSE]

Kafka consumer

optional arguments:
  -h, --help            show this help message and exit
  -g GROUP, --group GROUP
                        group ID
  -o {latest,earliest}, --offset {latest,earliest}
                        auto.offset.reset
  -t TIMEOUT, --timeout TIMEOUT
                        poll timeout (sec)
  -r RANGE, --range RANGE
                        number of polling iterations
  -v VERBOSE, --verbose VERBOSE
                        output additional info
```

## Notes

These notes provide an overview of the terms and concepts of Kafka.

### Overview

Overview of Kafka terms and concepts.

#### Cluster

The Kafka cluster is a combination of one or more servers each of which is called a broker. The Kafka cluster retains all published messages for a configurable period of time, called the log retention. Messages are not discarded after being read by a consumer, rather upon the expiration of the log retention.

#### Topics

The Topic is defined in the Confluent Cloud GUI after creating a Cluster. Kafka organizes message feeds into categories called topics. A topic is an ordered log of events. When an external system
writes a record (message) to Kafka, it is appended to the end of a topic.

>Note: The terms records and messages are often used interchangeably. A message is a simple array of bytes. The value of the message might be JSON or Protobuf as an example. The default maximum message size is 1MB, but is configurable.

All Kafka messages are stored and published into topics. Producer applications write messages to topics
and consumer applications read from topics. Records published to the cluster stay in the cluster until a configurable (log retention) period has passed by.

#### Message Keys

Kafka messages consist of a key / value pairs. While the value is the data of the message, the message key determines the partition of the topic. If the message key is null, the records (messages) are stored round-robin across all partitions. Messages that have the same key will be written to the same partititon.

Kafka uses the [key](https://stackoverflow.com/questions/29511521/is-key-required-as-part-of-sending-messages-to-kafka) of the message to select the partition of the topic. Kafka has guarantees on ordering of the messages only at partition level. 

#### Partitions

Each topic can have multiple partitions, the default number of partitions for Confluent Cloud is six. This value can be changed when creating the topic in the GIU. Each partition is a single log file where records (messages) are written to it append-only.

#### Offset

The offset is an integer value that identifies the order of messages within a partition. The consumer can begin reading at a specific offset value within a partition. Offsets are zero relative.

#### Consumer Offset

The consumer offset keeps track of what has already been read by one or more consumers sharing the same consumer ID.  Like a bookmark, it allows reading from where it left off the last time. 

## Additional Information

For additional information on an Ansible interface to Cisco Tetration Network Policy Publisher (Kafka broker) review the repository at https://github.com/joelwking/ansible-tetration and browse the links, videos and sample code.

## Author

Joel W. King @joelwking
