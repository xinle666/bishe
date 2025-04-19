<!-- eslint-disable vue/multi-word-component-names -->
<script>
export default {
  name: "projectsControl",
  data(){


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
           id: 0,
        name: '',
        folder_path: '',
        directory_image_url: '',
        created_at: '',
        updated_at: '',
        user_id:  0,
        username:'',
        user_name:""

      },
      addForm:{
           id: 0,
        name: '',
        folder_path: '',
        directory_image_url: '',
        created_at: '',
        updated_at: '',
        user_id:  0,
        username:'',
        user_name:""

      },
      rules: {
        name: [{ required: true, message: '项目名称不能为空', trigger: 'blur' }, ],
        folder_path: [{ required: true, message: '文件夹路径不能为空', trigger: 'blur' }],
        directory_image_url: [{ required: true, message: '项目目录图片不能为空', trigger: 'blur' }],

        created_at: [{ required: true, message: '创建时间不能为空', trigger: 'blur' }],


        updated_at: [{ required: true, message: '更新时间不能为空', trigger: 'blur' }],
        user_name: [{ required: true, message: '用户名称不能为空', trigger: 'blur' }],
      },


    }
  },
  methods:{
    getData(){
      //从后端获取数据
      this.$axios.post(this.$httpUrl + "/project/list",{
        pageSize: this.pageSize,
        pageNum: this.pageNum,
        name: this.userName,
        user:this.user
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
           id: 0,
        name: '',
        folder_path: '',
        directory_image_url: '',
        created_at: '',
        updated_at: '',
        user_id:  0,
        username:'',
        user_name:""

      };
    },
    modUp(){
      this.$refs['modForm'].validate((valid) => {
        if (valid) {
          //向后端提交修改后的user
          this.$axios.post(this.$httpUrl + "/project/up",this.modForm).then(res => res.data)
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
    delUser(id){
      this.$axios.get(this.$httpUrl + "/project/delete?id=" + id).then(res => res.data)
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

    formatDate(row) {
      const date = new Date(row.created_at);
      return date.toLocaleDateString(); // 将日期转换为合适的本地格式
    },
    formatDate2(row) {
      const date = new Date(row.updated_at);
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
          placeholder="输入项目名"
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

    </div>

    <el-table :data="tableData" stripe class="border-chinese" style="width: 100%;">
      <el-table-column prop="name" label="项目名称" />
      <el-table-column prop="folder_path" label="文件夹路径" />
      <el-table-column prop="directory_image_url" label="项目目录图片 URL" />

   <el-table-column
    prop="created_at"
    label="创建时间"
    :formatter="formatDate" />
  <el-table-column
    prop="updated_at"
    label="更新时间"
    :formatter="formatDate2" />
  <el-table-column
    prop="user_name"
    label="管理员名称"
  />
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
    <el-dialog title="编辑" width="550px" :visible.sync="showMod" style="text-align: start;" center>
      <div style="display: flex;justify-content: center; width: 100%;">
        <el-form ref="modForm" :model="modForm" :rules="rules" style="width:100%;">
          <el-form-item label="项目名称">
            <el-input v-model="modForm.name"  class="inputUser"></el-input>
          </el-form-item>



          <el-form-item label="项目目录图片" prop="directory_image_url">
            <el-input v-model="modForm.directory_image_url" class="inputUser"></el-input>
          </el-form-item>


          <el-form-item label="创建时间" prop="created_at">
            <el-input v-model="modForm.created_at"  type="date" placeholder="选择日期"></el-input>
          </el-form-item>
          <el-form-item label="更新时间" prop="updated_at">
            <el-date-picker v-model="modForm.updated_at" type="date" placeholder="选择日期"></el-date-picker>
          </el-form-item>


        </el-form>
      </div>
      <span slot="footer" class="dialog-footer">
          <el-button type="primary" @click="modUp()">提交</el-button>
          <el-button @click="resetForm()">关闭</el-button>
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

