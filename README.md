# Birthday-Calendar

This is a tool for reminding you of one's birthday or anniversary by sending you a email before the specific day. 
Supported by `Github Actions`. 

### 初期设想
* 自定义配置文件，配置多人生日，支持农历/阳历
* Python脚本读取配置，查看是否生日临近，发送提醒邮件
* 编写Action workflow，每天定时执行Python脚本
* 编写邮件模板

### 后续优化
- [ ] 使用数据库，取代配置文件；
- [ ] 提供接口，web，或第三方平台接入;

### 问题
- [x] 配置文件为明文，smtp信息和个人信息不安全    
已解决：使用七牛云对象存储保存配置文件，在setting中配置secret

- [ ] 农历和阳历日期转换
