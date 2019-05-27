# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/1/19 12:13'

from metadata.file_info import MetadataFileInfo
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    print("metadata file info")
    metadata_file_info = MetadataFileInfo()

    # user_name = "liuyf"
    # dir_path = user_name+"/dir"
    # file_path = user_name+"/test.txt"
    # file_info = {"file_id": "293847103564", "file_size": 10245}  # 内容空视为文件夹

    user_name = "刘"
    dir_path = "刘/目录"
    file_path = "刘/文件.txt"
    file_info = {"file_id": "293847103564", "file_size": 10245}  # 内容空视为文件夹

    print("check file exists")
    res = metadata_file_info.check_file_exists(file_path)  # file不存在
    print(res)

    print("create file info")
    res = metadata_file_info.create_file_info(file_path, file_info)  # 新建file
    print(res)
    res = metadata_file_info.create_file_info(file_path, file_info)  # 新建file, file已存在，操作失败
    print(res)
    res = metadata_file_info.create_file_info(file_path, file_info, cover=True)  # 新建file，file已存在则覆盖
    print(res)
    res = metadata_file_info.create_file_info(dir_path+'/test2.pdf', file_info)  # 新建file, file已存在，操作失败
    print(res)

    print("check file exists")
    res = metadata_file_info.check_file_exists(file_path)  # file存在
    print(res)

    print("get file info")
    res = metadata_file_info.get_file_info("")  # 获取file信息，为空
    print(res)
    res = metadata_file_info.get_file_info(file_path)  # 获取file信息
    print(res)
    res = metadata_file_info.get_file_info("wrong")  # 获取file信息，file不存在，操作失败
    print(res)


    print("list dir name")
    res = metadata_file_info.list_dir_name("")  # file名列表，根目录
    print(res)
    res = metadata_file_info.list_dir_name(user_name)  # file名列表
    print(res)
    res = metadata_file_info.list_dir_name(file_path)  # file名列表
    print(res)
    res = metadata_file_info.list_dir_name("wrong")  # file名列表，file不存在，操作失败
    print(res)

    print("list dir info")
    res = metadata_file_info.list_dir_info("")  # file信息列表，根目录
    print(res)
    res = metadata_file_info.list_dir_info(user_name)  # file信息列表
    print(res)
    res = metadata_file_info.list_dir_info(file_path)  # file信息列表
    print(res)
    res = metadata_file_info.list_dir_info("wrong")  # file信息列表，file不存在，操作失败
    print(res)

    print("list all dir name")
    res = metadata_file_info.list_all_dir_name("")  # file信息列表，根目录
    print(res)
    res = metadata_file_info.list_all_dir_name(user_name)  # file信息列表
    print(res)
    res = metadata_file_info.list_all_dir_name(dir_path)  # file信息列表
    print(res)
    res = metadata_file_info.list_all_dir_name("wrong")  # file信息列表，file不存在，操作失败
    print(res)

    print("list all dir info")
    res = metadata_file_info.list_all_dir_info("")  # file信息列表，根目录
    print(res)
    res = metadata_file_info.list_all_dir_info(user_name)  # file信息列表
    print(res)
    res = metadata_file_info.list_all_dir_info(dir_path)  # file信息列表
    print(res)
    res = metadata_file_info.list_all_dir_info("wrong")  # file信息列表，file不存在，操作失败
    print(res)

    print("delete file info")
    res = metadata_file_info.delete_file_info(file_path)  # 删除file
    print(res)
    res = metadata_file_info.delete_file_info(file_path)  # 删除file, file不存在，操作失败
    print(res)

    print("create dir info")
    res = metadata_file_info.create_dir_info(dir_path+"/new/dir1/1")  # 新建dir
    print(res)
    res = metadata_file_info.create_dir_info(dir_path+"/new/dir1/1")  # 新建dir, dir已存在
    print(res)

    print("delete dir info")
    res = metadata_file_info.delete_file_info(dir_path+"/new/dir1")  # 删除dir, 存在children，操作失败
    print(res)
    res = metadata_file_info.delete_file_info(dir_path+"/new/dir1", recursive=True)  # 删除dir，存在children,则递归删除
    print(res)
    res = metadata_file_info.delete_file_info(dir_path+"/new")  # 删除dir, 正常
    print(res)
    res = metadata_file_info.delete_file_info(dir_path+"/new")  # 删除dir, dir不存在，操作失败
    print(res)

    metadata_file_info.delete_dir_info(user_name)  # 删除测试用户下所有目录
    metadata_file_info.zk_stop()  # 关闭连接

