# RecSys

1. Подготовить датасеты:
    - Открыть фаил src/notebooks/distances.ipynb
    - Запустить задание 1. Если требуется поправить (или указать прямой путь до датасетов) в папке datasets
    - Запустить задание 2.
    - Запустить задание 3. Если требуется поправить (или указать прямой путь) для записи датасетов в 
    паку assets

2. После этого настроить переменные окружения:
    - Создать фаил c расширением .env:
        В нем создать:
        * MOVIES= указать путь до movies.csv
        * DISTANCE= указать путь до distance.csv
        * API_KEY= для получения API зарегистрироватьс на сайте [OMDb API](https://www.omdbapi.com/)

В фаиле app.py если требуется поправляем или указываем прямой путь до:
    - file = open("..\\misc\\images\\cinema.gif", "rb")
    - file_2 = open("..\\misc\\images\\prog.gif", "rb")

3. Запуск сервиса:
    Создаем терминал.
    cd ./src/
    pip install -r requirements.txt
    streamlit run app.py

_________________________________________________________________________________________________________________________

# RecSys

1. Prepare datacets:
- Open file src/notebooks/distances.ipynb
- Run Job 1. If you want to correct (or specify a direct path to datasets) in the datasets folder
- Run Job 2.
- Run Job 3. If you want to correct (or specify a direct path) to record datacets in
pack assets

2. Then configure the environment variables:
- Create file with .env extension:
In it create:
* MOVIES = specify path to movies.csv
* DISTANCE = specify path to distance.csv
* API_KEY= register with [OMDb API] to receive API (https://www.omdbapi.com/)

In the file app.py if necessary, we correct or indicate a direct path to:
- file = open("..\\misc\\images\\cinema.gif", "rb")
- file_2 = open("..\\misc\\images\\prog.gif", "rb")

3. Service Launch:
We create a terminal.
cd ./src/
pip install -r requirements.txt
streamlit run app.py