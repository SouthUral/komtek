# project description
- Сервис представляет собой базу данных co справочниками и API для доступа к их содержимому  
### technologies
- Django REST framework
- PostgreSQL

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
    3. для запуска введите команду make runserver

- доступ в админ-панель осуществляется по ссылке: [http://localhost:7000/admin]()
    - логин: admin
    - пароль: admin

## database structure
- Справочник (Handbook)
    - Идентификатор (id-uuid)
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
***
##### Получение списка справочников: /handbooks
###### request:

    GET http://localhost:7000/api/v1/handbooks
###### response:
    {
    "count": 4,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "911312b1-b2d7-4b2c-b1e4-c731ffa29a26",
            "code": "1",
            "title": "Клиенты"
        },
        {
            "id": "6940419a-ecfc-4319-a9bc-b1a18737746d",
            "code": "2",
            "title": "Номенклатура"
        },
        {
            "id": "b3908710-c3f9-49c8-a299-011351e7931a",
            "code": "3",
            "title": "Врачи"
        },
        {
            "id": "1749a71b-be21-4f10-b0f0-477bbd30c6df",
            "code": "4",
            "title": "Назначения"
        }
    ]
}
***

##### Получение списка справочников актуальных на текущую дату: 
- /handbooks/get_on_date
###### request:

    GET http://localhost:7000/api/v1/handbooks/get_on_date
###### response:
    {
    "refbooks": [
        {
            "id": "1749a71b-be21-4f10-b0f0-477bbd30c6df",
            "code": "4",
            "title": "Назначения"
        },
        {
            "id": "6940419a-ecfc-4319-a9bc-b1a18737746d",
            "code": "2",
            "title": "Номенклатура"
        },
        {
            "id": "911312b1-b2d7-4b2c-b1e4-c731ffa29a26",
            "code": "1",
            "title": "Клиенты"
        },
        {
            "id": "b3908710-c3f9-49c8-a299-011351e7931a",
            "code": "3",
            "title": "Врачи"
        }
    ]
    }
***

##### Получение списка справочников актуальных на указанную дату: 
- /handbooks/get_on_date/?date=2022-10-22
###### request:

	GET http://localhost:7000/api/v1/handbooks/get_on_date/?date=2022-10-22
###### response:
    {
    "refbooks": [
        {
            "id": "6940419a-ecfc-4319-a9bc-b1a18737746d",
            "code": "2",
            "title": "Номенклатура"
        },
        {
            "id": "911312b1-b2d7-4b2c-b1e4-c731ffa29a26",
            "code": "1",
            "title": "Клиенты"
        },
        {
            "id": "b3908710-c3f9-49c8-a299-011351e7931a",
            "code": "3",
            "title": "Врачи"
        }
    ]
    }
***
##### Получение элементов заданного справочника текущей версии:
- по параметру 'title': /elements/get_elements/?title=Врачи
- по параметру 'id': /elements/get_elements/?id=b3908710-c3f9-49c8-a299-011351e7931a  
'id' должен быть UUID
###### request:

	GET http://localhost:7000/api/v1/elements/get_elements?title=Врачи
###### response:
    {
    "Врачи.2: 2022-10-22": [
        {
            "id": "a581fba3-856c-46a3-a64c-d9972b50dcaa",
            "version": "http://localhost:7000/api/v1/version/cb574277-0bb7-453e-bbf9-7ab9b93ebfb0/",
            "code": "1",
            "value": "Николай Анатольевич"
        },
        {
            "id": "cd9d1554-9912-4c56-89a4-aae65b0f7d0e",
            "version": "http://localhost:7000/api/v1/version/cb574277-0bb7-453e-bbf9-7ab9b93ebfb0/",
            "code": "2",
            "value": "Валентина Александровна"
        },
        {
            "id": "11e63c17-455e-404b-9f13-b2a3e8c93592",
            "version": "http://localhost:7000/api/v1/version/cb574277-0bb7-453e-bbf9-7ab9b93ebfb0/",
            "code": "3",
            "value": "Елена"
        }
    ]
    }
***
##### Получение элементов заданного справочника указанной версии:
- для получения версии дополнительно используется параметр 'version':  
/elements/get_elements?title=Врачи&version=1
###### request:

	GET http://localhost:7000/api/v1/elements/get_elements?title=Врачи&version=1
###### response:
    {
    "Врачи.1: 2022-10-21": [
        {
            "id": "dc586fb7-4c22-45db-b2fc-c1dfdab6566e",
            "version": "http://localhost:7000/api/v1/version/1b7d08f7-116f-428d-9b78-7033ae6c8437/",
            "code": "1",
            "value": "Игорь Сергеевич"
        },
        {
            "id": "490c09e5-b7b5-4728-b115-230d34e300f1",
            "version": "http://localhost:7000/api/v1/version/1b7d08f7-116f-428d-9b78-7033ae6c8437/",
            "code": "2",
            "value": "Олег Владимирович"
        },
        {
            "id": "91707b81-0125-453b-8d53-abc636885d31",
            "version": "http://localhost:7000/api/v1/version/1b7d08f7-116f-428d-9b78-7033ae6c8437/",
            "code": "3",
            "value": "Елена Алексеевна"
        }
    ]
    }
***
##### Валидация элементов заданного справочника текущей версии:
- для валидации используются параметры: p1, p2, p3 ...  
- для валидации элементов текущей версии справочника не используется параметр 'version'  
/elements/validate_elements?title=Врачи&p1=Николай Анатольевич&p2=Валентина
###### request:
    GET http://localhost:7000/api/v1/elements/validate_elements?title=Врачи&p1=Николай Анатольевич&p2=Валентина
###### response:
    {
    "Врачи.2: 2022-10-22": {
        "Николай Анатольевич": true,
        "Валентина": false
    }
    }
***
##### валидация элемента(ов) заданного справочника по указанной версии:
- используется параметр 'version'
- валидацию можно проводить по одному параметру
/elements/validate_elements?title=Врачи&p4=Влад&version=1
###### request:
	GET http://localhost:7000/api/v1/elements/validate_elements?title=Врачи&p4=Влад&version=1
###### response:
    {
    "Врачи.1: 2022-10-21": {
        "Влад": false
    }
    }
