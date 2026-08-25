-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: website
-- ------------------------------------------------------
-- Server version	8.0.21

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin` (
  `aid` int NOT NULL AUTO_INCREMENT,
  `email` varchar(45) NOT NULL,
  `details` varchar(45) DEFAULT NULL,
  `password` varchar(250) NOT NULL,
  `join_date` datetime DEFAULT NULL,
  `username` varchar(45) NOT NULL,
  PRIMARY KEY (`aid`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'vaggaravikumar118@gmail.com','new admin','YOUR_PASSWORD_HASH','2026-08-14 17:36:52','Ravi Kumar');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cart`
--

DROP TABLE IF EXISTS `cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `pid` int NOT NULL,
  `quantity` int NOT NULL,
  `vid` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `username_idx` (`user_id`),
  KEY `fk_cart_3_idx` (`vid`),
  KEY `fk_cart_2_idx` (`pid`),
  CONSTRAINT `fk_cart_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `fk_cart_2` FOREIGN KEY (`pid`) REFERENCES `products` (`pid`),
  CONSTRAINT `fk_cart_3` FOREIGN KEY (`vid`) REFERENCES `seller` (`vid`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart`
--

LOCK TABLES `cart` WRITE;
/*!40000 ALTER TABLE `cart` DISABLE KEYS */;
/*!40000 ALTER TABLE `cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notification`
--

DROP TABLE IF EXISTS `notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notification` (
  `id` int NOT NULL AUTO_INCREMENT,
  `person1_id` int NOT NULL,
  `pname` varchar(45) NOT NULL,
  `content` varchar(45) NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_notification_1_idx` (`person1_id`),
  CONSTRAINT `fk_notification_1` FOREIGN KEY (`person1_id`) REFERENCES `seller` (`vid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notification`
--

LOCK TABLES `notification` WRITE;
/*!40000 ALTER TABLE `notification` DISABLE KEYS */;
INSERT INTO `notification` VALUES (1,1,'new1','Accepted','2026-08-14 12:38:03'),(2,1,'new2','Rejected','2026-08-14 15:03:26'),(3,1,'new1','Pending','2026-08-14 16:09:30');
/*!40000 ALTER TABLE `notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_details`
--

DROP TABLE IF EXISTS `order_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_details` (
  `did` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `company` varchar(100) DEFAULT NULL,
  `number` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `add1` varchar(100) NOT NULL,
  `add2` varchar(100) DEFAULT NULL,
  `city` varchar(100) NOT NULL,
  `District` varchar(100) DEFAULT NULL,
  `Postcode` varchar(100) DEFAULT NULL,
  `order_notes` varchar(100) DEFAULT NULL,
  `payment_method` varchar(45) NOT NULL,
  `datetime` datetime DEFAULT NULL,
  PRIMARY KEY (`did`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_details`
--

LOCK TABLES `order_details` WRITE;
/*!40000 ALTER TABLE `order_details` DISABLE KEYS */;
INSERT INTO `order_details` VALUES
(3,'Ravi','Kumar','','987654321','vaggaravikumar118@gmail.com','Andhra Pradesh','Andhra Pradesh, Kurnool District','Yemmiganur','Kurnool','518360','NA','cash','2026-08-14 10:00:00'),
(4,'Ravi','Kumar','','987654321','vaggaravikumar118@gmail.com','Andhra Pradesh','Andhra Pradesh, Kurnool District','Yemmiganur','Kurnool','518360','NA','cash','2026-08-14 10:10:00'),
(5,'Ravi','Kumar','','987654321','vaggaravikumar118@gmail.com','Andhra Pradesh','Andhra Pradesh, Kurnool District','Yemmiganur','Kurnool','518360','NA','cash','2026-08-14 10:20:00'),
(6,'Ravi','Kumar','','987654321','vaggaravikumar118@gmail.com','Andhra Pradesh','Andhra Pradesh, Kurnool District','Yemmiganur','Kurnool','518360','NA','cash','2026-08-14 10:30:00'),
(7,'Ravi','Kumar','','987654321','vaggaravikumar118@gmail.com','Andhra Pradesh','Andhra Pradesh, Kurnool District','Yemmiganur','Kurnool','518360','NA','cash','2026-08-14 10:40:00'),
(8,'Ravi','Kumar','','987654321','vaggaravikumar118@gmail.com','Andhra Pradesh','Andhra Pradesh, Kurnool District','Yemmiganur','Kurnool','518360','NA','cash','2026-08-14 10:50:00'),
(9,'Ravi','Kumar','','987654321','vaggaravikumar118@gmail.com','Andhra Pradesh','Andhra Pradesh, Kurnool District','Yemmiganur','Kurnool','518360','NA','cash','2026-08-14 11:00:00'),
(10,'Ravi','Kumar','','987654321','vaggaravikumar118@gmail.com','Andhra Pradesh','Andhra Pradesh, Kurnool District','Yemmiganur','Kurnool','518360','NA','cash','2026-08-14 11:10:00'),
(11,'Ravi','Kumar','','987654321','vaggaravikumar118@gmail.com','Andhra Pradesh','Andhra Pradesh, Kurnool District','Yemmiganur','Kurnool','518360','NA','cash','2026-08-14 11:20:00'),
(12,'Ravi','Kumar','','987654321','vaggaravikumar118@gmail.com','Andhra Pradesh','Andhra Pradesh, Kurnool District','Yemmiganur','Kurnool','518360','NA','cash','2026-08-14 11:30:00'),
(13,'Ravi','Kumar','','987654321','vaggaravikumar118@gmail.com','Andhra Pradesh','Andhra Pradesh, Kurnool District','Yemmiganur','Kurnool','518360','NA','cash','2026-08-14 11:40:00'),
(14,'Ravi','Kumar','','987654321','vaggaravikumar118@gmail.com','Andhra Pradesh','Andhra Pradesh, Kurnool District','Yemmiganur','Kurnool','518360','NA','cash','2026-08-14 11:50:00'),
(15,'Ravi','Kumar','','987654321','vaggaravikumar118@gmail.com','Andhra Pradesh','Andhra Pradesh, Kurnool District','Yemmiganur','Kurnool','518360','NA','cash','2026-08-14 12:00:00'),
(16,'Ravi','Kumar','','987654321','vaggaravikumar118@gmail.com','Andhra Pradesh','Andhra Pradesh, Kurnool District','Yemmiganur','Kurnool','518360','NA','cash','2026-08-14 12:10:00'),
(17,'Ravi','Kumar','','987654321','vaggaravikumar118@gmail.com','Andhra Pradesh','Andhra Pradesh, Kurnool District','Yemmiganur','Kurnool','518360','NA','cash','2026-08-14 12:20:00'),
(18,'Ravi','Kumar','','987654321','vaggaravikumar118@gmail.com','Andhra Pradesh','Andhra Pradesh, Kurnool District','Yemmiganur','Kurnool','518360','NA','cash','2026-08-14 12:30:00'),
(19,'Ravi','Kumar','','987654321','vaggaravikumar118@gmail.com','Andhra Pradesh','Andhra Pradesh, Kurnool District','Yemmiganur','Kurnool','518360','NA','cash','2026-08-14 12:40:00'),
(20,'Ravi','Kumar','','987654321','vaggaravikumar118@gmail.com','Andhra Pradesh','Andhra Pradesh, Kurnool District','Yemmiganur','Kurnool','518360','NA','cash','2026-08-14 12:50:00');/*!40000 ALTER TABLE `order_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `pro_id` int NOT NULL,
  `quantity` int NOT NULL,
  `price` int NOT NULL,
  `datetime` datetime NOT NULL,
  `delivery_status` varchar(45) NOT NULL DEFAULT 'Not Delivered',
  `vid` int DEFAULT NULL,
  `did` int DEFAULT NULL,
  PRIMARY KEY (`order_id`),
  UNIQUE KEY `order_id_UNIQUE` (`order_id`),
  KEY `fk_orders_1_idx` (`user_id`),
  KEY `fk_orders_2_idx` (`pro_id`),
  KEY `fk_orders_3_idx` (`vid`),
  KEY `fk_orders_4_idx` (`did`),
  CONSTRAINT `fk_orders_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `fk_orders_2` FOREIGN KEY (`pro_id`) REFERENCES `products` (`pid`),
  CONSTRAINT `fk_orders_3` FOREIGN KEY (`vid`) REFERENCES `seller` (`vid`),
  CONSTRAINT `fk_orders_4` FOREIGN KEY (`did`) REFERENCES `order_details` (`did`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,1,1,4,200,'2026-08-14 12:38:03','Delivered',1,3),(2,1,3,2,400,'2026-08-14 13:38:03','Delivered',1,4),(3,1,1,1,200,'2026-08-14 14:38:49','Delivered',1,5),(4,1,1,2,200,'2026-08-14 15:38:49','Delivered',1,6),(5,1,3,6,400,'2026-08-14 16:05:47','Delivered',1,7),(6,1,1,1,200,'2026-08-14 17:05:47','Delivered',2,8);
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `price`
--

DROP TABLE IF EXISTS `price`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `price` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pid` int NOT NULL,
  `vid` int NOT NULL,
  `price` int NOT NULL,
  `disprice` int DEFAULT NULL,
  `dateAdded` date NOT NULL,
  `stock` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_price_1_idx` (`pid`),
  KEY `fk_price_2_idx` (`vid`),
  CONSTRAINT `fk_price_1` FOREIGN KEY (`pid`) REFERENCES `products` (`pid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_price_2` FOREIGN KEY (`vid`) REFERENCES `seller` (`vid`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `price`
--

LOCK TABLES `price` WRITE;
/*!40000 ALTER TABLE `price` DISABLE KEYS */;
INSERT INTO `price` VALUES (1,1,1,200,150,'2026-08-14',12),(2,2,1,400,200,'2026-08-14',88),(3,3,1,400,344,'2026-08-14',92),(36,4,1,500,460,'2026-08-14',100),(37,5,1,500,490,'2026-08-14',100),(38,6,1,500,400,'2026-08-14',98),(39,7,1,500,NULL,'2026-08-14',100),(40,8,1,500,NULL,'2026-08-14',100),(41,9,1,500,NULL,'2026-08-14',100),(42,10,1,500,NULL,'2026-08-14',100),(43,11,1,400,NULL,'2026-08-14',100),(44,1,2,200,100,'2026-08-14',69);
/*!40000 ALTER TABLE `price` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `pid` int NOT NULL AUTO_INCREMENT,
  `pname` varchar(45) NOT NULL,
  `price` double NOT NULL,
  `pdetails` varchar(45) DEFAULT NULL,
  `new` varchar(45) DEFAULT 'NO',
  `category` varchar(45) NOT NULL,
  `deleted` int DEFAULT NULL,
  `rating` double NOT NULL DEFAULT '0',
  `no_of_ppl` int NOT NULL DEFAULT '0',
  `rid` int DEFAULT NULL,
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'Men\'s short',200,'qwe','1','clothing',0,0,0,NULL),(2,'Mens\'s top',400,'qwe',NULL,'clothing',0,0,0,NULL),(3,'Women\'s top',400,'qwe','1','clothing',0,3,0,NULL),(4,'Grey swetshirt',500,'qwe','1','clothing',0,0,0,NULL),(5,'Wooden Wall Clock',500,'soft cotten made',NULL,'homedecor',0,0,0,NULL),(6,'Decorative Wall Lamp',500,'beautiful and useful',NULL,'homedecor',0,0,0,NULL),(7,'Watch 1',500,NULL,'1','watches',0,0,0,NULL),(8,'Watch 2',500,NULL,NULL,'watches',0,0,0,NULL),(9,'Green Apple',500,NULL,NULL,'pantry',0,0,0,NULL),(10,'Pantry 1',500,NULL,'1','pantry',0,0,0,NULL),(11,'Pantry 3',500,NULL,NULL,'pantry',0,0,0,NULL);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pid` int NOT NULL,
  `uid` int NOT NULL,
  `comment` varchar(500) DEFAULT NULL,
  `rating` int DEFAULT NULL,
  `datetime` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_comments_1_idx` (`pid`),
  KEY `fk_comments_2_idx` (`uid`),
  CONSTRAINT `fk_comments_1` FOREIGN KEY (`pid`) REFERENCES `products` (`pid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `fk_comments_2` FOREIGN KEY (`uid`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (1,1,1,'1sdvfdvb',4,'2026-08-14 17:36:52'),(2,3,1,'nice',3,'2026-08-14 18:08:20');
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `seller`
--

DROP TABLE IF EXISTS `seller`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `seller` (
  `vid` int NOT NULL AUTO_INCREMENT,
  `seller_name` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `description` varchar(45) DEFAULT NULL,
  `join_date` date NOT NULL,
  `streetname` varchar(45) NOT NULL,
  `city` varchar(45) NOT NULL,
  `state` varchar(45) NOT NULL,
  `pincode` int NOT NULL,
  `Deleted` int DEFAULT '0',
  `password` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`vid`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `seller`
--

LOCK TABLES `seller` WRITE;
/*!40000 ALTER TABLE `seller` DISABLE KEYS */;
INSERT INTO `seller` VALUES (1,'Ravi Kumar','vaggaravikumar118@gmail.com','Online seller','2026-08-14','Andhra Pradesh','Yemmiganur','Andhra Pradesh',518360,0,'YOUR_SELLER_PASSWORD_HASH');
/*!40000 ALTER TABLE `seller` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `temporary_product`
--

DROP TABLE IF EXISTS `temporary_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `temporary_product` (
  `rid` int NOT NULL AUTO_INCREMENT,
  `vid` int NOT NULL,
  `pname` varchar(45) NOT NULL,
  `price` varchar(45) DEFAULT NULL,
  `pdetails` varchar(45) DEFAULT NULL,
  `disprice` varchar(45) DEFAULT NULL,
  `category` varchar(45) DEFAULT NULL,
  `stock` varchar(45) DEFAULT NULL,
  `datetime` datetime NOT NULL,
  PRIMARY KEY (`rid`),
  KEY `fk_temporary_product_1_idx` (`vid`),
  CONSTRAINT `fk_temporary_product_1` FOREIGN KEY (`vid`) REFERENCES `seller` (`vid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `temporary_product`
--

LOCK TABLES `temporary_product` WRITE;
/*!40000 ALTER TABLE `temporary_product` DISABLE KEYS */;
 /*!40000 ALTER TABLE `temporary_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(250) NOT NULL,
  `join_date` date NOT NULL,
  `Deleted` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='contains information of users registered';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Ravi Kumar','vaggaravikumar118@gmail.com','YOUR_USER_PASSWORD_HASH','2026-08-14',0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-14 18:00:00
