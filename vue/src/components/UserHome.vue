<template>
  <div>
    <!-- 背景渐变动画 -->
    <div
        :style="{ 'background-image': 'linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab)', opacity: 0.9 }"
        style="display: flex; justify-content: center; align-items: center; flex-direction: column; height: 400px; animation: gradient 15s ease infinite;"
    >
      <!-- 动态头像与用户名 -->
      <div @mouseover="avatarHover = true" @mouseleave="avatarHover = false">
        <el-avatar :size="avatarHover ? 210 : 200" :style="{ 'transition': 'all 0.5s', 'box-shadow': '0px 4px 15px rgba(0,0,0,0.3)' }">{{ user.username ? user.username.charAt(0) : '?' }}</el-avatar>
      </div>
      <span class="name">{{ user.name }}</span>
      <span class="time">{{ currentTime }}</span>
      <span class="quote">{{ currentQuote }}</span>
    </div>

    <!-- 个人信息展示 -->
    <div class="info-container">
      <el-descriptions :column="3" direction="vertical" title="个人信息" border>
        <el-descriptions-item label="账号">{{ user.username }}</el-descriptions-item>
        <el-descriptions-item label="电话">{{ user.phone || '无' }}</el-descriptions-item>
        <el-descriptions-item label="出生日期">{{ user.birth_date || '无' }}</el-descriptions-item>
        <el-descriptions-item label="角色">{{ user.role === 1 ? '管理' : '用户'}}</el-descriptions-item>
        <el-descriptions-item label="性别">{{user.sex === 1 ? '男' : '女'}}</el-descriptions-item>
      </el-descriptions>

      <!-- 修改信息按钮 -->
      <el-button icon="el-icon-edit" size="small" type="primary" @click="mod()" class="modify-button">修改信息</el-button>
    </div>

    <!-- 弹窗表单 -->
    <el-dialog :before-close="handleClose" :visible.sync="centerDialogVisible" center title="用户信息修改" width="30%">
      <el-form ref="form" :model="form" :rules="rules" label-width="80px" status-icon>
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="form.password" show-password></el-input>
        </el-form-item>
        <el-form-item label="性别" prop="sex">
          <el-radio-group v-model="form.sex">
            <el-radio label="0">男</el-radio>
            <el-radio label="1">女</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="centerDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitModification">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: JSON.parse(sessionStorage.getItem('User')),
      avatarHover: false,
      currentTime: '',
      currentQuote: '',
      form:JSON.parse(sessionStorage.getItem('User')),
      rules: {
        name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
      },
      centerDialogVisible: false,
      quotes: [
        "成功不是最终的，失败也不是致命的，重要的是继续前进的勇气。",
        "努力不一定成功，但放弃注定失败。",
        "生活不是等待风暴过去，而是学会在雨中翩翩起舞。"
      ]
    }
  },
  created() {
    this.updateTime();
    this.showRandomQuote();
    setInterval(this.updateTime, 1000);
    setInterval(this.showRandomQuote, 5000);
  },
  methods: {
    updateTime() {
      this.currentTime = new Date().toLocaleString();
    },
    showRandomQuote() {
      this.currentQuote = this.quotes[Math.floor(Math.random() * this.quotes.length)];
    },
    mod() {
      this.centerDialogVisible = true;
    },
    submitModification() {
        this.$refs['form'].validate((valid) => {
        if (valid) {  // 如果表单验证通过
          // 提交数据
          this.$axios.post(this.$httpUrl + "/user/up", this.form)

              .then(res => {
                console.log(res)
                if (res.data.code === 200) {
                  this.$message({
                    message: '修改成功',
                    type: 'success'
                  });
   this.centerDialogVisible = false;
                } else {
                  this.$message.error('错了哦，修改失败');
                }
              })
              .catch(error => {
                console.error('请求失败', error);
                this.$message.error('请求失败，请稍后再试');
              });
        } else {  // 如果表单验证失败
          this.$message.error('表单验证失败，请检查输入');
        }
        sessionStorage.setItem("User", JSON.stringify(this.form));
        this.user = JSON.parse(sessionStorage.getItem('User'));
        this.centerDialogVisible = false;
      });

    },
    handleClose(done) {
      this.$confirm('确认关闭？未保存信息将丢失')
          .then(() => done())
          .catch(() => {});
    }
  },
  computed: {
    roleText() {
      return this.user.role === '0' ? '管理' : "用户"
    },
    genderText() {
      return this.user.sex === '0' ? '男' : '女';
    }
  }
}
</script>

<style scoped>
@keyframes gradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
.username {
  font-size: 30px;
  font-weight: 600;
  color: #ffffff;
  margin-top: 15px;
}
.time {
  font-size: 16px;
  color: #cccccc;
  margin-top: 5px;
}
.quote {
  font-size: 18px;
  font-style: italic;
  color: #dddddd;
  margin-top: 10px;
  animation: fade 5s ease-in-out infinite;
}
.modify-button {
  width: 100%;
  margin-top: 20px;
  background-color: #4A90E2;
  transition: all 0.3s;
}
.modify-button:hover {
  background-color: #3A78C2;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
}
.dialog-footer .el-button {
  width: 100px;
}
@keyframes fade {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}
</style>
