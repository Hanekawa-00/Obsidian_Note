MyBatis 的 `<foreach>` 标签用于遍历集合，生成动态 SQL 片段，常用于处理 IN 子句、多条件查询、批量更新等场景。以下是其详细用法和示例：

#### 基本语法

```xml
<foreach item="item" index="index" collection="collectionName" open="(" separator="," close=")">
    #{item}
</foreach>
```

- `item`: 当前遍历元素的变量名。
- `index`: 当前索引的变量名（可选）。
- `collection`: 要遍历的集合属性名。
- `open`: 开始符号，如 "("。
- `close`: 结束符号，如 ")"。
- `separator`: 分隔符，如 ","。

#### 常见用法示例

1. **生成 IN 子句**

   Java 代码：

   ```java
   List<Long> ids = Arrays.asList(1L, 2L, 3L);
   List<Record> records = mapper.selectByIds(ids);
   ```

   Mapper XML:

   ```xml
   <select id="selectByIds" resultType="Record">
       SELECT * FROM table_name
       WHERE id IN
       <foreach item="id" collection="list" open="(" separator="," close=")">
           #{id}
       </foreach>
   </select>
   ```

2. **传入 Map 包含集合**

   Java 代码：

   ```java
   Map<String, Object> params = new HashMap<>();
   params.put("ids", Arrays.asList(1L, 2L, 3L));
   List<Record> records = mapper.selectByIds(params);
   ```

   Mapper XML:

   ```xml
   <select id="selectByIds" resultType="Record">
       SELECT * FROM table_name
       WHERE id IN
       <foreach item="id" collection="ids" open="(" separator="," close=")">
           #{id}
       </foreach>
   </select>
   ```

3. **动态 WHERE 条件**

   Java 代码：

   ```java
   Map<String, String> conditions = new HashMap<>();
   conditions.put("name", "John");
   conditions.put("age", "30");
   List<User> users = mapper.selectByConditions(conditions);
   ```

   Mapper XML:

   ```xml
   <select id="selectByConditions" resultType="User">
       SELECT * FROM users
       WHERE 1=1
       <foreach item="condition" collection="conditions" separator=" AND ">
           ${condition.key} = #{condition.value}
       </foreach>
   </select>
   ```

#### 注意事项

1. **SQL 注入风险**: 使用 `${}` 会直接拼接字符串，可能导致 SQL 注入，尽量使用 `#{}` 进行预编译处理。
2. **参数传递**: 确保 `collection` 的值和传入的参数对应，否则会导致错误。
3. **性能问题**: 避免在循环中进行过多的 SQL 操作，影响性能。

#### 高级用法

- **使用 status 属性**

  ```xml
  <foreach item="item" index="index" collection="list" status="status">
      <!-- 可以使用 #{status.index}, #{status.count}, #{status.first}, #{status.last} 等 -->
  </foreach>
  ```