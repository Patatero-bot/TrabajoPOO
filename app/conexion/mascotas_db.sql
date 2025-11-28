CREATE DATABASE IF NOT EXISTS mascotas_db;
USE mascotas_db;

create table mascota(
    id INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    edad INT NOT NULL,
    indicador VARCHAR(100)
);

INSERT INTO mascota VALUES(1,'Firulais',5,'Kiltro');
INSERT INTO mascota VALUES(2,'Misifu',3,'Blanco');

COMMIT;
