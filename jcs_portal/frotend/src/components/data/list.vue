<template>
  <section>
    <!--列表-->
    <template>
      <el-table  highlight-current-row :data="List" style="width: 100%;">
        <el-table-column type="index" label="序号" width="120">
        </el-table-column>
        <el-table-column prop="name" label="proxy_name" width="250">
        </el-table-column>
        <el-table-column prop="operate" label="file_operate" width="250">
        </el-table-column>
        <el-table-column prop="date" label="日期" width="250">
        </el-table-column>
        <el-table-column prop="detail" label="详细信息" min-width="100">
        </el-table-column>
      </el-table>
    </template>

  </section>
</template>

<script type="text/ecmascript-6">
  const cloud=['aliyun-beijing','baiduyun-beijing','ksyun-beijing'];
  const op=['get_file','get_url','put_file','delete_file'];
  export default {
    data() {
      return {
        List:[]
      }
    },
    created() {
      this.fetch_data();
    },
    methods: {
      fetch_data: function () {
        for (let i = 0; i < 30; i++) {
          this.List.push({
            id: i,
            name:cloud[Math.round(Math.random()*(cloud.length-1))],
            operate:op[Math.round(Math.random()*(op.length-1))],
            date:new Date(parseInt(1483200000+Math.random()*20000000) * 1000).toLocaleString().replace(/:\d{1,2}$/,' '),
            detail:""
          });
        }
      }
    }
  }

</script>

<style>
</style>
