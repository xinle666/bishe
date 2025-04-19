<template>
  <div class="container">
    <!-- 列名可编辑 -->
    <div class="header-inputs" style="margin-bottom: 16px;">
      <span v-for="(header, index) in tableHeaders" :key="index" class="header-item">
        <el-input
          v-model="tableHeaders[index]"
          size="small"
          class="header-input"
          placeholder="列名"
          :style="inputStyle"
        ></el-input>
      </span>
    </div>

    <!-- 动态表格 -->
    <el-table :data="tableData" border style="width: 100%" class="animated-table">
      <el-table-column
        v-for="(key, index) in tableHeaders"
        :key="index"
        :prop="key"
        :label="key"
      >
        <template #default="{ row, column }">
          <el-input
            v-model="row[column.property]"
            size="small"
            class="table-input"
          ></el-input>
        </template>
      </el-table-column>
    </el-table>

    <!-- 操作按钮 -->
    <div class="buttons-container">
      <el-button class="button-animate" type="primary" @click="addRow">添加行</el-button>
      <el-button class="button-animate" type="primary" @click="addColumn">添加列</el-button>
      <el-button class="button-animate" type="success" @click="saveChanges">保存修改</el-button>
      <!-- 下载按钮 -->
      <el-button class="button-animate" @click="downloadFile" type="success">下载文件</el-button>
    </div>
  </div>
</template>


<style scoped>
.container {
  background: linear-gradient(135deg, #f9f2f2, #ffffff);
  padding: 16px;
  height: 100vh;
  font-family: "Arial", sans-serif;
  border-radius: 8px;
}

.header-inputs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.header-item {
  flex: 1;
  min-width: 120px;
}

.header-input {
  transition: transform 0.3s ease-in-out, background-color 0.3s ease-in-out;
}

.header-input:focus {
  transform: scale(1.05);
  background-color: #f0f0f0;
  border-color: #d1d1d1;
}

.animated-table {
  animation: fadeIn 0.6s ease-out;
}

.table-input {
  transition: background-color 0.3s ease-in-out, transform 0.3s ease-in-out;
}

.table-input:focus {
  background-color: #f0f0f0;
  transform: scale(1.05);
}

.buttons-container {
  display: flex;
  gap: 16px;
  margin-top: 16px;
  justify-content: flex-start;
}

.button-animate {
  transition: transform 0.2s ease-in-out, background-color 0.2s ease-in-out;
}

.button-animate:hover {
  transform: scale(1.1);
  background-color: #d1d1d1;
}

.button-animate:active {
  transform: scale(0.98);
  background-color: #c2c2c2;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>

<script>
export default {
  name: "ExeclP",
  data() {
    return {
      id: "",
      user:'',
      file_path:'',
      tableData: [], // 表格数据
      tableHeaders: [], // 表头数组
    };
  },
  methods: {
      downloadFile() {
    // 获取文件的 URL
    const fileUrl = this.file_path;

    if (fileUrl) {
      const link = document.createElement('a');
      link.href = fileUrl;
      link.download = fileUrl.split('/').pop(); // 从 URL 中提取文件名并设置为下载文件名
      link.click(); // 模拟点击下载
    } else {
      alert('文件链接无效！');
    }
  },
        // 用户进入编辑页面时添加文件与用户的关联
    addFileing() {
      this.$axios
        .post(this.$httpUrl + '/project/fileing_add', {
          user_id: this.user.id,
          file_id: this.id
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
    // 获取表格数据
    fetchExcelData() {
      this.$axios
        .post(this.$httpUrl + "/file/execl_get", { file_id: this.id })
        .then((response) => {
          console.log(response.data.data)
          if (response.status === 200) {
            console.log(response.data.data.data)
            this.tableData = response.data.data.data;
            this.file_path=response.data.data.file
            this.tableHeaders = Object.keys(this.tableData[0] || {}); // 初始化表头
             this.addFileing()
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },

    // 添加新行
    addRow() {
      const newRow = {};
      this.tableHeaders.forEach((key) => {
        newRow[key] = ""; // 默认值为空
      });
      this.tableData.push(newRow);
    },

    // 添加新列
    addColumn() {
      const newColumnKey = `new_column_${this.tableHeaders.length + 1}`;
      this.tableHeaders.push(newColumnKey); // 新列名
      this.tableData.forEach((row) => {
        row[newColumnKey] = ""; // 默认值为空
      });
    },
    deleteFileing() {
      this.$axios
        .get(this.$httpUrl + '/project/fileing_del', { params: { id: this.id } })
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
    },
    // 提交数据到后端
    saveChanges() {
      const payload = {
        data: this.tableData,
        headers: this.tableHeaders,
        file_id: this.id,
      };
      this.$axios
        .post(this.$httpUrl + "/file/execl_set", payload)
        .then((response) => {
          if (response.status === 200) {
            this.$message.success("数据保存成功");
          } else {
            this.$message.error(response.data.message);
          }
        })
        .catch((error) => {
          console.error(error);
          this.$message.error("数据保存失败");
        });
    },
  },
  created() {
    this.$axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
    this.$axios.defaults.withCredentials = true;
    const id = this.$route.query.id;
     const userData = JSON.parse(sessionStorage.getItem('User'));

    if (userData) {
      this.user = userData;
    }
    if (id) {
      this.id = id;
      this.fetchExcelData();
    }
  },
   beforeDestroy() {
    this.deleteFileing();  // 页面销毁时删除文件关联
  },
};
</script>
