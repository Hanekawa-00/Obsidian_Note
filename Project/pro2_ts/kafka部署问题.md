当宿主机的 IP 地址是动态分配的（例如通过 DHCP 分配的 IP），直接使用固定的 IP 地址（如 `192.168.121.128`）可能会导致 Kafka 进程绑定到错误的 IP 地址，从而影响连接性。为了应对这种情况，可以考虑以下几种方案：

### 1. 使用 `0.0.0.0` 绑定所有网络接口

将 Kafka 的 `KAFKA_ADVERTISED_HOST_NAME` 和 `HOST_IP` 配置为 `0.0.0.0`。这样，Kafka 会绑定到所有可用的网络接口，而不是一个具体的 IP 地址。

修改你的 Docker 命令如下：

```Shell
docker run -d --name kafka --publish 9092:9092 \
--link zookeeper:zookeeper \
--env KAFKA_BROKER_ID=100 \
--env HOST_IP=0.0.0.0 \
--env KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
--env KAFKA_ADVERTISED_HOST_NAME=0.0.0.0 \
--env KAFKA_ADVERTISED_PORT=9092 \
--restart=always \
--volume /etc/localtime:/etc/localtime \
wurstmeister/kafka
```

- **`HOST_IP=0.0.0.0`**：意味着 Kafka 进程监听所有可用的网络接口。
    
- **`KAFKA_ADVERTISED_HOST_NAME=0.0.0.0`**：告诉 Kafka 广告它在所有网络接口上可用，客户端可以通过任何可用的接口连接到 Kafka。
    

### 问题：

使用 `0.0.0.0` 会导致 Kafka 广告给客户端的地址不明确，这样 Kafka 可能无法在集群中工作得很好，因为客户端（包括其他 Kafka broker 和消费者/生产者）需要一个具体的 IP 地址来连接 Kafka。如果你在单机环境中运行，使用 `0.0.0.0` 可能没问题，但在多机集群或实际生产环境中不推荐。

### 2. 使用主机名代替 IP 地址

如果宿主机的 IP 是动态分配的，可以考虑使用宿主机的主机名。通过 Docker 的 `--hostname` 选项，可以确保 Kafka 广告的是主机名，而不是具体的 IP 地址，客户端可以通过主机名解析其实际 IP 地址。

修改 Docker 命令如下：

```Shell
docker run -d --name kafka --publish 9092:9092 \
--link zookeeper:zookeeper \
--hostname kafka-host \
--env KAFKA_BROKER_ID=100 \
--env KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
--env KAFKA_ADVERTISED_HOST_NAME=kafka-host \
--env KAFKA_ADVERTISED_PORT=9092 \
--restart=always \
--volume /etc/localtime:/etc/localtime \
wurstmeister/kafka
```

在这种方式下：

- **`--hostname kafka-host`**：设置容器的主机名为 `kafka-host`。
    
- **`KAFKA_ADVERTISED_HOST_NAME=kafka-host`**：Kafka 广告的是主机名，而不是 IP 地址。
    

这样一来，Kafka 广告的主机名可以通过 DNS 或者 `/etc/hosts` 文件解析为正确的 IP 地址，适应 IP 动态分配的情况。

### 3. 动态获取宿主机 IP

还有一种办法是让容器动态获取宿主机的实际 IP 地址，并在启动时将它配置为 `KAFKA_ADVERTISED_HOST_NAME`。可以通过以下脚本来实现：

```Shell
HOST_IP=$(hostname -I | awk '{print $1}')

docker run -d --name kafka --publish 9092:9092 \
--link zookeeper:zookeeper \
--env KAFKA_BROKER_ID=100 \
--env HOST_IP=$HOST_IP \
--env KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
--env KAFKA_ADVERTISED_HOST_NAME=$HOST_IP \
--env KAFKA_ADVERTISED_PORT=9092 \
--restart=always \
--volume /etc/localtime:/etc/localtime \
wurstmeister/kafka
```

这个脚本使用 `hostname -I` 命令获取宿主机的当前 IP 地址，并将其传递给 Docker 作为环境变量。