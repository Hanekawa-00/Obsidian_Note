### 常见的垃圾回收算法：
1. **复制算法**：将内存平均分成两个部分，然后每次只使用其中一部分，当这部分内存占满之后复制到另一个部分（在这时进行垃圾回收），然后清空这部分。在新生代的幸存者区就是使用这种算法。
	* **优点**：实现简单，不产生内存碎片，提高了内存利用率
	* **缺点**：因为将内存缩小了一半，浪费了一半的空间，代价太高，而且在对象存活率较高的情况下，复制对象太浪费时间，因此适合用在**存活率较低，对象数量少**的地方，比如说幸存者区（***Survivor***）
2. **标记清除法**：使用**可达性算法**标记可以回收(已经判定为死亡)的对象，然后进行垃圾回收
	* **缺点**：效率低，需要两次遍历；标记清除后会产生大量不连续的碎片。JVM就不得不维持一个内存的空闲列表，这又是一种开销。而且在分配数组对象的时候，寻找连续的内存空间会不太好找。
3. **标记压缩法(标记整理法)**：在标记删除法的基础上进行了改进，同样是标记死亡对象，但是存活对象向一端移动，然后清除所有边界外的对象
	* **优点**：弥补了复制算法的内存利用率低和标记清除法的内存碎片化的问题
	* **缺点**：如果存活的对象较多，在整理的时候进行太多的复制操作导致算法效率太低
### JVM使用的垃圾回收算法：
JVM使用的是分代回收算法，实际上就是复制算法和标记整理法的结合。
因为老年代相对很少进行垃圾回收，对象存活率高，一般采用标记删除和标记整理的混合实现。
而复制算法的效率只和存活对象的大小有关，通过hotspot中的两个幸存者区的设计得到缓解