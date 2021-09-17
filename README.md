# Test task for Sayollo

###Project is set up with fast-api and mongodb.
###Run this project with 

`$ docker-compose up`

###after that you can open swagger page with endpoints on 

`http://0.0.0.0:8000/docs`


###project structure:

- `Dockerfile` and `docker-compose.yml` - Docker files 
- `tests.py` - basic pytests for API endponts
- `models.py` - object orientented entities
- `db_utils.py` - common functions to work with mongodb
- `requirements.txt` - python required packages