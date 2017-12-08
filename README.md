# docker-aiohttp


### OS X Instructions

1. Start new machine - `docker-machine create -d virtualbox dev2`
1. Build images - `docker-compose build`
1. Start services - `docker-compose up -d`
1. Create migrations - `cat web/sql/01_item_schema.sql | docker exec -i dockeraiohttp_postgres_1 psql -U postgres postgres`
1. Grab IP - `docker-machine ip dev2` - and view in your browser
