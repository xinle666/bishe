<!-- eslint-disable vue/multi-word-component-names -->
<script>
export default {
  name: "userControl",
  data(){
    var checkNo = (rule, value, callback) => {
      console.log(value)
      this.$axios.get(this.$httpUrl + '/user/only?username=' + value).then(res => res.data).then(res => {
        console.log(res)
        if (res.code === 200){
          callback();
        }else {
          return callback(new Error('该账号已存在！'));
        }
      })
    };

    return{
      tableData:[],
      userName: '',
      user: JSON.parse(sessionStorage.getItem('User')),
      pageSize:10,
      pageNum:1,
      total:0,
      showMod:false,
      showAdd:false,

      modForm:{
        username: '',
        password: '',
        phone: '',
        name: '',
        role: 1,
        birth_date: '',
        sex: '',

      },
      addForm:{
        username: '',
        password: '',
        phone: '',
        name: '',
        role: 1,
        birth_date: '',
        sex: '',

      },
      rules: {
        username: [{ required: true, message: '账号不能为空', trigger: 'blur' }, { validator: checkNo, trigger: 'blur' }],
        password: [{ required: true, message: '密码不能为空', trigger: 'blur' }],
        name: [{ required: true, message: '出生日期不能为空', trigger: 'blur' }],

        sex: [{ required: true, message: '性别不能为空', trigger: 'blur' }],


        phone: [{ required: true, message: '手机号码不能为空', trigger: 'blur' }],
      },
      rules2: {
        username: [{ required: true, message: '账号不能为空', trigger: 'blur' }, { validator: checkNo, trigger: 'blur' }],
        password: [{ required: true, message: '密码不能为空', trigger: 'blur' }],
        name: [{ required: true, message: '出生日期不能为空', trigger: 'blur' }],

        sex: [{ required: true, message: '性别不能为空', trigger: 'blur' }],


        phone: [{ required: true, message: '手机号码不能为空', trigger: 'blur' }],
      }

    }
  },
  methods:{
    getData(){
      //从后端获取数据
      this.$axios.post(this.$httpUrl + "/user/list",{
        pageSize: this.pageSize,
        pageNum: this.pageNum,
        name: this.userName
      }).then(res => res.data).then(res => {
        console.log(res.data)
        this.tableData = res.data;
        this.total = res.total;
      })
    },
    reset(){
      this.userName ='';
      this.getData();
    },
    mod(user){
      this.modForm = user;
      this.showMod = true;
    },
    resetForm(){
      this.modForm = {};
      this.showMod = false;
    },
    resetAddForm(){
      this.addForm = {
        username: '',
        password: '',
        phone: '',
        name: '',
        role: 1,
        birth_date: '',
        sex: '',

      };
    },
    modUp(){
      this.$refs['modForm'].validate((valid) => {
        if (valid) {
          //向后端提交修改后的user
          this.$axios.post(this.$httpUrl + "/user/up",this.modForm).then(res => res.data)
              .then(res => {
                if (res.code === 200){
                  this.$message({
                    message: '修改成功',
                    type: 'success'
                  });
                  this.modForm = {};
                  this.showMod = false;
                  this.getData();
                }else {
                  this.$message.error('错了哦，修改失败');
                }
              })
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    addUp(){
      this.$refs['addForm'].validate((valid) => {
        if (valid) {
          this.$axios.post(this.$httpUrl + "/user/add",this.addForm).then(res => res.data)
              .then(res => {
                console.log(res)
                if (res.code === 200){
                  this.$message({
                    message: '添加成功',
                    type: 'success'
                  });
                  this.resetAddForm();
                  this.showAdd = false;
                  this.getData();
                }else {
                  this.$message.error('错了哦，添加失败');
                }
              })
        } else {
          console.log('error submit!!');
          return false;
        }
      });

    },
    delUser(id){
      this.$axios.get(this.$httpUrl + "/user/delete?id=" + id).then(res => res.data)
          .then(res => {
            if (res.code === 200){
              this.$message({
                message: '删除成功',
                type: 'success'
              });
              this.getData();
            }else {
              this.$message.error('删除失败');
            }
          })
    },
  formatSex(row) {
      return row.sex === 1 ? '男' : '女';
    },
    formatRole(row) {
      return row.role === '0' ? '管理员' : '用户';
    },
    formatDate(row) {
      const date = new Date(row.birth_date);
      return date.toLocaleDateString(); // 将日期转换为合适的本地格式
    },

    handleSizeChange(val) {
      this.pageNum = 1;
      this.pageSize = val;
      this.getData();
    },
    handleCurrentChange(val) {
      this.pageNum = val;
      this.getData();
    }
  },
  created() {
    this.$axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
    this.$axios.defaults.withCredentials = true; // 如果需要跨域请求时发送 cookie，请设置为 true
    this.getData();
  }
}
</script>

<template>
  <div class="font-chinese" style="text-align: center; padding: 20px;">
    <div style="display: flex; align-items: center;">
      <el-input
          v-model="userName"
          placeholder="输入用户名"
          class="font-chinese border-chinese"
          style="width: 400px; margin-right: 10px;"
      />
      <el-button
          icon="el-icon-search"
          @click="getData"
          type="primary"
          class="bg-primary font-chinese animate-float"
      >
        查询
      </el-button>
      <el-button
          icon="el-icon-refresh"
          @click="reset"
          type="info"
          class="bg-dark font-chinese animate-float"
      >
        重置
      </el-button>
      <el-button
          icon="el-icon-upload"
          @click="showAdd=true;"
          type="success"
          class="font-chinese animate-float"
      >
        添加用户
      </el-button>
    </div>

    <el-table :data="tableData" stripe class="border-chinese" style="width: 100%;">
      <el-table-column prop="username" label="账号" />
      <el-table-column prop="password" label="密码" />
      <el-table-column prop="name" label="名称" />
  <el-table-column
    prop="sex"
    label="性别"
    :formatter="formatSex" />
      <el-table-column prop="phone" label="手机号码" />
   <el-table-column
    prop="birth_date"
    label="生日"
    :formatter="formatDate" />
    <el-table-column
    prop="role"
    label="角色"
    :formatter="formatRole" />

      <!-- 操作栏带有编辑和删除按钮 -->
      <el-table-column label="操作" prop="operate">
        <template #default="scope">
          <el-button
              size="small"
              type="success"
              @click="mod(scope.row)"
              class="animate-float"
          >
            编辑
          </el-button>
          <el-popconfirm
              confirm-button-text="好的"
              cancel-button-text="点错了"
              icon="el-icon-info"
              icon-color="red"
              title="确定删除吗？"
              @confirm="delUser(scope.row.id)"
          >
            <el-button slot="reference" type="danger" size="small">删除</el-button>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页器 -->
    <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :page-sizes="[5, 10, 20, 40]"
        :page-size="pageSize"
        :current-page="pageNum"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
    />
    <el-dialog title="编辑用户" width="550px" :visible.sync="showMod" style="text-align: start;" center>
      <div style="display: flex;justify-content: center; width: 100%;">
        <el-form ref="modForm" :model="modForm" :rules="rules" style="width:100%;">
          <el-form-item label="账号">
            <el-input v-model="modForm.username" disabled class="inputUser"></el-input>
          </el-form-item>

          <el-form-item label="密码" prop="password">
            <el-input v-model="modForm.password" class="inputUser" show-password type="password"></el-input>
          </el-form-item>

          <el-form-item label="昵称" prop="name">
            <el-input v-model="modForm.name" class="inputUser"></el-input>
          </el-form-item>


          <el-form-item label="电话号码" prop="phone">
            <el-input v-model="modForm.phone" class="inputUser"></el-input>
          </el-form-item>
          <el-form-item label="出生日期" prop="birth_date">
            <el-date-picker v-model="modForm.birth_date" type="date" placeholder="选择日期"></el-date-picker>
          </el-form-item>
      <el-form-item label="性别">
  <el-radio-group v-model="modForm.sex">
    <el-radio-button :label="1">男</el-radio-button>
    <el-radio-button :label="0">女</el-radio-button>
  </el-radio-group>
</el-form-item>

<el-form-item label="角色">
  <el-radio-group v-model="modForm.role">
    <el-radio-button :label="0">管理员</el-radio-button>
    <el-radio-button :label="1">用户</el-radio-button>
  </el-radio-group>
</el-form-item>

        </el-form>
      </div>
      <span slot="footer" class="dialog-footer">
          <el-button type="primary" @click="modUp()">提交</el-button>
          <el-button @click="resetForm()">关闭</el-button>
      </span>
    </el-dialog>

    <el-dialog title="添加用户" width="550px" center :visible.sync="showAdd" style="text-align:start;">
      <el-form ref="addForm" :rules="rules2" :model="addForm" >
        <el-form-item label="账号" prop="username">
          <el-input v-model="addForm.username" class="inputUser"></el-input>
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input v-model="addForm.password" class="inputUser" show-password type="password"></el-input>
        </el-form-item>

        <el-form-item label="昵称" prop="name">
          <el-input v-model="addForm.name" class="inputUser"></el-input>
        </el-form-item>

        <el-form-item label="电话号码" prop="phone">
          <el-input v-model="addForm.phone" class="inputUser"></el-input>
        </el-form-item>
        <el-form-item label="出生日期" prop="birth_date">
          <el-date-picker v-model="addForm.birth_date" type="date" placeholder="选择日期"></el-date-picker>
        </el-form-item>
        <el-form-item label="性别" >
          <el-radio-group v-model="addForm.sex">
            <el-radio-button label='1' >男</el-radio-button>
            <el-radio-button label='0' >女</el-radio-button>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="角色">
          <el-radio-group v-model="addForm.role">
            <el-radio-button label='0' >管理员</el-radio-button>
            <el-radio-button label='1' >用户</el-radio-button>

          </el-radio-group>
        </el-form-item>
      </el-form>

      <span slot="footer" class="dialog-footer">
          <el-button type="primary" @click="addUp()">提交</el-button>
          <el-button @click="resetAddForm()">重置</el-button>
      </span>
    </el-dialog>
  </div>
</template>


/* 添加全局中国风样式 */
<style scoped>
.inputUser {
  width: 400px;
  border-radius: 8px;
  background-color: #f2e6d9; /* 浅米色背景 */
}

/* 基础配色 */
.primary-color {
  color: #a54d2e; /* 温柔的茶色 */
}
.bg-primary {
  background-color: #e6ccb2; /* 米色调 */
  color: #5b423b; /* 深茶色字体 */
}
.bg-dark {
  background-color: #3b3a36; /* 柔和的深灰色 */
  color: #e8e3df; /* 浅米白色字体 */
}
.font-chinese {
  font-family: 'KaiTi', '楷体', 'serif';
}
.border-chinese {
  border: 1px solid #a54d2e; /* 茶色边框 */
  border-radius: 8px;
  padding: 6px;
  background-color: #f2e6d9;
}

/* 按钮样式和动画 */
.el-button {
  transition: all 0.3s ease;
  font-family: 'KaiTi', '楷体';
  background-color: #b58564; /* 浅茶色背景 */
  color: #3b3a36; /* 深色字体 */
}
.el-button:hover {
  transform: scale(1.05); /* 悬浮效果 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  background-color: #a54d2e; /* 悬浮时的深茶色 */
  color: #fff;
}
.el-button--primary {
  background-color: #e6ccb2; /* 柔和的米色 */
  color: #5b423b; /* 茶色字体 */
}
.el-button--primary:hover {
  background-color: #c49a6e; /* 更深的米色 */
}

/* 输入框动画 */
.el-input__inner {
  border: 1px solid #a54d2e; /* 茶色边框 */
  background-color: #f8f0e3; /* 米白背景 */
  border-radius: 8px;
  transition: border-color 0.3s ease;
  color: #5b423b; /* 茶色字体 */
}
.el-input__inner:focus {
  border-color: #8a4a2b; /* 聚焦时的深茶色 */
  box-shadow: 0 0 8px rgba(165, 77, 46, 0.2);
}

/* 对话框 */
.el-dialog {
  border-radius: 12px;
  border: 2px solid #a54d2e; /* 茶色边框 */
  box-shadow: 0 0 12px rgba(0, 0, 0, 0.2);
  font-family: 'KaiTi', '楷体';
  background-image: linear-gradient(to right, #f8f4f0, #f1ebe6); /* 渐变米色 */
}
.el-dialog__title {
  color: #5b423b; /* 茶色标题 */
  font-size: 20px;
  font-weight: bold;
  font-family: 'KaiTi', '楷体';
  border-bottom: 2px solid #a54d2e; /* 茶色下划线 */
}

/* 表格样式 */
.el-table th, .el-table td {
  font-family: 'KaiTi', '楷体';
  padding: 12px;
  background-color: #f8f4f0; /* 米白背景 */
  color: #3b3a36; /* 深灰色字体 */
}
.el-tag--primary {
  background-color: #a54d2e; /* 茶色标签 */
  color: #fff;
}
.el-tag--success {
  background-color: #c49a6e; /* 柔和的棕色 */
  color: #fff;
}

/* 悬浮动画效果 */
@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-3px);
  }
}
.animate-float {
  animation: float 3s ease-in-out infinite;
}
</style>

