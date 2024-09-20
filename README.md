# UI-тест 
Тестирование заказа на www.saucedemo.com/

## Тест содержит:
 - 3 тестовых маршрута `./__tests__/` с файлами для тестирования
 - 2 FW - `pytest`, `playwright`.
 - В кучестве установщика библиотек используется `Poetry`. 
   - `requirements.txt` результат авто-сборки  от `Poetry`.
 - Config-файлы для проверки кода 
   - `.pre-commit-config.yaml`,
   - `.flake8`,
   - '.pylintrc'. Часть из этих правил игнорируются (особенности \
   синтаксиса тестаю ).
   -  и команды представленные ниже

Данный тест построен на принципе,  каждый следующий файл берет данные \
из предыдущего.  
Note: Исправление логики теста может повредить все остальные тесты. 



## Команды
Команды представленные ниже подразумевают, что у вы клонировали репозиторий и \
установили библиотеки. Установщик на ваш выбор.

### Запуск всех тестов
```text
pytest __tests__/
```
### Запуск отдельно взятого файла
```text
pytest __tests__/tests_cart_for_buy/test_rewrite_fields.py
```

### Запуск 'git commit'
Запуск данной команды приводит к запуску автоматической проверке \
стиля написания кода.\
`--no-verify` Если правила надо проигнорировать. Например \
```text
git commit -am "your commit" --no-verify
```

## О тестах
### tests_main_page
Тестируется форма авторизации, на главной странице. \
```python
from __tests__.dotenv_ import TEST_HOST, TEST_LOGIN, TEST_PASSWORD
testdata = [
    (TEST_LOGIN, TEST_PASSWORD, "0", True),
    (" ", TEST_PASSWORD, "1", False),
    (TEST_LOGIN, " ", "2", False),
    (" ", " ", "3", False),
    # .....
]
```
- Ожидаемый ответ (`True`/`False`) теста с текущим набором данных. 
- `testdata` варианты данных для тестирования. Шаблоны данных описываются в \
основной функции теста. Например `test_autorization_form_group`.

### tests_inventory_page
На странице `/inventory.html` выбираем одну из позиций и тестируем клики для \
перехода в корзину. Плюс добавление.
- Варианты набора данных `inventory_testdata` не имеет конечного ожидаемого \
ответа. Если в консоли не видим ошибку - тест пройден и на оборот.

### tests_cart_for_buy
Имеет 2 тестовых файла.

#### test_views.py
Тестируем поля формы для оформления заказа. 
- `buy_testdata` имеет ожидаемый ответ (`True`/`False`) теста.

В `buy_testdata` верные (якобы) данные представлены в `buy_testdata[0]`.\
Далее намерено внесены ошибки. \
Тест показал, что форма не имеет базовой валидации \
 `First Name` и `Last Name` могут иметь:
 - множества заглавных символов.
 - множество пробелов в именах
 - различные символы
 - и так далее если бы были известны условия проверки данных \
которых придерживается проект для внесения данных в db.

### test_rewrite_fields.py
Зависимость на `test_views.py`.
Дважды заполняем форму:
1. оставляем `First Name` пустым.
2. `First Name` заполняем корректно.

Цель теста это вызвать ошибку при нажатии на кнопку `Conrinue`, якобы \
создать заказ. и проверить  - создадим заказ после исправления ошибки или нет.

## Итого
Вариаций действий/событий для совершения заказа полно. Вопрос  времени\
доступного для совершения заказа.

P.:S.: Вайлы с тестами можно сделать независимыми. Приведет к \
дублированию строк кода и параметров. 