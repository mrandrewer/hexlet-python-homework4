insert into teachers (full_name, phone, email) values
('Иванова Светлана Валерьевна', '+79218764533', 'ivanovasv@yandex.ru'),
('Петров Виктор Александрович', '+79116543322', 'petrov-viktor@mail.ru'),
('Серебрякова Инна Леонидовна', '+79045878432', null),
('Коноплева Валерия Викторовна', null, 'konopleva1965@mail.ru');

insert into tests (teacher_id, name, content) values
(1, 'Задача 1', 'Создать игру кликер до 27.11.'),
(2, 'Задача 2', 'Создать приложение с подключением к БД.\nДобавить в приложение CRUD для таблицы Teachers на базе QSqlQueryModel до 2.12.'),
(3, 'Задача 3', 'Добавить в приложение CRUD для таблицы Test на базе QSqlTableModel до 9.12.'),
(3, 'Задача 4', 'Добавить в приложение CRUD для таблицы Test на базе QSqlRelationalTableModel до 16.12.');

insert into variants (teacher_id, title) values
(1, 'Вариант 1'),
(1, 'Вариант 2'),
(2, 'Вариант 3'),
(3, 'Вариант 4'),
(4, 'Вариант 5');
