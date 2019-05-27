webpackJsonp([1],{NHnr:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var n=a("7+uW"),i={name:"ElContainer",componentName:"ElContainer",props:{direction:String},computed:{isVertical:function(){return"vertical"===this.direction||"horizontal"!==this.direction&&(!(!this.$slots||!this.$slots.default)&&this.$slots.default.some(function(t){var e=t.componentOptions&&t.componentOptions.tag;return"el-header"===e||"el-footer"===e}))}}},r={render:function(){var t=this.$createElement;return(this._self._c||t)("section",{staticClass:"el-container",class:{"is-vertical":this.isVertical}},[this._t("default")],2)},staticRenderFns:[]},o={components:{ElContainer:a("VU/8")(i,r,!1,null,null,null).exports},data:function(){return{activeIndex:"1",activeIndex2:"1"}},mounted:function(){var t=sessionStorage.getItem("user");t?(t=JSON.parse(t),this.sysUserName=t.name||"",this.sysUserAvatar=t.avatar||""):this.$router.push({path:"/login"})},methods:{handleSelect:function(t,e){console.log(t,e)}}},l={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("el-container",[a("el-header",[a("el-menu",{staticClass:"el-menu-demo",attrs:{"default-active":t.activeIndex,mode:"horizontal"},on:{select:t.handleSelect}},[a("h3",{staticStyle:{float:"left"}},[t._v("Joint Cloud   ")]),t._v(" "),a("el-menu-item",{attrs:{index:"1"}},[a("router-link",{attrs:{to:"/cloud"}},[t._v("云际存储")])],1),t._v(" "),a("el-submenu",{attrs:{index:"2"}},[a("template",{slot:"title"},[t._v("云际监控")]),t._v(" "),a("el-menu-item",{attrs:{index:"2-1"}},[a("router-link",{attrs:{to:"/data/list"}},[t._v("操作记录")])],1),t._v(" "),a("el-menu-item",{attrs:{index:"2-2"}},[a("router-link",{attrs:{to:"/data/map"}},[t._v("地理分布")])],1)],2)],1)],1),t._v(" "),a("el-main",[a("router-view")],1),t._v(" "),a("el-footer")],1)},staticRenderFns:[]};var s=a("VU/8")(o,l,!1,function(t){a("eV5E")},null,null).exports,c=a("/ocq"),u=a("bOdI"),d=a.n(u),m=a("mtWM"),h=a.n(m),p={data:function(){return d()({fileList:[],bread:[{path:"/",desc:"全部文件"}],current:{dir:"",page:"1",num:"100",desc:"1",order:"size"}},"fileList",[])},created:function(){sessionStorage.getItem("user")||this.$router.push({path:"/login"}),this.fetch_data()},methods:{change_dir:function(){this.current.dir="",this.fetch_data()},check_file:function(t){"文件夹"==t.isdir?(""!=this.current.dir&&(this.current.dir+="/"),this.current.dir+=t.name,this.fetch_data()):this.download_file(t)},delete_file:function(t){var e=this,a=this.current;"文件夹"==t.isdir?this.$confirm("此操作将删除该文件夹以及文件夹下全部文件, 是否继续?","提示",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then(function(){h.a.post("/api/cloud/delete_dir",{dir:""==a.dir?t.name:a.dir+"/"+t.name}).then(function(t){console.log(t)}),e.$message({type:"success",message:"删除成功!"}),e.fetch_data()}).catch(function(){e.$message({type:"info",message:"已取消删除"})}):this.$confirm("此操作将删除该文件, 是否继续?","提示",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then(function(){h.a.post("/api/cloud/delete_file",{dir:""==a.dir?t.name:a.dir+"/"+t.name}).then(function(t){console.log(t)}),e.$message({type:"success",message:"删除成功!"}),e.fetch_data()}).catch(function(){e.$message({type:"info",message:"已取消删除"})})},download_file:function(t){var e=this.current;h.a.post("/api/cloud/download",{dir:""==e.dir?t.name:e.dir+"/"+t.name}).then(function(t){console.log(t.data)})},fetch_data:function(){var t=this,e=this.current;this.fileList=[],h.a.post("/api/cloud/get",{params:e}).then(function(e){if(e=e.data,console.log(e),0===e.status)for(var a in e.result)t.fileList.push({name:e.result[a].file_name,isdir:1==e.result[a].isdir?"文件夹":"文件",size:1==e.result[a].isdir?"-":e.result[a].size,ctime:1==e.result[a].isdir?"-":new Date(1e3*parseInt(e.result[a].ctime)).toLocaleString().replace(/:\d{1,2}$/," "),cloud:1==e.result[a].isdir?"-":e.result[a].cloud})})},create_dir:function(){var t=this,e=this.current;this.$prompt("请输入名称","新建文件夹",{confirmButtonText:"确定",cancelButtonText:"取消"}).then(function(a){var n=a.value;h.a.post("/api/cloud/create",{dir:""==e.dir?n:e.dir+"/"+n}).then(function(t){console.log(t)}),t.$message({type:"success",message:"新建文件夹: "+n}),t.fetch_data()}).catch(function(){t.$message({type:"info",message:"取消输入"})})}}},f={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[[a("el-button",{attrs:{type:"primary"}},[a("el-upload",{staticClass:"upload-demo",attrs:{action:"update"}},[t._v("点击上传\n      ")])],1),t._v(" "),a("el-button",{on:{click:t.create_dir}},[t._v("新建文件夹")]),t._v("  \n    "),a("el-button",{attrs:{type:"text"},on:{click:function(e){t.change_dir()}}},[t._v("全部文件")]),t._v(" \n    "),a("span",{staticStyle:{color:"#409eff"}},[t._v("/"+t._s(t.current.dir))])],t._v(" "),[a("el-table",{staticStyle:{width:"100%"},attrs:{"highlight-current-row":"",data:t.fileList}},[a("el-table-column",{attrs:{prop:"name",label:"文件名",width:"250"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("el-button",{attrs:{type:"text"},on:{click:function(a){t.check_file(e.row)}}},[t._v(t._s(e.row.name))])]}}])}),t._v(" "),a("el-table-column",{attrs:{prop:"isdir",label:"文件类型",width:"150"}}),t._v(" "),a("el-table-column",{attrs:{prop:"size",label:"大小",width:"100"}}),t._v(" "),a("el-table-column",{attrs:{prop:"ctime",label:"修改时间",width:"200"}}),t._v(" "),a("el-table-column",{attrs:{prop:"cloud",label:"存储云端",width:"200"}}),t._v(" "),a("el-table-column",{attrs:{prop:"md5_value",label:"操作",width:"300"},scopedSlots:t._u([{key:"default",fn:function(e){return[a("el-button",{attrs:{type:"text"},on:{click:function(a){t.delete_file(e.row)}}},[t._v("删除")]),t._v(" "),a("el-button",{attrs:{type:"text"},on:{click:function(a){t.download_file(e.row)}}},[t._v("下载")])]}}])})],1)]],2)},staticRenderFns:[]};var v=a("VU/8")(p,f,!1,function(t){a("y8xx")},null,null).exports,g=a("XLwt");a("Bhwq");var y={data:function(){return{main:null,chartColumn:null,chartBar:null,chartLine:null,chartPie:null}},created:function(){sessionStorage.getItem("user")||this.$router.push({path:"/login"})},methods:{drawmainChart:function(){this.main=g.init(document.getElementById("main"));var t=[[{name:"阿里云上海"},{memory:100,number:95}],[{name:"百度云上海"},{memory:50,number:90}],[{name:"阿里云北京"},{memory:30,number:80}],[{name:"百度云北京"},{memory:90,number:30}],[{name:"金山云北京"},{memory:60,number:30}],[{name:"阿里云广州"},{memory:80,number:30}]],e=[];[["阿里云上海",[121.22551,31.771022]],["百度云上海",[121.2991,30.950075]],["阿里云北京",[116.589392,40.863174]],["百度云北京",[117.178105,40.217526]],["金山云北京",[115.651129,39.679441]],["阿里云广州",[113.5107,23.2196]]].forEach(function(a,n){e.push({name:a[0],type:"effectScatter",coordinateSystem:"geo",zlevel:2,rippleEffect:{brushType:"stroke"},label:{normal:{show:!0,position:"right",formatter:"{b}"}},symbolSize:function(){return t[n][1].memory/8},data:a[1].map(function(){return{name:t[n][0].name,value:a[1]}})})}),this.main.setOption({tooltip:{padding:10,backgroundColor:"#222",borderColor:"#777",borderWidth:1,formatter:function(e){e.data;return'<div style="border-bottom: 1px solid rgba(255,255,255,.3); font-size: 18px;padding-bottom: 7px;margin-bottom: 7px">'+e.seriesName+"</div>存储量："+t[e.dataIndex][1].memory+"G<br>文件个数："+t[e.dataIndex][1].number+"<br>"}},title:{text:"数据地理分布"},geo:{map:"china",label:{emphasis:{show:!1}},roam:!0,left:"3%",itemStyle:{normal:{areaColor:"#C4C4C4",borderColor:"#FFFFFF"}}},series:e})},drawmainChart2:function(){this.chartColumn=g.init(document.getElementById("main2")),this.chartColumn.setOption({title:{text:"云际间数据传输"},tooltip:{},animationDurationUpdate:1500,animationEasingUpdate:"quinticInOut",series:[{type:"graph",layout:"none",symbolSize:50,label:{normal:{show:!0}},edgeLabel:{normal:{textStyle:{fontSize:20}}},data:[{name:"阿里云北京",x:350,y:100,value:30,itemStyle:{normal:{color:"#ff6600"}},symbolSize:"50"},{name:"百度云北京",x:450,y:100,value:90,symbolSize:"90"},{name:"金山云北京",x:400,y:120,value:60,itemStyle:{normal:{color:"#09F7F7"}},symbolSize:"60"},{name:"阿里云上海",x:500,y:300,value:100,itemStyle:{normal:{color:"#ff6600"}},symbolSize:"100"},{name:"百度云上海",x:550,y:300,value:50,symbolSize:"50"},{name:"阿里云广州",x:350,y:400,value:60,itemStyle:{normal:{color:"#ff6600"}},symbolSize:"60"}],links:[{source:"阿里云北京",target:"金山云北京",value:5,z:100,lineStyle:{normal:{width:2,color:"#FFCC00"}}},{source:"金山云北京",target:"百度云北京",value:5,z:100,lineStyle:{normal:{width:1,color:"#2BD54D"}}},{source:"阿里云北京",target:"阿里云广州",value:5,z:100,lineStyle:{normal:{width:5,color:"#FFCC00"}}},{source:"百度云上海",target:"百度云北京",value:10,z:100,lineStyle:{normal:{width:10,color:"#2BD54D"}}},{source:"百度云北京",target:"阿里云上海",value:6,z:100,lineStyle:{normal:{width:6,color:"#FFCC00"}}},{source:"阿里云上海",target:"阿里云北京",value:4,z:100,lineStyle:{normal:{width:4,color:"#FFCC00"}}}]}]})},drawColumnChart:function(){this.chartColumn=g.init(document.getElementById("chartColumn")),this.chartColumn.setOption({title:{text:"存储量"},tooltip:{},xAxis:{data:["阿里云上海","百度云上海","阿里云北京","百度云北京","金山云北京","阿里云广州"]},yAxis:{},series:[{name:"存储量",type:"bar",data:[100,50,30,90,60,80]}]})},drawBarChart:function(){this.chartBar=g.init(document.getElementById("chartBar")),this.chartBar.setOption({title:{text:"用户流量"},tooltip:{trigger:"axis",axisPointer:{type:"shadow"}},legend:{data:["上传量","下载量"]},grid:{left:"3%",right:"4%",bottom:"3%",containLabel:!0},xAxis:{type:"value",boundaryGap:[0,.01]},yAxis:{type:"category",data:["阿里云上海","百度云上海","阿里云北京","百度云北京","金山云北京","阿里云广州"]},series:[{name:"上传量",type:"bar",data:[18,23,29,10,13,16]},{name:"下载量",type:"bar",data:[19,23,31,12,13,6]}]})},drawLineChart:function(){this.chartLine=g.init(document.getElementById("chartLine")),this.chartLine.setOption({title:{text:""},tooltip:{trigger:"axis"},legend:{data:["邮件营销","联盟广告","搜索引擎"]},grid:{left:"3%",right:"4%",bottom:"3%",containLabel:!0},xAxis:{type:"category",boundaryGap:!1,data:["周一","周二","周三","周四","周五","周六","周日"]},yAxis:{type:"value"},series:[{name:"上传",type:"line",stack:"总量",data:[120,132,101,134,90,230,210]},{name:"下载",type:"line",stack:"总量",data:[220,182,191,234,290,330,310]},{name:"浏览",type:"line",stack:"总量",data:[820,932,901,934,1290,1330,1320]}]})},drawPieChart:function(){this.chartPie=g.init(document.getElementById("chartPie")),this.chartPie.setOption({title:{text:"Pie Chart",subtext:"纯属虚构",x:"center"},tooltip:{trigger:"item",formatter:"{a} <br/>{b} : {c} ({d}%)"},legend:{orient:"vertical",left:"left",data:["上传","下载","操作"]},series:[{name:"访问来源",type:"pie",radius:"55%",center:["50%","60%"],data:[{value:335,name:"上传"},{value:310,name:"下载"},{value:234,name:"操作"}],itemStyle:{emphasis:{shadowBlur:10,shadowOffsetX:0,shadowColor:"rgba(0, 0, 0, 0.5)"}}}]})},drawCharts:function(){this.drawmainChart(),this.drawmainChart2(),this.drawColumnChart(),this.drawBarChart(),this.drawLineChart(),this.drawPieChart()}},mounted:function(){this.drawCharts()},updated:function(){this.drawCharts()}},b={render:function(){var t=this.$createElement,e=this._self._c||t;return e("section",{staticClass:"chart-container"},[e("el-row",[e("el-col",{attrs:{span:13}},[e("div",{staticStyle:{width:"100%",height:"800px"},attrs:{id:"main"}})]),this._v(" "),e("el-col",{attrs:{span:11}},[e("div",{staticStyle:{width:"100%",height:"800px"},attrs:{id:"main2"}})]),this._v(" "),e("el-col",{attrs:{span:12}},[e("div",{staticStyle:{width:"100%",height:"400px"},attrs:{id:"chartColumn"}})]),this._v(" "),e("el-col",{attrs:{span:12}},[e("div",{staticStyle:{width:"100%",height:"400px"},attrs:{id:"chartBar"}})]),this._v(" "),e("el-col",{attrs:{span:12}},[e("div",{staticStyle:{width:"100%",height:"400px"},attrs:{id:"chartLine"}})]),this._v(" "),e("el-col",{attrs:{span:12}},[e("div",{staticStyle:{width:"100%",height:"400px"},attrs:{id:"chartPie"}})])],1)],1)},staticRenderFns:[]};var _=a("VU/8")(y,b,!1,function(t){a("mUDM")},null,null).exports,x=["aliyun-beijing","baiduyun-beijing","ksyun-beijing"],w=["get_file","get_url","put_file","delete_file"],C={data:function(){return{List:[]}},created:function(){sessionStorage.getItem("user")||this.$router.push({path:"/login"}),this.fetch_data()},methods:{fetch_data:function(){for(var t=0;t<30;t++)this.List.push({id:t,name:x[Math.round(Math.random()*(x.length-1))],operate:w[Math.round(Math.random()*(w.length-1))],date:new Date(1e3*parseInt(14832e5+2e7*Math.random())).toLocaleString().replace(/:\d{1,2}$/," "),detail:""})}}},S={render:function(){var t=this.$createElement,e=this._self._c||t;return e("section",[[e("el-table",{staticStyle:{width:"100%"},attrs:{"highlight-current-row":"",data:this.List}},[e("el-table-column",{attrs:{type:"index",label:"序号",width:"120"}}),this._v(" "),e("el-table-column",{attrs:{prop:"name",label:"proxy_name",width:"250"}}),this._v(" "),e("el-table-column",{attrs:{prop:"operate",label:"file_operate",width:"250"}}),this._v(" "),e("el-table-column",{attrs:{prop:"date",label:"日期",width:"250"}}),this._v(" "),e("el-table-column",{attrs:{prop:"detail",label:"详细信息","min-width":"100"}})],1)]],2)},staticRenderFns:[]};var k=a("VU/8")(C,S,!1,function(t){a("yuQ3")},null,null).exports,F={data:function(){return{logining:!1,ruleForm2:{account:"actuser",checkPass:"123456"},rules2:{account:[{required:!0,message:"请输入账号",trigger:"blur"}],checkPass:[{required:!0,message:"请输入密码",trigger:"blur"}]},checked:!0}},created:function(){sessionStorage.getItem("user")||this.$router.push({path:"/cloud"})},methods:{handleReset2:function(){this.$refs.ruleForm2.resetFields()},handleSubmit2:function(t){sessionStorage.setItem("user","actuser"),this.$router.push({path:"/cloud"})}}},$={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("el-form",{ref:"ruleForm2",staticClass:"demo-ruleForm login-container",attrs:{model:t.ruleForm2,rules:t.rules2,"label-position":"left","label-width":"0px"}},[a("h3",{staticClass:"title"},[t._v("系统登录")]),t._v(" "),a("el-form-item",{attrs:{prop:"account"}},[a("el-input",{attrs:{type:"text","auto-complete":"off",placeholder:"账号"},model:{value:t.ruleForm2.account,callback:function(e){t.$set(t.ruleForm2,"account",e)},expression:"ruleForm2.account"}})],1),t._v(" "),a("el-form-item",{attrs:{prop:"checkPass"}},[a("el-input",{attrs:{type:"password","auto-complete":"off",placeholder:"密码"},model:{value:t.ruleForm2.checkPass,callback:function(e){t.$set(t.ruleForm2,"checkPass",e)},expression:"ruleForm2.checkPass"}})],1),t._v(" "),a("el-checkbox",{staticClass:"remember",attrs:{checked:""},model:{value:t.checked,callback:function(e){t.checked=e},expression:"checked"}},[t._v("记住密码")]),t._v(" "),a("el-form-item",{staticStyle:{width:"100%"}},[a("el-button",{staticStyle:{width:"100%"},attrs:{type:"primary",loading:t.logining},nativeOn:{click:function(e){e.preventDefault(),t.handleSubmit2(e)}}},[t._v("登录")])],1)],1)},staticRenderFns:[]};var z=a("VU/8")(F,$,!1,function(t){a("OvcN")},"data-v-0c25b4e8",null).exports;n.default.use(c.a);var B=new c.a({mode:"history",routes:[{path:"/",redirect:"/login"},{path:"/login",component:z},{path:"/cloud",component:v},{path:"/data/map",component:_},{path:"/data/list",component:k}]}),L=a("zL8q"),I=a.n(L);a("tvR6");n.default.use(I.a),n.default.config.productionTip=!1,new n.default({el:"#app",router:B,components:{App:s},template:"<App/>"})},OvcN:function(t,e){},eV5E:function(t,e){},mUDM:function(t,e){},tvR6:function(t,e){},y8xx:function(t,e){},yuQ3:function(t,e){}},["NHnr"]);
//# sourceMappingURL=app.814b1de8755167836f18.js.map