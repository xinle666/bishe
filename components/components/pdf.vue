<template>
  <div class="container">
    <!-- 文件显示区域 -->
    <div v-if="fileUrl" class="pdf-viewer">
      <iframe :src="fileUrl" frameborder="0"></iframe>
    </div>

    <!-- 操作按钮 -->
    <div class="button-group">
      <el-button @click="saveAsPdf" type="primary" class="animated-button">
        转为 Word 保存
      </el-button>
      <el-button @click="downloadFile" type="success" class="animated-button">
        下载文件
      </el-button>
    </div>
  </div>
</template>
<script>
export default {
  name: "HomeP",
  data() {
    return {
      user: '',
      filesData: {}, // 存储文件信息
      fileUrl: '',    // 用于存储文件的 URL
    };
  },

  methods: {
      downloadFile() {
    // 获取文件的 URL
    const fileUrl = this.filesData.file_url;

    if (fileUrl) {
      const link = document.createElement('a');
      link.href = fileUrl;
      link.download = fileUrl.split('/').pop(); // 从 URL 中提取文件名并设置为下载文件名
      link.click(); // 模拟点击下载
    } else {
      alert('文件链接无效！');
    }
  },
    // 获取文件信息，并根据 URL 显示 PDF
    fetchFileData() {
      this.$axios
        .post(this.$httpUrl + '/file/list', { file_id: this.id ,type:'pdf'})
        .then((response) => {
          if (response.status === 200) {
            this.filesData = response.data.data;
            const fileUrl = this.filesData.file_url;
            console.log(fileUrl)
            if (fileUrl.endsWith('.pdf')) {
              this.fileUrl = fileUrl;  // 设置 PDF 文件 URL
            } else {
              console.error("该文件不是 PDF 格式");
            }
          } else {
            console.error("获取文件失败");
          }
        })
        .catch((error) => {
          console.error("请求失败", error);
        });
    },

    // 保存为 PDF 格式
    saveAsPdf() {
      this.$axios
        .post(this.$httpUrl + '/file/save_as_word', { file_id: this.filesData.id, user_id: this.user.id })
        .then((response) => {
          if (response.status === 200) {
            alert("Word 保存成功！");
          } else {
            alert("Word 保存失败！");
          }
        })
        .catch((error) => {
          console.error("PDF 保存失败", error);
        });
    },
  },

  created() {
    this.$axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
    this.$axios.defaults.withCredentials = true; // 如果需要跨域请求时发送 cookie，请设置为 true
    const id = this.$route.query.id; // 获取传递的 ID
    const userData = JSON.parse(sessionStorage.getItem('User'));

    if (userData) {
      this.user = userData;
    }
    if (id) {
      this.id = id;
      this.fetchFileData();
    }
  },
};
</script>

<style scoped>
.container {
  padding: 30px;
  background: linear-gradient(to bottom right, #f2eada, #d7c4a5);
  font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
  color: #333;
  min-height: 100vh;
}

/* PDF 查看区域 */
.pdf-viewer {
  margin-bottom: 20px;
  padding: 10px;
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.3s ease-in-out;
}

.pdf-viewer:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  transform: translateY(-5px);
}

.pdf-viewer iframe {
  width: 100%;
  height: 700px;
  border: none;
}

/* 按钮组样式 */
.button-group {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

/* 按钮样式 */
.el-button {
  border-radius: 30px;
  font-size: 16px;
  padding: 10px 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease-in-out;
}

.el-button:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
}

/* 按钮动画 */
.animated-button {
  position: relative;
  overflow: hidden;
  background: linear-gradient(to right, #ff7e5f, #feb47b);
  color: #fff;
}

.animated-button::after {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 200%;
  height: 100%;
  background: rgba(255, 255, 255, 0.2);
  transform: skewX(-45deg);
  transition: all 0.3s ease-in-out;
}

.animated-button:hover::after {
  left: 100%;
}

/* 按钮颜色 */
.el-button--primary {
  background: linear-gradient(to right, #89f7fe, #66a6ff);
  border: none;
}

.el-button--success {
  background: linear-gradient(to right, #56ab2f, #a8e063);
  border: none;
}
</style>
