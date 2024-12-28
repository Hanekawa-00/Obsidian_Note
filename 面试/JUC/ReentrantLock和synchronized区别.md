* `synchronized`是一个独占锁，加锁和解锁全部自动进行，操作简短，但是它不够灵活。而`ReentrantLock` 也是独占锁，但是加锁和解锁需要手动进行，比较灵活。
* 二者都是可重入锁。
* `synchronized`不可以[[响应中断]]，一个线程获取不到锁就一直等待；`ReentrantLock`可以响应中断。
* `sychronized`不具备公平锁的特点，而`ReentrantLock` 可以手动设计成公平锁。