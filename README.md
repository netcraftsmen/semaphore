# semaphore

Project name, **Semaphore**: a system of sending messages by holding the arms or two flags or poles in certain positions according to an alphabetic code.

## Title
Introduction to network telemetry using Apache Kafka in Confluent Cloud.

## Abstract

The use of telemetry is an increased focus in IT operations providing raw data to the Machine Learning / Artificial Intelligence (ML/AI) algorithms for AIOps (Artificial Intelligence for IT Operations).

Network operators have relied upon [SNMP](https://www.ietf.org/rfc/rfc9232.html#RFC3416)] and [Syslog](https://www.ietf.org/rfc/rfc9232.html#RFC5424) to monitor the network. Network telemetry (streaming data pushed to a collector) is replacing the polling of network devices. The push approach is less burden to the CPU of the device, can be delivered promptly, and is initiated by the device when a state change is detected.

There are open source tools to receive telemetry data, store it, visualize and alert; how should the network operator provide access to infrastructure telemetry data, in real-time, at scale across all technology stakeholders?

This session illustrates publishing telemetry data from the Meraki SDK to Apache Kafka deployed in Confluent Cloud. Kafka is a distributed event store and stream-processing platform designed for big data and high throughput. Using the developer instance of Confluent Cloud and the Python SDK, we examine the ease at which a network operator can publish and consume telemetry data to implement its own AIOps approach.

## Presentation

The live stream and recorded [presentation](https://www.youtube.com/watch?v=ABMcflO1ix8) (following the event on January 25th 2023) is available at https://www.youtube.com/@infrastructureautomation Programmability and Automation Meetup youtube channel.

## Telemetry Source

To illustrate the concepts of publishing telemetry to Kafka, the telemetry source is the Meraki dashboard API [Loss and Latency](https://developer.cisco.com/meraki/api-v1/#!get-device-loss-and-latency-history) via the Meraki SDK is used in the demonstration code.

## Notes

These notes provide an overview of the terms and concepts of Kafka

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

### Offset

The offset is an integer value that identifies the order of messages within a partition. The consumer can begin reading at a specific offset value within a partition. 


## Other Notes
 OpenTelemetry provides a vendor-agnostic method of collecting telemetry data. 



 Kafka to stream logs once and be consumed by multiple receivers.

 
Uses https://kafka.apache.org/uses

## References

The following references were used in developing this use case.

 * *A Message Bus is commonly used in micro-service architectures to allow applications to communicate over a common, shared set of services RabbitMQ and Kafka are two popular messaging systems serving different use cases. Kafka is designed for massive data and high throughput, while RabbitMQ is for simple use cases with low traffic volumes.* <https://stackoverflow.com/questions/42151544/when-to-use-rabbitmq-over-kafka>

* *RFC 9232 Network Telemetry Framework* <https://www.ietf.org/rfc/rfc9232.html>

Telegraf is a popular collector, which receives the telemetry data, coupled with InfluxDB which stores it, and Grafana which is responsible for visualizations and alerting.

https://prometheus.io/docs/introduction/overview/

https://blogs.cisco.com/developer/getting-started-with-model-driven-telemetry

https://github.com/ericchou1/network-devops-kafka-up-and-running

https://www.goodreads.com/book/show/59661159-kafka-up-and-running-for-network-devops

https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying


 Policies Publisher is an advanced Cisco Secure Workload feature allowing third party vendors to implement their own enforcement algorithms optimized for network appliances such as load balancers or firewalls.


https://www.geeksforgeeks.org/apache-kafka-message-keys/

https://medium.com/fintechexplained/12-best-practices-for-using-kafka-in-your-architecture-a9d215e222e3

https://www.aiopsforeveryone.com/observability-vs-telemetry-vs-monitoring-is-all-same/

https://www.spiceworks.com/tech/data-management/articles/what-is-kafka/

Kafka, however, has a reasonably low overhead compared to other messaging systems since it does not monitor user activity or remove messages that have been read. On the other hand, it keeps all messages for a predetermined period and leaves it up to the user to track which messages have been read. 

https://www.linkedin.com/pulse/kafka-consumer-auto-offset-reset-rob-golder/

auto offset reset consumer configuration defines how a consumer should behave when consuming from a topic partition when there is no initial offset.