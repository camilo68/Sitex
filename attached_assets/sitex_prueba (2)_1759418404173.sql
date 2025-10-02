-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 27-09-2025 a las 03:22:54
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
  `id_empleados` int(11) NOT NULL,
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
  `id_empleados` int(11) DEFAULT NULL,
  `revision_vehiculo` varchar(3) DEFAULT NULL,
  `revision_conductor` varchar(3) DEFAULT NULL,
  `medida_inicial` varchar(45) DEFAULT NULL,
  `cantidad_descargue` varchar(45) DEFAULT NULL,
  `medida_final` varchar(45) DEFAULT NULL,
  `diferencias` varchar(45) DEFAULT NULL,
  `id_registro_medidas` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  `id_empleados` int(11) NOT NULL,
  `nombre_empleado` varchar(30) DEFAULT NULL,
  `apellido_empleado` varchar(30) DEFAULT NULL,
  `numero_documento` varchar(20) DEFAULT NULL,
  `tipo_documento` varchar(20) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `telefono` varchar(15) DEFAULT NULL,
  `direccion` varchar(45) DEFAULT NULL,
  `cargo_establecido` varchar(45) DEFAULT NULL,
  `contrasena` varchar(255) DEFAULT NULL,
  `usuario` varchar(15) DEFAULT NULL,
  `temporal` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `empleado`
--

INSERT INTO `empleado` (`id_empleados`, `nombre_empleado`, `apellido_empleado`, `numero_documento`, `tipo_documento`, `email`, `telefono`, `direccion`, `cargo_establecido`, `contrasena`, `usuario`, `temporal`) VALUES
(1, 'Nicolas', 'Pinzon ', '1000162', 'CC', 'nicolas@gmail.com', '31420099', 'Calle 61 ', 'encargado', '$2b$12$KYGykidPIXY9PozThjIOQORIxGXiW4etl6j7gmsKp15mrqWeA7pCm', '1000162', 0),
(2, 'dayana', 'saenz', '1000885', 'CC', 'dayana@gmail.com', '3138746344', 'calle 10', 'admin', '$2b$12$xONs4FtlA5RjdnQ96hA0XuuNCyAs/P9QLWR1v8is1KIBKHTbr3LNa', '1000885', 0),
(3, 'camilo', 'alarcon', '100062666', 'CE', 'esclavo@gmail.com', '7372161223', 'calle escalva', 'islero', '$2b$12$rR6IpNqbuykaD4oW1fNrU.9nwJBkKTrFRI2DUoIZYEUCoNHdXl5ES', '100062666', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inicio_de_sesion`
--

CREATE TABLE `inicio_de_sesion` (
  `userNumDoc` varchar(20) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `temporal` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inicio_de_sesion_has_empleado`
--

CREATE TABLE `inicio_de_sesion_has_empleado` (
  `id_empleados` int(11) NOT NULL,
  `userNumDoc` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `medicion_cargue`
--

CREATE TABLE `medicion_cargue` (
  `id_medicion_cargue` int(11) NOT NULL,
  `medida_anterior` varchar(45) DEFAULT NULL,
  `medida_posterior` varchar(45) DEFAULT NULL,
  `formato_de_entrega` varchar(45) DEFAULT NULL,
  `galones_totales` varchar(45) DEFAULT NULL,
  `id_tanques` int(11) DEFAULT NULL
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
  `id_empleados` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registro_medidas`
--

CREATE TABLE `registro_medidas` (
  `id_registro_medidas` int(11) NOT NULL,
  `medida_combustible` varchar(45) DEFAULT NULL,
  `id_empleados` int(11) DEFAULT NULL,
  `fecha_hora_registro` datetime DEFAULT NULL,
  `galones` int(11) DEFAULT NULL,
  `id_tanques` int(11) DEFAULT NULL,
  `novedad` varchar(255) DEFAULT NULL,
  `tipo_medida` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registro_medidas_has_medicion_cargue`
--

CREATE TABLE `registro_medidas_has_medicion_cargue` (
  `id_registro_medidas` int(11) NOT NULL,
  `id_medicion_cargue` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tanques`
--

CREATE TABLE `tanques` (
  `id_tanques` int(11) NOT NULL,
  `tipo_combustible` varchar(45) DEFAULT NULL,
  `capacidad` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tanques`
--

INSERT INTO `tanques` (`id_tanques`, `tipo_combustible`, `capacidad`) VALUES
(1, 'Diesel', 6000),
(2, 'Diesel', 12000),
(3, 'ACPM', 12000),
(4, 'Extra', 6000);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas`
--

CREATE TABLE `ventas` (
  `idVenta` int(11) NOT NULL,
  `id_tanques` int(11) DEFAULT NULL,
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
  ADD KEY `fk_descargues_empleado` (`id_empleados`);

--
-- Indices de la tabla `documento`
--
ALTER TABLE `documento`
  ADD PRIMARY KEY (`idDocumento`),
  ADD KEY `id_empleados` (`id_empleados`),
  ADD KEY `id_registro_medidas` (`id_registro_medidas`);

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
  ADD PRIMARY KEY (`id_empleados`);

--
-- Indices de la tabla `inicio_de_sesion`
--
ALTER TABLE `inicio_de_sesion`
  ADD PRIMARY KEY (`userNumDoc`);

--
-- Indices de la tabla `inicio_de_sesion_has_empleado`
--
ALTER TABLE `inicio_de_sesion_has_empleado`
  ADD PRIMARY KEY (`id_empleados`,`userNumDoc`),
  ADD KEY `userNumDoc` (`userNumDoc`);

--
-- Indices de la tabla `medicion_cargue`
--
ALTER TABLE `medicion_cargue`
  ADD PRIMARY KEY (`id_medicion_cargue`),
  ADD KEY `id_tanques` (`id_tanques`);

--
-- Indices de la tabla `pedido_combustible`
--
ALTER TABLE `pedido_combustible`
  ADD PRIMARY KEY (`idPedido_Combustible`),
  ADD KEY `id_empleados` (`id_empleados`);

--
-- Indices de la tabla `registro_medidas`
--
ALTER TABLE `registro_medidas`
  ADD PRIMARY KEY (`id_registro_medidas`),
  ADD KEY `id_empleados` (`id_empleados`),
  ADD KEY `id_tanques` (`id_tanques`);

--
-- Indices de la tabla `registro_medidas_has_medicion_cargue`
--
ALTER TABLE `registro_medidas_has_medicion_cargue`
  ADD PRIMARY KEY (`id_registro_medidas`,`id_medicion_cargue`),
  ADD KEY `id_medicion_cargue` (`id_medicion_cargue`);

--
-- Indices de la tabla `tanques`
--
ALTER TABLE `tanques`
  ADD PRIMARY KEY (`id_tanques`);

--
-- Indices de la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD PRIMARY KEY (`idVenta`),
  ADD KEY `id_tanques` (`id_tanques`);

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
  MODIFY `id_empleados` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `medicion_cargue`
--
ALTER TABLE `medicion_cargue`
  MODIFY `id_medicion_cargue` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `pedido_combustible`
--
ALTER TABLE `pedido_combustible`
  MODIFY `idPedido_Combustible` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `registro_medidas`
--
ALTER TABLE `registro_medidas`
  MODIFY `id_registro_medidas` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tanques`
--
ALTER TABLE `tanques`
  MODIFY `id_tanques` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

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
  ADD CONSTRAINT `fk_descargues_empleado` FOREIGN KEY (`id_empleados`) REFERENCES `empleado` (`id_empleados`);

--
-- Filtros para la tabla `documento`
--
ALTER TABLE `documento`
  ADD CONSTRAINT `documento_ibfk_1` FOREIGN KEY (`id_empleados`) REFERENCES `empleado` (`id_empleados`),
  ADD CONSTRAINT `documento_ibfk_2` FOREIGN KEY (`id_registro_medidas`) REFERENCES `registro_medidas` (`id_registro_medidas`);

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
  ADD CONSTRAINT `inicio_de_sesion_has_empleado_ibfk_1` FOREIGN KEY (`id_empleados`) REFERENCES `empleado` (`id_empleados`),
  ADD CONSTRAINT `inicio_de_sesion_has_empleado_ibfk_2` FOREIGN KEY (`userNumDoc`) REFERENCES `inicio_de_sesion` (`userNumDoc`);

--
-- Filtros para la tabla `medicion_cargue`
--
ALTER TABLE `medicion_cargue`
  ADD CONSTRAINT `medicion_cargue_ibfk_1` FOREIGN KEY (`id_tanques`) REFERENCES `tanques` (`id_tanques`);

--
-- Filtros para la tabla `pedido_combustible`
--
ALTER TABLE `pedido_combustible`
  ADD CONSTRAINT `pedido_combustible_ibfk_1` FOREIGN KEY (`id_empleados`) REFERENCES `empleado` (`id_empleados`);

--
-- Filtros para la tabla `registro_medidas`
--
ALTER TABLE `registro_medidas`
  ADD CONSTRAINT `registro_medidas_ibfk_1` FOREIGN KEY (`id_empleados`) REFERENCES `empleado` (`id_empleados`),
  ADD CONSTRAINT `registro_medidas_ibfk_2` FOREIGN KEY (`id_tanques`) REFERENCES `tanques` (`id_tanques`);

--
-- Filtros para la tabla `registro_medidas_has_medicion_cargue`
--
ALTER TABLE `registro_medidas_has_medicion_cargue`
  ADD CONSTRAINT `registro_medidas_has_medicion_cargue_ibfk_1` FOREIGN KEY (`id_registro_medidas`) REFERENCES `registro_medidas` (`id_registro_medidas`),
  ADD CONSTRAINT `registro_medidas_has_medicion_cargue_ibfk_2` FOREIGN KEY (`id_medicion_cargue`) REFERENCES `medicion_cargue` (`id_medicion_cargue`);

--
-- Filtros para la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`id_tanques`) REFERENCES `tanques` (`id_tanques`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
