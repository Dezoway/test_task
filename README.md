# Документация

## Интерактивное меню программы
Меню программы реализовано в селективной форме, пользователю не нужно вводить команды. Навигация в меню осуществляется стрелками на клавиатуре.

### Первый запуск программы
При первом запуске программы в настройках необходимо добавить API ключ сервиса dadata, полученный в личном кабинете. При попытке получить координаты адреса с незаполненным\неверным API ключем программа будет выдавать ошибку подключения.

#### Настройки программы
В настройках программы доступны 3 функции:  
:one: Изменить URL адрес подключения API (не рекомендуется т.к. скрипт написан под конкретный функционал API)   
:two: Создать/изменить API ключ - при выборе данной команды на экране консоли будет показан текущий API ключ пользователя, а также приглашение к вводу нового API ключа.  
:three: Выбор языка ответа(по умолчанию ru) - язык на котором поступают ответы (в данном случае адреса) от сервиса dadata, при выборе en язык ответов сменится на английский


#### Получение координат адреса:house:
При валидном API ключе, после ввода пользователем адреса, будет доступен список из 20 доступных адресов. При выборе конкретного адреса программа выведет на экран координаты адреса(широта, долгота). После нажатия ENTER программа продолжит своё выполнение до выхода из неё.
