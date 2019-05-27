# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/6/26 13:04'

from optimizer.storage_cost import StorageCost

class MigrationPolicy(object):
    def __init__(self):
        pass

    def migration_policy(self, file_metadata, old_policy, new_policy):
        # 迁移策略和迁移成本
        migration_diff = self.get_list_diff(old_policy['bucket_name_list'], new_policy['bucket_name_list'])
        migration_cost = self.cal_migration_cost(file_metadata, migration_diff)
        return migration_diff, migration_cost

    def cal_migration_cost(self, file_metadata, bucket_diff):
        """
        计算迁移成本，即需要下载的纠删码块成本
        :param file_metadata:
        :param old_policy:
        :param new_policy:
        :return:
        """
        storage_features = {
            'storage_size': file_metadata['block_size'],
            'storage_time': file_metadata['storage_time'],
            'download_size': file_metadata['block_size'] * file_metadata['storage_time'] * 1,
            'request_frequency': 1,  # 下载一次的成本
        }
        print "*************"
        print 'storage_features', storage_features
        migration_cost = 0.0
        storage_cost_cal = StorageCost()
        for bucket_name in bucket_diff:
            sotrage_cost_res = storage_cost_cal.get_storage_cost(storage_features, bucket_name)
            migration_cost += sotrage_cost_res['download_expense']
            print "sotrage_cost_res['download_expense']", sotrage_cost_res['download_expense']
        print 'migration_cost', migration_cost
        return migration_cost

    def get_list_diff(self, old_list, new_list):
        """
        两个list进行diff，组成diff_dict
        :param old_list:
        :param new_list:
        :return:
        """
        old_diff = []
        for old_one in old_list:
            if old_one not in new_list:
                old_diff.append(old_one)
        new_diff = []
        for new_one in new_list:
            if new_one not in old_list:
                new_diff.append(new_one)
        diff_dict = {}
        for i, old_one in enumerate(old_diff):
            diff_dict[old_one] = new_diff[i]
        return diff_dict

