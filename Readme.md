# Readme

✅实现的功能

- 服务端

  - [x] 屏幕实时共享

  - [x] 屏幕录制，本地存储与回放
  - [x] 聊天室

  - [ ] 用户控制列表

- 客户端
  - [x] 用户注册与登录
  - [ ] 本地存储直播链接
  - [x] 直播观看
  - [ ] 实现视频直播的暂停、回放、帧率显示、播放进度
  - [x] 聊天室

⭐⭐⭐怎么使用

- step1：安装依赖项

```
pip install -r requirements.txt
```

- step2：配置SQL数据库，在sql.py的connect_db()中修改相关的密码

```
cnx = mysql.connector.connect(user='root', password='123456',host='127.0.0.1',database='screenshot')
```

- step3：修改transmit.py中的url，启动服务端，开始共享屏幕

```
python transmit.py
```

- step4：配置Nginx服务器，进入nginx 1.7.11.3 Gryphon文件夹，在/conf/screensharing.conf中修改rtmp的url，准备接收视频流

```
$ nginx.exe -c /conf/screensharing.conf
```

- step5：启动客户端服务器

```
python ./gui/gui.py
```

