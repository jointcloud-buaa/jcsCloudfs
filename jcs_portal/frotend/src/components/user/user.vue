<template>
    <section class="chart-container">
        <el-row style="border:1px solid #6d9eeb;">
            <h3 style="margin-left:20px;">用户信息&nbsp;&nbsp;&nbsp;</h3>
            <el-form ref="form" :model="form" label-width="80px" style="margin:20px;">
                <el-form :inline="true" :model="form" class="demo-form-inline">
                    <el-form-item label="登陆账号">
                        <el-input v-model="form.name" :disabled="true"></el-input>
                    </el-form-item>
                    <el-form-item label="密码">
                        <el-input v-model="form.password"></el-input>
                    </el-form-item>
                </el-form>
                <el-form :inline="true" :model="form" class="demo-form-inline">
                    <el-form-item label="邮箱">
                        <el-input v-model="form.mail"></el-input>
                    </el-form-item>
                    <el-form-item label="电话">
                        <el-input v-model="form.phone"></el-input>
                    </el-form-item>
                </el-form>
                <el-button type="primary" @click="edit">修改</el-button>
            </el-form>
        </el-row>
        <el-row style="border:1px solid #6d9eeb;margin-top:20px;">
            <h3 style="margin-left:20px;">云际存储&nbsp;&nbsp;&nbsp;</h3>
            <el-col :span="12">
                <div id="main1" style="width:100%; height:500px;"></div>
            </el-col>
            <el-col :span="12">
                <div id="main2" style="width:100%; height:500px;"></div>
            </el-col>

        </el-row>
    </section>
</template>

<script type="text/ecmascript-6">
import axios from "axios";
var echarts = require('echarts');
const ERR_OK = 0;

export default {
  data() {
    return {
        pie:null,
        line:null,
        form: {
            name: sessionStorage.getItem('user'),
            mail:sessionStorage.getItem('mail'),
            password:sessionStorage.getItem('password'),
            phone:sessionStorage.getItem('phone')
        },
        result:null,
        cloudstatistics:{}
    }
  },
  created() {
    this.fetch_data();
  },
  methods: {
      fetch_data(){
          var form=this.form;
          axios.post('/api/user/map',{form }).then((response) => {
          this.cloudstatistics=response.data;
          console.log(this.cloudstatistics)
          this.drawCharts()
        });
      },
      edit() {
        var form=this.form;
        this.$confirm('此操作将修改用户信息, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
            axios.post("/api/user/edit",{ form }).then(response => {
                if(response.data.status==ERR_OK){
                  sessionStorage.setItem('password', form.password);
                  sessionStorage.setItem('mail', form.mail);
                  sessionStorage.setItem('phone', form.phone);
                }
            });
            this.$message({
              type: 'success',
              message: '修改成功!'
            });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消'
          });
        });
      },
      drawmainChart(){
        this.main=echarts.init(document.getElementById('main1'));
        this.main.setOption({
          title: { text: '各地域云内存储数据量' },
          xAxis: {
            type: 'value'
          },
          yAxis: {
            type: 'category',
            data: this.cloudstatistics['cloud_bar'][0],
            axisLabel: {
              interval: 0,
              rotate: 30
            },
          },
          series: [{
            name:this.cloudstatistics['cloud_bar'][0]+':'+this.cloudstatistics['cloud_bar'][1],
            data: this.cloudstatistics['cloud_bar'][1],
            label: {
              normal: {
                position: 'right',
                show: true
              }
            },
            type: 'bar',
            color:'#4472C4'
          }]
        })
      },
      drawmainChart2() {
        var cloudstatistics = this.cloudstatistics;
        var links=[];
        var planePath = 'path://M 200 100 L 300 300 L 100 300 z';
        cloudstatistics['cloud_trans'].forEach(
          function(item,i){
            var x1=item[1];
            var y1=item[2];
            var x2=item[4];
            var y2=item[5];
            links.push({
              name:item[0]+'->'+item[3]+':'+item[6],
              coords:[[x1,y1],[x2,y2]],
              lineStyle:{
                width:item[6]/10+1,
                color:item[7],
                opacity:1,
                curveness: 0.2,
              },
            })
          }
        )
        this.chartColumn = echarts.init(document.getElementById('main2'));
        this.chartColumn.setOption({
          title: { text: '云际间数据传输' },
          backgroundColor:'#F0F0F0',
          tooltip: {},
          xAxis: {
            show:false,
            type: 'value',
            name: 'x轴',
            min:0,
            max:90
          },
          yAxis: {
            show:false,
            type: 'value',
            name: 'y轴',
            min:0,
            max:90
          },
          series : [{
            tooltip:{
              show:false,
            },
            type: 'scatter',
            data: cloudstatistics['cloud_used_storage'],
            z:2,
            symbolSize: function (data) {
              return data[4]*2+10;
            },
            itemStyle:{
              color:function(param){
                return param.data[3];
              },
            },
            label: {
              emphasis: {
                show: true,
                formatter: function (param) {
                  return param.data[2];
                },
                position: 'top'
              }
            },
          },{
            tooltip:{
              show:false,
            },
            type: 'scatter',
            symbol:'roundRect',
            symbolSize:[200,100],
            itemStyle:{
              borderWidth:1,
              borderColor:'#000000',
              borderStyle:'dashed',
              color:'#FFFFFF',
            },
            data: cloudstatistics['cloud_block'],
            label: {
              emphasis: {
                show: true,
                color:'#000',
                fontsize:15,
                formatter: function (param) {
                  return param.data[2];
                },
                position: 'top'
              }
            },
            z:1,
          },{
            type: 'lines',
            zlevel: 1,
            coordinateSystem:'cartesian2d',
            symbol: ['none', 'arrow'],
            symbolSize: 10,
            effect: {
              show: true,
              period: 6,
              trailLength: 0,
              symbol: planePath,
              symbolSize: 15
            },
            data:links,
          }]
        })
      },
      drawCharts() {
          var form=this.form;
          axios.post("/api/user/stat",{ form }).then(response => {
            this.result=response;
            this.drawmainChart();
            this.drawmainChart2();
        });
    },
  },
  mounted: function() {},
  updated: function() {}
};
</script>

<style>
</style>
