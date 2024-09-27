# DAT系统指南

# 使用指南

## 直接通过公网ip访问系统（目前关闭）

### 一、访问公网ip地址进入系统体验

#### 步骤1: 点击进入网页

请在浏览器中输入地址：

>

#### 步骤2: 输入用户名和密码

默认管理员账户：（请勿外传）

>用户名:admin
>密码:admin

#### 步骤3: 系统体验

任务介绍：

![image-20240327203310013](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20240327203310013.png)

开始发散性思维能力测试：

![image-20240327203334812](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20240327203334812.png)

查询作答结果：

![image-20240327203353608](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20240327203353608.png)

总体数据分析

![image-20240327203410348](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20240327203410348.png)

管理任务测验时间

![image-20240327203426009](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20240327203426009.png)

批量用户上传

![image-20240327203441859](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20240327203441859.png)

---

## 在Windows环境下的安装步骤

### 一、安装所需的Python包（确保Python版本大于3.8）

#### 步骤1: 进入到`dat_django_project`文件目录

打开命令提示符或PowerShell，首先定位到你的`dat_django_project`项目目录。使用`cd`命令可以帮助你进入到相应的文件夹中。例如：

```bash
cd path\to\dat_django_project
```

请将`path\to\dat_django_project`替换成你的实际文件夹路径。

#### 步骤2: 创建并激活虚拟环境

为了保持项目的依赖环境干净，我们将使用`virtualenv`创建一个隔离的Python环境。首先，确保你已经安装了`virtualenv`。如果没有，可以通过以下命令安装：

```bash
pip install virtualenv
```

安装完成后，创建一个新的虚拟环境：

```bash
virtualenv 虚拟环境名称
```

接下来，激活刚创建的虚拟环境：

```bash
cd 虚拟环境名称
.\Scripts\activate
#在Linux环境为
source bin/activate
```

#### 步骤3: 安装项目依赖

现在虚拟环境已经激活，你可以安装项目所需的所有依赖包了。确保`requirements.txt`文件位于当前目录下，然后执行以下命令：

```bash
pip install -r requirements.txt
```

#### 步骤4: 运行DAT系统

安装完所有依赖后，你就可以启动DAT系统了。使用下面的命令来启动Django服务器：

```bash
python manage.py runserver 0.0.0.0:8000
```

这里使用了8000端口，但你可以根据需要选择其他端口。

### 二、配置DAT系统

#### 1. 数据库配置

在DAT系统首次运行之前，你需要配置数据库连接。这一步骤通常涉及编辑`settings.py`文件，指定数据库的类型、名称、用户、密码等信息。

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}
```

以上是一个使用SQLite数据库的示例配置。根据你的实际需求，你可能需要配置MySQL、PostgreSQL等其他类型的数据库。

#### 2. 迁移数据库

配置数据库后，使用以下命令来创建或更新数据库结构：

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 3. 创建超级用户

为了访问DAT系统的管理界面，你需要创建一个超级用户：

```bash
python manage.py createsuperuser
```

按提示输入用户名、电子邮件地址和密码。

#### 4. 请下载模型

由于系统限制，我们只能够上传1024m以内的源代码，但本系统需要使用到腾讯AI实验室所训练的word2vec模型，请根据您的电脑情况，下载200维的word2vec模型。

>[Embedding Datasets Download (tencent.com)](https://ai.tencent.com/ailab/nlp/en/download.html)

并通过`deal_model.py`文件，预处理下载下来的word2vec模型，才能够使得系统正常运行。

### 三、访问DAT系统

启动服务器后，打开浏览器并访问`http://localhost:8000`。如果一切设置正确，你将看到DAT系统的首页。

登录管理界面，请访问`http://localhost:8000/admin`，并使用之前创建的超级用户凭据登录。

以上就是在Windows环境下安装和配置DAT系统的基本步骤。希望这能帮助你顺利地完成安装。如果遇到任何问题，不要忘记查看相关文档或寻求社区的帮助。

---

# 项目目录结构

### `dat`目录

- `asgi.py`: ASGI配置，用于异步web服务器。
- `settings.py`: 项目配置，包含数据库、中间件、模板等设置。
- `urls.py`: URL声明，相当于网站的目录。
- `wsgi.py`: WSGI配置，用于Web服务器运行Django项目。

### `dat_app`目录

- `middleware`:

  - `auth.py`: 自定义认证中间件。
  - `dynamic_menu.py`: 动态菜单生成中间件。

- `migrations`: 数据库迁移文件。

- `static`: 存放静态文件（CSS、JavaScript、图片等）。

  - `img`: 存放图片文件。

- `utils`:

  - `__init__.py`: 指示此目录为Python包。
  - `admin.py`: Django admin的配置。
  - `apps.py`: 应用配置。
  - `models`: 模型文件夹，请存在模型于此目录。
    - `deal_model.py`:通过此程序处理模型文件。

  - `tests.py`: 测试代码。
  - `views.py`: 视图函数定义。

### `static`目录

- 存放项目的全局静态文件。

### `templates`目录

- 存放Django模板文件，如`dat_score.html`、`dat_test.html`等。

### `data`目录

用于存放目前实验提供的数据，仅供参考

### 根目录文件

- `manage.py`: 项目管理工具。
- `README.md`: 项目说明文档。
- `requirements.txt`: 项目依赖列表。

---

