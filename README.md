# Demo2-BE
## Steps

## DB
```bash
#创建并运行一个名为 "VisualTon" 的MySQL容器
docker run -d --name VisualTon -e MYSQL_ROOT_PASSWORD=0505jo -e MYSQL_DATABASE=example -p 3390:3306 mysql:latest 
docker run --name myphpadminVisualTon -d --link VisualTon:db -p 8081:80 phpmyadmin/phpmyadmin

#构建自定义镜像(不需要)
docker build -t visualtonimage:latest .

#連接container (pwd: 0505jo)
docker exec -it VisualTon1 mysql -u root -p

# 透過container name 查找host
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' VisualTon

#顯示全部DB
SHOW DATABASES;

#創建DB
CREATE DATABASE Example;

#選擇DB
USE Example;

#查看當前DB
SELECT DATABASE();

#查看當前DB有哪些table
SHOW TABLES;

#查看DB的table
DESCRIBE transactions;

#從table拿資料
SELECT * FROM transactions;

# 刪除table
DROP TABLE transactions;
```