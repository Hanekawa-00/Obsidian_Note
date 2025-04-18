* 在使用联合索引时，必须满足从左到右的匹配原则。如果一个联合索引包含多个列，查询条件必须必须包括第一列，然后是第二列，以此类推
### 注意：
1. **连续匹配**：查询条件必须按照索引定义顺序连续匹配，中间如果跳过了某些列则后面的索引无效
2. **范围查询之后的列失效**：如果某一列使用了范围查询（`>,<,between`）,那么后面的列无法使用索引。
	* **如果遇到如 >=、<=、BETWEEN、前缀like（xx%）的范围查询，则不会停止匹配**。因为这些查询包含一个等值判断，可以直接定位到某个数据，然后往后扫描即可。

**例子**：
假设有一个复合索引 `INDEX (col1, col2, col3)`：

- **有效查询**：
    
    - `WHERE col1 = 'a' AND col2 = 'b' AND col3 = 'c'`：完全匹配索引。
        
    - `WHERE col1 = 'a' AND col2 = 'b'`：匹配索引的前两列。
        
    - `WHERE col1 = 'a'`：匹配索引的最左侧列。
        
- **部分有效查询**：
    
    - `WHERE col1 = 'a' AND col3 = 'c'`：只能用到 `col1`，因为跳过了 `col2`。
        
    - `WHERE col1 = 'a' AND col2 > 'b' AND col3 = 'c'`：只能用到 `col1` 和 `col2`，因为 `col2` 是范围查询，`col3` 无法使用索引。
        
- **无效查询**：
    
    - `WHERE col2 = 'b' AND col3 = 'c'`：不包含最左侧列 `col1`，索引无法使用。
        
    - `WHERE col3 = 'c'`：不包含最左侧列 `col1`，索引无法使用。