-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 16-09-2025 a las 16:47:33
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `sitex_prueba`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `descargues`
--

CREATE TABLE `descargues` (
  `idDescargue` int(11) NOT NULL,
  `idEmpleados` int(11) NOT NULL,
  `medida_inicial_cm` decimal(10,2) DEFAULT NULL,
  `medida_inicial_gl` decimal(10,2) DEFAULT NULL,
  `descargue_cm` decimal(10,2) DEFAULT NULL,
  `descargue_gl` decimal(10,2) DEFAULT NULL,
  `medida_final_cm` decimal(10,2) DEFAULT NULL,
  `medida_final_gl` decimal(10,2) DEFAULT NULL,
  `diferencia` decimal(10,2) DEFAULT NULL,
  `tanque` varchar(50) DEFAULT NULL,
  `observaciones1` varchar(255) DEFAULT NULL,
  `observaciones2` varchar(255) DEFAULT NULL,
  `kit_derrames` varchar(5) DEFAULT NULL,
  `extintores` varchar(5) DEFAULT NULL,
  `conos` varchar(5) DEFAULT NULL,
  `boquillas` varchar(5) DEFAULT NULL,
  `botas` varchar(5) DEFAULT NULL,
  `gafas` varchar(5) DEFAULT NULL,
  `tapaoidos` varchar(5) DEFAULT NULL,
  `guantes` varchar(5) DEFAULT NULL,
  `brillante` varchar(5) DEFAULT NULL,
  `traslucido` varchar(5) DEFAULT NULL,
  `claro` varchar(5) DEFAULT NULL,
  `solidos` varchar(5) DEFAULT NULL,
  `separacion` varchar(50) DEFAULT NULL,
  `fecha` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `descargues`
--

INSERT INTO `descargues` (`idDescargue`, `idEmpleados`, `medida_inicial_cm`, `medida_inicial_gl`, `descargue_cm`, `descargue_gl`, `medida_final_cm`, `medida_final_gl`, `diferencia`, `tanque`, `observaciones1`, `observaciones2`, `kit_derrames`, `extintores`, `conos`, `boquillas`, `botas`, `gafas`, `tapaoidos`, `guantes`, `brillante`, `traslucido`, `claro`, `solidos`, `separacion`, `fecha`) VALUES
(8, 2, 21455.00, 125.00, 5625.00, 1255.00, 1255.00, 455.00, 25.00, 'Tanque 1', 'perfecto', 'perfecto', 'si', 'si', 'si', 'si', 'si', 'si', 'si', 'si', 'no', 'no', 'si', 'no', '', '2025-08-26');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `documento`
--

CREATE TABLE `documento` (
  `idDocumento` int(11) NOT NULL,
  `nombre_documento` varchar(100) DEFAULT NULL,
  `fecha_informe` date DEFAULT NULL,
  `tipo_documento_informe` varchar(45) DEFAULT NULL,
  `tipo_medicion` varchar(45) DEFAULT NULL,
  `fecha_descargue` date DEFAULT NULL,
  `id_empleado` varchar(45) DEFAULT NULL,
  `idEmpleados` int(11) DEFAULT NULL,
  `revision_vehiculo` varchar(3) DEFAULT NULL,
  `revision_conductor` varchar(3) DEFAULT NULL,
  `medida_inicial` varchar(45) DEFAULT NULL,
  `cantidad_descargue` varchar(45) DEFAULT NULL,
  `medida_final` varchar(45) DEFAULT NULL,
  `diferencias` varchar(45) DEFAULT NULL,
  `idRegistro_medidas` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `documento`
--

INSERT INTO `documento` (`idDocumento`, `nombre_documento`, `fecha_informe`, `tipo_documento_informe`, `tipo_medicion`, `fecha_descargue`, `id_empleado`, `idEmpleados`, `revision_vehiculo`, `revision_conductor`, `medida_inicial`, `cantidad_descargue`, `medida_final`, `diferencias`, `idRegistro_medidas`) VALUES
(2, 'informe_medicion.txt', '2025-06-27', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `documento_adjunto`
--

CREATE TABLE `documento_adjunto` (
  `idAdjunto` int(11) NOT NULL,
  `idDocumento` int(11) DEFAULT NULL,
  `nombre_archivo` varchar(100) DEFAULT NULL,
  `url_archivo` text DEFAULT NULL,
  `fecha_subida` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `documento_historial`
--

CREATE TABLE `documento_historial` (
  `idHistorial` int(11) NOT NULL,
  `idDocumento` int(11) DEFAULT NULL,
  `fecha_evento` datetime DEFAULT NULL,
  `descripcion_evento` varchar(255) DEFAULT NULL,
  `usuario_responsable` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `documento_tipo`
--

CREATE TABLE `documento_tipo` (
  `idTipoDocumento` int(11) NOT NULL,
  `nombre_tipo` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleado`
--

CREATE TABLE `empleado` (
  `idEmpleados` int(11) NOT NULL,
  `nombre_empleado` varchar(20) DEFAULT NULL,
  `apellido_empleado` varchar(20) DEFAULT NULL,
  `numero_documento` varchar(20) DEFAULT NULL,
  `tipo_documento` varchar(20) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `telefono` varchar(15) DEFAULT NULL,
  `direccion` varchar(45) DEFAULT NULL,
  `cargo_establecido` varchar(45) DEFAULT NULL,
  `contrasena` varchar(255) DEFAULT NULL,
  `usuario` varchar(15) DEFAULT NULL,
  `temporal` tinyint(1) DEFAULT 1,
  `confirmado` tinyint(1) DEFAULT 0,
  `rol` varchar(20) DEFAULT 'usuario'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `empleado`
--

INSERT INTO `empleado` (`idEmpleados`, `nombre_empleado`, `apellido_empleado`, `numero_documento`, `tipo_documento`, `email`, `telefono`, `direccion`, `cargo_establecido`, `contrasena`, `usuario`, `temporal`, `confirmado`, `rol`) VALUES
(1, 'Camilo', 'Alarcon', '123456789', 'CC', 'camilo@correo.com', '3001234567', 'Calle Falsa 123', 'Islero', NULL, NULL, 0, 0, 'usuario'),
(2, 'Laura', 'Rodríguez', '987654321', 'CC', 'laura@correo.com', '3012345678', 'Carrera 10 #20-30', 'Islero', NULL, NULL, 0, 0, 'usuario'),
(3, 'Juan', 'Martínez', '112233445', 'CC', 'juan@correo.com', '3023456789', 'Av. Siempre Viva 742', 'Islero', NULL, NULL, 0, 0, 'usuario'),
(4, 'Sofía', 'Gómez', '556677889', 'CC', 'sofia@correo.com', '3034567890', 'Cl. 45 #12-34', 'Islero', NULL, NULL, 0, 0, 'usuario'),
(5, 'Nicolas', 'Pinzon Murcia', '1010101010', 'CE', 'nicolasfdpinzon885@gmail.com', '3142009909', 'Calle 61 a bis sur N 87f 44', 'Administracion', NULL, NULL, 0, 0, 'usuario'),
(6, 'larry', 'diaz', '12312321354', 'CC', 'larry@gmail.com', '32138858555', 'calle 76', 'islero', NULL, NULL, 0, 0, 'usuario'),
(7, 'tatiana', 'diaz', '30000', 'CE', 'tatis@gmail.com', '21323545547777', 'calle 45', 'islero', NULL, NULL, 0, 0, 'usuario'),
(8, 'luis', 'pinzon', '1000162', 'CE', 'nicolas@gmail.com', '314200', 'calle 61 a bis ', 'encargado', '$2b$12$fst4f/nChZ1.X2iKpdJ7NOKAWjayhqVo6wNVun4RNJCU6mjT29nw.', '1000162', 0, 0, 'usuario'),
(9, 'alejo', 'cifuentes', '888222', 'CC', 'alejo@gmail.com', '847236265', 'calle 132', 'islero', '$2b$12$y83C7nIh.3m8mwuiokbpd.4bIJLm/gz7/mW4Nia3qG/tM43JHSr5a', '888222', 0, 0, 'usuario'),
(10, 'alex', 'murcia', '11002202', 'CC', 'alex@gmail.com', '23123875', 'calle 2', 'admin', '$2b$12$NR0.oAz4CDRVpwTEdV6ROuIPqjL1psjxv6vKtJUVRPrzw3E/1bMfO', '11002202', 0, 0, 'usuario'),
(11, 'petri', 'salgado', '22345334444', 'CC', 'petri@gmail.com', '23123', 'calle tal', 'islero', '$2b$12$2X2dcbkEjZ497wuf.x9it.HRclFL/yAgCP4Y9sKFcCnBGqsnt9K/W', '232312543', 1, 0, 'usuario'),
(12, 'diego', 'aponte', '7284932782', 'CC', 'diego@gmail.com', '726389456732', 'calle sapo perro', 'admin', '$2b$12$jiGaTsbZJsJGI/74Ha8yaOQ6ZRTk9JrVK/gGcm2cUlFs4p.00xirO', '342344344', 1, 0, 'usuario'),
(13, 'wddwa', 'wdawda', '213123', 'CE', 'sdsa@gmail.com', '43432', 'dwqdw', 'islero', '$2b$12$h48kDShbX0CKR4DYkeuKze8LF9QUTga.0OI9Ff3KB0TNy5MUm1SlW', '34324', 1, 0, 'usuario'),
(14, 'fesfees', 'fewfse', '3424234567886', 'CC', 'oasdow@gmial.com', '2132131', 'fefwadw', 'admin', '$2b$12$xQjbBqF8/x3GX33u.xdXmeD1uiDS2iUCZBvbSUOfr0/9ckfrM22Qy', '452345234', 1, 0, 'usuario'),
(15, 'Aida Estefania', 'Fernández Zea', '1234567890', 'CC', 'stefy8464@gmail.com', '3555641558', 'calle 81', 'islero', '$2b$12$Zbxs2rZnJNyR5KvrVgjwWeJGlRQPsdyrlvSFv06Vt1nHW0khnEY4K', '1234567890', 0, 0, 'usuario'),
(16, 'Juan Camilo', 'Alarcón Rivas', '1109187505', 'CC', 'alarconrivasjuancamilo016@gmail.com', '3555641558', 'calle 81', 'admin', '$2b$12$MJIM5TJZJ.nLoWQpcE0VFeU3y5dPG9wURibhZpl1qhFBDyCkxboki', '1109187505', 0, 0, 'usuario'),
(17, 'Angela ', 'Acosta', '147258369', 'CC', 'agelita23@gmail.com', '3584968148', 'crra 115', 'admin', '$2b$12$S2Iu0rOaj04lZyfG9KxtL.bCb7qdXJFEjGb8OuIK4oyV/x2DTmLYK', '147258369', 0, 0, 'usuario');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inicio_de_sesion`
--

CREATE TABLE `inicio_de_sesion` (
  `userNumDoc` varchar(20) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `temporal` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `inicio_de_sesion`
--

INSERT INTO `inicio_de_sesion` (`userNumDoc`, `password`, `temporal`) VALUES
('1000162', '885', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inicio_de_sesion_has_empleado`
--

CREATE TABLE `inicio_de_sesion_has_empleado` (
  `idEmpleados` int(11) NOT NULL,
  `userNumDoc` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `medicion_cargue`
--

CREATE TABLE `medicion_cargue` (
  `idMedicion_cargue` int(11) NOT NULL,
  `idEmpleados` int(11) NOT NULL,
  `medicion_anterior` varchar(45) DEFAULT NULL,
  `medicion_posterior` varchar(45) DEFAULT NULL,
  `formato_de_entrega` varchar(45) DEFAULT NULL,
  `galones_totales` varchar(45) DEFAULT NULL,
  `fecha` datetime DEFAULT current_timestamp(),
  `idTanques` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedido_combustible`
--

CREATE TABLE `pedido_combustible` (
  `idPedido_Combustible` int(11) NOT NULL,
  `galones_acpm` varchar(45) DEFAULT NULL,
  `galones_corriente` varchar(45) DEFAULT NULL,
  `galones_extra` varchar(45) DEFAULT NULL,
  `total_galones` varchar(45) DEFAULT NULL,
  `idEmpleados` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registro_medidas`
--

CREATE TABLE `registro_medidas` (
  `idRegistro_medidas` int(11) NOT NULL,
  `medida_combustible` varchar(45) DEFAULT NULL,
  `idEmpleados` int(11) DEFAULT NULL,
  `fecha_hora_registro` datetime DEFAULT NULL,
  `galones` int(11) DEFAULT NULL,
  `idTanques` int(11) DEFAULT NULL,
  `tipo_medida` varchar(30) DEFAULT 'rutinario',
  `novedad` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registro_medidas_has_medicion_cargue`
--

CREATE TABLE `registro_medidas_has_medicion_cargue` (
  `idRegistro_medidas` int(11) NOT NULL,
  `idMedicion_cargue` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tanques`
--

CREATE TABLE `tanques` (
  `idTanques` int(11) NOT NULL,
  `tipo_combustible` varchar(45) DEFAULT NULL,
  `contenido` int(11) DEFAULT NULL,
  `capacidad_gal` decimal(10,2) NOT NULL,
  `volumen_m3` decimal(10,2) NOT NULL,
  `diametro_m` decimal(10,2) NOT NULL,
  `altura_m` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tanques`
--

INSERT INTO `tanques` (`idTanques`, `tipo_combustible`, `contenido`, `capacidad_gal`, `volumen_m3`, `diametro_m`, `altura_m`) VALUES
(1, 'Diesel', NULL, 6000.00, 22.71, 2.50, 4.63),
(2, 'Diesel', NULL, 12000.00, 45.42, 2.50, 9.25),
(3, 'ACPM', NULL, 12000.00, 45.42, 2.50, 9.25),
(4, 'Extra', NULL, 6000.00, 22.71, 2.50, 4.63);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas`
--

CREATE TABLE `ventas` (
  `idVenta` int(11) NOT NULL,
  `idTanque` int(11) DEFAULT NULL,
  `cantidad_galones` int(11) DEFAULT NULL,
  `fecha` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `descargues`
--
ALTER TABLE `descargues`
  ADD PRIMARY KEY (`idDescargue`),
  ADD KEY `fk_descargues_empleado` (`idEmpleados`);

--
-- Indices de la tabla `documento`
--
ALTER TABLE `documento`
  ADD PRIMARY KEY (`idDocumento`),
  ADD KEY `idEmpleados` (`idEmpleados`),
  ADD KEY `idRegistro_medidas` (`idRegistro_medidas`);

--
-- Indices de la tabla `documento_adjunto`
--
ALTER TABLE `documento_adjunto`
  ADD PRIMARY KEY (`idAdjunto`),
  ADD KEY `idDocumento` (`idDocumento`);

--
-- Indices de la tabla `documento_historial`
--
ALTER TABLE `documento_historial`
  ADD PRIMARY KEY (`idHistorial`),
  ADD KEY `idDocumento` (`idDocumento`);

--
-- Indices de la tabla `documento_tipo`
--
ALTER TABLE `documento_tipo`
  ADD PRIMARY KEY (`idTipoDocumento`);

--
-- Indices de la tabla `empleado`
--
ALTER TABLE `empleado`
  ADD PRIMARY KEY (`idEmpleados`);

--
-- Indices de la tabla `inicio_de_sesion`
--
ALTER TABLE `inicio_de_sesion`
  ADD PRIMARY KEY (`userNumDoc`);

--
-- Indices de la tabla `inicio_de_sesion_has_empleado`
--
ALTER TABLE `inicio_de_sesion_has_empleado`
  ADD PRIMARY KEY (`idEmpleados`,`userNumDoc`),
  ADD KEY `userNumDoc` (`userNumDoc`);

--
-- Indices de la tabla `medicion_cargue`
--
ALTER TABLE `medicion_cargue`
  ADD PRIMARY KEY (`idMedicion_cargue`),
  ADD KEY `idTanques` (`idTanques`),
  ADD KEY `fk_cargue_empleado` (`idEmpleados`);

--
-- Indices de la tabla `pedido_combustible`
--
ALTER TABLE `pedido_combustible`
  ADD PRIMARY KEY (`idPedido_Combustible`),
  ADD KEY `idEmpleados` (`idEmpleados`);

--
-- Indices de la tabla `registro_medidas`
--
ALTER TABLE `registro_medidas`
  ADD PRIMARY KEY (`idRegistro_medidas`),
  ADD KEY `idEmpleados` (`idEmpleados`),
  ADD KEY `idTanques` (`idTanques`);

--
-- Indices de la tabla `registro_medidas_has_medicion_cargue`
--
ALTER TABLE `registro_medidas_has_medicion_cargue`
  ADD PRIMARY KEY (`idRegistro_medidas`,`idMedicion_cargue`),
  ADD KEY `idMedicion_cargue` (`idMedicion_cargue`);

--
-- Indices de la tabla `tanques`
--
ALTER TABLE `tanques`
  ADD PRIMARY KEY (`idTanques`);

--
-- Indices de la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD PRIMARY KEY (`idVenta`),
  ADD KEY `idTanque` (`idTanque`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `descargues`
--
ALTER TABLE `descargues`
  MODIFY `idDescargue` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `documento`
--
ALTER TABLE `documento`
  MODIFY `idDocumento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `documento_adjunto`
--
ALTER TABLE `documento_adjunto`
  MODIFY `idAdjunto` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `documento_historial`
--
ALTER TABLE `documento_historial`
  MODIFY `idHistorial` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `documento_tipo`
--
ALTER TABLE `documento_tipo`
  MODIFY `idTipoDocumento` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `empleado`
--
ALTER TABLE `empleado`
  MODIFY `idEmpleados` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT de la tabla `medicion_cargue`
--
ALTER TABLE `medicion_cargue`
  MODIFY `idMedicion_cargue` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `pedido_combustible`
--
ALTER TABLE `pedido_combustible`
  MODIFY `idPedido_Combustible` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `registro_medidas`
--
ALTER TABLE `registro_medidas`
  MODIFY `idRegistro_medidas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT de la tabla `tanques`
--
ALTER TABLE `tanques`
  MODIFY `idTanques` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `ventas`
--
ALTER TABLE `ventas`
  MODIFY `idVenta` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `descargues`
--
ALTER TABLE `descargues`
  ADD CONSTRAINT `fk_descargues_empleado` FOREIGN KEY (`idEmpleados`) REFERENCES `empleado` (`idEmpleados`);

--
-- Filtros para la tabla `documento`
--
ALTER TABLE `documento`
  ADD CONSTRAINT `documento_ibfk_1` FOREIGN KEY (`idEmpleados`) REFERENCES `empleado` (`idEmpleados`),
  ADD CONSTRAINT `documento_ibfk_2` FOREIGN KEY (`idRegistro_medidas`) REFERENCES `registro_medidas` (`idRegistro_medidas`);

--
-- Filtros para la tabla `documento_adjunto`
--
ALTER TABLE `documento_adjunto`
  ADD CONSTRAINT `documento_adjunto_ibfk_1` FOREIGN KEY (`idDocumento`) REFERENCES `documento` (`idDocumento`);

--
-- Filtros para la tabla `documento_historial`
--
ALTER TABLE `documento_historial`
  ADD CONSTRAINT `documento_historial_ibfk_1` FOREIGN KEY (`idDocumento`) REFERENCES `documento` (`idDocumento`);

--
-- Filtros para la tabla `inicio_de_sesion_has_empleado`
--
ALTER TABLE `inicio_de_sesion_has_empleado`
  ADD CONSTRAINT `inicio_de_sesion_has_empleado_ibfk_1` FOREIGN KEY (`idEmpleados`) REFERENCES `empleado` (`idEmpleados`),
  ADD CONSTRAINT `inicio_de_sesion_has_empleado_ibfk_2` FOREIGN KEY (`userNumDoc`) REFERENCES `inicio_de_sesion` (`userNumDoc`);

--
-- Filtros para la tabla `medicion_cargue`
--
ALTER TABLE `medicion_cargue`
  ADD CONSTRAINT `fk_cargue_empleado` FOREIGN KEY (`idEmpleados`) REFERENCES `empleado` (`idEmpleados`),
  ADD CONSTRAINT `medicion_cargue_ibfk_1` FOREIGN KEY (`idTanques`) REFERENCES `tanques` (`idTanques`);

--
-- Filtros para la tabla `pedido_combustible`
--
ALTER TABLE `pedido_combustible`
  ADD CONSTRAINT `pedido_combustible_ibfk_1` FOREIGN KEY (`idEmpleados`) REFERENCES `empleado` (`idEmpleados`);

--
-- Filtros para la tabla `registro_medidas`
--
ALTER TABLE `registro_medidas`
  ADD CONSTRAINT `registro_medidas_ibfk_1` FOREIGN KEY (`idEmpleados`) REFERENCES `empleado` (`idEmpleados`),
  ADD CONSTRAINT `registro_medidas_ibfk_2` FOREIGN KEY (`idTanques`) REFERENCES `tanques` (`idTanques`);

--
-- Filtros para la tabla `registro_medidas_has_medicion_cargue`
--
ALTER TABLE `registro_medidas_has_medicion_cargue`
  ADD CONSTRAINT `registro_medidas_has_medicion_cargue_ibfk_1` FOREIGN KEY (`idRegistro_medidas`) REFERENCES `registro_medidas` (`idRegistro_medidas`),
  ADD CONSTRAINT `registro_medidas_has_medicion_cargue_ibfk_2` FOREIGN KEY (`idMedicion_cargue`) REFERENCES `medicion_cargue` (`idMedicion_cargue`);

--
-- Filtros para la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`idTanque`) REFERENCES `tanques` (`idTanques`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
