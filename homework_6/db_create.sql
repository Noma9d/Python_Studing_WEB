
DROP table IF EXISTS [groups];
create table if not exists [groups] (
    id INTEGER primary key AUTOINCREMENT NOT NULL,
    name varchar(30)
);

DROP table IF EXISTS students;
create table if not exists students (
    id INTEGER primary key AUTOINCREMENT NOT NULL,
    name varchar(30),
    id_group INTEGER,
    FOREIGN key (id_group) references [groups](id)
        on delete set null
        ON UPDATE CASCADE
);

DROP table IF EXISTS teachers;
create table if not exists teachers (
    id INTEGER primary key AUTOINCREMENT NOT NULL,
    name varchar(30)
);

DROP table IF EXISTS items;
create table if not exists items (
    id INTEGER primary key AUTOINCREMENT NOT NULL,
    name varchar(30),
    id_teacher INTEGER,
    FOREIGN key (id_teacher) references teachers(id)
        on delete set null
        on UPDATE CASCADE
);

DROP table IF EXISTS grades;
create table if not exists grades (
    id INTEGER primary key AUTOINCREMENT NOT NULL,
    id_students INTEGER,
    id_items INTEGER,
    grade INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN key (id_students) references students(id)
        on delete set null
        on UPDATE CASCADE
    FOREIGN key (id_items) references items(id)
        on delete set null
        on UPDATE CASCADE
);