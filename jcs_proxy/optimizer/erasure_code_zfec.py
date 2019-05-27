# coding: utf-8
__author__ = 'liuyf'
__date__ = '2018/5/2 16:26'

import os
import zfec

class ErasureCodeZfec(object):
    def __init__(self):
        pass

    def split_file(self, file_path, dst_path, erasure_code_n, erasure_code_k):
        split_file = file(file_path, 'r')
        file_size = os.path.getsize(file_path)
        blocks_prefix = file_path
        zfec.filefec.encode_to_files(split_file, file_size, dst_path, blocks_prefix,
                                     erasure_code_k, erasure_code_n, overwrite=True)
        split_file.close()

    def merge_blocks(self, blocks_path_list, dst_path):
        merge_file = file(dst_path, 'w+b')
        merge_blocks_list = []
        for block_path in blocks_path_list:
            merge_block = file(block_path, 'rb')
            merge_blocks_list.append(merge_block)
        zfec.filefec.decode_from_files(merge_file, merge_blocks_list)
        for merge_block in merge_blocks_list:
            merge_block.close()
        merge_file.close()



if __name__ == '__main__':
    ec_zfec = ErasureCodeZfec()

    file_path = '/storage/liuyf_test/jcsProxyDir/datatest/test_4'
    dst_path = file_path
    erasure_code_n = 5
    erasure_code_k = 3
    print 'split file'
    ec_zfec.split_file(file_path, dst_path, erasure_code_n, erasure_code_k)

    blocks_path_list = []
    for i in range(erasure_code_n):
        if erasure_code_n > 9 and i <= 9:
            block_path = '/storage/liuyf_test/jcsProxyDir/datatest/test_4.0' + str(i) + '_' + str(erasure_code_n) + '.fec'
        else:
            block_path = '/storage/liuyf_test/jcsProxyDir/datatest/test_4.'+str(i)+'_'+str(erasure_code_n)+'.fec'
        blocks_path_list.append(block_path)


    dst_path = file_path+'_merge'
    print 'merge blocks'
    ec_zfec.merge_blocks(blocks_path_list, dst_path)

    # 删除纠删码块
    for local_block_path in blocks_path_list:
        os.remove(local_block_path)

