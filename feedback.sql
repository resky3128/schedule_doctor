-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Feb 24, 2024 at 03:29 AM
-- Server version: 5.7.39
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_dokter`
--

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

CREATE TABLE `feedback` (
  `id` int(11) NOT NULL,
  `dokter_id` int(11) DEFAULT NULL,
  `query` varchar(255) DEFAULT NULL,
  `relevansi` enum('ya','tidak') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `feedback`
--

INSERT INTO `feedback` (`id`, `dokter_id`, `query`, `relevansi`) VALUES
(1, 1, 'dr', 'ya'),
(2, 1, 'dr', 'ya'),
(3, 2, 'dr', 'ya'),
(4, 3, 'dr', 'ya'),
(5, 110, 'dr', 'tidak'),
(6, 1, 'edy', 'ya'),
(7, 52, 'edy', 'ya'),
(8, 84, 'edy', 'ya'),
(9, 99, 'edy', 'ya'),
(10, 1, 'edy', 'ya'),
(11, 1, 'edy', 'ya'),
(12, 52, 'edy', 'ya'),
(13, 1, 'edy', 'ya'),
(14, 52, 'edy', 'tidak'),
(15, 84, 'edy', 'ya'),
(16, 99, 'edy', 'ya'),
(17, 1, 'edu', 'ya'),
(18, 1, 'edy', 'ya'),
(19, 52, 'edy', 'tidak'),
(20, 52, 'edy', 'tidak'),
(21, 84, 'edy', 'ya'),
(22, 99, 'edy', 'tidak'),
(23, 1, 'eddy', 'ya'),
(24, 52, 'eddy', 'tidak'),
(25, 84, 'eddy', 'ya');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`id`),
  ADD KEY `dokter_id` (`dokter_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `feedback`
--
ALTER TABLE `feedback`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `feedback`
--
ALTER TABLE `feedback`
  ADD CONSTRAINT `feedback_ibfk_1` FOREIGN KEY (`dokter_id`) REFERENCES `dokter` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
