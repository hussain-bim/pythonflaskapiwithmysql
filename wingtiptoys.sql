-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 21, 2020 at 11:26 AM
-- Server version: 10.3.16-MariaDB
-- PHP Version: 7.1.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `wingtiptoys`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_names` (IN `id_input` INT)  BEGIN
select * from pet where id = id_input;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SELECT_FROM_TBL_V3` (IN `tbl_name` VARCHAR(200))  NO SQL
BEGIN
 SET @t1 =CONCAT('SELECT * FROM ',tbl_name );
 PREPARE stmt3 FROM @t1;
 EXECUTE stmt3;
 DEALLOCATE PREPARE stmt3;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SELECT_FROM_TBL_V5` (IN `tbl_name` VARCHAR(200))  NO SQL
BEGIN
 SET @t1 =CONCAT('SELECT *, "A" AS A FROM ',tbl_name );
 PREPARE stmt3 FROM @t1;
 EXECUTE stmt3;
 DEALLOCATE PREPARE stmt3;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `pet`
--

CREATE TABLE `pet` (
  `id` int(11) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `species` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `pet`
--

INSERT INTO `pet` (`id`, `name`, `species`) VALUES
(1, 'Dog', 'Domestic'),
(2, 'Cat', 'Domestic'),
(3, 'Fish', 'Domestic');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_user`
--

CREATE TABLE `tbl_user` (
  `user_id` bigint(20) NOT NULL,
  `user_name` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_email` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `user_password` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `tbl_user`
--

INSERT INTO `tbl_user` (`user_id`, `user_name`, `user_email`, `user_password`) VALUES
(4, '1', '1', 'pbkdf2:sha256:150000$tKgEnE3p$118a4c441454017cef317de7604522ad69318afd1a464bb7a99c152b1605f4d0'),
(6, '2', '2', 'pbkdf2:sha256:150000$EsSHttlP$5cdafcf2d39946486189ce847cfc15c79277435137db777aeddb4f5e8a783420'),
(8, '3', '3', 'pbkdf2:sha256:150000$dXqnzXWK$c66744eacb764ff2e4ee55e946decb89c9bd8d6ecbbd043eac7e2daf908e05a1'),
(9, '4', '4', 'pbkdf2:sha256:150000$SuSenSN7$aec180eea0a9ba20fc55edc82c5bbf1dbd9c00b0ef9d0384883d4c89ecea195a'),
(11, '5', '5', 'pbkdf2:sha256:150000$yMO4amM7$d11b420767f4408d09f62b5b99965821572f80572cc2363143fdfaaae34113a7'),
(12, '6', '6', 'pbkdf2:sha256:150000$XXjevlbI$2ef55be742cadd78a317ea73b8400fd8224b39926ebd6de4b246d81f53826f69');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tbl_user`
--
ALTER TABLE `tbl_user`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tbl_user`
--
ALTER TABLE `tbl_user`
  MODIFY `user_id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
