<!-- eslint-disable vue/multi-word-component-names -->
<script>
export default {
  name: "Aside",

  data() {
    return {
      user: {},

      isCollapse: false,
    };
  },

  methods: {

  },

  created() {
    // 初始化用户信息
    this.user = JSON.parse(sessionStorage.getItem("User"));



    // 每分钟检查是否需要自动保存数据
    this.$eventBus.$on('toggleCollapse', (value) => {
      this.isCollapse = value;
    });
  },


}

</script>

<template>
  <el-menu :collapse="isCollapse" router>
    <el-menu-item index="/home">
      <i class="el-icon-s-home"></i>
      <span slot="title">首页</span>
    </el-menu-item>

    <el-menu-item  index="/userControl" v-if="user.role === '0'">
      <i class="el-icon-s-custom"></i>
      <span slot="title">系统用户管理</span>
    </el-menu-item>
    <el-menu-item  index="/project" v-if="user.role === '1'">
      <i class="el-icon-s-goods"></i>
      <span slot="title">我的项目</span>
    </el-menu-item>
    <el-menu-item  index="/projectsControl" v-if="user.role === '0'">
      <i class="el-icon-s-help"></i>
      <span slot="title">项目管理</span>
    </el-menu-item>
        <el-menu-item  index="/userHome" v-if="user.role === '1'">
      <i class="el-icon-user-solid"></i>
      <span slot="title">我的主页</span>
    </el-menu-item>
  </el-menu>
</template>
<style scoped>
/* 导航栏整体背景样式 */
.el-menu {
  background-color: #f5f5dc; /* 米色背景 */
  color: #3a3a3a; /* 深灰色字体 */
  border-right: 2px solid #c2b280; /* 茶色分隔线 */
  font-family: 'KaiTi', '楷体'; /* 使用中文楷体 */
}

/* 菜单项样式 */
.el-menu-item {
  transition: all 0.3s ease;
  font-size: 16px;
  padding: 12px;
  color: #3a3a3a; /* 深灰色字体 */
  display: flex;
  align-items: center;
}

/* 悬浮效果 */
.el-menu-item:hover {
  background-color: #c2b280; /* 茶色悬浮效果 */
  color: #fff;
  transform: scale(1.05); /* 放大效果 */
}

/* 图标样式 */
.el-menu-item i {
  margin-right: 10px;
  color: #5a5a5a; /* 青花蓝色 */
  font-size: 20px;
  transition: color 0.3s ease;
}

.el-menu-item:hover i {
  color: #7f7f7f; /* 悬浮时图标颜色稍深 */
}

/* 高亮样式 */
.el-menu-item.is-active {
  background-color: #d9a673; /* 淡朱砂色选中状态 */
  color: #fff;
}

.el-menu-item.is-active i {
  color: #bd5747; /* 深朱砂红色图标 */
}

/* 柔和动画效果 */
@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-1px);
  }
}
.animate-float {
  animation: float 6s ease-in-out infinite;
}
</style>
