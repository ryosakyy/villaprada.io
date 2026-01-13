-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 12-01-2026 a las 19:08:47
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
-- Base de datos: `villa_prada`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `id` int(11) NOT NULL,
  `dni` varchar(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `direccion` varchar(150) DEFAULT NULL,
  `fecha_registro` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id`, `dni`, `nombre`, `telefono`, `correo`, `direccion`, `fecha_registro`) VALUES
(1, '12345678', 'jose quisp', '987654321', 'jose@gmail.com', 'av garcilaso', '2025-11-30 06:30:48'),
(10, '122121', 'MANUEL RISO ', '984494649', 'jose@gmail.com', 'AV ABAMVAY', '2025-12-28 17:32:54'),
(17, '12345698', 'manuel rios peña ', '9874454565', 'asas@gmail.com', 'av.cines', '2025-12-28 17:43:44'),
(37, '76038773', 'inka', '967953115', 'inca@gmail.com', 'av.abancay', '2025-12-31 19:19:56'),
(39, '76038771', 'oso', '97656565', 'oso@gmail.com', 'av.abancayy', '2025-12-31 19:45:29'),
(40, '76038771', 'oso', '97656565', 'oso@gmail.com', 'av.abancayy', '2025-12-31 19:45:30'),
(42, '76038779', 'manuel rioss', '984464613', 'manuel@gmail.com', 'av.abbbb', '2026-01-02 10:49:58'),
(43, '7984565', 'robin contreras', '984494676', 'robin@gmail.com', 'av.bancay', '2026-01-02 11:04:07'),
(46, 'rerer', 'ererer', 'erer', 'erer', 'erer', '2026-01-02 20:07:39'),
(47, '76038773', 'manuel angel', '98775656', NULL, 'Registrado desde Contratos', '2026-01-07 11:34:49'),
(48, '79889895', 'manuel angel ', '987797989', NULL, 'Registrado desde Contratos', '2026-01-07 12:42:44'),
(49, '7638775', 'robin ', '5655656565', '54545@utea', 'Sin direccion', '2026-01-08 16:09:01'),
(50, '76038773', 'manuel', '94655665', 'manuel@gmail.com', 'Sin direccion', '2026-01-09 19:30:33'),
(51, '77887878', 'ASASAS', '154545', 'SASAS', 'ASASAS', '2026-01-11 23:03:52');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `contratos`
--

CREATE TABLE `contratos` (
  `id` int(11) NOT NULL,
  `cliente_id` int(11) NOT NULL,
  `fecha_evento` date NOT NULL,
  `hora_inicio` time NOT NULL,
  `hora_fin` time NOT NULL,
  `paquete` varchar(100) NOT NULL,
  `monto_total` float NOT NULL,
  `adelanto` float DEFAULT NULL,
  `saldo` float DEFAULT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `contratos`
--

INSERT INTO `contratos` (`id`, `cliente_id`, `fecha_evento`, `hora_inicio`, `hora_fin`, `paquete`, `monto_total`, `adelanto`, `saldo`, `estado`, `fecha_creacion`) VALUES
(1, 1, '2025-12-20', '18:00:00', '23:00:00', 'Paquete Gold', 1500, 500, 700, 'parcial', '2025-11-30 06:58:48'),
(5, 10, '2025-12-10', '19:10:00', '19:36:00', 'asas', 7000, 300, 6700, 'activo', '2025-12-28 18:09:46'),
(9, 10, '2025-12-15', '21:38:00', '20:38:00', 'bodaaa premiu ', 7300, 300, 0.0000977516, 'parcial', '2025-12-28 18:36:58'),
(10, 1, '2025-12-16', '22:11:00', '23:13:00', 'bodasasasas', 7000, 700, 0, 'completo', '2025-12-28 19:07:26'),
(12, 17, '2025-12-02', '01:49:00', '17:50:00', 'bodaaa', 8000, 0, 0, 'completo', '2025-12-28 23:48:00'),
(13, 17, '2025-12-30', '16:56:00', '08:57:00', 'boda premiun ', 800, 500, 0, 'completo', '2025-12-29 14:53:04'),
(17, 37, '2025-12-31', '19:23:00', '22:23:00', '15 años', 5000, 500, 0, 'completo', '2025-12-31 19:23:20'),
(18, 40, '2026-01-04', '13:45:00', '23:45:00', '50 años', 4500, 300, 0, 'completo', '2025-12-31 19:48:21'),
(23, 48, '2026-01-01', '17:57:00', '17:57:00', 'BÁSICO', 2500, 500, 0, 'activo', '2026-01-07 16:57:38'),
(25, 47, '2026-01-01', '18:18:00', '19:18:00', 'BÁSICO', 2500, 500, 0, 'activo', '2026-01-07 17:18:08'),
(28, 37, '2026-01-04', '13:45:00', '23:45:00', 'BÁSICO', 2500, 300, 1700, 'parcial', '2026-01-07 17:45:44'),
(29, 37, '2026-01-01', '20:36:00', '23:36:00', 'BÁSICO  + mozos extras', 4000, 400, 0, 'activo', '2026-01-07 19:36:44'),
(30, 49, '2026-01-13', '20:10:00', '19:10:00', 'boda  + mas chelas + mozos extras', 71000, 500, 65500, 'parcial', '2026-01-08 16:10:50'),
(31, 50, '2026-01-20', '21:39:00', '21:39:00', 'BÁSICO + mozos extras', 6000, 500, 0, 'activo', '2026-01-09 19:39:51'),
(32, 50, '2026-01-01', '19:42:00', '22:42:00', 'BÁSICO + mozos extras + mozos extras', 3500, 1000, 2000, 'parcial', '2026-01-09 19:43:04'),
(33, 51, '2026-01-06', '11:08:00', '04:10:00', 'BÁSICO + mozos extras', 3000, 0, 0, 'activo', '2026-01-12 00:08:02'),
(34, 50, '2026-01-01', '03:18:00', '22:22:00', 'BÁSICO + mozos extras + mozos extras', 3500, 500, 2500, 'parcial', '2026-01-12 00:18:45');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `disponibilidad`
--

CREATE TABLE `disponibilidad` (
  `id` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `motivo` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `disponibilidad`
--

INSERT INTO `disponibilidad` (`id`, `fecha`, `estado`, `motivo`) VALUES
(1, '2025-12-28', 'bloqueado', 'Mantenimiento general'),
(2, '2026-01-01', 'ocupado', 'Contrato ID 2'),
(8, '2025-12-10', 'ocupado', 'Contrato ID 5'),
(13, '2025-12-15', 'ocupado', 'Contrato N° 9 (bodaaa premiu )'),
(14, '2025-12-16', 'ocupado', 'Contrato N° 10 (bodasasasas)'),
(16, '2025-12-02', 'ocupado', 'Contrato N° 12 (bodaaa)'),
(17, '2025-12-30', 'ocupado', 'Contrato N° 13 (boda premiun )'),
(21, '2025-12-31', 'ocupado', 'Contrato N° 17 (15 años)'),
(22, '2026-01-04', 'ocupado', 'Contrato N° 18 (50 años)');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `egresos`
--

CREATE TABLE `egresos` (
  `id` int(11) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `monto` float NOT NULL,
  `categoria` varchar(100) NOT NULL,
  `fecha` date NOT NULL,
  `observacion` varchar(255) DEFAULT NULL,
  `contrato_id` int(11) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT NULL,
  `comprobante_url` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `egresos`
--

INSERT INTO `egresos` (`id`, `descripcion`, `monto`, `categoria`, `fecha`, `observacion`, `contrato_id`, `fecha_creacion`, `comprobante_url`) VALUES
(1, 'Decoración', 300, 'decoracion', '2025-12-01', 'Globos y flores', 1, '2025-11-30 08:15:16', NULL),
(2, 'limpieza', 400, 'Limpieza', '2025-12-23', '', NULL, '2025-12-28 20:18:44', NULL),
(3, 'FLORES', 700, 'Insumos', '2025-12-29', '', 10, '2025-12-28 20:30:11', NULL),
(4, 'pago ', 800, 'Limpieza', '2026-01-01', '', 17, '2025-12-31 19:24:55', NULL),
(5, 'flores', 500, 'Decoracion', '2026-01-07', 'sasasasasasas', NULL, '2026-01-07 18:39:42', 'static/comprobantes/afe2ddb7-2aa1-4729-9293-a08a13333e0e.jpg'),
(6, 'flores', 500, 'Mantenimiento', '2026-01-10', 'sas', 32, '2026-01-09 19:49:20', 'static/comprobantes/8c7e178e-7a6d-4a7d-aa08-69f95ea916a7.jfif');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `galeria`
--

CREATE TABLE `galeria` (
  `id` int(11) NOT NULL,
  `titulo` varchar(150) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `categoria` varchar(50) DEFAULT NULL,
  `imagen_url` varchar(500) NOT NULL,
  `public_id` varchar(200) NOT NULL,
  `contrato_id` int(11) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `galeria`
--

INSERT INTO `galeria` (`id`, `titulo`, `descripcion`, `categoria`, `imagen_url`, `public_id`, `contrato_id`, `fecha_creacion`) VALUES
(8, 'Imagen 3', NULL, 'boda', 'https://res.cloudinary.com/dgsfiy5vn/image/upload/v1764540504/villa_prada/galeria/tjdctsk2o3o013h1se5f.png', 'villa_prada/galeria/tjdctsk2o3o013h1se5f', NULL, '2025-11-30 17:08:25'),
(9, 'Imagen 4', NULL, 'boda', 'https://res.cloudinary.com/dgsfiy5vn/image/upload/v1764540506/villa_prada/galeria/uhoemyca4cv0wfuhmzx3.png', 'villa_prada/galeria/uhoemyca4cv0wfuhmzx3', NULL, '2025-11-30 17:08:27'),
(12, 'Imagen 7', NULL, 'boda', 'https://res.cloudinary.com/dgsfiy5vn/image/upload/v1764540511/villa_prada/galeria/uw2oiczjh16uls8naupw.png', 'villa_prada/galeria/uw2oiczjh16uls8naupw', NULL, '2025-11-30 17:08:31'),
(13, 'Imagen 8', NULL, 'boda', 'https://res.cloudinary.com/dgsfiy5vn/image/upload/v1764540512/villa_prada/galeria/iuyc0turtfnruhb8jzwo.png', 'villa_prada/galeria/iuyc0turtfnruhb8jzwo', NULL, '2025-11-30 17:08:33'),
(27, 'boda', NULL, 'boda', 'https://res.cloudinary.com/dgsfiy5vn/image/upload/v1768002727/villa_prada/galeria/unwfeetl2wogol3fvclb.jpg', 'villa_prada/galeria/unwfeetl2wogol3fvclb', NULL, '2026-01-09 18:52:07'),
(29, 'mesa', NULL, NULL, 'https://res.cloudinary.com/dgsfiy5vn/image/upload/v1768198708/villa_prada/galeria/hztesidhpkyq12zrfmtl.png', 'villa_prada/galeria/hztesidhpkyq12zrfmtl', NULL, '2026-01-12 01:18:29');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pagos`
--

CREATE TABLE `pagos` (
  `id` int(11) NOT NULL,
  `contrato_id` int(11) NOT NULL,
  `fecha_pago` date NOT NULL,
  `monto` float NOT NULL,
  `metodo` varchar(50) NOT NULL,
  `observacion` varchar(255) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT NULL,
  `comprobante_url` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pagos`
--

INSERT INTO `pagos` (`id`, `contrato_id`, `fecha_pago`, `monto`, `metodo`, `observacion`, `fecha_creacion`, `comprobante_url`) VALUES
(1, 1, '2025-12-01', 300, 'efectivo', 'Pago adicional', '2025-11-30 07:54:42', NULL),
(2, 10, '2025-12-29', 800, 'Efectivo', '', '2025-12-28 19:55:24', NULL),
(3, 10, '2025-12-29', 500, 'Efectivo', '', '2025-12-28 19:56:05', NULL),
(4, 10, '2025-12-29', 5000, 'Efectivo', '', '2025-12-28 19:56:38', NULL),
(5, 9, '2025-12-29', 400, 'Efectivo', '', '2025-12-28 19:57:47', NULL),
(6, 9, '2025-12-29', 6.6, 'Efectivo', '', '2025-12-28 20:00:04', NULL),
(7, 9, '2025-12-29', 6593.4, 'Efectivo', '', '2025-12-28 20:00:20', NULL),
(8, 12, '2025-12-29', 8000, 'Efectivo', '8000', '2025-12-28 23:48:56', NULL),
(9, 13, '2025-12-29', 300, 'Efectivo', '', '2025-12-29 14:54:16', NULL),
(10, 17, '2026-01-01', 4500, 'Efectivo', 'cancelo', '2025-12-31 19:24:00', NULL),
(11, 18, '2026-01-01', 3600, 'Efectivo', '', '2025-12-31 19:49:38', NULL),
(12, 18, '2026-01-01', 600, 'Efectivo', '', '2025-12-31 19:49:51', NULL),
(16, 28, '2026-01-07', 500, 'Yape', NULL, '2026-01-07 18:47:43', 'static/pagos/e7bb2d6a-8acb-43d0-8ad5-66e9f2280da1.jpg'),
(17, 30, '2026-01-08', 5000, 'Yape', 'tytgggf', '2026-01-08 16:12:04', 'static/pagos/692ca7f7-5338-450a-8de4-6747f8a73997.jpg'),
(18, 32, '2026-01-29', 500, 'Yape', 'aaaa', '2026-01-09 19:48:14', 'static/pagos/7fb3f484-c57c-4b47-8ff7-39efaa4c4b6b.jfif'),
(19, 34, '2026-01-11', 500, 'Transferencia', NULL, '2026-01-12 00:29:51', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `paquetes`
--

CREATE TABLE `paquetes` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `precio` float NOT NULL,
  `capacidad` int(11) NOT NULL,
  `servicios` text DEFAULT NULL,
  `imagen` varchar(200) DEFAULT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `paquetes`
--

INSERT INTO `paquetes` (`id`, `nombre`, `descripcion`, `precio`, `capacidad`, `servicios`, `imagen`, `estado`, `fecha_creacion`) VALUES
(1, 'BÁSICO', 'Ideal para eventos íntimos', 2500, 50, 'Decoración básica\nMesas y sillas\nMenajería completa\n6 horas de servicio\nMontaje y desmontaje\nPersonal de limpieza', 'basico.jpg', 'activo', '2025-11-30 07:37:31'),
(2, 'asas', '', 8000, 700, 'asasas', NULL, 'activo', '2025-12-28 22:43:29'),
(3, 'asas', '', 8000, 700, 'asasas', NULL, 'activo', '2025-12-28 22:43:30'),
(4, 'asddsa', '', 8000, 100, 'adsasdasd', NULL, 'activo', '2025-12-28 22:44:08'),
(5, 'asddsa', '', 8000, 100, 'adsasdasd', NULL, 'activo', '2025-12-28 22:44:08'),
(6, 'boda ', NULL, 5000, 100, 'luces   sillas', NULL, 'activo', '2026-01-07 16:24:50'),
(7, 'boda', NULL, 50000, 50, 'jheghhegdhggevh', NULL, 'activo', '2026-01-08 16:09:30'),
(8, 'gold', '', 600, 5, 'asasasas', NULL, 'activo', '2026-01-12 00:26:30');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reservas`
--

CREATE TABLE `reservas` (
  `id` int(11) NOT NULL,
  `cliente_id` int(11) NOT NULL,
  `contrato_id` int(11) DEFAULT NULL,
  `fecha_evento` date NOT NULL,
  `hora_inicio` time NOT NULL,
  `hora_fin` time NOT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `observaciones` varchar(255) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `reservas`
--

INSERT INTO `reservas` (`id`, `cliente_id`, `contrato_id`, `fecha_evento`, `hora_inicio`, `hora_fin`, `estado`, `observaciones`, `fecha_creacion`) VALUES
(1, 1, 1, '2025-12-20', '18:00:00', '23:00:00', 'pendiente', 'Evento para cumpleaños', '2025-11-30 07:12:10');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicios`
--

CREATE TABLE `servicios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `precio` float NOT NULL,
  `estado` varchar(20) DEFAULT 'activo',
  `fecha_creacion` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `servicios`
--

INSERT INTO `servicios` (`id`, `nombre`, `descripcion`, `precio`, `estado`, `fecha_creacion`) VALUES
(1, 'mozos extras', 'mozos ', 500, 'activo', '2026-01-07 19:35:25'),
(2, 'mozos extras', 'mozos ', 500, 'activo', '2026-01-07 19:35:25'),
(3, 'mozos extras', 'mozos ', 500, 'activo', '2026-01-07 19:35:25'),
(4, 'mozos extras', 'mozos ', 500, 'activo', '2026-01-07 19:35:25'),
(5, 'mozos extras', 'mozos ', 500, 'activo', '2026-01-07 19:35:25'),
(6, 'mozos extras', 'mozos ', 500, 'activo', '2026-01-07 19:35:26'),
(7, 'mozos extras', 'mozos ', 500, 'activo', '2026-01-07 19:35:28'),
(8, 'mozos extras', 'mozos ', 500, 'activo', '2026-01-07 19:35:28'),
(9, 'mozos extras', 'mozos ', 500, 'activo', '2026-01-07 19:35:28'),
(10, 'mozos extras', 'mozos ', 500, 'activo', '2026-01-07 19:35:28'),
(11, 'mas chelas', 'borrachos', 5000, 'activo', '2026-01-08 16:10:00'),
(12, 'hora loca ', '50 mozos adicionales de costo \n', 5000, 'activo', '2026-01-12 00:12:40'),
(13, 'hora locaaa', 'mas mozos para la hora loca ', 5000, 'activo', '2026-01-12 00:13:09');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombres` varchar(100) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(200) NOT NULL,
  `rol` varchar(20) DEFAULT NULL,
  `estado` tinyint(1) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombres`, `email`, `password_hash`, `rol`, `estado`, `fecha_creacion`) VALUES
(1, 'Administrador', 'admin@villa.com', '$2b$12$O6Id.MAPwtvIbgxjkgDObuAEPUiaKGv821cXe7j/9rSSiFOS4C8ni', 'admin', 1, '2025-12-01 04:33:12'),
(25, 'manuel', 'admin1@villa.com', '$2b$12$bElnszGP5Z.2XGf/6Egum.A1Fbv9As/ZFiAYkmrH.DcHskK3CUaZq', 'admin', 0, '2025-12-29 03:12:57'),
(26, 'MANUEL ANGEL', 'admin1234@villa.com', '$2b$12$dH9O/5IPigdQMJ1DUHQb9uvRym5hI9kjRz4h6RguQP0Ju5xb4eBgi', 'admin', 0, '2025-12-29 03:17:23'),
(27, 'MANUEL ANGEL', 'admin2@villa.com', '$2b$12$fVuIARlxbFMTEohS/vU5SeLHmj1aLvatmnxcaoCvwPWYHNH7KvMb.', 'admin', 0, '2025-12-29 03:17:46'),
(28, 'manuel', 'admin22@villa.com', '$2b$12$eOq9n7I2UDF5BzJO9Dd9Zuj6kzSO0NnvHNQwtiHh4toFUNv4TCsuu', 'admin', 1, '2025-12-29 04:37:59'),
(30, 'manuel', 'admin33@villa.com', '$2b$12$rtV6WLjNUTn7vHyFQw5TPeirnZ.HdODmPy8oXXiiEkYxICOUWt4oy', 'empleado', 1, '2026-01-01 00:26:41'),
(31, 'ANGEL', 'angel@gmail.com', '$2b$12$AOHNjGMfraPVlHjAfKLXEeqVRJLJAzJyJvcZXD.SBfP8AbnBifN7C', 'empleado', 1, '2026-01-12 04:10:14'),
(32, 'marie', 'adminaa@villa.com', '$2b$12$7kYC4hWu.Rd/0csZMyYRQufpJVt6PS6JTvF67vVmA3UWZ9fQbidxK', 'admin', 1, '2026-01-12 05:25:29');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_clientes_id` (`id`);

--
-- Indices de la tabla `contratos`
--
ALTER TABLE `contratos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cliente_id` (`cliente_id`),
  ADD KEY `ix_contratos_id` (`id`);

--
-- Indices de la tabla `disponibilidad`
--
ALTER TABLE `disponibilidad`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `fecha` (`fecha`),
  ADD KEY `ix_disponibilidad_id` (`id`);

--
-- Indices de la tabla `egresos`
--
ALTER TABLE `egresos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `contrato_id` (`contrato_id`),
  ADD KEY `ix_egresos_id` (`id`);

--
-- Indices de la tabla `galeria`
--
ALTER TABLE `galeria`
  ADD PRIMARY KEY (`id`),
  ADD KEY `contrato_id` (`contrato_id`),
  ADD KEY `ix_galeria_id` (`id`);

--
-- Indices de la tabla `pagos`
--
ALTER TABLE `pagos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `contrato_id` (`contrato_id`),
  ADD KEY `ix_pagos_id` (`id`);

--
-- Indices de la tabla `paquetes`
--
ALTER TABLE `paquetes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_paquetes_id` (`id`);

--
-- Indices de la tabla `reservas`
--
ALTER TABLE `reservas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cliente_id` (`cliente_id`),
  ADD KEY `contrato_id` (`contrato_id`),
  ADD KEY `ix_reservas_id` (`id`);

--
-- Indices de la tabla `servicios`
--
ALTER TABLE `servicios`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `ix_usuarios_id` (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;

--
-- AUTO_INCREMENT de la tabla `contratos`
--
ALTER TABLE `contratos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT de la tabla `disponibilidad`
--
ALTER TABLE `disponibilidad`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT de la tabla `egresos`
--
ALTER TABLE `egresos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `galeria`
--
ALTER TABLE `galeria`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT de la tabla `pagos`
--
ALTER TABLE `pagos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `paquetes`
--
ALTER TABLE `paquetes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `reservas`
--
ALTER TABLE `reservas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `servicios`
--
ALTER TABLE `servicios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `contratos`
--
ALTER TABLE `contratos`
  ADD CONSTRAINT `contratos_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`);

--
-- Filtros para la tabla `egresos`
--
ALTER TABLE `egresos`
  ADD CONSTRAINT `egresos_ibfk_1` FOREIGN KEY (`contrato_id`) REFERENCES `contratos` (`id`);

--
-- Filtros para la tabla `galeria`
--
ALTER TABLE `galeria`
  ADD CONSTRAINT `galeria_ibfk_1` FOREIGN KEY (`contrato_id`) REFERENCES `contratos` (`id`);

--
-- Filtros para la tabla `pagos`
--
ALTER TABLE `pagos`
  ADD CONSTRAINT `pagos_ibfk_1` FOREIGN KEY (`contrato_id`) REFERENCES `contratos` (`id`);

--
-- Filtros para la tabla `reservas`
--
ALTER TABLE `reservas`
  ADD CONSTRAINT `reservas_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`),
  ADD CONSTRAINT `reservas_ibfk_2` FOREIGN KEY (`contrato_id`) REFERENCES `contratos` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
