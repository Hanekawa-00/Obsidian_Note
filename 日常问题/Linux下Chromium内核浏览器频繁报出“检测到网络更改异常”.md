建议关闭网络设置中的IPv6，因为IPv6在某些系统中可能会导致错误。以下是具体的解决步骤：
1. **打开GRUB配置文件以编辑**：
   - 打开终端，使用以下命令在Nano编辑器中打开GRUB配置文件：
     ```bash
     sudo nano /etc/default/grub
     ```
   - 使用方向键找到以`GRUB_CMDLINE_LINUX`开头的行，将其值修改为：
     ```bash
     GRUB_CMDLINE_LINUX="ipv6.disable=1"
     ```
   - 保存更改，使用`Ctrl+x`，然后按`Y`或回车确认。
2. **更新GRUB**：
   - 使用以下命令更新GRUB：
     ```bash
     sudo update-grub
     ```
   - 重启系统后，IPv6将被关闭，问题应该得到解决。
尽管在系统设置中关闭IPv6，但问题并没有得到解决，直到使用上述命令行方法。
