# Домашняя работа № 8

Выполнил: Груданов Николай Алексеевич

---

## Запуск записи сессии

```bash
script typescript.txt
```
![alt text](image.png)

## Выполнение базовых команд

### 1. Проверка DNS сервера Google

```bash
ping 8.8.8.8
```

![alt text](image-1.png)

### 2. Трассировка маршрута

```bash
traceroute 8.8.4.4
```

![alt text](image-2.png)

### 3. Определение сетевого адреса VM

```bash
ip a
```
![alt text](image-3.png)

### 4. MX-запись домена

```bash
nslookup -type=MX google.com
```
![alt text](image-4.png)

### 5. Сканирование портов

```bash
nmap -p22,80,443 localhost
```
![alt text](image-5.png)


### 6. Запрос DNS информации

```bash
dig @8.8.8.8 google.com
```
![alt text](image-6.png)

### 7. Захват сетевого трафика

```bash
sudo tcpdump > tcp.dump
```
![alt text](image-7.png)

![alt text](image-8.png)

## Настройка SSH

### 1. Проверка службы SSH

```bash
sudo systemctl is-active ssh
```
![alt text](image-9.png)


### 2. Создание SSH ключей

```bash
ssh-keygen
```

![alt text](image-10.png)

![alt text](image-11.png)

### 4. Настройка пользователя ubuntu

```bash
sudo su - ubuntu
mkdir -p ~/.ssh
vim ~/.ssh/authorized_keys
```

![alt text](image-12.png)

![alt text](image-13.png)

Выполняем на хосте

![alt text](image-14.png)

![alt text](image-15.png)

Скопируем весь вывод команды `cat ~/.ssh/id_ed25519.pub` и вставим в файл `authorized_keys` на виртуальной машине

![alt text](image-16.png)

### 5. Настройка прав доступа

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```
![alt text](image-17.png)

### 6. Создание резервной копии конфигурации

```bash
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup
```
![alt text](image-18.png)

### 7. Редактирование конфигурации SSH

```bash
sudo vim /etc/ssh/sshd_config
```
![alt text](image-19.png)

![alt text](image-21.png)


### 8. Перезапуск службы SSH

```bash
sudo systemctl restart ssh
```
![alt text](image-22.png)

### 9. Выход из VM

```bash
exit
```

![alt text](image-23.png)

### 10. Тестирование подключения с хоста с использованием ключа
```cmd
ssh -p 2222 -i ~/.ssh/id_ed25519 ubuntu@127.0.0.1
```
![alt text](image-24.png)

![alt text](image-25.png)


