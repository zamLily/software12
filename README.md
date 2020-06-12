# 软件工程第12组

一、使用方法  
1. 将代码clone至本地：git clone https://github.com/zamLily/software12.git  
2. 进入software12目录
3. 执行命令pip install -r requirements.txt（报错的话可以先跳过这步试试）  
4、进入虚拟环境：env\Scripts\activate  
5、运行：flask run   
6、用浏览器打开 http://127.0.0.1:5000/  


二、文件介绍  
1、data.db 数据库  
2、env 虚拟环境相关  
3、点开watchlist文件夹，  
里面的model.py为数据库相关的，view.py为主要代码（功能实现）  
templates文件夹里面为html文件  
static文件夹里面为css文件，pic文件夹装了css相关的图片（由于前端还没有给主页，因此暂时用了别的代替所以有两个css，等前端写好即替换掉）  
4、test_watchlist.py为测试文件，先不用

三、功能介绍  
1、目前实现了主页、登录页面、注册页面之间的逻辑  
2、加入了数据库存储用户资料，登录时有“用户不存在!”、“密码错误”、“登陆成功”等信息提示在页面左上角或者主页上方，注册同理有些提示  
3、在主页点击regist注册，点击login登录，登陆后点击logout可退出登录  
4、实现了login_required,即登陆后才能操作  

注意：UI界面排版还需等待前端调整，目前是能实现前后端对接，flask渲染 



