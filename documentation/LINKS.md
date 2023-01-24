## Other Notes and References
 OpenTelemetry provides a vendor-agnostic method of collecting telemetry data. 

 
Uses https://kafka.apache.org/uses


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