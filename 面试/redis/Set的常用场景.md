---
      
title: Set的常用场景
      
created: 2025-04-02
      
source: Cherry Studio
      
tags: redis使用场景
      
---
### 🤖 Assistant

好的，同学，我们来深入探讨一下 Set 数据结构在实际业务中的应用，并给出使用 Redisson 客户端的 Demo 示例。Redisson 是一个流行的 Redis Java 客户端，提供了更高级的 API 和分布式特性，用起来更方便。

以下示例基于 Spring Boot + Redisson 实现。你需要先在你的 Spring Boot 项目中引入 Redisson 的依赖：

```xml
<!-- Maven -->
<dependency>
    <groupId>org.redisson</groupId>
    <artifactId>redisson-spring-boot-starter</artifactId>
    <version>3.25.0</version> <!-- 请使用最新版本 -->
</dependency>
```

或者

```gradle
// Gradle
implementation 'org.redisson:redisson-spring-boot-starter:3.25.0' // 请使用最新版本
```

然后在 `application.yml` 或 `application.properties` 中配置 Redisson 连接信息：

```yaml
# application.yml
spring:
  redis:
    host: 127.0.0.1
    port: 6379
    password: your_redis_password # 如果有密码
```

配置完成后，就可以在你的 Spring Bean 中注入 `RedissonClient` 来操作 Redis 了。

---

## Set 数据结构应用场景示例（Redisson 实现）

### 1. 标签（Tags）

*   **场景描述：**  给用户打标签，方便进行用户画像和个性化推荐。例如，一个电商网站，可以给用户打上“数码爱好者”、“母婴用户”、“运动达人”等标签。

*   **代码示例：**

    ```java
    import org.redisson.api.RSet;
    import org.redisson.api.RedissonClient;
    import org.springframework.beans.factory.annotation.Autowired;
    import org.springframework.stereotype.Service;

    @Service
    public class TagService {

        @Autowired
        private RedissonClient redissonClient;

        private final String TAGS_PREFIX = "user:tags:"; // Key 前缀，方便管理

        // 给用户添加标签
        public void addTag(String userId, String tag) {
            RSet<String> userTags = redissonClient.getSet(TAGS_PREFIX + userId);
            userTags.add(tag);
        }

        // 批量添加标签
        public void addTags(String userId, String... tags) {
            RSet<String> userTags = redissonClient.getSet(TAGS_PREFIX + userId);
            userTags.addAll(java.util.Arrays.asList(tags)); // Redisson 的 addAll 接受 Collection 参数
        }

        // 移除用户的标签
        public void removeTag(String userId, String tag) {
            RSet<String> userTags = redissonClient.getSet(TAGS_PREFIX + userId);
            userTags.remove(tag);
        }

        // 获取用户的所有标签
        public java.util.Set<String> getTags(String userId) {
            RSet<String> userTags = redissonClient.getSet(TAGS_PREFIX + userId);
            return userTags.readAll(); // Redisson 的 readAll() 方法获取所有元素
        }

        // 判断用户是否拥有某个标签
        public boolean hasTag(String userId, String tag) {
            RSet<String> userTags = redissonClient.getSet(TAGS_PREFIX + userId);
            return userTags.contains(tag);
        }

        public static void main(String[] args) {
            // 示例用法 (需要先配置 RedissonClient)
            // 假设你已经创建了一个 RedissonClient 实例 redissonClient
            // TagService tagService = new TagService(redissonClient);

            // 模拟用户ID
            String userId = "1001";

            // 添加标签
            // tagService.addTag(userId, "数码爱好者");
            // tagService.addTag(userId, "科技");

            // 获取标签
            // java.util.Set<String> tags = tagService.getTags(userId);
            // System.out.println("用户 " + userId + " 的标签: " + tags);

            // 判断是否包含某个标签
            // boolean hasTag = tagService.hasTag(userId, "科技");
            // System.out.println("用户 " + userId + " 是否有 '科技' 标签: " + hasTag);

            // 移除标签
            // tagService.removeTag(userId, "科技");
            // tags = tagService.getTags(userId);
            // System.out.println("移除 '科技' 标签后，用户 " + userId + " 的标签: " + tags);
        }
    }
    ```

*   **代码解释：**
    *   `@Autowired private RedissonClient redissonClient;`:  自动注入 Redisson 客户端实例。
    *   `RSet<String> userTags = redissonClient.getSet(TAGS_PREFIX + userId);`:  获取一个 Redisson 的 RSet 对象，对应 Redis 中的 Set 数据结构。Redisson 的 API 设计更贴近 Java 集合类。
    *   `userTags.add(tag)`, `userTags.addAll(Arrays.asList(tags))`:  向 Set 中添加元素。
    *   `userTags.remove(tag)`:  从 Set 中移除元素。
    *   `userTags.readAll()`:  读取 Set 中的所有元素。
    *   `userTags.contains(tag)`:  判断 Set 中是否包含某个元素。
    *   `TAGS_PREFIX`:  Key 前缀，良好的 Key 命名习惯，方便管理和查找。

### 2. 共同好友

*   **场景描述：**  社交应用中，查找两个用户共同的好友。

*   **代码示例：**

    ```java
    import org.redisson.api.RSet;
    import org.redisson.api.RedissonClient;
    import org.springframework.beans.factory.annotation.Autowired;
    import org.springframework.stereotype.Service;

    @Service
    public class FriendService {

        @Autowired
        private RedissonClient redissonClient;

        private final String FRIENDS_PREFIX = "user:friends:";

        // 添加好友
        public void addFriend(String userId, String friendId) {
            RSet<String> userFriends = redissonClient.getSet(FRIENDS_PREFIX + userId);
            userFriends.add(friendId);
        }

        // 获取共同好友
        public java.util.Set<String> getMutualFriends(String userId1, String userId2) {
            RSet<String> user1Friends = redissonClient.getSet(FRIENDS_PREFIX + userId1);
            RSet<String> user2Friends = redissonClient.getSet(FRIENDS_PREFIX + userId2);

            // 使用 Redisson 的 intersection 方法计算交集
            return user1Friends.intersection(user2Friends.getName()); // 注意: 这里需要传入另一个 Set 的 KeyName
        }

        public static void main(String[] args) {
            // 示例用法 (需要先配置 RedissonClient)
            // 假设你已经创建了一个 RedissonClient 实例 redissonClient
            // FriendService friendService = new FriendService(redissonClient);

            // 模拟用户ID
            String userId1 = "1001";
            String userId2 = "1002";

            // 添加好友
            // friendService.addFriend(userId1, "2001");
            // friendService.addFriend(userId1, "2002");
            // friendService.addFriend(userId1, "2003");

            // friendService.addFriend(userId2, "2002");
            // friendService.addFriend(userId2, "2003");
            // friendService.addFriend(userId2, "2004");

            // 获取共同好友
            // java.util.Set<String> mutualFriends = friendService.getMutualFriends(userId1, userId2);
            // System.out.println("用户 " + userId1 + " 和 " + userId2 + " 的共同好友: " + mutualFriends); // 应该是 2002 和 2003
        }
    }
    ```

*   **代码解释：**
    *   `user1Friends.intersection(user2Friends.getName())`:  Redisson 提供了 `intersection` 方法，可以直接计算两个 Set 的交集，返回共同好友的集合。**注意：Redisson的`intersection`方法需要传入另一个Set的Key Name，而不是 RSet 对象本身**。 这是 Redisson API 的一个特点。

### 3. 抽奖

*   **场景描述：**  在线抽奖活动，保证每个用户只能中奖一次。

*   **代码示例：**

    ```java
    import org.redisson.api.RSet;
    import org.redisson.api.RedissonClient;
    import org.springframework.beans.factory.annotation.Autowired;
    import org.springframework.stereotype.Service;

    import java.util.UUID;

    @Service
    public class LotteryService {

        @Autowired
        private RedissonClient redissonClient;

        private final String WINNERS_KEY = "lottery:winners"; // 中奖者集合的 Key

        // 参与抽奖 (返回是否中奖)
        public boolean participate(String userId) {
            RSet<String> winners = redissonClient.getSet(WINNERS_KEY);

            // 尝试将用户添加到中奖者集合中
            boolean isNewWinner = winners.add(userId);

            return isNewWinner; // 如果添加成功，说明是新的中奖者，返回 true
            // 如果添加失败 (已经存在)，说明已经中过奖了，返回 false
        }

        // 抽取中奖者 (随机抽取一个)
        public String drawWinner() {
            RSet<String> winners = redissonClient.getSet(WINNERS_KEY);
            return winners.random(); // 随机返回一个元素 (不删除)
            // 如果需要删除，可以使用 winners.removeRandom()
        }

        // 查看当前中奖人数
        public int getWinnerCount() {
            RSet<String> winners = redissonClient.getSet(WINNERS_KEY);
            return winners.size();
        }


        public static void main(String[] args) {
            // 示例用法 (需要先配置 RedissonClient)
            // 假设你已经创建了一个 RedissonClient 实例 redissonClient
            // LotteryService lotteryService = new LotteryService(redissonClient);

            // 模拟用户ID
            String userId1 = UUID.randomUUID().toString(); // 随机生成一个用户ID
            String userId2 = UUID.randomUUID().toString();

            // 参与抽奖
            // boolean isWinner1 = lotteryService.participate(userId1);
            // System.out.println("用户 " + userId1 + " 是否中奖: " + isWinner1); // 第一次应该是 true

            // boolean isWinner2 = lotteryService.participate(userId2);
            // System.out.println("用户 " + userId2 + " 是否中奖: " + isWinner2);

            // 再次尝试让第一个用户参与抽奖 (应该失败)
            // boolean isWinnerAgain1 = lotteryService.participate(userId1);
            // System.out.println("用户 " + userId1 + " 再次中奖是否成功: " + isWinnerAgain1); // 应该是 false

            // 抽取中奖者
            // String winner = lotteryService.drawWinner();
            // System.out.println("随机抽取的中奖者: " + winner);

            // 查看中奖人数
            // int winnerCount = lotteryService.getWinnerCount();
            // System.out.println("当前中奖人数: " + winnerCount);
        }
    }
    ```

*   **代码解释：**
    *   `winners.add(userId)`:  尝试将用户 ID 添加到中奖者集合中。由于 Set 的唯一性，如果用户已经存在于集合中，`add()` 方法会返回 `false`，表示该用户已经中过奖了。
    *   `winners.random()`:  随机返回 Set 中的一个元素（不删除）。如果需要删除，可以使用 `winners.removeRandom()`。
    *   `UUID.randomUUID().toString()`: 生成唯一的字符串 ID，模拟用户ID。

### 4. UV（Unique Visitor）统计

*   **场景描述：**  统计网站的独立访客数量。

*   **代码示例：**

    ```java
    import org.redisson.api.RSet;
    import org.redisson.api.RedissonClient;
    import org.springframework.beans.factory.annotation.Autowired;
    import org.springframework.stereotype.Service;

    import java.time.LocalDate;
    import java.time.format.DateTimeFormatter;

    @Service
    public class UVService {

        @Autowired
        private RedissonClient redissonClient;

        private final String UV_PREFIX = "uv:";

        // 记录用户访问
        public void recordVisit(String userId) {
            // 使用今天的日期作为 key 的一部分，每天一个单独的 UV Set
            String today = LocalDate.now().format(DateTimeFormatter.ISO_DATE);
            RSet<String> dailyUV = redissonClient.getSet(UV_PREFIX + today);
            dailyUV.add(userId);
        }

        // 获取今天的 UV
        public int getTodayUV() {
            String today = LocalDate.now().format(DateTimeFormatter.ISO_DATE);
            RSet<String> dailyUV = redissonClient.getSet(UV_PREFIX + today);
            return dailyUV.size();
        }

        public static void main(String[] args) {
            // 示例用法 (需要先配置 RedissonClient)
            // 假设你已经创建了一个 RedissonClient 实例 redissonClient
            // UVService uvService = new UVService(redissonClient);

            // 模拟用户访问
            // uvService.recordVisit("user1");
            // uvService.recordVisit("user2");
            // uvService.recordVisit("user1"); // 同一个用户再次访问

            // 获取今天的 UV
            // int todayUV = uvService.getTodayUV();
            // System.out.println("今天的 UV: " + todayUV); // 应该是 2 (user1 和 user2)
        }
    }
    ```

*   **代码解释：**
    *   `LocalDate.now().format(DateTimeFormatter.ISO_DATE)`:  获取今天的日期，并格式化成 `YYYY-MM-DD` 的字符串，作为 Key 的一部分。
    *   `RSet<String> dailyUV = redissonClient.getSet(UV_PREFIX + today);`:  每天创建一个单独的 Set 来记录 UV，避免数据量过大。
    *   `dailyUV.add(userId)`:  记录用户访问。由于 Set 的去重性，同一个用户多次访问只会被记录一次。
    *   `dailyUV.size()`:  获取 Set 的大小，即今天的 UV。

---

**总结：**

*   这些示例展示了 Set 数据结构在不同业务场景下的应用。Redisson 提供了更简洁易用的 API，简化了 Redis 操作。
*   注意：这些示例为了演示方便，都比较简单。在实际项目中，需要考虑更多因素，比如：
    *   Key 的命名规范
    *   数据过期策略
    *   异常处理
    *   并发控制
    *   Redisson 的配置和优化