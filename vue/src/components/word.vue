<template>
  <div class="container">
    <el-card shadow="hover" class="editor-card" >
      <h2 class="title">docx在线编辑</h2>

      <!-- 增加下拉框 -->
      <el-form :model="formData" ref="formRef">


        <!-- 富文本编辑器 -->
        <el-form-item  prop="content" class="form-item">
          <quill-editor
            v-model="formData.content"
            :options="editorOptions"
            ref="quillEditor"
            class="quill-editor"
          ></quill-editor>
        </el-form-item>

        <!-- 按钮组 -->
        <div class="button-group">
          <el-button @click="submitForm" type="primary" class="custom-button">
            保存原格式
          </el-button>
          <el-button @click="saveAsPdf" type="primary" class="custom-button">
            转为PDF保存
          </el-button>
          <el-button @click="downloadFile" type="success" class="custom-button">
            下载文件
          </el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { quillEditor } from 'vue-quill-editor'; // 导入 vue-quill-editor
import 'quill/dist/quill.snow.css'; // 引入 Quill 编辑器的样式


export default {
  name: "HomeP",
  components: {
    quillEditor,
  },

  data() {
    return {
      user: '',
      filesData: {}, // 存储文件信息
      formData: {
        content: '', // 用来存储富文本内容
        file: this.filesData,
      },
      editorOptions: {
        theme: 'snow', // 编辑器的主题
        placeholder: '请输入内容...', // 输入框提示信息
        modules: {
          toolbar: [
            [{ header: '1' }, { header: '2' }, { font: [] }],
            [{ list: 'ordered' }, { list: 'bullet' }],
            ['bold', 'italic', 'underline'],
            [{ align: [] }],
            ['link', 'image'],
            ['clean'],
          ],
        },
      },
    };
  },

  methods: {
     // 下载文件
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
  // 获取文件数据并显示在 Quill 编辑器中
  fetchFileData() {
    console.log(this.id);
    this.$axios
      .post(this.$httpUrl + '/file/list', { file_id: this.id ,type:'word'})
      .then((response) => {
        if (response.status === 200) {
          this.filesData = response.data.data;
          console.log(this.filesData);  // 查看返回的文件信息和 HTML 内容
             this.addFileing();  // 页面加载时添加文件关联
          this.insertHtmlContent(this.filesData.html_content);  // 将返回的 HTML 内容插入到 Quill 编辑器中
        } else {
          console.error("获取文件失败");
        }
      })
      .catch((error) => {
        console.error("请求失败", error);
      });
  },

  // 将 HTML 内容插入到 Quill 编辑器
  insertHtmlContent(htmlContent) {
    const quillEditor = this.$refs.quillEditor; // 获取 quillEditor 组件引用
    if (quillEditor) {
      const quill = quillEditor.quill;
      quill.focus();  // 确保编辑器获得焦点
      const range = quill.getSelection();
      console.log(quill)
      console.log(range)
      if (range) {
        const position = range.index;
        // 将 HTML 内容插入到 Quill 编辑器中
        quill.root.innerHTML = quill.root.innerHTML.slice(0, position) + htmlContent + quill.root.innerHTML.slice(position);
      }
    }
  },

    // 提交表单（保存原格式）
    submitForm() {
      console.log(this.formData.content); // 提交内容时，打印富文本内容

      this.$axios
        .post(this.$httpUrl + '/file/save_content', { content: this.formData.content, file_id: this.filesData.id, user_id: this.user.id })
        .then((response) => {
          if (response.status === 200) {
            alert("保存成功！");
            this.fetchFileData()
          } else {
            alert("保存失败！");
          }
        })
        .catch((error) => {
          console.error("提交失败", error);
        });
    },

    // 保存为 PDF 格式
    saveAsPdf() {
      // 在这里你需要调用一个生成 PDF 的方法
      // 假设你有一个 API 可以将富文本转为 PDF 并保存
      this.$axios
        .post(this.$httpUrl + '/file/save_as_pdf', { content: this.formData.content, file_id: this.filesData.id, user_id: this.user.id })
        .then((response) => {
          if (response.status === 200) {
            alert("PDF 保存成功！");
          } else {
            alert("PDF 保存失败！");
          }
        })
        .catch((error) => {
          console.error("PDF 保存失败", error);
        });
    },
    // 用户进入编辑页面时添加文件与用户的关联
    addFileing() {
      this.$axios
        .post(this.$httpUrl + '/project/fileing_add', {
          user_id: this.user.id,
          file_id: this.filesData.id
        })
        .then((response) => {
          if (response.status === 200) {
            console.log("文件编辑关联添加成功");
          } else {
            console.error("文件编辑关联添加失败");
          }
        })
        .catch((error) => {
          console.error("请求失败", error);
        });
    },

    // 用户退出页面时删除文件与用户的关联
    deleteFileing() {
      this.$axios
        .get(this.$httpUrl + '/project/fileing_del', { params: { id: this.filesData.id } })
        .then((response) => {
          if (response.status === 200) {
            console.log("文件编辑关联删除成功");
          } else {
            console.error("文件编辑关联删除失败");
          }
        })
        .catch((error) => {
          console.error("请求失败", error);
        });
    }
  },
 beforeDestroy() {
    this.deleteFileing();  // 页面销毁时删除文件关联
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


<style lang="scss">
/* 页面布局调整 */
.container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 20px;
  background: linear-gradient(135deg, #fefcea, #f1da36);
  min-height: 100vh;

}

/* 卡片样式 */
.editor-card {
  max-width:1000px;
  height: 800px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.9);
  padding: 20px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}
.editor-card:hover {
  transform: translateY(-10px);
}

/* 标题样式 */
.title {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
  font-family: "KaiTi", "STKaiti", "SimSun", sans-serif;
}

/* 表单项样式 */
.form-item {

  margin-bottom: 20px;
}

/* 下拉框样式 */
.dropdown {
  width: 100%;
}

/* 富文本编辑器样式 */
.quill-editor {
  height: 600px; /* 调整高度 */
  border: 1px solid #e6e6e6;
  border-radius: 5px;
  padding: 10px;
  background: #fff;
  overflow-y: auto; /* 启用滚动条 */
}

/* 按钮组样式 */
.button-group {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

/* 自定义按钮 */
.custom-button {
  transition: all 0.3s ease;
  font-size: 16px;
  padding: 10px 20px;
  border-radius: 5px;
}
.custom-button:hover {
  background-color: #e6b8af;
  color: #fff;
  transform: scale(1.05);
}
</style>