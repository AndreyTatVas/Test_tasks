from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

import csv
from sqlalchemy import create_engine
import os


def insert_data_open_sky(path, logs, file):
    # Отсекаем .csv
    file = file[:-4]

    # Создаем соединение к БД
    cnx_gp = create_engine('postgresql://user:password@host:port/table')  # Строка с параметрами подключения к БД

    # Счетчик для контроля количества запросов
    i = 0
    # Словарь, в котором сохраняются запросы
    dict_query = {
        "query_data_test_flight_information": "lock table test_registered_flights;",
        "query_data_test_aircraft_information": "lock table test_registered_flights;",
        "query_data_test_registered_flights": ""
    }

    # Список столбцов для таблицы query_data_test_registered_flights
    list_column_flights = ['callsign', 'icao24', 'origin', 'destination', 'firstseen', 'lastseen', 'day', 'latitude_1',
                           'longitude_1', 'altitude_1', 'latitude_2', 'longitude_2', 'altitude_2']

    with open(f"{path}/{file}.csv", encoding='utf-8') as r_file:

        # Создаем объект reader, указываем символ-разделитель ","
        file_reader = csv.DictReader(r_file, delimiter=",")

        # Считывание данных из CSV файла
        for row in file_reader:

            if (row['origin'] != '' and row['destination'] != '') and row['origin'] != row['destination']:
                # увеличиваем счетчик
                i += 1

                # Получаем информацию о рейсе
                dict_query["query_data_test_flight_information"] += f"""
                insert into test_flight_information (callsign, number)
                values ({', '.join((f"'{item}'" if item != '' else 'null' for item in
                                    (row['callsign'], row['number'])))})
                on conflict on constraint PK_callsign do update
                set number = {f"'{row['number']}'" if row['number'] != '' else 'null'} 
                where test_flight_information.number is null;
                """

                # Получаем информацию о самолете
                dict_query["query_data_test_aircraft_information"] += f"""
                insert into test_aircraft_information (icao24, registration, typecode)
                values ({', '.join((f"'{item}'" if item != '' else 'null' for item in (row['icao24'],
                                                                                       row['registration'],
                                                                                       row['typecode'])))})
                on conflict on constraint PK_icao24 do nothing;
                """

                # Получаем информацию о полетах
                dict_query["query_data_test_registered_flights"] += f"""
                insert into test_registered_flights 
                ({', '.join(item for item in list_column_flights)})
                values ({', '.join((f"'{row[item]}'" if row[item] != '' else 'null' for item in list_column_flights))})
                ;
                """

                try:
                    # Если запросов накопилось определенное количество, то кидаем их в БД и очищаем переменные в
                    # dict_query
                    if i % 1000 == 0:
                        for key in dict_query:
                            if len(dict_query[key]) > 0:
                                cnx_gp.execute(dict_query[key])
                        # Очищаем словарь, в котором сохраняются запросы
                        dict_query = {
                            "query_data_test_flight_information": "lock table test_registered_flights;",
                            "query_data_test_aircraft_information": "lock table test_registered_flights;",
                            "query_data_test_registered_flights": ""
                        }

                except Exception as err:
                    print('ошибка', err)
                    # При ошибке сохраняем запросы, на которых возникла ошибка
                    for key in dict_query:
                        if len(dict_query[key]) > 0:
                            err_file = open(f"{logs}/{file}_{key}_{i}.txt", "w")
                            err_file.write(dict_query[key])
                            err_file.close()
                    # Очищаем словарь, в котором сохраняются запросы
                    dict_query = {
                        "query_data_test_flight_information": "lock table test_registered_flights;",
                        "query_data_test_aircraft_information": "lock table test_registered_flights;",
                        "query_data_test_registered_flights": ""
                    }

        # После цикла заливаем все остатки в БД, если они есть
        try:
            # увеличиваем счетчик
            i += 1

            for key in dict_query:
                if len(dict_query[key]) > 0:
                    cnx_gp.execute(dict_query[key])

        except Exception as err:
            print('ошибка', err)
            for key in dict_query:
                if len(dict_query[key]) > 0:
                    err_file = open(f"{logs}/{file}_{key}_{i}.txt", "w")
                    err_file.write(dict_query[key])
                    err_file.close()


insert_data_open_sky_dag = DAG(
    dag_id='insert_data_open_sky',
    start_date=days_ago(0, 0, 0, 0, 0),
    schedule_interval=None,
    concurrency=2,  # Параметр для указания одновременно выполняемых тасков
    tags=["test"],
    default_args={'owner': 'atatarenko'}
)

path = 'flights/data'  # Папка с файлами
logs = 'flights/logs'  # Папка, в которую сохраняем запросы, на которых возникла ошибка

insert_data_open_sky_task_list = []

for file in os.listdir(path):
    # insert_data_open_sky(path, logs, file)
    insert_data_open_sky_task = PythonOperator(
        task_id=f'insert_data_open_sky_task_{file}',
        dag=insert_data_open_sky_dag,
        python_callable=insert_data_open_sky,
        op_kwargs={
            "path": path,
            "logs": logs,
            "file": file
        }
    )

    insert_data_open_sky_task_list.append(insert_data_open_sky_task)

insert_data_open_sky_task_list
