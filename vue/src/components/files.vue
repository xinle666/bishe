<!-- eslint-disable vue/multi-word-component-names -->
// eslint-disable-next-line
<script>
export default {
  name: "teacherControl",
  data() {


    return {
      id:0,
      istableData:false,
      tableData: [],




      total: 0,


      user: JSON.parse(sessionStorage.getItem('User')), // 初始为空
      isUserLoaded: false, // 标志位，表示用户数据是否加载完成
      generatingExam: false, // 控制生成试题按钮的加载状态

      rules: {
        name: [
          {required: true, message: '请输入名称', trigger: 'blur'}
        ],


      }
    }
  },
  methods: {
        delUser(id) {
      this.$axios.get(this.$httpUrl + "/project/file_del?id=" + id).then(res => res.data)
          .then(res => {
            if (res.code === 200) {
              this.$message({
                message: '删除成功',
                type: 'success'
              });
              this.getData();
            } else {
              this.$message.error('删除失败');
            }
          })
    },
    getData() {


      //从后端获取数据
      this.$axios.post(this.$httpUrl + "/project/filelist", {

        project_id: this.id


      }).then(res => res.data).then(res => {

        this.tableData = res.data;
        this.total = res.total;
        console.log(   this.tableData)

      })
    },
      // 开始定时请求数据
  startAutoFetchData() {
    // 调用一次 getData() 获取初始数据
    this.getData();

    // 每5秒请求一次数据
    this.timer = setInterval(() => {
      this.getData();
    }, 5000);
  },

  // 停止定时请求数据
  stopAutoFetchData() {
    if (this.timer) {
      clearInterval(this.timer); // 清除定时器
      this.timer = null;
    }
  },
    reset() {

      this.getData(0);
    },










beforeUpload(file) {
      const isWord = file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';
      const isExcel = file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
      const isPdf = file.type === 'application/pdf';

      if (!(isWord || isExcel || isPdf)) {
        this.$message.error('只能上传 Word、Excel 或 PDF 文件');
        return false;  // 取消上传
      }
      return true;
    },
   // 上传失败回调
    handleUploadError(error, file) {
      if (error.response && error.response.status === 400) {
        this.$message.error(`文件 ${file.name} 上传失败，文件名重复！`);
      } else {
        this.$message.error(`文件 ${file.name} 上传失败，请稍后重试！`);
      }
    },
// 根据文件的扩展名选择图片
    getFileImage(file) {
      const fileName = file.name.toLowerCase();
      if (fileName.endsWith('.docx')) {
        return require('../assets/img/word.jpg'); // docx 文件显示 word 图片
      } else if (fileName.endsWith('.xlsx')) {
        return require('../assets/img/execl.jpg'); // xlsx 文件显示 excel 图片
      } else if (fileName.endsWith('.pdf')) {
        return require('../assets/img/pdf.png'); // pdf 文件显示 pdf 图片
      }
    },
        handleUploadSuccess2() {
      this.$message.success('上传成功');
      this.getData(0)

    },
    // 根据文件类型返回不同的路由链接
 getFileLink(file) {
  const fileName = file.name.toLowerCase();
  // 如果文件正在被编辑，禁止跳转
  if (file.fileing_status === 1) {
    return null; // 返回 null，表示没有跳转路径
  }
  // 根据文件扩展名返回相应的跳转路径
  if (fileName.endsWith('.docx')) {
    return { path: '/word', query: { id: file.id } };
  } else if (fileName.endsWith('.xlsx')) {
    return { path: '/excel', query: { id: file.id } };
  } else if (fileName.endsWith('.pdf')) {
    return { path: '/pdf', query: { id: file.id } };
  } else {
    return { path: '/default', query: { id: file.id } };
  }
},

  // 生成试题方法
  generateExam() {
    this.generatingExam = true;
    this.$axios.post(this.$httpUrl + "/project/generate_exam", {
      project_id: this.id,
      user_id: this.user.id
    }).then(res => res.data).then(res => {
      if (res.code === 200) {
        this.$message({
          message: '试题生成成功',
          type: 'success'
        });
        // 刷新文件列表
        this.getData();
      } else {
        this.$message.error('试题生成失败: ' + (res.msg || '未知错误'));
      }
    }).catch(err => {
      console.error('生成试题出错:', err);
      this.$message.error('试题生成失败，请稍后重试');
    }).finally(() => {
      this.generatingExam = false;
    });
  },

  }
,





  created() {

    this.$axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
    this.$axios.defaults.withCredentials = true; // 如果需要跨域请求时发送 cookie，请设置为 true
    const id = this.$route.query.id; // 获取传递的 ID
    if (id) {
      this.id=id
      this.getData();
           this.startAutoFetchData();
    }
        const userData = JSON.parse(sessionStorage.getItem('User'));


    if (userData) {
      this.user = userData;
    }
    // 更新标志位，表示用户数据已加载
    this.isUserLoaded = true;
  },
  beforeDestroy() {
  // 组件销毁时停止自动请求
  this.stopAutoFetchData();
}
}
</script>
<template>
  <div class="container">
    <div class="header">
      <el-upload
        class="upload-demo"
        action="http://localhost:8000/file/upload"
        :before-upload="beforeUpload"
        :on-success="handleUploadSuccess2"
        :on-error="handleUploadError"
        :show-file-list="false"
        accept=".docx,.xlsx,.pdf"
        :data="{user_id: user.id, project_id: id}"
      >
        <el-button icon="el-icon-upload" type="success">上传文件</el-button>
      </el-upload>
      
      <el-button 
        icon="el-icon-document" 
        type="primary" 
        @click="generateExam" 
        :loading="generatingExam">
        生成试题
      </el-button>
    </div>

    <div class="card-container">
      <el-row :gutter="20">
        <el-col
          v-for="file in tableData"
          :key="file.id"
          :span="6"
          class="card-col"
        >
          <el-card class="box-card" :class="{ editing: file.fileing_status === 1 }">
            <div v-if="file.fileing_status === 1" class="editing-overlay">
              <span class="editing-text">正在编辑中</span>
            </div>
            <router-link :to="getFileLink(file)" v-if="file.fileing_status !== 1">
              <img :src="getFileImage(file)" class="course-image" />
            </router-link>
            <div v-else>
              <img :src="getFileImage(file)" class="course-image" />
            </div>
            <div class="course-content">
              <p class="file-name">{{ file.name }}</p>
              <p>创建时间：{{ file.created_at }}</p>
              <p>创造人：{{ file.user__name }}</p>
              <p>
                <span v-if="file.fileing_status === 1" class="editing-status">正在被编辑</span>
                <span v-else class="available-status">可编辑</span>
              </p>
            </div>
            <div
              v-if="isUserLoaded && user && user.id === file.project_user_id"
              class="clearfix actions"
            >
              <el-popconfirm
                confirm-button-text="好的"
                cancel-button-text="点错了"
                icon="el-icon-info"
                icon-color="red"
                title="确定删除吗？"
                @confirm="delUser(file.id)"
              >
                <el-button slot="reference" type="danger" size="small">删除</el-button>
              </el-popconfirm>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<style scoped>



.el-popconfirm {
  border-radius: 5px;
}

.course-status {
  color: #409EFF; /* 课程状态颜色 */
  font-weight: bold;
}

.course-level {
  color: #67C23A; /* 课程难度颜色 */
  font-weight: bold;
}
.container {
  text-align: center;
  padding: 20px;
  background: linear-gradient(to bottom right, #e3f2fd, #f8bbd0);
  min-height: 100vh;
  font-family: "Roboto", sans-serif;
}

.header {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
  gap: 20px; /* 按钮之间的间距 */
}

.card-container {
  margin-top: 20px;
}

.card-col {
  margin-left: 60px;
}

.box-card {
  transition: all 0.3s ease-in-out;
  border-radius: 8px;
  margin-top: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.box-card:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.box-card.editing {
  border: 2px solid #f48fb1;
  position: relative;
}

.course-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 8px;
}

.course-content {
  text-align: left;
  padding: 10px;
}

.file-name {
  font-weight: bold;
  color: #455a64;
}

.actions {
  margin-top: 10px;
}

.el-button {
  border-radius: 20px;
  transition: all 0.3s ease;
}

.el-button:hover {
  background-color: #82b1ff;
  color: white;
}

.editing-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 150px;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 8px;
  z-index: 1;
}

.editing-text {
  color: white;
  font-size: 18px;
  font-weight: bold;
  background-color: #f48fb1;
  padding: 5px 10px;
  border-radius: 4px;
}

.editing-status {
  color: #f44336;
  font-weight: bold;
}

.available-status {
  color: #4caf50;
  font-weight: bold;
}

</style>