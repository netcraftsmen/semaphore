# semaphore

**Semaphore**: a system of sending messages by holding the arms or two flags or poles in certain positions according to an alphabetic code.

## Abstract

The use of telemetry is an increased focus in IT operations to feed the Machine Learning / Artificial Intelligence (ML/AL) algorithms being developed and deployed.

Network operators have relied upon [SNMP](https://www.ietf.org/rfc/rfc9232.html#RFC3416)] and [Syslog](https://www.ietf.org/rfc/rfc9232.html#RFC5424) to monitor the network. Network telemetry (streaming data pushed to a collector) is replacing polling data from network devices.
 
While there are tools (TIG) to receive telemetry data, store it and visualize and alert, how should the network operator provide access to infrastructure telementry data, in real time, at scale across all technology stateholders?

This session illustrates using Apache Kafka, a distributed event store and stream-processing platform designed for massive data and high throughput.

We begin by providing an overview of the Kafa architectual components and then demonstrate publish messages to Confluent Cloud, (SaaS for Apache Kafka) from the Meraki dashboard API [Loss and Latency](https://developer.cisco.com/meraki/api-v1/#!get-device-loss-and-latency-history) of network interface. The code to publish and consume the is demonstrated and available to the attendees via a public GitLab repository.


 OpenTelemetry provides a vendor-agnostic method of collecting telemetry data. 

A Message Bus is commonly used in micro-service architectures to allow applications to communicate over a common, shared set of services. RabbitMQ and Kafka are two popular messaging systems serving different use cases. Kafka is designed for massive data and high throughput, while RabbitMQ is for simple use cases with low traffic volumes.

Telegraf is a popular collector, which receives the telemetry data, coupled with InfluxDB which stores it, and Grafana which is responsible for visualizations and alerting.

https://prometheus.io/docs/introduction/overview/

 

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