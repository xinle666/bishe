<!-- eslint-disable vue/multi-word-component-names -->
// eslint-disable-next-line
<script>
export default {
  name: "teacherControl",
  data() {


    return {
      istableData:false,
      tableData: [],
      courseName: '',
      userForm: {
        project: 0,
        username: ""
      },

      pageSize: 10,
      pageNum: 1,
      total: 0,
      showMod: false,
      showAdd: false,
      showAdmin: false,
      showUser: false,
      modForm: {
        id: 0,
        name: '',
        folder_path: '',
        directory_image_url: '',
        created_at: '',
        updated_at: '',
        user_id: 0,
        username: '',
        user_name: ""


      },
      user: JSON.parse(sessionStorage.getItem('User')), // 初始为空
      isUserLoaded: false, // 标志位，表示用户数据是否加载完成

      addForm: {
        id: 0,
        name: '',
        folder_path: '',
        directory_image_url: '',
        created_at: '',
        updated_at: '',
        user_id: 0,
        username: '',
        user_name: "",


      },
      rules: {
        name: [
          {required: true, message: '请输入名称', trigger: 'blur'}
        ],


      }
    }
  },
  methods: {
    getData() {
      //从后端获取数据
      this.$axios.post(this.$httpUrl + "/project/list", {
        pageSize: this.pageSize,
        pageNum: this.pageNum,
        name: this.courseName,
        user: this.user

      }).then(res => res.data).then(res => {

        this.tableData = res.data;
        this.total = res.total;
        console.log(   this.tableData)
        this.tableData.forEach(project => {
        if (project && project.id) {

      this.$axios.post(this.$httpUrl + '/project/project_user_list', {
        project_id: project.id // 传递项目的 id
      }).then(res => {
       console.log(res.data)
        if (res.data.code === 200) {

  this.$set(project, 'partners', res.data.data);
     console.log(this.tableData)
     this.istableData=true
        } else {
          this.$message.error('获取伙伴信息失败，请重试');
        }
      }).catch(error => {
        console.error(error);
        this.$message.error('请求失败，请重试');
      });
        }
      });
      })
    },
    reset() {
      this.courseName = '';
      this.getData();
    },
    mod(aaa) {
      this.modForm = aaa;
      this.showMod = true;
    },
    resetForm(admin) {
      if( admin==="admin"){  this.modForm = {};
      this.showAdmin = false;}
      else {    this.modForm = {};
      this.showMod = false;}

    },
    resetAddForm() {
      this.addForm = {
        id: 0,
        name: '',


        created_at: '',
        updated_at: '',
        directory_image_url: '',
        user: this.user.id,


      };
    },

    modUp() {
      this.$refs['modForm'].validate((valid) => {
        if (valid) {
          console.log(this.modForm)

          this.$axios.post(this.$httpUrl + "/project/up", this.modForm).then(res => res.data)
              .then(res => {
                if (res.code === 200) {
                  this.$message({
                    message: '修改成功',
                    type: 'success'
                  });
                  this.modForm = {};
                  this.showMod = false;
                  this.showAdmin = false;
                  this.getData();
                } else {
                  this.$message.error('错了哦，修改失败');
                }
              })
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    addUp() {
      this.$refs['addForm'].validate((valid) => {
        if (valid) {
          this.addForm.username = this.user.username
          this.$axios.post(this.$httpUrl + "/project/add", this.addForm).then(res => res.data)
              .then(res => {
                console.log(res)
                if (res.code === 200) {
                  this.$message({
                    message: '添加成功',
                    type: 'success'
                  });
                  this.resetAddForm();
                  this.showAdd = false;
                  this.getData();
                } else {
                  this.$message.error('错了哦，添加失败');
                }
              })
        } else {
          console.log('error submit!!');
          return false;
        }
      });

    },
    admin(project) {
      this.modForm = project;
      this.showAdmin = true;
    },

    delUser(id) {
      this.$axios.get(this.$httpUrl + "/project/delete?id=" + id).then(res => res.data)
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


    handleSizeChange(val) {
      this.pageNum = 1;
      this.pageSize = val;
      this.getData();
    },
    handleCurrentChange(val) {
      this.pageNum = val;
      this.getData();
    },
    handleUploadSuccess(response) {
      this.$message.success('图片上传成功');
      console.log(response);  // 这里可以显示或使用返回的 URL
      this.addForm.directory_image_url = response.file_url
      this.addForm.folder_path = response.file_path
      console.log(this.addForm)
    },
    beforeUpload(file) {
      const isImage = file.type.startsWith('image/');
      if (!isImage) {
        this.$message.error('只能上传图片文件');
      }
      return isImage;
    },
    handleUploadSuccess2(response) {
      this.$message.success('头像上传成功');
      console.log(response);
      this.modForm.directory_image_url = response.file_url
      this.modForm.folder_path = response.file_path
    },
    beforeUpload2(file) {
      const isImage = file.type.startsWith('image/');
      if (!isImage) {
        this.$message.error('只能上传图片文件');
      }
      return isImage;
    },
    adduser(project) {
      this.showUser = true;

      this.userForm.project_id = project.id;  // 传递项目id到表单
    },

    // 提交添加伙伴的请求
    submitAdd() {
      if (!this.userForm.username) {
        this.$message.error('请填写伙伴的用户名');
        return;
      }

      this.$axios.post(this.$httpUrl + '/project/project_user_add', {
        project_id: this.userForm.project_id,
        username: this.userForm.username
      }).then(res => {
        if (res.data.code === 200) {
          this.$message({
            message: '伙伴添加成功',
            type: 'success'
          });
          this.showUser = false;
          this.getData();  // 更新项目列表
        } else {
          this.$message.error('添加失败，请重试');
        }
      }).catch(error => {
        console.error(error);
        this.$message.error('请求失败，请重试');
      });
    },
    // 删除单个伙伴
    deluser(partner, project) {

      // 从 partner 和 project 获取所需信息
      const projectId = project.id;
      const username = partner.username;

      // 发送请求到后端，去除指定项目的伙伴
      this.$axios.post(this.$httpUrl +'/project/project_user_delete', {
        project_id: projectId,
        username: username
      })
          .then(response => {
            if (response.status === 200) {
              this.$message.success('伙伴已成功移除');
              this.getData(); // 更新项目列表，移除已删除伙伴的项目
            } else {
              this.$message.error(response.data.message || '操作失败，请重试');
            }
          })
          .catch(error => {
            console.error(error);
            this.$message.error('请求失败，请重试');
          });
    },

  },
  created() {
    this.$axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';
    this.$axios.defaults.withCredentials = true; // 如果需要跨域请求时发送 cookie，请设置为 true
        const userData = JSON.parse(sessionStorage.getItem('User'));
    this.getData();

    if (userData) {
      this.user = userData;
    }
    // 更新标志位，表示用户数据已加载
    this.isUserLoaded = true;
  }
}
</script>

<template>
  <div style="text-align: center;padding: 10px;" class="container">
<div >
    <!-- 操作栏 -->
    <div class="toolbar">
      <el-input v-model="courseName" placeholder="项目名称" style="width: 400px; margin: 0 10px;"></el-input>
      <el-button icon="el-icon-search" @click="getData" type="primary">搜索</el-button>
      <el-button icon="el-icon-refresh" @click="reset" type="info">重置</el-button>
      <el-button icon="el-icon-upload" @click="showAdd=true;" type="success">添加项目</el-button>
    </div>

    <!-- 背景装饰 -->
    <div class="background-decor"></div>

    <!-- 课程卡片 -->
    <el-row :gutter="20" class="course-list">
      <el-col
        v-for="project in tableData"
        :key="project.id"
        :span="6"
        class="course-card"
      >
<el-card shadow="hover" class="box-card custom-card">
  <router-link :to="{ path: '/files', query: { id: project.id } }">
    <img :src="project.directory_image_url" alt="课程图片" class="course-image" />
  </router-link>
  <div class="course-content">
    <p class="course-title">{{ project.name }}</p>
    <p class="course-info">创建时间：{{ project.created_at }}</p>
    <p class="course-info">创造人：{{ project.user_name }}</p>
    <p class="course-info">
      <span>伙伴：</span>
      <template v-if="project.partners && project.partners.length > 0">
        <el-tag
          v-for="(partner) in project.partners"
          :key="partner.id"
            :closable="isUserLoaded && user && user.id === project.user_id"

          :type="partner.type || 'primary'"
          @close="deluser(partner, project)"
        >
          {{ partner.name }}
        </el-tag>
      </template>
      <span v-else>暂无伙伴</span>
    </p>
  </div>
  <div
    v-if="isUserLoaded && user && user.id === project.user_id"
    class="course-actions"
  >
    <div class="action-grid">
      <el-button size="small" type="success" style="width: 100% ;margin-right: 22px" @click="mod(project)" class="action-button">编辑</el-button>
      <el-button size="small" type="success"  style="width: 100%" @click="admin(project)" class="action-button">修改项目管理员</el-button>
      <el-button size="small"  style="width: 100%;margin-right: 22px" type="success" @click="adduser(project)" class="action-button">添加伙伴</el-button>
      <el-popconfirm
        confirm-button-text="好的"
        cancel-button-text="点错了"
        icon="el-icon-info"
        icon-color="red"
        title="确定删除吗？"
        @confirm="delUser(project.id)"
      >
        <el-button slot="reference" type="danger" size="small"  style="width: 100%;margin-left: 11px" class="action-button">删除</el-button>
      </el-popconfirm>
    </div>
  </div>
</el-card>

      </el-col>
    </el-row>

    <!-- 分页 -->
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :page-sizes="[5, 10, 20, 40]"
      :page-size="this.pageSize"
      :current-page="this.pageNum"
      layout="total, sizes, prev, pager, next, jumper"
      :total="this.total"
      class="pagination"
    ></el-pagination>
  </div>
    <el-dialog title="添加伙伴" :visible.sync="showUser" width="450px">
      <el-form :model="userForm" ref="addForm">
        <el-form-item label="伙伴用户名" prop="username">
          <el-input v-model="userForm.username" placeholder="请输入伙伴的用户名"></el-input>
        </el-form-item>
      </el-form>

      <span slot="footer" class="dialog-footer">
    <el-button @click="showUser = false">取消</el-button>
    <el-button type="primary" @click="submitAdd">提交</el-button>
  </span>
    </el-dialog>


    <el-dialog title="编辑" width="550px" :visible.sync="showAdmin" style="text-align: start;" center>
      <div style="display: flex; justify-content: center; width: 100%;">
        <el-form ref="modForm" :model="modForm" :rules="rules" style="width: 100%;">
          <el-form-item label="账号" prop="user_name">
            <el-input v-model="modForm.user_name" class="inputUser"></el-input>
          </el-form-item>


        </el-form>
      </div>
      <span slot="footer" class="dialog-footer">
    <el-button type="primary" @click="modUp()">提交</el-button>
    <el-button @click="resetForm('admin')">关闭</el-button>
  </span>
    </el-dialog>
    <el-dialog title="编辑信息" width="550px" :visible.sync="showMod" style="text-align: start;" center>
      <div style="display: flex; justify-content: center; width: 100%;">
        <el-form ref="modForm" :model="modForm" :rules="rules" style="width: 100%;">
          <el-form-item label="名称" prop="name">
            <el-input v-model="modForm.name" class="inputUser"></el-input>
          </el-form-item>


          <!-- 头像URL上传 -->
          <el-form-item label="课程封面图" prop="imageUrl">
            <el-upload
                class="avatar-uploader"
                action=" http://localhost:8000/jpg/upload"
                :show-file-list="false"
                :on-success="handleUploadSuccess2"
                :before-upload="beforeUpload2"
            >
              <el-button size="small" type="primary">上传封面图</el-button>
              <img v-if="modForm.directory_image_url" :src="modForm.directory_image_url" class="avatar"/>
            </el-upload>
          </el-form-item>


        </el-form>
      </div>
      <span slot="footer" class="dialog-footer">
    <el-button type="primary" @click="modUp()">提交</el-button>
    <el-button @click="resetForm('add')">关闭</el-button>
  </span>
    </el-dialog>

    <el-dialog title="添加信息" width="550px" center :visible.sync="showAdd" style="text-align:start;">
      <el-form ref="addForm" :model="addForm" :rules="rules" style="width: 100%;">
        <el-form-item label="名称" prop="name">
          <el-input v-model="addForm.name" class="inputUser"></el-input>
        </el-form-item>


        <!-- 头像URL上传 -->
        <el-form-item label="课程封面图" prop="imageUrl">
          <el-upload
              class="avatar-uploader"
              action=" http://localhost:8000/jpg/upload"
              :show-file-list="false"
              :on-success="handleUploadSuccess"
              :before-upload="beforeUpload"
          >
            <el-button size="small" type="primary">上传封面图</el-button>
            <img v-if="addForm.directory_image_url" :src="addForm.directory_image_url" class="avatar"/>
          </el-upload>
        </el-form-item>


      </el-form>

      <span slot="footer" class="dialog-footer">
          <el-button type="primary" @click="addUp()">提交</el-button>
          <el-button @click="resetAddForm()">重置</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<style scoped>
.container {
    font-family: 'KaiTi', '楷体';
  height: 100vh;
  background: linear-gradient(to bottom, #f5f5dc, #ffe4e1);
  padding: 20px;
}





.background-decor {
  font-family: 'KaiTi', '楷体';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 300px;
  z-index: -1;
  opacity: 0.1;
}

.course-list {
  padding: 20px 0;
}

.course-card {
    font-family: 'KaiTi', '楷体';
  transition: transform 0.3s;
}

.course-card:hover {
  transform: translateY(-5px);
}

.course-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 5px;
}

.course-title {  font-family: 'KaiTi', '楷体';

  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.course-actions {
    font-family: 'KaiTi', '楷体';
  margin-top: 10px;
}

.pagination {
    font-family: 'KaiTi', '楷体';
  margin-top: 20px;
  text-align: center;
}

.custom-card {
  background-color: #f7f5f2; /* 柔和的背景色 */
  border-radius: 12px; /* 圆角 */
  overflow: hidden;
  transition: transform 0.3s, box-shadow 0.3s;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.custom-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.course-content {
  padding: 16px;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif; /* 中国风字体 */
}

.course-title {
  font-size: 1.4em;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.course-info {
  font-size: 1.1em;
  color: #555;
  margin-bottom: 4px;
}

.action-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  padding: 16px;
}

.action-button {
  font-size: 1em;
  font-weight: bold;
  border-radius: 8px;
  transition: background-color 0.3s, color 0.3s;
}

.action-button.success {
  background-color: #a8d5ba;
  color: #fff;
}

.action-button.success:hover {
  background-color: #81c497;
}

.action-button.danger {
  background-color: #f28b82;
  color: #fff;
}

.action-button.danger:hover {
  background-color: #f06a6a;
}

.clearfix {
  padding: 10px 15px;
}


</style>