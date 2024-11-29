```shell
docker exec -it mymongo mongosh  
use admin  
db.createUser({user:'root',pwd:'123', roles:[{role:'root', db:'admin'}]})  
db.auth('root','123')
```
