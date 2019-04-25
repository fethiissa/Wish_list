-- -----------------------------------------------------
-- Table `mydb`.`belts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`belts` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `color` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`dojos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`dojos` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL DEFAULT NULL,
  `address` VARCHAR(255) NULL DEFAULT NULL,
  `city` VARCHAR(45) NULL DEFAULT NULL,
  `zipcode` CHAR(22) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`ninjas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`ninjas` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `dojo_id` INT(11) NOT NULL,
  `first_name` VARCHAR(255) NULL DEFAULT NULL,
  `last_name` VARCHAR(255) NULL DEFAULT NULL,
  `address` VARCHAR(255) NULL DEFAULT NULL,
  `city` VARCHAR(45) NULL DEFAULT NULL,
  `zipcode` CHAR(22) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NULL,
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_ninjas_dojos1_idx` (`dojo_id` ASC) VISIBLE,
  CONSTRAINT `fk_ninjas_dojos1`
    FOREIGN KEY (`dojo_id`)
    REFERENCES `mydb`.`dojos` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`belt_certifications`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`belt_certifications` (
  `id` VARCHAR(45) NOT NULL,
  `belt_id` INT(11) NOT NULL,
  `ninja_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_belts_has_ninjas_ninjas1_idx` (`ninja_id` ASC) VISIBLE,
  INDEX `fk_belts_has_ninjas_belts1_idx` (`belt_id` ASC) VISIBLE,
  CONSTRAINT `fk_belts_has_ninjas_belts1`
    FOREIGN KEY (`belt_id`)
    REFERENCES `mydb`.`belts` (`id`),
  CONSTRAINT `fk_belts_has_ninjas_ninjas1`
    FOREIGN KEY (`ninja_id`)
    REFERENCES `mydb`.`ninjas` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`books`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`books` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NULL DEFAULT NULL,
  `author` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`categories` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`products` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`categories_has_products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`categories_has_products` (
  `category_id` INT(11) NOT NULL,
  `product_id` INT(11) NOT NULL,
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  INDEX `fk_categories_has_products_products1_idx` (`product_id` ASC) VISIBLE,
  INDEX `fk_categories_has_products_categories1_idx` (`category_id` ASC) VISIBLE,
  CONSTRAINT `fk_categories_has_products_categories1`
    FOREIGN KEY (`category_id`)
    REFERENCES `mydb`.`categories` (`id`),
  CONSTRAINT `fk_categories_has_products_products1`
    FOREIGN KEY (`product_id`)
    REFERENCES `mydb`.`products` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`clientele`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`clientele` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL DEFAULT NULL,
  `email` VARCHAR(255) NULL DEFAULT NULL,
  `phone_number` VARCHAR(255) NULL DEFAULT NULL,
  `favorite_dish` VARCHAR(255) NULL DEFAULT NULL,
  `created_id` DATETIME NULL DEFAULT NULL,
  `updated_id` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`customers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`customers` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL DEFAULT NULL,
  `email` VARCHAR(255) NULL DEFAULT NULL,
  `phone_number` VARCHAR(255) NULL DEFAULT NULL,
  `favorite_dish` VARCHAR(255) NULL DEFAULT NULL,
  `created_id` DATETIME NULL DEFAULT NULL,
  `updated_id` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`dishes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`dishes` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  `main_ingredient` VARCHAR(45) NULL DEFAULT NULL,
  `prep_time` INT(11) NULL DEFAULT NULL,
  `non_GMO` TINYINT(3) UNSIGNED NOT NULL DEFAULT '1' COMMENT '0 - non GMO\\n1 - may contain GMO',
  `created_id` DATETIME NULL DEFAULT NULL,
  `updated_id` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`customers_fav_dishes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`customers_fav_dishes` (
  `customer_id` INT(11) NOT NULL,
  `dish_id` INT(11) NOT NULL,
  PRIMARY KEY (`customer_id`, `dish_id`),
  INDEX `fk_customers_has_dishes_dishes1_idx` (`dish_id` ASC) VISIBLE,
  INDEX `fk_customers_has_dishes_customers_idx` (`customer_id` ASC) VISIBLE,
  CONSTRAINT `fk_customers_has_dishes_customers`
    FOREIGN KEY (`customer_id`)
    REFERENCES `mydb`.`customers` (`id`),
  CONSTRAINT `fk_customers_has_dishes_dishes1`
    FOREIGN KEY (`dish_id`)
    REFERENCES `mydb`.`dishes` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`foodmenu`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`foodmenu` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `client_id` INT(11) NOT NULL,
  `name` VARCHAR(45) NULL DEFAULT NULL,
  `main_ingredient` VARCHAR(45) NULL DEFAULT NULL,
  `prep_time` INT(11) NULL DEFAULT NULL,
  `non_GMO` TINYINT(3) UNSIGNED NOT NULL DEFAULT '1' COMMENT '0 - non GMO\\n1 - may contain GMO',
  `created_id` DATETIME NULL DEFAULT NULL,
  `updated_id` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_foodmenu_clientele1_idx` (`client_id` ASC) VISIBLE,
  CONSTRAINT `fk_foodmenu_clientele1`
    FOREIGN KEY (`client_id`)
    REFERENCES `mydb`.`clientele` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `favorites` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `mydb`.`users_fav_books`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`users_fav_books` (
  `id` INT(11) NOT NULL,
  `users_id` INT(11) NOT NULL,
  `books_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_users_has_books_books1_idx` (`books_id` ASC) VISIBLE,
  INDEX `fk_users_has_books_users1_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_books_books1`
    FOREIGN KEY (`books_id`)
    REFERENCES `mydb`.`books` (`id`),
  CONSTRAINT `fk_users_has_books_users1`
    FOREIGN KEY (`users_id`)
    REFERENCES `mydb`.`users` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

