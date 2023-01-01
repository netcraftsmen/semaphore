# semaphore

**Semaphore**: a system of sending messages by holding the arms or two flags or poles in certain positions according to an alphabetic code.

## Title
Introduction to network telemetry using Apache Kafka in Confluent Cloud.

## Abstract

The use of telemetry is an increased focus in IT operations providing raw data to the Machine Learning / Artificial Intelligence (ML/AI) algorithms for AIOps (Artificial Intelligence for IT Operations).

Network operators have relied upon [SNMP](https://www.ietf.org/rfc/rfc9232.html#RFC3416)] and [Syslog](https://www.ietf.org/rfc/rfc9232.html#RFC5424) to monitor the network. Network telemetry (streaming data pushed to a collector) is replacing the polling of network devices. The push approach is less burden to the CPU of the device, can be delivered promptly, and is initiated by the device when a state change is detected.

There are open source tools to receive telemetry data, store it, visualize and alert; how should the network operator provide access to infrastructure telemetry data, in real-time, at scale across all technology stakeholders?

This session illustrates publishing telemetry data from the Meraki SDK to Apache Kafka deployed in Confluent Cloud. Kafka is a distributed event store and stream-processing platform designed for big data and high throughput. Using the developer instance of Confluent Cloud and the Python SDK, we examine the ease at which a network operator can publish and consume telemetry data to implement its own AIOps approach.

## Notes

We begin by providing an overview of the Kafa architectual components and then demonstrate publish messages to Confluent Cloud, (SaaS for Apache Kafka) from the Meraki dashboard API [Loss and Latency](https://developer.cisco.com/meraki/api-v1/#!get-device-loss-and-latency-history) of network interface. The code to publish and consume the is demonstrated and available to the attendees via a public GitLab repository.


 OpenTelemetry provides a vendor-agnostic method of collecting telemetry data. 

A Message Bus is commonly used in micro-service architectures to allow applications to communicate over a common, shared set of services. RabbitMQ and Kafka are two popular messaging systems serving different use cases. Kafka is designed for massive data and high throughput, while RabbitMQ is for simple use cases with low traffic volumes.

Telegraf is a popular collector, which receives the telemetry data, coupled with InfluxDB which stores it, and Grafana which is responsible for visualizations and alerting.

https://prometheus.io/docs/introduction/overview/

 Policies Publisher is an advanced Cisco Secure Workload feature allowing third party vendors to implement their own enforcement algorithms optimized for network appliances such as load balancers or firewalls.

Illustrates using a free trial version of Confluent Cloud -Walk through the basic building blocks of Kafka and Confluent Cloud.



 Kafka to stream logs once and be consumed by multiple receivers.

The number of partitions by default is 6 when creating a Topic in confluent.cloud
 
Uses https://kafka.apache.org/uses

## References

https://stackoverflow.com/questions/42151544/when-to-use-rabbitmq-over-kafka

https://www.ietf.org/rfc/rfc9232.html

https://blogs.cisco.com/developer/getting-started-with-model-driven-telemetry

https://github.com/ericchou1/network-devops-kafka-up-and-running

https://www.goodreads.com/book/show/59661159-kafka-up-and-running-for-network-devops

https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying

https://stackoverflow.com/questions/29511521/is-key-required-as-part-of-sending-messages-to-kafka

 Kafka has guarantees on ordering of the messages only at partition level. Kafka uses the key of the message to select the partition of the topic.  Kafka will partition the data in a round-robin fashion. Using the same key will put all these messages in the same partititon.

https://www.geeksforgeeks.org/apache-kafka-message-keys/

https://medium.com/fintechexplained/12-best-practices-for-using-kafka-in-your-architecture-a9d215e222e3

https://www.aiopsforeveryone.com/observability-vs-telemetry-vs-monitoring-is-all-same/

https://www.spiceworks.com/tech/data-management/articles/what-is-kafka/

Kafka, however, has a reasonably low overhead compared to other messaging systems since it does not monitor user activity or remove messages that have been read. On the other hand, it keeps all messages for a predetermined period and leaves it up to the user to track which messages have been read. 

https://www.linkedin.com/pulse/kafka-consumer-auto-offset-reset-rob-golder/

auto offset reset consumer configuration defines how a consumer should behave when consuming from a topic partition when there is no initial offset.