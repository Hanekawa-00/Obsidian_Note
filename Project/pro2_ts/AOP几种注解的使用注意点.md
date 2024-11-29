# 一、Spring AOP通知类型及其参数和返回值要求：
- **@Before**：方法执行前执行，无返回值，参数可以是`JoinPoint`。
    
- **@After**：方法执行结束后执行，无返回值，参数可以是`JoinPoint`。
    
- **@AfterReturning**：方法成功返回后执行，可获取返回值，参数可以是`JoinPoint`和`@return`。
    
- **@AfterThrowing**：方法抛出异常后执行，可获取异常信息，参数可以是`JoinPoint`和`@throwing`。
    
- **@Around**：环绕通知，方法执行前后都可操作，可控制方法执行，必须有返回值，参数必须是`ProceedingJoinPoint`。