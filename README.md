# Demo2-BE
## Steps
```bash
#ssh to ec2 instance (terminal 1)
ssh -i VisualTonKeyPair.pem ec2-user@3.112.222.156

#(ONLY DO ONCE) create and run container after ssh to instance (terminal 1)
docker run -d --name VisualTon -e MYSQL_ROOT_PASSWORD=0505jo -e MYSQL_DATABASE=example -p 3306:3306 mysql:latest 

# 連接container  (terminal 1)(pwd: 0505jo)
docker exec -it VisualTon mysql -u root -p

#(optional) 用phpmyadmin 觀察data (terminal 2)
docker run --name myphpadminVisualTon -d -e PMA_HOST=3.112.222.156 -e PMA_PORT=3306 -p 8081:80 phpmyadmin/phpmyadmin

#create DB
python scripts/create_DB.py

#get the block id(the start block)
python scripts/get_latest_basechain_height.py

#paste the result to cronjob.py 'prev_latest_block' variable

#run the cronjob
python cronjob.py

#observe the DB and debug...
```


## check DB
```bash
#顯示全部DB
SHOW DATABASES;

#創建DB
CREATE DATABASE Example;

#選擇DB
USE example;

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