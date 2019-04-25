CREATE TABLE IF NOT EXISTS `employee_jobs_db`.`jobs` (
  `id` INT(10) NOT NULL AUTO_INCREMENT,
  `assigned_to_id` INT(11) NULL DEFAULT NULL,
  `title` VARCHAR(65) CHARACTER SET 'utf8' COLLATE 'utf8_general_ci' NOT NULL,
  `location` VARCHAR(65) CHARACTER SET 'utf8' COLLATE 'utf8_general_ci' NOT NULL,
  `posted_by_id` INT(11) NOT NULL,
  `job_desc` TEXT CHARACTER SET 'utf8' COLLATE 'utf8_general_ci' NOT NULL,
  `job_category` TEXT CHARACTER SET 'utf8' COLLATE 'utf8_general_ci' NULL DEFAULT NULL,
  `other` TEXT NULL DEFAULT NULL,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_jobs_registered_users1`
    FOREIGN KEY (`assigned_to_id`)
    REFERENCES `employee_jobs_db`.`registered_users` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 44
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE INDEX `fk_jobs_registered_users1_idx` ON `employee_jobs_db`.`jobs` (`assigned_to_id` ASC) VISIBLE;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;