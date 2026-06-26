# Universal File Extractor

Универсальный инструмент для извлечения файлов из текстовых шаблонов с поддержкой комментариев.

## 📋 Описание

extract.py распаковывает файлы из текстовых шаблонов, распознавая маркеры start_my_file/end_my_file с комментариями. Поддерживает 30+ форматов файлов.

## 🚀 Быстрый старт

Скачать скрипт:
wget https://raw.githubusercontent.com/yourusername/file-extractor/main/extract.py

Запустить:
python extract.py

## 📖 Использование

python extract.py [SOURCE_FILE] [OPTIONS]

Опции:
- SOURCE_FILE - файл с шаблоном (по умолчанию: template.txt)
- -o, --output PATH - директория для извлечения (по умолчанию: ./extracted_files)
- -y, --yes - автоматическое согласие
- -v, --verbose - подробный вывод
- -h, --help - справка

Примеры:
python extract.py                    # Интерактивный режим
python extract.py my_template.txt    # Указать файл
python extract.py -o ./output        # Указать выходную папку
python extract.py -y                 # Автоматический режим

## 📝 Формат шаблонов

Простой формат:
start_my_file file.txt
Content
end_my_file file.txt

С комментариями (рекомендуется):

Python:
# start_my_file script.py
print("Hello")
# end_my_file script.py

JavaScript:
// start_my_file app.js
console.log("Hello");
// end_my_file app.js

HTML:
<!-- start_my_file index.html -->
<html>...</html>
<!-- end_my_file index.html -->

CSS:
/* start_my_file style.css */
body { color: red; }
/* end_my_file style.css */

SQL:
-- start_my_file query.sql
SELECT * FROM users;
-- end_my_file query.sql

INI:
; start_my_file config.ini
[Settings]
debug = true
; end_my_file config.ini

## 🔧 Поддерживаемые форматы

| Тип | Расширения | Стиль комментариев |
|-----|------------|-------------------|
| Python, Shell | .py, .sh, .bash | # |
| JS, TS, Java, C/C++ | .js, .ts, .java, .c, .cpp | // |
| HTML, XML | .html, .xml, .svg | <!-- --> |
| CSS, SCSS | .css, .scss | /* */ |
| SQL | .sql | -- |
| INI, YAML, TOML | .ini, .yml, .toml | ; или # |

## 📁 Структура проекта

file-extractor/
├── extract.py          # Основной скрипт
├── README.md           # Документация
├── LICENSE             # Лицензия
├── .gitignore          # Игнорируемые файлы
├── examples/           # Примеры шаблонов
└── tests/              # Тесты

## 🐛 Решение проблем

"No file blocks found!" - проверьте наличие маркеров start_my_file/end_my_file

"File not found" - проверьте путь к файлу

Маркеры не распознаются - используйте один из форматов:
start_my_file file.ext
# start_my_file file.ext
// start_my_file file.ext
<!-- start_my_file file.ext -->
/* start_my_file file.ext */
-- start_my_file file.ext
; start_my_file file.ext

## 🧪 Тестирование

Создать тестовый шаблон:
echo '# start_my_file hello.txt\nHello World!\n# end_my_file hello.txt' > test.txt

Запустить извлечение:
python extract.py test.txt -o ./output

Проверить результат:
cat ./output/hello.txt

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку (git checkout -b feature/amazing)
3. Закоммитьте изменения (git commit -m 'Add feature')
4. Отправьте в форк (git push origin feature/amazing)
5. Откройте Pull Request

## 📄 Лицензия

MIT License

## 📞 Контакты

- Автор: Виктор Макаров
- Email: vmakarov.kzn@gmail.com
- GitHub: @VikM78

---

⭐ Поставьте звезду, если проект полезен!
