<template>
  <div class="Body">
    <div class="background-animation"></div>
    <div class="box animate__animated animate__fadeInDown">
      <div class="title">文档协同系统</div>

      <!-- 登录表单 -->
      <div v-if="isLogin">
        <el-input v-model="loginForm.username" clearable placeholder="账号" class="inputs" />
        <el-input
            type="password"
            show-password
            clearable
            v-model="loginForm.password"
            placeholder="密码"
            class="inputs"
        />
        <el-button class="login-button" type="primary" @click="login">登录</el-button>
        <div class="switch-link">
          <span @click="isLogin = false" class="switch-text">没有账号？去注册</span>
        </div>
      </div>

      <!-- 注册表单 -->
      <div v-else>
        <el-input v-model="registerForm.username" clearable placeholder="用户名" class="inputs" />
        <el-input v-model="registerForm.password" type="password" show-password clearable placeholder="密码" class="inputs" />
        <el-input v-model="registerForm.phone" clearable placeholder="电话" class="inputs" />
        <el-input v-model="registerForm.name" clearable placeholder="姓名" class="inputs" />

        <el-date-picker v-model="registerForm.birth_date" type="date" placeholder="出生日期" class="inputs" />
        <el-select v-model="registerForm.sex" placeholder="性别" class="inputs">
          <el-option label="男" value="0" />
          <el-option label="女" value="1" />
        </el-select>

        <el-button class="register-button" type="success" @click="register">注册</el-button>
        <div class="switch-link">
          <span @click="isLogin = true" class="switch-text">已有账号？去登录</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "LoginP",
  data() {
    return {
      isLogin: true, // 控制当前显示登录表单还是注册表单
      user: {   username: "",
        password: "",
        phone: "",
        name: "",
        role: 1,
        birth_date: "",
        sex: "",},
      loginForm: {
        username: "",
        password: "",
      },
      registerForm: {
        username: "",
        password: "",
        phone: "",
        name: "",
        role: 1,
        birth_date: "",
        sex: "",
      },
    };
  },
  methods: {
    login() {
      console.log("Logging in with:", this.loginForm);
      this.$axios.post(this.$httpUrl + "/user/login", this.loginForm)
          .then(res => res.data)
          .then(res => {
            if (res.code === 200) {
              this.user = res.data.user;
              console.log( this.user);
              this.$notify({
                title: this.user.name,
                message: "欢迎回家",
                type: "success",
              });
              sessionStorage.setItem("User", JSON.stringify(this.user));
              this.$router.replace("/home");
            } else {
              this.$message({
                message: "账号或密码错误！",
                type: "error",
              });
            }
          });
    },
    register() {
      console.log("Registering with:", this.registerForm);
      this.$axios.post(this.$httpUrl + "/user/add", this.registerForm)
          .then(res => res.data)
          .then(res => {
            if (res.code === 200) {
              this.$notify({
                title: "注册成功",
                message: "用户已成功注册",
                type: "success",
              });
              this.isLogin = true; // 注册成功后自动跳转到登录界面
            } else {
              this.$message({
                message: res.message || "注册失败",
                type: "error",
              });
            }
          })
          .catch(() => {
            this.$message({
              message: "服务器内部错误",
              type: "error",
            });
          });
    },
  },
};
</script>

<style scoped>
@import "https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css";

.Body {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #3b3c5c, #24243e);
}

.background-animation {
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.6), rgba(255, 255, 255, 0));
  animation: gradient-animation 8s ease infinite;
  z-index: -1;
}

@keyframes gradient-animation {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.box {
  width: 360px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 15px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
  padding: 30px;
  text-align: center;
  z-index: 10;
  backdrop-filter: blur(10px);
}

.title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 15px;
}

.inputs {
  width: 90%;
  margin: 10px 0;
}

.login-button, .register-button {
  width: 90%;
  margin-top: 10px;
  transition: transform 0.3s, box-shadow 0.3s;
}

.login-button:hover, .register-button:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 15px rgba(0, 123, 255, 0.4);
}

.switch-link {
  margin-top: 15px;
  text-align: center;
}

.switch-text {
  color: #409eff;
  cursor: pointer;
}
</style>
