-- ==========================================
-- RESETEAR BASE DE DATOS COMPLETA
-- ==========================================

DROP DATABASE IF EXISTS concesionaria;
CREATE DATABASE concesionaria;
USE concesionaria;

-- ==========================================
-- TABLA: persona
-- ==========================================
CREATE TABLE persona (
    idPersona INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    email VARCHAR(80)
);

-- ==========================================
-- TABLA: departamento
-- (se crea ANTES que empleado y gerente)
-- ==========================================
CREATE TABLE departamento (
    idDepartamento INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    idGerente INT
);

-- ==========================================
-- TABLA: empleado
-- (empleado.departamento = idDepartamento)
-- ==========================================
CREATE TABLE empleado (
    idEmpleado INT AUTO_INCREMENT PRIMARY KEY,
    idPersona INT NOT NULL,
    fechaInicio DATE NOT NULL,
    salario FLOAT NOT NULL,
    departamento INT,

    FOREIGN KEY (idPersona) REFERENCES persona(idPersona)
        ON DELETE CASCADE ON UPDATE CASCADE,

    FOREIGN KEY (departamento) REFERENCES departamento(idDepartamento)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- ==========================================
-- TABLA: gerente
-- (idGerente = idEmpleado)
-- (departamentoACargo = idDepartamento)
-- ==========================================
CREATE TABLE gerente (
    idGerente INT PRIMARY KEY,
    departamentoACargo INT,

    FOREIGN KEY (idGerente) REFERENCES empleado(idEmpleado)
        ON DELETE CASCADE ON UPDATE CASCADE,

    FOREIGN KEY (departamentoACargo) REFERENCES departamento(idDepartamento)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- Ahora que gerente ya existe, ponemos FK en departamento
ALTER TABLE departamento
ADD CONSTRAINT fk_dep_ger
FOREIGN KEY (idGerente) REFERENCES gerente(idGerente)
    ON DELETE SET NULL ON UPDATE CASCADE;

-- ==========================================
-- TABLA: proyecto
-- ==========================================
CREATE TABLE proyecto (
    idProyecto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT,
    idDepartamento INT,

    FOREIGN KEY (idDepartamento) REFERENCES departamento(idDepartamento)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- ==========================================
-- TABLA: registro_tiempo
-- ==========================================
CREATE TABLE registro_tiempo (
    idRegistro INT AUTO_INCREMENT PRIMARY KEY,
    idEmpleado INT NOT NULL,
    idProyecto INT NOT NULL,
    fecha DATE NOT NULL,
    horasTrabajadas FLOAT NOT NULL,
    descripcion TEXT,

    FOREIGN KEY (idEmpleado) REFERENCES empleado(idEmpleado)
        ON DELETE CASCADE ON UPDATE CASCADE,

    FOREIGN KEY (idProyecto) REFERENCES proyecto(idProyecto)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ==========================================
-- DATOS INICIALES
-- ==========================================

INSERT INTO persona (nombre, apellido, telefono, email)
VALUES
('Juan', 'Soto', '99999999', 'juan@mail.com'),
('Ana', 'Pérez', '88888888', 'ana@mail.com'),
('Carlos', 'López', '77777777', 'carlos@mail.com');

INSERT INTO departamento (nombre)
VALUES
('Ventas'),      -- ID 1
('TI'),          -- ID 2
('Marketing');   -- ID 3

INSERT INTO empleado (idPersona, fechaInicio, salario, departamento)
VALUES
(1, '2020-01-10', 850000, 1),
(2, '2021-03-15', 950000, 2),
(3, '2022-07-01', 700000, 3);

INSERT INTO gerente (idGerente, departamentoACargo)
VALUES (3, 3);

UPDATE departamento SET idGerente = 3 WHERE idDepartamento = 3;

INSERT INTO proyecto (nombre, descripcion, idDepartamento)
VALUES
('Sistema de Ventas', 'Desarrollo de sistema interno', 2),
('Campaña 2025', 'Publicidad global', 3);

INSERT INTO registro_tiempo (idEmpleado, idProyecto, fecha, horasTrabajadas, descripcion)
VALUES
(1, 1, '2024-01-10', 5, 'Diseño inicial'),
(2, 1, '2024-02-01', 8, 'Implementación backend'),
(3, 2, '2024-02-05', 6, 'Reunión con clientes');
