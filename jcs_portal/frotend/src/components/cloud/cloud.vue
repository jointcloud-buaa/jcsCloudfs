<template>
  <div>
    <template>
      <input type="file" name="excelFile" id="excelFile" style="display:none" @change="upload_file">
      <el-button type="primary" @click="choose_file">
        上传文件
      </el-button>
      <el-button @click="dialogVisible = true">传输进度</el-button>
      <el-dialog title="进度" :visible.sync="dialogVisible">
        <el-table :data="gridData">
          <el-table-column property="data" label="文件" width="150"></el-table-column>
          <el-table-column property="type" label="操作" width="200"></el-table-column>
          <el-table-column property="progress" label="进度">
            <template slot-scope="scope">
              <el-progress :percentage="scope.row.progress"></el-progress>
            </template>
          </el-table-column>
        </el-table>
      </el-dialog>
      <el-button @click="create_dir">新建文件夹</el-button>&nbsp;&nbsp;
      <el-button @click="refresh"><i class="el-icon-refresh"></i></el-button>&nbsp;&nbsp;
      <el-button @click="backward"><i class="el-icon-back"></i></el-button>&nbsp;&nbsp;
      <el-button
        type="text"
        @click="change_dir()"
      >全部文件</el-button>&nbsp;
      <span style="color:#409eff">/{{current.dir}}</span>
      <el-button style="float:right" @click="search"><i class="el-icon-search"></i></el-button>&nbsp;&nbsp;
      <el-input style="width:200px;float:right" v-model="input" placeholder="查找文件"></el-input>
    </template>
    <template>
      <el-table  highlight-current-row :data="fileList" style="width: 100%;">
        <el-table-column type="expand" >
      	    <template slot-scope="scope">
            <el-form label-position="left" inline class="demo-table-expand">
                <el-form-item label="名称">
                    <span>{{ scope.row.name }}</span>
                </el-form-item>
                <el-form-item label="总分块" v-if="scope.row.cloud==''">
                    <span>{{ scope.row.erasure_code_n}}</span>
                </el-form-item>
                <el-form-item label="存储云端" v-if="scope.row.cloud==''">
                    <span>{{ scope.row.bucketlist }}</span>
                </el-form-item>
            </el-form>
            </template>
          </el-table-column>
        <el-table-column prop="name" label="文件名" width="250">
          <template slot-scope="scope">
            <el-button @click="check_file(scope.row)" type="text" >{{scope.row.name}}</el-button>
          </template>
        </el-table-column>
        <el-table-column prop="isdir" label="文件类型" width="150">
        </el-table-column>
        <el-table-column prop="size" label="大小" width="100">
        </el-table-column>
        <el-table-column prop="ctime" label="修改时间" width="200">
        </el-table-column>
        <el-table-column prop="cloud" label="存储云端" width="200">
	          <template slot-scope="scope" v-if="scope.row.cloud==''">
                 <img :src="alipicurl" v-if="scope.row.ali" alt="icon" title="阿里云">
                 <img :src="baidupicurl" v-if="scope.row.baidu" alt="icon" title="百度云">
                 <img :src="kspicurl" v-if="scope.row.ks" alt="icon" title="金山云">
            </template>
        </el-table-column>
        <el-table-column prop="md5_value" label="操作" width="300">
          <template slot-scope="scope">
            <el-button type="text" @click="delete_file(scope.row)">删除</el-button>
            <el-button type="text" @click="download_file(scope.row)">下载</el-button>
          </template>
        </el-table-column>
      </el-table>
    </template>
  </div>
</template>
<script type="text/ecmascript-6">
import axios from "axios";
import qs from "qs";
const ERR_OK = 0;
export default {
  data() {
    return {
      fileList: [],
      bread: [
        {
          path: "/",
          desc: "全部文件"
        }
      ],
      current: {
        user : sessionStorage.getItem('user'),
        dir: "",
        page: "1",
        num: "100",
        desc: "1",
        order: "size",
      },
      progress: 0,
      fileList: [],
      dialogVisible: false,
      gridData: [],
      input:"",
      alipicurl:'/static/images/ali.jpg',
      baidupicurl:'/static/images/baidu.jpg',
      kspicurl:'/static/images/ks.jpg',
    };
  },
  created() {
    if (typeof this.$route.query['dir'] === 'undefined') {
        this.$router.push({path: 'cloud', query: {vmode: 'list', dir: this.current.dir}});
      } else {
        this.current.dir = this.$route.query['dir'];
      }
    this.fetch_data();
  },

  methods: {
    change_dir() {
      this.current.dir = "";
      this.$router.push({path: 'cloud', query: {vmode: 'list', dir: this.current.dir}});
      //this.fetch_data();
    },
    refresh() {
      this.fetch_data();
    },
    backward() {
      if(this.current.dir.lastIndexOf('/')!=-1)
         this.current.dir=this.current.dir.slice(0,this.current.dir.lastIndexOf('/'));
      else if(this.current.dir.length!=0)
         this.current.dir='';
      this.$router.push({path: 'cloud', query: {vmode: 'list', dir: this.current.dir}});
    },
    search(){
      this.$router.push({path: 'cloud', query: {vmode: 'search', search: this.input}});
      var params = this.input;
      console.log(params);
      if(params!=""){
        axios.post("/api/cloud/search", { input:params,user:sessionStorage.getItem('user') }).then(response => {
          response = response.data;
          console.log(response);
          if (response.status === ERR_OK) {
            if(response.result.length==0){
            const h = this.$createElement;
            this.$notify({
              title: '查找文件',
              message: h('i', { style: 'color: teal'}, '未找到对应文件')
              });
            }
            else
            {
              this.fileList = [];
              for (let key in response.result) {
                this.fileList.push({
                  index:key,
                  name: response.result[key],
                  isdir: "-",
                  size: "-",
                  ctime: "-",
                  bucketlist: "-",
                  cloud: "-",
                  ali: "-",
                  baidu: "-",
                  ks: "-",
                  cloud1: "-",
                  cloud2: "-",
                  cloud3: "-",
                  erasure_code_k: "-",
                  erasure_code_n: "-",
                });
              }
            }
          }
        });
      }
      else
        this.fetch_data();
    },
    check_file(row) {
      if (row.isdir == "文件夹") {
        if (this.current.dir != "") this.current.dir += "/";
        this.current.dir += row.name;
        this.$router.push({path: 'cloud', query: {vmode: 'list', dir: this.current.dir}});
        //this.fetch_data();
      } else this.download_file(row);
    },
    delete_file(row) {
      var params = this.current;
      if (row.isdir == "文件夹") {
        this.$confirm(
          "此操作将删除该文件夹以及文件夹下全部文件, 是否继续?",
          "提示",
          {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            type: "warning"
          }
        )
          .then(() => {
            axios
              .post("/api/cloud/delete_dir", {
                dir: params.dir == "" ? row.name : params.dir + "/" + row.name,user:sessionStorage.getItem('user')
              })
              .then(response => {
                console.log(response);
              });
            this.$message({
              type: "success",
              message: "删除成功!"
            });
            this.fileList.splice(row.index,1);
          })
          .catch(() => {
            this.$message({
              type: "info",
              message: "已取消删除"
            });
          });
      } else {
        this.$confirm("此操作将删除该文件, 是否继续?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        })
          .then(() => {
            axios
              .post("/api/cloud/delete_file", {
                dir: params.dir == "" ? row.name : params.dir + "/" + row.name,user:sessionStorage.getItem('user')
              })
              .then(response => {
                console.log(response);
              });
            this.$message({
              type: "success",
              message: "删除成功!"
            });
            this.fileList.splice(row.index,1);
          })
          .catch(() => {
            this.$message({
              type: "info",
              message: "已取消删除"
            });
          });
      }
    },
    download_file(row) {
      var params = this.current;
      var number = this.gridData.push({
        data: row.name,
        type: "下载",
        progress: 0
      });
      axios
        .post(
          "/api/cloud/download",
          { dir: params.dir == "" ? row.name : params.dir + "/" + row.name ,user:sessionStorage.getItem('user')},
          { responseType: "arraybuffer" }
        )
        .then(response => {
          var fileDownload = require("js-file-download");
          console.log(response);
          this.gridData[number - 1].progress = 100;
          fileDownload(response.data, row.name);
        });
    },
    fetch_data: function() {
      var params = this.current;
      this.fileList = [];
      axios.post("/api/cloud/get", { params }).then(response => {
        response = response.data;
        console.log(response);
        if (response.status === ERR_OK) {
          this.fileList = [];
          for (let key in response.result) {
            var bucket = "";
            this.fileList.push({
              index:key,
              name: response.result[key]["file_name"],
              isdir: response.result[key]["isdir"] == true ? "文件夹" : "文件",
              size: response.result[key]["isdir"] == true ? "-" : response.result[key]["file_size"].toFixed(2)+ "M",
              ctime:
                response.result[key]["isdir"] == true
                  ? "-"
                  : response.result[key]["file_ctime"],
              bucketlist: response.result[key]["isdir"] == true ? "-" : response.result[key]["cloud_block_name"],
              cloud: response.result[key]["isdir"] == true ? "-" : "",
              ali:
                response.result[key]["isdir"] == true
                  ? "-"
                  : response.result[key]["cloud_block_area"][0],
              baidu:
                response.result[key]["isdir"] == true
                  ? "-"
                  : response.result[key]["cloud_block_area"][1],
              ks:
                response.result[key]["isdir"] == true
                  ? "-"
                  : response.result[key]["cloud_block_area"][2],
              erasure_code_n:
                response.result[key]["isdir"] == true
                  ? "-"
                  : response.result[key]["cloud_block_name"].length
            });
          }
        }
      });
    },
    create_dir() {
      var params = this.current;
      this.$prompt("请输入名称", "新建文件夹", {
        confirmButtonText: "确定",
        cancelButtonText: "取消"
      })
        .then(({ value }) => {
          axios
            .post("/api/cloud/create", {
              dir: params.dir == "" ? value : params.dir + "/" + value,user:sessionStorage.getItem('user')
            })
            .then(response => {
              console.log(response);
            });
          this.$message({
            type: "success",
            message: "新建文件夹: " + value
          });
          this.fetch_data();
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消输入"
          });
        });
    },
    choose_file() {
      document.getElementById("excelFile").click();
    },
    upload_file(e) {
      var params = this.current;
      let file = e.target.files[0];
      let param = new FormData();
      param.append("file", file, file.name);
      param.append("dir", params.dir);
      param.append("user", sessionStorage.getItem('user'));
      var number = this.gridData.push({
        data: file.name,
        type: "上传中",
        progress: 0
      });
      let config = {
        withCredentials: true,
        onUploadProgress: progressEvent => {
          var complete = (progressEvent.loaded / progressEvent.total * 90) | 0;
          this.gridData[number - 1].progress = complete;
        }
      };
      this.dialogVisible=true;
      axios.post("/api/cloud/upload", param, config).then(response => {
        this.gridData[number - 1].progress = 100;
        this.gridData[number - 1].type = "上传完毕";
        this.fetch_data();
      });
    }
  },
  watch: {
      '$route'(to, from) {
        if (this.$route.path.startsWith('/cloud') && this.$route.query['vmode'] === 'list') {
            this.current.dir = this.$route.query['dir'];
            this.fetch_data();
        }
      }
    },
};
</script>

<style >
.demo-table-expand {
  font-size: 0;
}
.demo-table-expand label {
  width: 90px;
  color: #99a9bf;
}
.demo-table-expand .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 100%;
}
</style>
