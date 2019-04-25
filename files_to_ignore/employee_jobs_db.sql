-- MySQL dump 10.13  Distrib 8.0.15, for osx10.13 (x86_64)
--
-- Host: localhost    Database: employee_jobs_db
-- ------------------------------------------------------
-- Server version	8.0.15

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `jobs`
--

DROP TABLE IF EXISTS `jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `jobs` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `assigned_to_id` int(11) DEFAULT NULL,
  `title` varchar(65) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `location` varchar(65) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `posted_by_id` int(11) NOT NULL,
  `job_desc` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `job_category` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `other` text,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_jobs_registered_users1_idx` (`assigned_to_id`),
  CONSTRAINT `fk_jobs_registered_users1` FOREIGN KEY (`assigned_to_id`) REFERENCES `registered_users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jobs`
--

LOCK TABLES `jobs` WRITE;
/*!40000 ALTER TABLE `jobs` DISABLE KEYS */;
INSERT INTO `jobs` VALUES (19,NULL,'Nii EmBaba','Here, CA',16,'Null Job','Pet Care','Lets see','2019-04-22 21:59:10','2019-04-23 15:10:06'),(30,NULL,'Check Validation','Here, CA',16,'Focus on Error','Pet Care','focus','2019-04-23 14:01:29','2019-04-23 14:36:17'),(33,16,'Posted with Owner','Santa Clara, CA',16,'Check JOb Id','Pet Care','Check JOb ID','2019-04-23 15:33:41','2019-04-23 15:33:41'),(34,NULL,'Owner Posted This','Warm Springs, CA',16,'Check It','Pet Care','JOB ID','2019-04-23 15:38:14','2019-04-23 15:38:14'),(35,16,'test','test',16,'Test','Pet Care','','2019-04-23 16:04:43','2019-04-23 16:04:43'),(36,19,'Wire Job','',16,'Kitchen','Electrical','','2019-04-23 16:07:09','2019-04-23 16:16:08'),(37,NULL,'Why','this',19,'Does','Pet Care','Not Work?','2019-04-23 16:17:12','2019-04-23 16:17:12'),(38,NULL,'This was subd By DummyUser','User',19,'Dummy','Pet Care','Dummy User','2019-04-23 17:26:35','2019-04-23 17:26:35'),(39,NULL,'No Cats','',16,'Pls Work',' ','','2019-04-23 19:07:45','2019-04-23 19:07:45'),(40,NULL,'Cable Work','San Jose, CA',16,'TV Setup',' items ','Program All My Sports Channels','2019-04-23 19:37:26','2019-04-23 19:37:51'),(41,NULL,'Clean Up Porch','Fremont, CA',16,'Real Work',' ','','2019-04-23 19:38:36','2019-04-23 19:38:36'),(43,16,'XYZ','Here, CA',16,'ABC',' items ','','2019-04-23 19:39:49','2019-04-23 19:39:49');
/*!40000 ALTER TABLE `jobs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registered_users`
--

DROP TABLE IF EXISTS `registered_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `registered_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `last_name` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password_hash` varchar(77) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `gender` varchar(12) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `birthday` date NOT NULL,
  `interests` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `about` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registered_users`
--

LOCK TABLES `registered_users` WRITE;
/*!40000 ALTER TABLE `registered_users` DISABLE KEYS */;
INSERT INTO `registered_users` VALUES (16,'Emp #1','Uno','emp1@jobs.com','$2b$12$CifFhKAvn7F3mQW0SOw.iezY7288hGJ0/GvTHxyAolkZJ7E7a53j6','Male','1989-04-22','Yoga','Work Now','2019-04-22 13:02:31','2019-04-22 13:02:31'),(17,'David','Osorno','dav@id.oso','$2b$12$O9UP3ew1tU.qtZ5BtoE87eHbN0wTrsZUOJfO5pstZmiu2T8rTog/q','Male','1989-04-22','Yoga','I LOVE DEBUGGING!!!','2019-04-23 12:35:05','2019-04-23 12:35:05'),(18,'Fe2hi','S. Issa','fethi@said.isa','$2b$12$pl4O6GVqOCjTRs74WXd1dOee5ECCXMtjBo3eRblh/IWYyS6n0RFa6','Male','1991-04-22','Bowling','I try','2019-04-23 12:39:46','2019-04-23 12:39:46'),(19,'DummyUser1','DummyUser1','DummyUser1@DummyUser1.com','$2b$12$/Rq/ew0fqBijABVQvs.r8eNhmlO1RoGM3hsmGaUyN9VLZ1xeSir5u','Male','1991-04-22','Bowling','DummyUser1','2019-04-23 12:58:25','2019-04-23 12:58:25'),(20,'DummyUser2','DummyUser2','DummyUser2@DummyUser2.com','$2b$12$01FwvuP9k9B38gAtyi5kRuBwU3c5pb0/Tr84/yJALR3AVQviXOVSa','Female','1989-04-22','Skiing','DummyUser2','2019-04-23 17:34:17','2019-04-23 17:34:17');
/*!40000 ALTER TABLE `registered_users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-04-23 20:58:37
