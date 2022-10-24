# project description
- Сервис представляет собой базу данных co справочниками и API для доступа к их содержимому

## requirement
- Linux operating system
- python = 3.10
- poetry = 1.1.15
- docker = 20.10.20
- Docker Compose = 2.10.2

## installation
1. клонируйте репозиторий
2. в корневой директории проекта введите команду make install

- для запуска сервиса введите команды находясь в корневой директории проекта
    1. make docker_up
    2. make migrate
    3. я запуска введите команду make runserver

- доступ в админ-панель осуществляется по ссылке: http://localhost:7000/admin
    - логин: admin
    - пароль: admin

## database structure
- Справочник (Handbook)
    - Идентификатор (id)
    - Код (code)
    - Наименование (title)
    - Описание (description)

- Версия справочника (VersionHandbook)
    - Идентификатор (id)
    - Идентификатор справочника (handbook)
    - Версия (version)
    - Дата начала действия версии (date_start)

- Элемент справочника ()
    - Идентификатор (id)
    - Идентификатор версии справочника (version)
    - Код (code)
    - Значение элемента (value)

## REST API
- Получение списка справочников: /handbooks
    request
    GET http://localhost:7000/handbooks

- Получение списка справочников актуальных на текущую дату: /handbooks/get_on_date
    request
    GET http://localhost:7000/handbooks/get_on_date

- Получение списка справочников актуальных на указанную дату: 
