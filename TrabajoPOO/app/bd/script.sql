
-- CREACIÓN DE BASE DE DATOS
CREATE DATABASE IF NOT EXISTS concesionaria;
USE concesionaria;

-- ==========================================
-- TABLA: persona 
-- Base para empleados y gerentes
DROP TABLE IF EXISTS persona;
CREATE TABLE persona (
    idPersona INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    email VARCHAR(80)
);

-- ==========================================
-- TABLA: empleado 
-- Hereda de persona
DROP TABLE IF EXISTS empleado;

CREATE TABLE empleado (
    idEmpleado INT AUTO_INCREMENT PRIMARY KEY,
    idPersona INT NOT NULL,
    fechaInicio DATE NOT NULL,
    salario FLOAT NOT NULL,
    departamento VARCHAR(50),

    FOREIGN KEY (idPersona) REFERENCES persona(idPersona)
);

-- ==========================================
-- TABLA: gerente
-- Hereda de empleado
DROP TABLE IF EXISTS gerente;

CREATE TABLE gerente (
    idGerente INT PRIMARY KEY,
    departamentoACargo VARCHAR(50),
    FOREIGN KEY (idGerente) REFERENCES empleado(idEmpleado)
);

-- ==========================================
-- TABLA: departamento
-- Tiene asociado un gerente
DROP TABLE IF EXISTS departamento;

CREATE TABLE departamento (
    idDepartamento INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    idGerente INT,

    FOREIGN KEY (idGerente) REFERENCES gerente(idGerente)
);

-- ==========================================
-- TABLA: proyecto
-- Asociado a un departamento
DROP TABLE IF EXISTS proyecto;

CREATE TABLE proyecto (
    idProyecto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT,
    idDepartamento INT,

    FOREIGN KEY (idDepartamento) REFERENCES departamento(idDepartamento)
);

-- ==========================================
-- TABLA: registro_tiempo
-- Para registrar horas trabajadas
DROP TABLE IF EXISTS registro_tiempo;

CREATE TABLE registro_tiempo (
    idRegistro INT AUTO_INCREMENT PRIMARY KEY,
    idEmpleado INT NOT NULL,
    idProyecto INT NOT NULL,
    fecha DATE NOT NULL,
    horasTrabajadas FLOAT NOT NULL,
    descripcion TEXT,

    FOREIGN KEY (idEmpleado) REFERENCES empleado(idEmpleado),
    FOREIGN KEY (idProyecto) REFERENCES proyecto(idProyecto)
);

-- ==========================================
-- INSERTS OPCIONALES DE DATOS INICIALES

-- Personas (ejemplo)
INSERT INTO persona (nombre, apellido, telefono, email)
VALUES 
('Juan', 'Soto', '99999999', 'juan@mail.com'),
('Ana', 'Pérez', '88888888', 'ana@mail.com'),
('Carlos', 'López', '77777777', 'carlos@mail.com');

-- Empleados base
INSERT INTO empleado (idPersona, fechaInicio, salario, departamento)
VALUES
(1, '2020-01-10', 850000, 'Ventas'),
(2, '2021-03-15', 950000, 'TI'),
(3, '2022-07-01', 700000, 'Marketing');

-- Gerente (Carlos)
INSERT INTO gerente (idGerente, departamentoACargo)
VALUES (3, 'Marketing');

-- Departamentos
INSERT INTO departamento (nombre, idGerente)
VALUES
('Ventas', NULL),
('TI', NULL),
('Marketing', 3);

-- Proyectos
INSERT INTO proyecto (nombre, descripcion, idDepartamento)
VALUES
('Sistema de Ventas', 'Desarrollo de sistema interno', 2),
('Campaña 2025', 'Publicidad global', 3);

-- Registros de tiempo
INSERT INTO registro_tiempo (idEmpleado, idProyecto, fecha, horasTrabajadas, descripcion)
VALUES
(1, 1, '2024-01-10', 5, 'Diseño inicial'),
(2, 1, '2024-02-01', 8, 'Implementación backend'),
(3, 2, '2024-02-05', 6, 'Reunión con clientes');