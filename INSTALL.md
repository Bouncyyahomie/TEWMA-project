## Getting Started

|    Name    | Required version(s) |
| :--------: | :-----------------: |
|   Python   |   3.7 or higher     |
|   Django   |   3.1 or higher     |

If you use Linux/MacOS your command is  `python3` `pip3`, on other systems just `python` and `pip`.

## Update your `pip` command.
```
python -m pip install --upgrade pip
```

## Install virtualenv
```
python -m pip install virtualenv
```
## Installation Steps
1. clone this repo to your computer.
    ```
    git clone https://github.com/Bouncyyahomie/TEWMA-project.git
    ```
2. change your directory into project's directory.
    ```
    cd /some/directory/TEWMA-project
    ```

3. Create a virtualenv directory named `env` inside the project directory.
    ```
    virtualenv env
    ```
4. Activate the virtualenv using the activate script.
    For Window OS
    ```
    env\Scripts\activate
    ```
    For MacOs and Linux
    ```bash
    .  env/bin/activate
    ```
    or
    ```bash
    source venv/bin/activate
    ```

5. run this command to install all require packages.
    ``` 
    pip install -r requirements.txt
    ```
6. run this command to migrate the database.
    ```
    python manage.py migrate
    ```
7. run this command to create a sample user.
    ```
    python manage.py loaddata users.json
    ```
8. Login to TEWMA tutoring web application using demo account   
    **Username:** sample1   
    **Password:** isp123456

7. start running the server by this command.
    ```
    python manage.py runserver
     ```
8. Exit the virtualenv using `deactivate`.
    ```
    deactivate
    ```
