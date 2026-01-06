# Клиент API для FusionPOS

Этот проект представляет собой CLI (интерфейс командной строки) на Python для взаимодействия с API POS-системы FusionPOS.

## Установка

1.  **Клонируйте репозиторий (если вы этого еще не сделали):**
    ```bash
    git clone https://github.com/raf0viy/fusionAPI.git
    cd fusionAPI
    ```

2.  **Создайте и активируйте виртуальное окружение:**
    *   В Windows:
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```
    *   В macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Установите зависимости:**
    ```bash
    pip install -r requirements.txt
    ```

## Использование

Все команды выполняются через `main.py`. В Windows используйте `venv\Scripts\python.exe main.py`, а в macOS/Linux — `python3 main.py`.

### 1. Авторизация

Первым делом необходимо авторизоваться. Ваши учетные данные (токен и домен) будут сохранены в файл `auth.json`, который игнорируется системой контроля версий.

```bash
venv\Scripts\python.exe main.py login --domain <домен> --username <логин> --password <пароль>
```
*   `--domain`: Ваш домен в системе FusionPOS (например, `mycompany` из `mycompany.fusionpos.ru`).
*   `--username`: Ваш логин.
*   `--password`: Ваш пароль.

### 2. Команды для работы с клиентами

#### Получить всех клиентов
```bash
venv\Scripts\python.exe main.py get-clients
```

#### Получить одного клиента по ID
```bash
venv\Scripts\python.exe main.py get-client --id <ID клиента>
```

#### Добавить нового клиента
**Важно:** `--id_network` и `--id_group` являются обязательными.
```bash
venv\Scripts\python.exe main.py add-client --name <имя> --id_network <ID сети> --id_group <ID группы> [другие опции]
```
*   Пример с дополнительными опциями:
    ```bash
    venv\Scripts\python.exe main.py add-client --name "Иван" --lastname "Петров" --phone "79991234567" --id_network 1 --id_group 10
    ```

#### Обновить клиента
Нужно указать ID клиента и хотя бы одно поле для обновления.
```bash
venv\Scripts\python.exe main.py update-client --id <ID клиента> --name "НовоеИмя" --phone "79997654321"
```

#### Удалить клиента
```bash
venv\Scripts\python.exe main.py delete-client --id <ID клиента>
```

#### Пополнить баланс клиента
```bash
venv\Scripts\python.exe main.py refill-client --id <ID клиента> --amount <сумма> --comment "Комментарий к пополнению"
```

#### Получить список доступных действий
```bash
venv\Scripts\python.exe main.py get-client-actions
```
_Эта команда возвращает список действий, настроенных для клиентов в вашей системе FusionPOS. Если результат — пустой список `[]`, это означает, что в системе не настроено никаких специальных действий._

## План разработки

Статус реализации всех эндпоинтов API можно отслеживать в файле [TODO.md](TODO.md).
