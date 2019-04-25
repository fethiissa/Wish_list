-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema wish_list_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema wish_list_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `wish_list_db` DEFAULT CHARACTER SET utf8 ;


USE `wish_list_db` ;

-- -----------------------------------------------------
-- Table `wish_list_db`.`registered_users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `wish_list_db`.`registered_users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) CHARACTER SET 'utf8mb4' NOT NULL,
  `last_name` VARCHAR(45) CHARACTER SET 'utf8mb4' NOT NULL,
  `email` VARCHAR(45) CHARACTER SET 'utf8mb4' NOT NULL,
  `password_hash` VARCHAR(77) CHARACTER SET 'utf8mb4' NOT NULL,
  `gender` VARCHAR(12) CHARACTER SET 'utf8mb4' NOT NULL,
  `birthday` DATE NOT NULL,
  `interests` VARCHAR(45) CHARACTER SET 'utf8mb4' NOT NULL,
  `about` VARCHAR(45) CHARACTER SET 'utf8mb4' NOT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 19
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `wish_list_db`.`wishes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `wish_list_db`.`wishes` (
  `id` INT(10) NOT NULL AUTO_INCREMENT,
  `made_by_id` INT(11) NOT NULL,
  `title` VARCHAR(65) CHARACTER SET 'utf8mb4' NULL DEFAULT NULL,
  `granted_or_not` TINYINT NOT NULL,
  `description` TEXT CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_0900_ai_ci' NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `granted_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `title_UNIQUE` (`title` ASC) VISIBLE,
  INDEX `fk_books_registered_users1_idx` (`made_by_id` ASC) VISIBLE,
  CONSTRAINT `fk_books_registered_users1`
    FOREIGN KEY (`made_by_id`)
    REFERENCES `wish_list_db`.`registered_users` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 33
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `wish_list_db`.``
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `wish_list_db`.`liked_wishes` (
  `user_id` INT(11) NOT NULL,
  `wish_id` INT(10) NOT NULL,
  INDEX `fk_favorites_registered_users1_idx` (`user_id` ASC) VISIBLE,
  PRIMARY KEY (`wish_id`),
  CONSTRAINT `fk_favorites_registered_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `wish_list_db`.`registered_users` (`id`),
  CONSTRAINT `fk_likes_wishes1`
    FOREIGN KEY (`wish_id`)
    REFERENCES `wish_list_db`.`wishes` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

