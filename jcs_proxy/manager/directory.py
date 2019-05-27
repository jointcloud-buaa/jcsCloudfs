# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/1/17 16:26'

from metadata.file_info import MetadataFileInfo

class Directory(object):
    """
    文件夹操作
    """
    def __init__(self):
        pass

    def list_dir(self, user_name, cloud_file_path):
        """
        目录列表
        :param user_name:
        :param cloud_file_path:
        :return:
        """
        if cloud_file_path == "":
            cloud_file_key = user_name
        else:
            cloud_file_key = user_name + "/" + cloud_file_path
        metadata_file_info = MetadataFileInfo()
        dict_res = metadata_file_info.list_dir_info(cloud_file_key)
        return dict_res

    def create_dir(self, user_name, cloud_file_path):
        """
        新建文件夹
        :param user_name:
        :param cloud_file_path:
        :return:
        """
        cloud_file_key = user_name + "/" + cloud_file_path
        metadata_file_info = MetadataFileInfo()
        dict_res = metadata_file_info.create_dir_info(cloud_file_key)
        return dict_res

    def delete_dir(self, user_name, cloud_file_path, recursive=False):
        """
        删除文件夹
        :param user_name:
        :param cloud_file_path:
        :param recursive:   是否递归删除
        :return:
        """
        cloud_file_key = user_name + "/" + cloud_file_path
        metadata_file_info = MetadataFileInfo()
        dict_res = metadata_file_info.delete_dir_info(cloud_file_key, recursive)
        return dict_res


if __name__ == '__main__':
    print("directory tree")

    user_name = "liuyf_test"
    cloud_file_path = "newdir"

    dir_tree = Directory()
    res = dir_tree.create_dir(user_name, cloud_file_path)
    print(res)

    res = dir_tree.list_dir(user_name, "")
    print(res)

    res = dir_tree.delete_dir(user_name, cloud_file_path, recursive=True)
    print(res)
