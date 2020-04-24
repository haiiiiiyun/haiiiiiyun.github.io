Install from source: https://thingsboard.io/docs/user-guide/contribution/how-to-contribute/

1. Compile with mvn first, which will create,
then import it into IDE as maven 

```bash
cd ~/workspace/thingsboard/application
mvn clean install -DskipTests
```

2. Create DB schema and populate demo data:

```bash
cd ${TB_WORK_DIR}/application/target/bin/install
chmod +x install_dev_db.sh
./install_dev_db.sh
```

default DB:
"${SPRING_DATASOURCE_URL:jdbc:postgresql://localhost:5432/thingsboard}"
username: "${SPRING_DATASOURCE_USERNAME:postgres}"
password: "${SPRING_DATASOURCE_PASSWORD:postgres}"

```bash
sudo service postgresql start
```

http://www.atjiang.com/postgresql-beginner-11-tasks/

install pgadmin4: https://wiki.postgresql.org/wiki/Apt
