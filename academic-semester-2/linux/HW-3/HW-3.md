# Домашняя работа № 3

Выполнил: Груданов Николай Алексеевич

## Подготовка к выполнению

### 1. Запуск записи сеанса

Перед началом выполнения заданий запустим команду для записи сеанса:

```bash
script typescript.txt
```
![alt text](image.png)

![alt text](image-1.png)

## Часть 1: Управление пользователями и группами

### Задание 1: Переход в домашний каталог

```bash
cd ~
```
![alt text](image-2.png)

### Задание 2: Определение бюджета пользователя vagrant

```bash
cat /etc/passwd | grep vagrant
```

![alt text](image-3.png)

![alt text](image-4.png)


### Задание 3: Определение минимального возраста пароля

```bash
sudo cat /etc/shadow | grep vagrant
```
![alt text](image-5.png)

### Задание 4: Дата последнего изменения пароля

```bash
sudo passwd -S vagrant
```
![alt text](image-6.png)

### Задание 5: Создание пользователя user01

Созданим сначала группу 

```bash
sudo groupadd user01
```
После добавим туда нового пользователя

```bash
sudo useradd -d /home/user01 -s /bin/sh -g user01 -e 2026-12-13 -m user01
```
![alt text](image-8.png)


### Задание 6: Установка пароля пользователю user01
```bash
sudo passwd user01
```
![alt text](image-9.png)

### Задание 7: Вход под учетной записью user01

```bash
su user01
```

Введем пароль, который мы установили на предыдущем шаге.


### Задание 8: Проверка текущего пользователя
```bash
whoami
```
![alt text](image-10.png)

### Задание 9: Переход в домашний каталог и проверка содержимого
```bash
cd ~
pwd
ls -la
```
![alt text](image-11.png)

### Задание 10: Установка информации о пользователе
```bash
chfn
```
Команда запросит ввод полного имени, номера комнаты, рабочего и домашнего телефонов.

![alt text](image-12.png)

### Задание 11: Просмотр информации о пользователе
```bash
finger user01
```
![alt text](image-13.png)

### Задание 12: Выход из сеанса user01
```bash
exit
```
![alt text](image-14.png)

### Задание 13: Добавление user01 в группу sudo
```bash
sudo usermod -a -G sudo user01
```
![alt text](image-15.png)

### Задание 14: Повторный вход от имени user01
```bash
su user01
```
![alt text](image-16.png)

### Задание 15: Проверка прав sudo
```bash
sudo whoami
```
![alt text](image-17.png)

Вывело `root`, значит права sudo предоставлены корректно.

### Задание 16: Создание группы group01

```bash
sudo groupadd group01
```

![alt text](image-18.png)

### Задание 17: Добавление пользователей в группу group01

```bash
sudo usermod -a -G group01 user01
sudo usermod -a -G group01 vagrant
```
![alt text](image-19.png)

### Задание 18: Проверка членов группы

```bash
sudo groupmems -g group01 -l
```
![alt text](image-20.png)

### Задание 19: Выход из сеанса user01
```bash
exit
```
![alt text](image-21.png)
## Часть 2: Управление доступом к файлам и каталогам

### Задание 1: Переход в домашний каталог
```bash
cd ~
```
![alt text](image-22.png)

### Задание 2: Создание каталога test
```bash
mkdir test
cd test
```
![alt text](image-23.png)

![alt text](image-24.png)

### Задание 3: Создание файла и проверка прав
```bash
touch file
ls -l file
```
![alt text](image-25.png)

### Задание 4: Запрет всех действий с файлом
```bash
chmod 000 file
```
![alt text](image-26.png)

### Задание 5: Попытка записи в файл
```bash
echo "тест" > file
```
![alt text](image-27.png)

Видем ошибку "Permission denied".

### Задание 6: Попытка чтения файла
```bash
cat file
```
![alt text](image-28.png)

Видем ошибку "Permission denied".

### Задание 7: Установка прав только на запись для владельца
```bash
chmod 200 file
```
![alt text](image-29.png)

Видем `--w-------`, значит все применилось успешно

### Задание 8: Запись в файл и попытка чтения
```bash
echo "test" > file
```
![alt text](image-30.png)

```bash
cat file
```

![alt text](image-31.png)

Запись успешно, чтение -  ошибка.

### Задание 9: Разрешение чтения для группы

```bash
chmod 240 file
```

![alt text](image-32.png)

Видем `--w-r-----`, значит все применилось успешно

### Задание 10: Попытка чтения файла
```bash
cat file
```
![alt text](image-33.png)

Все еще   ошибка, так как у владельца нет права чтения.

### Задание 11: Разрешение чтения владельцу
```bash
chmod 640 file
```
![alt text](image-34.png)

### Задание 12: Чтение содержимого файла
```bash
cat file
```
![alt text](image-35.png)

### Задание 13: Создание каталога и файла в нем
```bash
mkdir dir
echo "file 2" > dir/new_file
```
![alt text](image-36.png)

### Задание 14: Просмотр содержимого каталога
```bash
ls -l dir
```
![alt text](image-37.png)

### Задание 15: Изменение прав каталога
```bash
chmod -x dir
cat dir/new_file
rm dir/new_file
```
![alt text](image-38.png)

Обе операции выдали ошибку "Permission denied".

### Задание 16: Попытка изменения владельца
```bash
chown root file
chgrp root file
```
![alt text](image-39.png)

Обе команды выдали ошибку, так как обычный пользователь не может изменить владельца.

### Задание 17: Установка umask для создания приватных файлов
```bash
umask 077
touch file1
ls -l file1
```
![alt text](image-40.png)

### Задание 18: Установка umask для полного доступа
```bash
umask 000
touch file2
ls -l file2
```
![alt text](image-41.png)

Права  `-rw-rw-rw-`

### Задание 19: Вход как root
```bash
sudo su
```
![alt text](image-42.png)

### Задание 20: Изменение владельца от имени root
```bash
chown root file
chmod 400 file
exit
```
![alt text](image-43.png)

### Задание 21: Попытка чтения файла обычным пользователем
```bash
cat file
```
![alt text](image-44.png)

### Задание 22: Предоставление прав группе от имени root
```bash
sudo su
chmod 440 file
exit
```
![alt text](image-45.png)

### Задание 23: Чтение файла обычным пользователем
```bash
cat file
```
![alt text](image-46.png)

## Создание итогового файла dz3.txt


```bash
cat /etc/passwd >> dz3.txt
cat /etc/group >> dz3.txt
```
![alt text](image-47.png)

## Завершение работы

```bash
exit
```

![alt text](image-48.png)