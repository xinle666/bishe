from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='用户ID')  # 自增主键
    username = models.CharField(max_length=50, verbose_name='用户名')  # 用户名
    password = models.CharField(max_length=100, verbose_name='密码')  # 密码
    phone = models.CharField(max_length=15, null=True, blank=True, verbose_name='电话号码')  # 电话号码，可为空
    role = models.CharField(max_length=20, verbose_name='角色')  # 用户角色
    birth_date = models.DateField(verbose_name='出生日期')  # 出生日期
    name = models.CharField(max_length=50, verbose_name='姓名')  # 姓名
    sex = models.IntegerField(verbose_name='性别')  # 性别 (0: 女, 1: 男等）

    class Meta:
        db_table = 'user'  # 指定数据库中的表名
        verbose_name = '用户'
        verbose_name_plural = '用户'

class Project(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='主键')
    name = models.CharField(max_length=100, verbose_name='项目名称')
    folder_path = models.CharField(max_length=255, verbose_name='文件夹路径')
    directory_image_url = models.CharField(max_length=255, null=True, blank=True, verbose_name='项目目录图片 URL')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='项目管理员',
        related_name='projects'
    )

    class Meta:
        db_table = 'project'  # 设置表名为 'project'

class File(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='主键')
    name = models.CharField(max_length=255)          # 文件名
    file_url = models.CharField(max_length=255)      # 文件 URL
    file_path = models.CharField(max_length=255)     # 文件路径
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间，自动设置
    updated_at = models.DateTimeField(auto_now=True)  # 更新时间，自动更新时间
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,

    )
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'file'  # 设置表名为 'file'
class FileProjectAssociation(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='主键')
    file = models.ForeignKey(File, on_delete=models.CASCADE)         # 关联文件
    project = models.ForeignKey(Project, on_delete=models.CASCADE)  # 关联项目

    class Meta:


        db_table = 'file_project_association'  # 设置表名为 'file'
    def __str__(self):
        return f"{self.file.name} - {self.project.name}"


class ProjectUserAssociation(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='主键')
    project = models.ForeignKey('Project', on_delete=models.CASCADE)  # 关联项目
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 关联用户

    class Meta:

        db_table = 'project_user_association'  # 设置表名为 'file'
    def __str__(self):
        return f"{self.project.name} - {self.user.username}"
# 创建关联表：Fileing
class Fileing(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='主键')
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 关联 User 表
    file = models.ForeignKey(File, on_delete=models.CASCADE)  # 关联 File 表
    ing_at = models.DateTimeField(auto_now_add=True)  # 记录上传时间

    class Meta:
        db_table = 'fileing'  # 设置表名为 'file'
    def __str__(self):
        return f"{self.user.username} uploaded {self.file.name}"