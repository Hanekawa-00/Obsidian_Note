以下是整合前后端开发的完整双周计划，每个Sprint均明确划分前后端任务，保持技术细节完整：

---

### **Sprint 1-2（1.23-2.5）基础框架搭建**
#### **后端任务**
```mermaid
gantt
    title Sprint 1-2 后端任务
    dateFormat  YYYY-MM-DD
    section 核心架构
    Spring Boot多模块工程 :done, 2025-01-23, 3d
    全局异常处理 :a1, 2025-01-25, 2d
    section 用户服务
    JWT签发/验证 :crit, active, a2, 2025-01-26, 5d
    RBAC模型设计 :a3, after a2, 3d
```

**技术实现**：
1. 多环境配置
   ```yaml
   # application-dev.yml
   spring:
     datasource:
       url: jdbc:mysql://localhost:3306/bi_dev
       username: dev_user
       password: dev123
   ```
2. JWT工具类
   ```java
   public class JwtUtils {
       public static String generateToken(UserDetails user) {
           return Jwts.builder()
               .setSubject(user.getUsername())
               .setExpiration(new Date(System.currentTimeMillis() + 3600 * 1000))
               .signWith(SignatureAlgorithm.HS512, SECRET_KEY)
               .compact();
       }
   }
   ```

#### **前端任务**
```mermaid
gantt
    title Sprint 1-2 前端任务
    section 工程基础
    React项目初始化 :done, 2025-01-24, 1d
    Ant Design集成 :active, a1, 2025-01-25, 2d
    section 认证模块
    登录页面开发 :a2, after a1, 3d
    路由守卫实现 :a3, after a2, 2d
```

**联调重点**：
- JWT令牌在axios拦截器中的自动携带
- 401状态码的全局处理

---

### **Sprint 3-4（2.6-2.19）数据核心功能**
#### **后端任务**
```mermaid
gantt
    title Sprint 3-4 后端任务
    section 数据接入
    Excel分片上传 :crit, active, a1, 2025-02-06, 5d
    MySQL元数据管理 :a2, after a1, 4d
    section 中间件
    Redis缓存热点数据 :a3, 2025-02-07, 3d
    异步任务队列 :a4, after a3, 5d
```

**关键技术**：
1. 分片上传接口
   ```java
   @PostMapping("/upload/chunk")
   public Response uploadChunk(
       @RequestParam String fileKey,
       @RequestParam Integer chunkIndex,
       @RequestPart MultipartFile chunk) {
       
       // 保存分片到临时目录
       // 更新Redis中的分片记录
       return Response.success();
   }
   ```
2. 元数据表设计
   ```sql
   CREATE TABLE dataset_meta (
     id BIGINT PRIMARY KEY COMMENT '主键',
     name VARCHAR(255) NOT NULL COMMENT '数据集名称',
     columns JSON NOT NULL COMMENT '字段定义',
     created_by VARCHAR(64) COMMENT '创建人'
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
   ```

#### **前端任务**
```mermaid
gantt
    title Sprint 3-4 前端任务
    section 数据模块
    分片上传组件 :active, a1, 2025-02-06, 5d
    数据预览表格 :a2, after a1, 4d
    section 状态管理
    Redux状态机集成 :a3, 2025-02-07, 3d
```

**关键技术**：
1. 大文件分片上传
   ```tsx
   const uploadChunk = async (file: File) => {
     const chunkSize = 5 * 1024 * 1024; // 5MB
     for (let i = 0; i < Math.ceil(file.size / chunkSize); i++) {
       const chunk = file.slice(i * chunkSize, (i + 1) * chunkSize);
       await api.uploadChunk(chunk, file.name, i);
     }
     await api.mergeChunks(file.name);
   };
   ```

---

### **Sprint 5-6（2.20-3.5）智能分析引擎**
#### **后端任务**
```mermaid
gantt
    title Sprint 5-6 后端任务
    section AI服务
    Spring AI集成 :crit, active, a1, 2025-02-20, 7d
    本地模型微调 :a2, after a1, 4d
    section 分析服务
    规则引擎降级 :a3, 2025-02-22, 5d
    SQL执行引擎 :a4, after a3, 3d
```

**关键技术**：
1. NL2SQL服务
   ```java
   @Service
   public class NL2SQLService {
       public String parse(String question) {
           String prompt = """
               数据库结构：%s
               问题：%s
               要求：使用MySQL语法，包含注释
               """.formatted(getSchema(), question);
           return chatClient.call(prompt);
       }
   }
   ```
2. SQL执行安全校验
   ```java
   public void validateSQL(String sql) {
       if (sql.contains("DELETE") || sql.contains("UPDATE")) {
           throw new InvalidSQLException("只允许SELECT查询");
       }
   }
   ```

#### **前端任务**
```mermaid
gantt
    title Sprint 5-6 前端任务
    section 分析模块
    NLP输入框 :active, a1, 2025-02-20, 5d
    图表配置面板 :a2, after a1, 3d
    section 可视化
    基础图表渲染 :a3, 2025-02-22, 5d
```

**关键技术**：
1. 智能输入建议
   ```tsx
   <AutoComplete
     options={suggestions}
     onSearch={handleSearch}
     placeholder="输入分析需求..."
   />
   ```

---

### **Sprint 7-8（3.6-3.19）可视化系统**
#### **后端任务**
```mermaid
gantt
    title Sprint 7-8 后端任务
    section 数据服务
    宽表预计算 :crit, active, a1, 2025-03-06, 7d
    实时数据推送 :a2, after a1, 5d
    section 性能优化
    查询缓存 :a3, 2025-03-08, 3d
    SQL执行计划分析 :a4, after a3, 3d
```

**关键技术**：
1. WebSocket端点
   ```java
   @ServerEndpoint("/ws/realtime")
   public class RealtimeEndpoint {
       @OnMessage
       public void handleMessage(Session session, String message) {
           // 处理订阅请求
       }
       
       public void pushData(String topic, String data) {
           // 广播数据
       }
   }
   ```

#### **前端任务**
```mermaid
gantt
    title Sprint 7-8 前端任务
    section 可视化
    ECharts深度集成 :active, a1, 2025-03-06, 5d
    仪表盘编辑器 :a2, after a1, 7d
    section 实时
    WebSocket连接管理 :a3, 2025-03-08, 3d
```

**关键技术**：
1. 实时数据订阅
   ```tsx
   const [data, setData] = useState([]);
   useEffect(() => {
     const ws = new WebSocket('ws://api/ws/realtime');
     ws.onmessage = (e) => setData(JSON.parse(e.data));
     return () => ws.close();
   }, []);
   ```

---

### **Sprint 9-10（3.20-4.2）企业级扩展**
#### **后端任务**
```mermaid
gantt
    title Sprint 9-10 后端任务
    section 服务治理
    Nacos注册中心 :crit, active, a1, 2025-03-20, 5d
    配置热更新 :a2, after a1, 3d
    section 监控
    Prometheus埋点 :a3, 2025-03-22, 5d
    日志聚合 :a4, after a3, 5d
```

**关键技术**：
1. 监控指标配置
   ```java
   @Timed(value = "bi.query.duration", description = "查询耗时")
   @GetMapping("/query")
   public Response query(@RequestParam String sql) {
       // 业务逻辑
   }
   ```

#### **前端任务**
```mermaid
gantt
    title Sprint 9-10 前端任务
    section 企业功能
    权限管理界面 :active, a1, 2025-03-20, 5d
    操作审计日志 :a2, after a1, 3d
    section 监控
    Grafana看板嵌入 :a3, 2025-03-22, 5d
```

---

### **DevOps集成方案**
```mermaid
graph TD
    A[Git提交] --> B[Jenkins流水线]
    B --> C{测试通过?}
    C -->|是| D[构建Docker镜像]
    D --> E[部署到K8s集群]
    C -->|否| F[邮件告警]
```

**后端关键配置**：
```dockerfile
FROM openjdk:17-jdk-alpine
COPY target/bi-service.jar /app.jar
EXPOSE 8080
ENTRYPOINT ["java","-jar","/app.jar"]
```

---

该计划完整覆盖前后端开发，每个Sprint均包含：
1. **后端核心模块**：认证/数据/AI/监控等企业级功能
2. **前端交互实现**：组件开发/状态管理/可视化等
3. **联调验证点**：接口规范/数据格式/异常处理
4. **质量保障**：单元测试/压力测试/代码审查

建议使用Postman维护API文档集合，使用Swagger生成接口文档，确保前后端开发高效协同。