pip3 install faker

if [ "$CREATE_TABLE" = "true" ]
then
    python3 create_table.py
else
  echo "Pass in environment variable for CREATE_TABLE in docker-compose.yml"

fi

flask run --host=0.0.0.0 --port=5500