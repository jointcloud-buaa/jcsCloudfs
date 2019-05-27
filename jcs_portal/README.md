# JPS Portal 部署文档 (step by step)

## 整体思路

JPS Portal 依赖以下组件

- Python 2.7 和一些第三方库
- Node.js 8.9.4
- Nginx

其中 Python 相关的组件在部署 Proxy 时已经配置好了，在本文中不再重复。

## Node.js

```shell
# 直接 yum 安装
$ sudo yum install nodejs

# 验证安装
$ node --version
$ npm --version
```

## Nginx

## 修改项目配置

`jcs_portal/index.py`

```py
# 把 host 和 port 改为 proxy 的实际配置
CLOUD_PROXY = {
    'proto': 'http',
    'host': 'your-ip-address-here',
    'port': '8888',
}

# user_name 是实际运行该项目的用户名
user_name = "cloudfs"

# download_path 是 portal 从 proxy 下载文件时的缓存路径
local_download_path = "/home/cloudfs/tmp/download/"

# upload_path 是 portal 向 proxy 上传文件时的缓存路径
local_upload_path_linux = "/home/cloudfs/tmp/upload/"
# 注意上面两个目录需要手动创建

# 在文件的最后，配置后端服务的 ip 地址和端口
if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    app.run(host='your-ip-address-here',port=5000,debug=True)
```

`jcs_portal/templates/index.html`

```html
<!-- 修改 src 为前端服务地址，注意这里应该配置公网 ip 地址 -->
<body>
  <div id="app"></div>
  <script type="text/javascript" src="http://your-ip-address-here:5001/app.js"></script>
</body>
```

`jcs_portal/frotend/config/index.js`

```js
// 配置前端服务地址
dev: {
    host: 'your-ip-address-here',
    port: 5001,
}
```

## 启动服务

启动前端服务

```shell
$ cd jcs_portal/frotend

# 首次运行时需要安装运行环境
$ npm install
$ npm run dev
```

启动后端服务

```shell
# 先进入虚拟环境
$ source env/bin/activate

$ cd jcs_portal
$ python index.py
```