# Universal File Extractor & Packer

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Комплект инструментов для упаковки и распаковки файлов в текстовые шаблоны с поддержкой множества стилей комментариев.

## 📋 Описание

Проект состоит из трех основных компонентов:

- **`config.py`** - централизованная конфигурация стилей комментариев для 100+ типов файлов
- **`extract.py`** - распаковывает файлы из текстового шаблона с маркерами `start_my_file`/`end_my_file`
- **`pack.py`** - упаковывает файлы из папки в один текстовый шаблон

Все стили комментариев вынесены в отдельный файл конфигурации, что упрощает их расширение и поддержку.

## 🚀 Быстрый старт

```bash
# Скачать все файлы
wget https://raw.githubusercontent.com/VikM78/file-extractor/main/config.py
wget https://raw.githubusercontent.com/VikM78/file-extractor/main/extract.py
wget https://raw.githubusercontent.com/VikM78/file-extractor/main/pack.py

# Распаковать шаблон
python extract.py template.txt -o ./project

# Упаковать проект
python pack.py ./project -o ./templates -n my_pack.txt
```

## 📖 Использование

### extract.py - Распаковка

```bash
python extract.py [SOURCE_FILE] [OPTIONS]
```

**Опции:**
- `SOURCE_FILE` - файл с шаблоном (по умолчанию: `template.txt`)
- `-o, --output PATH` - директория для извлечения (по умолчанию: `./extracted_files`)
- `-y, --yes` - автоматическое согласие
- `-v, --verbose` - подробный вывод
- `-h, --help` - справка

**Примеры:**
```bash
python extract.py                    # Интерактивный режим
python extract.py DATA1.txt          # Указать файл
python extract.py -o ./output        # Указать выходную папку
python extract.py -y                 # Автоматический режим
```

### pack.py - Упаковка

```bash
python pack.py [SOURCE_DIR] [OPTIONS]
```

**Опции:**
- `SOURCE_DIR` - папка с файлами (по умолчанию: `./ПАПКА`)
- `-o, --output PATH` - выходная папка (по умолчанию: `./output`)
- `-n, --name NAME` - имя выходного файла (по умолчанию: `DATA_compact.txt`)
- `-e, --exclude PATTERN` - исключить файлы по паттерну (можно использовать несколько раз)
- `-y, --yes` - автоматическое согласие
- `-v, --verbose` - подробный вывод
- `-h, --help` - справка

**Примеры:**
```bash
python pack.py                       # Упаковать из ./ПАПКА
python pack.py ./my_project          # Упаковать из ./my_project
python pack.py -o ./templates -n pack # Свои настройки
python pack.py -e "*.pyc" -e "*.log" # Исключить файлы
```

## 📝 Формат шаблонов

**Простой формат:**
```
start_my_file file.txt
Content
end_my_file file.txt
```

**С комментариями (автоматически определяется):**

Python:
```python
# start_my_file script.py
print("Hello")
# end_my_file script.py
```

JavaScript:
```javascript
// start_my_file app.js
console.log("Hello");
// end_my_file app.js
```

HTML:
```html
<!-- start_my_file index.html -->
<html>...</html>
<!-- end_my_file index.html -->
```

CSS:
```css
/* start_my_file style.css */
body { color: red; }
/* end_my_file style.css */
```

SQL:
```sql
-- start_my_file query.sql
SELECT * FROM users;
-- end_my_file query.sql
```

INI:
```ini
; start_my_file config.ini
[Settings]
debug = true
; end_my_file config.ini
```

Lua:
```lua
--[[ start_my_file script.lua ]]
print("Hello")
--[[ end_my_file script.lua ]]
```

Haskell:
```haskell
{- start_my_file Main.hs -}
main = putStrLn "Hello"
{- end_my_file Main.hs -}
```

## 🔧 Поддерживаемые форматы

| Тип | Расширения | Стиль комментариев |
|-----|------------|-------------------|
| **Python, Shell, Ruby** | `.py`, `.sh`, `.rb` | `# ` |
| **JS, TS, Java, C/C++** | `.js`, `.ts`, `.java`, `.c` | `// ` |
| **HTML, XML, SVG** | `.html`, `.xml`, `.svg` | `<!-- -->` |
| **CSS, SCSS** | `.css`, `.scss` | `/* */` |
| **SQL** | `.sql`, `.psql`, `.mysql` | `-- ` |
| **INI, YAML, TOML** | `.ini`, `.yml`, `.toml` | `; ` или `# ` |
| **Lua** | `.lua` | `-- ` |
| **Haskell** | `.hs` | `{- -}` |
| **Pascal** | `.pas`, `.dpr` | `{ }` |
| **LaTeX** | `.tex` | `% ` |
| **PowerShell** | `.ps1` | `# ` |
| **Batch** | `.bat`, `.cmd` | `:: ` |
| **Dockerfile** | `Dockerfile` | `# ` |
| **Makefile** | `Makefile` | `# ` |

Полный список поддерживаемых форматов можно найти и расширить в файле `config.py`.

## 📁 Структура проекта

```
file-extractor/
├── config.py            # Конфигурация стилей комментариев
├── extract.py           # Распаковка файлов
├── pack.py              # Упаковка файлов
├── README.md            # Документация
├── LICENSE              # Лицензия MIT
├── .gitignore           # Игнорируемые файлы
├── examples/            # Примеры использования
│   ├── sample_template.txt
│   └── sample_project/
│       ├── hello.py
│       ├── config.ini
│       └── index.html
└── tests/               # Тесты
    ├── test_extract.py
    └── test_pack.py
```

## 🔄 Рабочий процесс

### 1. Упаковка проекта

```bash
# Собрать все файлы из папки в один шаблон
python pack.py ./my_project -o ./templates -n project_backup.txt
```

### 2. Распаковка шаблона

```bash
# Извлечь все файлы из шаблона
python extract.py ./templates/project_backup.txt -o ./restored_project
```

### 3. Автоматизация

```bash
# Неинтерактивный режим
python pack.py ./src -o ./backup -y
python extract.py ./backup/DATA_compact.txt -o ./restore -y
```

## 🛠 Расширение конфигурации

Все стили комментариев хранятся в файле `config.py`. Чтобы добавить новый тип файла:

1. Откройте `config.py`
2. Добавьте запись в словарь `COMMENT_STYLES`:

```python
COMMENT_STYLES = {
    # ... существующие стили ...
    '.new_ext': ('/* ', ' */'),  # Новый формат
}
```

3. Для специальных файлов без расширения добавьте в `SPECIAL_FILES`:

```python
SPECIAL_FILES = {
    # ... существующие файлы ...
    'newfile': ('# ', '# '),
}
```

4. Для добавления нового паттерна распознавания в `extract.py` добавьте в `EXTRACT_PATTERNS`:

```python
EXTRACT_PATTERNS = [
    # ... существующие паттерны ...
    (r'^\s*NEW\s*start_my_file\s+(.+)$', r'^\s*NEW\s*end_my_file\s+(.+)$', 'new_style'),
]
```

## 🐛 Решение проблем

| Проблема | Решение |
|----------|---------|
| **"No file blocks found!"** | Проверьте наличие маркеров `start_my_file`/`end_my_file` |
| **"File not found"** | Проверьте путь к файлу или папке |
| **"Permission denied"** | Проверьте права на запись в папку |
| **Маркеры не распознаются** | Используйте поддерживаемый формат (см. список выше) |
| **Ошибка импорта config** | Убедитесь, что `config.py` находится в той же папке |

## 🧪 Тестирование

```bash
# Создать тестовый проект
mkdir test_project
echo "print('Hello')" > test_project/main.py
echo "debug=true" > test_project/config.ini

# Упаковать
python pack.py test_project -o ./test_output -n test_pack.txt

# Распаковать
python extract.py ./test_output/test_pack.txt -o ./test_restore

# Проверить
diff -r test_project test_restore
```

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку (`git checkout -b feature/amazing`)
3. Закоммитьте изменения (`git commit -m 'Add feature'`)
4. Отправьте в форк (`git push origin feature/amazing`)
5. Откройте Pull Request

## 📄 Лицензия

MIT License

## 📞 Контакты

| | |
|---|---|
| **Автор** | Виктор Макаров |
| **Email** | vmakarov.kzn@gmail.com |
| **GitHub** | [@VikM78](https://github.com/VikM78) |

---

⭐ **Поставьте звезду, если проект полезен!**
