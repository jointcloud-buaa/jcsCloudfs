<template>
  <el-container>
    <el-header>
      <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
        <img :src="myurl" style="float:left">
        <h3 style="float:left">北京jcsproxy&nbsp;&nbsp;&nbsp;</h3>
        <el-menu-item index="1"><router-link to="/cloud">云际存储</router-link></el-menu-item>
        <el-submenu index="2">
          <template slot="title">云际监控</template>
          <el-menu-item index="2-2"><router-link to="/data/map">地理分布</router-link></el-menu-item>
        </el-submenu>
        <el-submenu index="3" style="float:right;margin-right:50px">
          <template slot="title">用户</template>
          <el-menu-item index="3-1"><router-link to="/user/user">信息管理</router-link></el-menu-item>
          <el-menu-item index="3-2" @click.native.prevent="exit" >退出登录</el-menu-item>
        </el-submenu>
      </el-menu>
    </el-header>
    <el-main>
      <router-view></router-view>
    </el-main>
    <el-footer></el-footer>
  </el-container>

</template>

<script type="text/ecmascript-6">
  import ElContainer from "element-ui/packages/container/src/main"

  export default {
    components: { ElContainer },
    data() {
      return {
        activeIndex: '1',
        activeIndex2: '1',
        myurl:'/static/images/Jointcloud.png',
      };
    },
    mounted() {
      var user = sessionStorage.getItem('user');
      if (user) {
      }
      else{
        this.$router.push({ path: '/user/login' });
      }
    },
    methods: {
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
      },
      exit() {
        console.log('quit');
        sessionStorage.removeItem('user');
        this.$router.push({ path: '/user/login' });
      }
    },
    updated:function (){
      this.myurl='/static/images/Jointcloud.png';
      var user = sessionStorage.getItem('user');
      if (user) {

      }
      else{
        this.$router.push({ path: '/user/login' });
      }

    }
  }
</script>

<style>
  a:link {
    text-decoration: none;
  }

  .router-link-active {
    text-decoration: none;
  }
  .el-menu{
    justify-content: center;
  }

</style>
