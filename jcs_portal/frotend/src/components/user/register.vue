<template>
  <el-form :model="ruleForm2" :rules="rules2" ref="ruleForm2" label-position="left" label-width="0px" class="demo-ruleForm login-container">
    <h3 class="title">注册</h3>
    <el-form-item prop="name">
      <el-input type="text" v-model="ruleForm2.name" auto-complete="off" placeholder="账号"></el-input>
    </el-form-item>
    <el-form-item prop="password">
      <el-input type="password" v-model="ruleForm2.password" auto-complete="off" placeholder="密码"></el-input>
    </el-form-item>
    <el-form-item style="width:100%;margin-top:10px">
      <el-button type="primary" style="width:47%;" @click.native.prevent="Submit" :loading="logining">注册</el-button>
      <el-button type="primary" style="width:47%;" @click.native.prevent="login" :loading="logining">回到登录</el-button>
    </el-form-item>
  </el-form>
</template>
<script type="text/ecmascript-6">
import axios from "axios";
const ERR_OK = 0;
  export default {
    data() {
      return {
        logining: false,
        ruleForm2: {
          name: '',
          password: ''
        },
        rules2: {
          name: [
            { required: true, message: '请输入账号', trigger: 'blur' },
            //{ validator: validaePass }
          ],
          password: [
            { required: true, message: '请输入密码', trigger: 'blur' },
            //{ validator: validaePass2 }
          ]
        },
        checked: true
      };
    },
    created() {
    },
    methods: {
      Submit(ev) {
      var params = this.ruleForm2;
      console.log(params);
      axios
        .post("/api/user/register",{ params })
        .then(response => {
          console.log(response);
          if(response.data.status==ERR_OK){
              sessionStorage.setItem('user', this.ruleForm2.name);
              sessionStorage.setItem('password', this.ruleForm2.password);
              this.$router.push({ path: '/cloud' });
          }
          else{
              this.$message.error("用户已存在，请登录");
          }
        });
      },
      login(ev) {
        sessionStorage.removeItem('user');
        this.$router.push({ path: '/user/login' });
      },
    }
  }
</script>

<style scoped>
  .login-container {
    /*box-shadow: 0 0px 8px 0 rgba(0, 0, 0, 0.06), 0 1px 0px 0 rgba(0, 0, 0, 0.02);*/
    -webkit-border-radius: 5px;
    border-radius: 5px;
    -moz-border-radius: 5px;
    background-clip: padding-box;
    margin: 180px auto;
    width: 350px;
    padding: 35px 35px 15px 35px;
    background: #fff;
    border: 1px solid #eaeaea;
    box-shadow: 0 0 25px #cac6c6;
    .title {
      margin: 0px auto 40px auto;
      text-align: center;
      color: #505458;
    }
    .remember {
      margin: 0px 0px 35px 0px;
    }
  }
</style>
