# Реализация скрипта для тестирования MTU в канале

## Пример запуска
```
docker build -t min-mtu . 
docker run -it --rm min-mtu --host ya.ru --v --timeout 1
```
Аргументы: 
- --host: Хост
- --v: Verbose mode
- --timeout: Максимальное время ожидания пакета