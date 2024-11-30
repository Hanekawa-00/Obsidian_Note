import os

def remove_part_from_filenames(directory, part_to_remove):
    """
    批量去掉文件名中的一部分，包括子文件夹中的文件
    :param directory: 文件所在的目录
    :param part_to_remove: 需要去掉的文件名部分
    """
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if part_to_remove in filename:
                # 新文件名
                new_name = filename.replace(part_to_remove, "")
                # 旧文件的完整路径
                old_file = os.path.join(root, filename)
                # 新文件的完整路径
                new_file = os.path.join(root, new_name)
                # 重命名文件
                os.rename(old_file, new_file)
                print(f"重命名 {old_file} 为 {new_file}")

# 示例用法
directory = r"C:\Users\Administrator\Downloads\课件"  # 替换为你的目录路径
part_to_remove = "【微 信 号 itcodeba 】【综合 网站 todo1024.com】"  # 替换为你想要去掉的文件名部分
remove_part_from_filenames(directory, part_to_remove)

