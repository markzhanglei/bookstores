bookstore

项目描述
本项目主要使用的数据库有mysql,redis
mysql是数据的存放位置，比较安全。
redis是做缓存，存放一些访问量比较大的网页或数据，redis中缓存的数据需要做定时清除，时间为一天。
gunicore做部署使用。
搜索使用的是whoosh做搜索引擎，haystack是搜索框架，实现全局搜索。
异步发送邮件使用celery执行异步任务。
系统的管理后台使用xadmin来实现。
使用富文本编辑器美化网站的一些详情页面。
验证码使用pillow和随机数来实现。
