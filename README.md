# Demo2-BE
## Steps

## DB
```bash
#创建一個MySQL容器，并指定容器的名称、MySQL root密码、以及要映射的端口号
docker run -d --name VisualTon1 -e MYSQL_ROOT_PASSWORD=0505jo -p 3390:3306 mysql:latest

#連接到MySQL容器
docker exec -it VisualTon1 mysql -u root -p

#顯示全部DB
SHOW DATABASES;

#創建DB
CREATE DATABASE Tx;

#選擇DB
USE Example;

#查看當前DB
SELECT DATABASE();

#查看當前DB有哪些table
SHOW TABLES;

#查看DB的table
DESCRIBE employees;
```

## run cronjob on EC2 instance (optional)
### upload script to EC2 instance
```bsah
#TODO
scp -i your-ec2-key.pem cronjob.py ec2-user@your-ec2-instance-ip:/home/ec2-user/
```
### connect to EC2 instance
```bash
ssh -i your-ec2-key.pem ec2-user@your-ec2-instance-ip
```