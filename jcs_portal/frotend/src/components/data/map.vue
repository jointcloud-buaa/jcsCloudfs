<template>
  <section class="chart-container">
    <el-row>
      <el-col :span="13">
        <div id="main" style="width:100%; height:800px;"></div>
      </el-col>
      <el-col :span="11">
        <div id="main2" style="width:100%; height:800px;"></div>
      </el-col>
    </el-row>
    <el-row>
      <el-col>
        <div id="main3" style="width:100%; height:800px;"></div>
      </el-col>
    </el-row>
  </section>
</template>

<script type="text/ecmascript-6">
  import axios from 'axios';
  var echarts = require('echarts');
  require('echarts/map/js/china');

  export default {
    data() {
      return {
        map:{},
        main:null,
        chartColumn: null,
        chartBar: null,
        chartLine: null,
        chartPie: null,
        cloudstatistics:{}
      }
    },
    created() {
      this.fetch_data();
    },
    methods: {
      fetch_data: function () {
        axios.post('/api/data/map',{}).then((response) => {
          this.cloudstatistics=response.data;
          this.drawCharts()
        });
      },
      drawmainChart() {
        this.main=echarts.init(document.getElementById('main'));
        var cloudstatistics=this.cloudstatistics;
        var geoCoordMap = [
          ['阿里云-青岛', [120.4058131861,36.0373135384],"#FA6B04"],
          ['阿里云-北京', [116.589392,40.863174],"#FA6B04"],
          ['阿里云-张家口', [114.8850547325,40.7697837132],"#FA6B04"],
          ['阿里云-杭州', [120.1530293773,30.1510512690],"#FA6B04"],
          ['阿里云-上海', [121.22551,31.771022],"#FA6B04"],
          ['阿里云-深圳', [114.0776336847,22.4877890441],"#FA6B04"],
          ['阿里云-呼和浩特', [111.8034594563,40.5863721864],"#FA6B04"],
          ['百度云-北京', [117.178105,40.217526], "#4472C4"],
          ['百度云-苏州', [120.5814138099,31.3034063568], "#4472C4"],
          ['百度云-广州', [113.3084422684,23.1162839543], "#4472C4"],
          ['金山云-北京', [115.651129,39.679441], "#7030A0"],
          ['金山云-上海', [121.22551,31.271022], "#7030A0"],
          ['阿里云-青岛-low', [120.9058131861,36.0373135384],"#FA6B04"],
          ['阿里云-北京-low', [117.089392,40.863174],"#FA6B04"],
          ['阿里云-张家口-low', [115.3850547325,40.7697837132],"#FA6B04"],
          ['阿里云-杭州-low', [120.6530293773,30.1510512690],"#FA6B04"],
          ['阿里云-上海-low', [121.72551,31.771022],"#FA6B04"],
          ['阿里云-深圳-low', [114.5776336847,22.4877890441],"#FA6B04"],
          ['阿里云-呼和浩特-low', [112.3034594563,40.5863721864],"#FA6B04"],
          ['百度云-北京-low', [117.678105,40.217526], "#4472C4"],
          ['百度云-苏州-low', [121.0814138099,31.3034063568], "#4472C4"],
          ['百度云-广州-low', [113.8084422684,23.1162839543], "#4472C4"],

        ];
        var point=[];
        geoCoordMap.forEach(
          function(item,i){
            point.push({
              name:item[0],
              type:'effectScatter',
              coordinateSystem:'geo',
              zlevel:2,
              rippleEffect: {
                brushType: 'stroke'
              },
              itemStyle:{
                color:function(param){
                  return item[2];
                },
              },
              label: {
                normal: {
                  show: true,
                  position: 'right',
                  formatter: '{b}'
                }
              },
              data: item[1].map(function () {
                return {
                  value: item[1]
                };
              })
            })
          }
        );
        this.main.setOption({
          tooltip: {
            padding: 10,
            backgroundColor: '#222',
            borderColor: '#777',
            borderWidth: 1,
            formatter: function (obj) {
              var value = obj.data;
              return '<div style="border-bottom: 1px solid rgba(255,255,255,.3); font-size: 18px;padding-bottom: 7px;margin-bottom: 7px">'
                + obj.seriesName
                + '</div>';
            }
          },
          title: {
            text: '数据地理分布'
          },
          geo: {
            map: 'china',
            label: {
              emphasis: {
                show: false
              }
            },
            roam:true,
            left:'3%',
            itemStyle: {
              normal: {
                areaColor: '#C4C4C4',
                borderColor: '#FFFFFF'
              }
            }
          },
          series: point

        });
      },
      drawmainChart2() {
        var cloudstatistics = this.cloudstatistics;
        var links=[];
        var planePath = 'path://M 200 100 L 300 300 L 100 300 z';
        console.log(this.cloudstatistics)
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
                width:item[6]/500+2,
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
              return data[4]*1+10;
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
      drawmainChart3(){
        this.main=echarts.init(document.getElementById('main3'));
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
      drawCharts() {
        this.drawmainChart()
        this.drawmainChart2()
        this.drawmainChart3()
      },
    },
    mounted: function () {

    },
    updated: function () {
      this.drawCharts()
    }
  }
</script>

<style>
  .chart-container {
    width: 100%;
    float: left;
  }
  .el-col {
    padding: 30px 20px;
  }
</style>
