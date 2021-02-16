# Урок 6. Публикуем комиксы во Вконтакте

Скрипт ```main.py``` загружает случайный комикс с сайта [xkcd.com](https://xkcd.com/) в вашу группу [Вконтакте](https://vk.com). Также
добавляется комментарий к каждому комиксу.

### Как установить

У вас уже должен быть установлен Python 3. Если его нет, то установите.
Также нужно установить необходимые пакеты:
```
pip3 install -r requirements.txt
```

### Как пользоваться скриптом

Вам понадобится:

1. Для работы скрипта нужно создать файл ```.env``` в директории, где лежит скрипт.
2. Создайте группу Вконтакте, в которую будете выкладывать комиксы.
3. Для постинга на стену нужен ключ доступа пользователя. Чтобы его получить, нужно создать “standalone приложение”
   на странице [Вконтакте для разработчиков](https://vk.com/dev). 
4. Получите ключ доступа пользователя. Вам потребуются следующие права: photos, groups, wall и offline.
5. Вставьте ваш access_token в файл ```.env```:
    ```
    VK_PERSON_TOKEN='7485d674495fd9c9ad6c980f40085fad861bc85ae1780d8c880bdc98b3ab60546c05880d249ed3f7e2a46'
    ```
6. Получить group_id для вашей группы. Узнать group_id можно [здесь](https://regvk.com/id/).
7.  Вставьте ваш group_id в файл ```.env```:
    ```
    VK_GROUP_ID=202545869
    ```

### Запуск скрипта
Для запуска скрипта вам необходимо запустить командную строку и перейти в каталог со скриптом:
```
[путь_до_файла] python3 main.py 
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).