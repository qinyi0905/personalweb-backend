1. clone code to local:
```shell
$ git clone https://github.com/qinyi0905/personalweb-backend.git
```

2. build docker image:
```shell
$ docker build -t <image_name> .
```

4. create database in your mysql:
```shell
$ mysql -u <username> -p
mysql> create database <database_name> charset utf8mb4;
```

5. run image:
```shell 
$ docker run -d -p 80:80 \
  --name <container_name>  \
  --restart=always         \
  -e DB_USERNAME=<mysql_username> \
  -e DB_PASSWORD=<mysql_password> \
  -e DB_HOST=<mysql_host> \
  -e DB_PORT=<mysql_port> \                   #option,default:3306
  -e DB_NAME=<database_name> \                #option,default:'personalweb'
  -e CACHE_REDIS_HOST=<redis_host> \
  -e CACHE_REDIS_PORT=<redis_port> \          #option,default:6379
  -e CACHE_REDIS_PASSWORD=<redis_password> \  #option,default: '7upJvu2eTuRg'
  <image_name>
```
  
