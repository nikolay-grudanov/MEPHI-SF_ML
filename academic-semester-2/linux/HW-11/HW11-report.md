# Домашняя работа № 11

**Выполнил:** Груданов Николай Алексеевич

---


## Выполнение работы

![alt text](image.png)

#### 1.1 Запуск всех виртуальных машин
```bash
vagrant up
```
![alt text](image-1.png)

![alt text](image-2.png)

#### 1.2 Проверка статуса после запуска
```bash
vagrant status
```
![alt text](image-3.png)

---

### 2. Проверка VM1

#### 2.1 Подключение к VM1 и проверка установленных пакетов

```bash
vagrant ssh vm1
```
![alt text](image-4.png)

![alt text](image-5.png)

```bash
dpkg -l | grep ubuntu-desktop-minimal
which chromium-browser
snap list | grep store
```
![alt text](image-6.png)

#### 2.2 Проверка службы Xrdp

```bash
sudo systemctl status xrdp
```
![alt text](image-7.png)

```bash
ss -tnlp | grep 3389
```
![alt text](image-8.png)


### 3. Проверка VM2 - Docker и WireGuard

#### 3.1 Подключение к VM2 и проверка Docker

```bash
vagrant ssh vm2
```
![alt text](image-9.png)

![alt text](image-10.png)

```bash
docker --version
sudo systemctl status docker
sudo systemctl status docker
```
![alt text](image-11.png)

#### 3.2 Проверка WireGuard tools

```bash
which wg
wg --version
```
![alt text](image-13.png)


#### 3.3 Проверка WireGuard UI контейнера

```bash
docker ps | grep wg-ui
docker logs wg-ui
```
![alt text](image-14.png)

#### 3.4 Проверка доступа к WireGuard UI через браузер

![alt text](image-15.png)

![alt text](image-16.png)

![alt text](image-17.png)

---

### 4. Проверка VM3 - Пользователь adam

#### 4.1 Подключение к VM3 и проверка пользователя adam

```bash
vagrant ssh vm3
```
![alt text](image-18.png)

```bash
id adam
getent passwd adam
```

![alt text](image-19.png)

#### 4.2 Проверка домашней директории и оболочки

```bash
grep adam /etc/passwd
```
![alt text](image-20.png)

#### 4.3 Проверка первичной группы adam
```bash
groups adam
getent group adam
```
![alt text](image-21.png)

---


