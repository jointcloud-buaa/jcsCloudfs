<template>
  <el-form :model="ruleForm2" :rules="rules2" ref="ruleForm2" label-position="left" label-width="0px" class="demo-ruleForm login-container">
    <h3 class="title">系统登录</h3>
    <el-form-item prop="name">
      <el-input type="text" v-model="ruleForm2.name" auto-complete="off" placeholder="账号"></el-input>
    </el-form-item>
    <el-form-item prop="password">
      <el-input type="password" v-model="ruleForm2.password" auto-complete="off" placeholder="密码"></el-input>
    </el-form-item>
    <el-checkbox v-model="checked" checked class="remember">记住密码</el-checkbox>
    <el-form-item style="width:100%;margin-top:10px">
      <el-button type="primary" style="width:47%;" @click.native.prevent="login" :loading="logining">登录</el-button>
      <el-button type="primary" style="width:47%;" @click.native.prevent="register" :loading="logining">注册</el-button>
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
          ],
          password: [
            { required: true, message: '请输入密码', trigger: 'blur' },
          ]
        },
        checked: true
      };
    },
    created() {
      var user = sessionStorage.getItem('user');
      if (user) {
        this.$router.push({ path: '/cloud' });
      }
      else {
      }
    },
    methods: {
      handleReset2() {
        this.$refs.ruleForm2.resetFields();
      },
      login(ev) {
        this.$refs.ruleForm2.validate((valid) => {
          if (valid) {
            var params = this.ruleForm2;
            axios
              .post("/api/user/login",{ params })
              .then(response => {
                console.log(response);
                if(response.data.status==ERR_OK){
                  if(response.data.result.password==this.ruleForm2.password){
                    var other=response.data.result.others;
                    console.log(other);
                    if(other.hasOwnProperty("phone"))
                        sessionStorage.setItem('phone', other.phone);
                    if(other.hasOwnProperty("mail"))
                        sessionStorage.setItem('mail', other.mail);
                    sessionStorage.setItem('user', this.ruleForm2.name);
                    sessionStorage.setItem('password', this.ruleForm2.password);
                    this.$router.push({ path: '/cloud' });
                  }
                  else
                    this.$message.error("密码错误");
                }
                else{
                    this.$message.error("用户不存在");
                }
              });
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      register(ev) {
        sessionStorage.setItem('user', 'actuser');
        this.$router.push({ path: '/user/register' });
      }
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
