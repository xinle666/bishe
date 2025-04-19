<!-- eslint-disable vue/multi-word-component-names -->
<script>
export default {
  name: "Head",
  data() {
    return {
      user: '',
      isCollapse: ''

    }
  },
  methods: {
    toggleCollapse() {
      this.isCollapse = !this.isCollapse;
      this.$eventBus.$emit('toggleCollapse', this.isCollapse); // 广播折叠状态
    },
    toUserHome() {
      this.$router.replace("/UserHome");
    },
    logOff() {
      this.$confirm('要退出了吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$notify({
          title: this.user.name,
          message: '已退出登陆',
          type: 'success'
        });
        sessionStorage.setItem("User", null);
        this.$router.replace("/");
      }).catch(() => {
      });
    },
  },
  created() {
    this.user = JSON.parse(sessionStorage.getItem("User"));
  }
}
</script>

<template>
  <div style="width: 100%; height: 100%; display: flex; justify-content: center; align-items: center;"><i
      :class="isCollapse ? 'el-icon-s-unfold' : 'el-icon-s-fold'"
      @click="toggleCollapse"
      style="font-size: 24px; cursor: pointer;"></i>

    <span style="font-size: larger; margin-left: 45%">协同文档管理系统</span>
    <div style="display: flex; align-items: center; margin-left: auto;">


      <el-dropdown>
        <div style="margin-top: 20px">
          <el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"></el-avatar>
        </div>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item @click.native="toUserHome">个人中心</el-dropdown-item>
          <el-dropdown-item @click.native="logOff">退出</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </div>
</template>


<style scoped>
/* 标题区域的样式 */
div[style*="协同文档管理系统"] {
  font-size: 22px;
  font-family: 'KaiTi', '楷体';
  color: #5b423b; /* 茶色字体 */
}

/* 折叠图标样式 */
.el-icon-s-unfold, .el-icon-s-fold {
  font-size: 24px;
  color: #a54d2e; /* 茶色 */
  transition: transform 0.3s ease, color 0.3s ease;
  cursor: pointer;
}
.el-icon-s-unfold:hover, .el-icon-s-fold:hover {
  color: #8a4a2b; /* 深茶色 */
  transform: scale(1.1);
}

/* 用户头像及下拉菜单的样式 */
.el-avatar {
  border: 2px solid #ce5f4e; /* 茶色边框 */
  box-shadow: 0 0 6px rgba(0, 0, 0, 0.2); /* 阴影效果 */
}
.el-dropdown {
  font-family: 'KaiTi', '楷体';
}
.el-dropdown-menu {
  background-color: #f8f4f0; /* 米色背景 */
  border: 1px solid #c46152; /* 茶色边框 */
}
.el-dropdown-item {
  color: #5b423b; /* 茶色字体 */
}
.el-dropdown-item:hover {
  background-color: #e6ccb2; /* 浅棕色背景 */
  color: #a54d2e; /* 深茶色 */
}

/* 退出确认对话框 */
.el-message-box {
  font-family: 'KaiTi', '楷体';
}
.el-message-box__header {
  color: #5b423b;
  font-size: 18px;
  font-weight: bold;

}
.el-message-box__message {
  color: #5b423b;
}
.el-button--primary {
  background-color: #a54d2e;
  color: #fff;
}
.el-button--primary:hover {
  background-color: #8a4a2b;
}

/* 通知样式 */
.el-notification {
  font-family: 'KaiTi', '楷体';
  color: #5b423b; /* 茶色字体 */
  background-color: #f8f4f0;
  border: 1px solid #d3361e;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>
