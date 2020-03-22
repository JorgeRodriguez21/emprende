#!/bin/bash
#If you can't run this, just paste it in your console:  chmod u+x create_database.sh (in the project directory)
docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d --restart=always postgres