-- MySQL dump 10.13  Distrib 8.0.35, for Win64 (x86_64)
--
-- Host: localhost    Database: sae301
-- ------------------------------------------------------
-- Server version	8.0.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages` (
  `idmsg` int NOT NULL AUTO_INCREMENT,
  `user` varchar(100) DEFAULT NULL,
  `texte` tinytext,
  `date` datetime DEFAULT NULL,
  `salon` int DEFAULT NULL,
  PRIMARY KEY (`idmsg`),
  KEY `user` (`user`),
  KEY `salon` (`salon`),
  CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`user`) REFERENCES `users` (`iduser`),
  CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`salon`) REFERENCES `salons` (`idsalon`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `salon_user`
--

DROP TABLE IF EXISTS `salon_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `salon_user` (
  `user` varchar(255) NOT NULL,
  `salon` int NOT NULL,
  PRIMARY KEY (`salon`,`user`),
  KEY `user` (`user`),
  CONSTRAINT `salon_user_ibfk_1` FOREIGN KEY (`user`) REFERENCES `users` (`iduser`) ON DELETE CASCADE,
  CONSTRAINT `salon_user_ibfk_2` FOREIGN KEY (`salon`) REFERENCES `salons` (`idsalon`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `salons`
--

DROP TABLE IF EXISTS `salons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `salons` (
  `idsalon` int NOT NULL AUTO_INCREMENT,
  `salon` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`idsalon`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `iduser` varchar(255) NOT NULL,
  `ip` varchar(15) DEFAULT NULL,
  `mdp` varchar(100) DEFAULT NULL,
  `admin` boolean DEFAULT NULL,
  `pseudo` varchar(100) DEFAULT NULL,
  `ban` boolean DEFAULT NULL,
  PRIMARY KEY (`iduser`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

insert into users (iduser, ip, mdp, admin, pseudo) values ('admin','127.0.0.1','toto','1', 'admin');
insert into users (iduser, ip, mdp, admin, pseudo) values ('manuel','127.0.0.2','toto','0', 'Manu');


INSERT INTO salons (salon) VALUES
    ('Général'),
    ('Blabla'),
    ('Comptabilité'),
    ('Informatique'),
    ('Marketing');
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-31  6:05:25
