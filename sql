CREATE TABLE `huobi`.`tick_one_min` (
  `tick_id` INT NOT NULL,
  `count` VARCHAR(45) NULL,
  `vol` VARCHAR(45) NULL,
  `high` VARCHAR(45) NULL,
  `amount` VARCHAR(45) NULL,
  `low` VARCHAR(45) NULL,
  `close` VARCHAR(45) NULL,
  `open` VARCHAR(45) NULL,
  PRIMARY KEY (`tick_id`));