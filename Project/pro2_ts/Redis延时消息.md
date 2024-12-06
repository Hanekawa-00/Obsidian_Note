### 为什么使用redis发送延时消息
使用 Redis 发送延时消息主要利用了 Redis 的有序集合（Sorted Set）和阻塞队列（Blocking Queue）特性。
1. **有序集合（Sorted Set）**：
   - **特性**：有序集合中的每个元素都会关联一个分数（score），Redis 会根据分数自动排序。
   - **用法**：可以使用 `ZADD` 命令将消息添加到有序集合中，并将消息的到期时间作为分数。通过 `ZRANGEBYSCORE` 命令可以获取到期的消息。

2. **阻塞队列（Blocking Queue）**：
   - **特性**：阻塞队列可以在队列为空时阻塞获取操作，直到队列中有新元素。
   - **用法**：可以使用 `RBlockingDeque` 和 `RDelayedQueue` 实现延时消息队列。`RDelayedQueue` 会在**消息到期时**将其转移到 `RBlockingDeque`，从而实现延时处理。

### 使用方法
1. **发送延时消息**：
   - 使用 `RedissonClient` 获取[[双端阻塞队列]] `RBlockingDeque`。
   - 使用 `RDelayedQueue` 将消息（如订单ID）添加到延时队列中，并设置延迟时间（**这里的延时时间是指达到时间后发送消息，然后可以被take()方法拿到**）。

2. **监听延时消息**：
   - 在 `@PostConstruct` 方法中启动一个新线程。
   - 使用 `RBlockingDeque` 的 `take()` 方法阻塞等待消息。
   - 当消息可用时(到达定时时间)，处理消息（如取消订单）。

### 原理
- **延时队列**：通过 `RDelayedQueue` 实现，将消息添加到延时队列中，并设置延迟时间。
- **阻塞队列**：使用 `RBlockingDeque` 实现消息的阻塞等待，`take` 方法会阻塞直到消息可用。
- **消息处理**：当延迟时间到达后，消息从延时队列转移到阻塞队列，`take` 方法获取消息并进行处理。

### 示例代码

**发送延时消息**：
```java
private void sendDelayMessage(Long orderId) {
    long delayTime = KafkaConstant.DELAY_TIME;
    try {
        RBlockingDeque<String> blockingDeque = redissonClient.getBlockingDeque(KafkaConstant.QUEUE_ORDER_CANCEL);
        RDelayedQueue<String> delayedQueue = redissonClient.getDelayedQueue(blockingDeque);
        delayedQueue.offer(orderId.toString(), delayTime, TimeUnit.SECONDS);
        log.info("添加延时队列成功，延迟时间{}s，订单id：{}", delayTime, orderId);
    } catch (Exception e) {
        log.error("添加延时队列失败，延迟时间{}s，订单id：{}", delayTime, orderId);
        e.printStackTrace();
    }
}
```

**监听延时消息**：
```java
@PostConstruct
public void listener() {
    new Thread(() -> {
        RBlockingDeque<String> blockingDeque = redissonClient.getBlockingDeque(KafkaConstant.QUEUE_ORDER_CANCEL);
        try {
            while (true) {
                String orderId = blockingDeque.take();
                if (!StrUtil.isEmpty(orderId)) {
                    log.info("接收延时消息成功，订单id：{}", orderId);
                    orderInfoService.cancelOrder(Long.parseLong(orderId));
                }
            }
        } catch (InterruptedException e) {
            log.error("接受延时消息失败");
            e.printStackTrace();
        }
    }).start();
}
```