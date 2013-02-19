SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

CREATE SCHEMA IF NOT EXISTS `ccdb` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci ;
USE `ccdb` ;

-- -----------------------------------------------------
-- Table `ccdb`.`Tracks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccdb`.`Tracks` ;

CREATE  TABLE IF NOT EXISTS `ccdb`.`Tracks` (
  `trackid` INT NOT NULL AUTO_INCREMENT ,
  `is_crawled` INT NOT NULL DEFAULT 0 ,
  `track_name` VARCHAR(45) NOT NULL ,
  `artist_name` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`trackid`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ccdb`.`User`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccdb`.`User` ;

CREATE  TABLE IF NOT EXISTS `ccdb`.`User` (
  `userid` INT NOT NULL AUTO_INCREMENT ,
  `user_name` VARCHAR(45) NOT NULL ,
  `is_crawled` INT NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`userid`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ccdb`.`User_Listens_Tracks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccdb`.`User_Listens_Tracks` ;

CREATE  TABLE IF NOT EXISTS `ccdb`.`User_Listens_Tracks` (
  `user_userid` INT NOT NULL ,
  `tracks_trackid` INT NOT NULL ,
  PRIMARY KEY (`user_userid`, `tracks_trackid`) )
ENGINE = InnoDB;

CREATE INDEX `fk_fan_has_Tracks_Tracks1` ON `ccdb`.`User_Listens_Tracks` (`tracks_trackid` ASC) ;

CREATE INDEX `fk_fan_has_Tracks_fan1` ON `ccdb`.`User_Listens_Tracks` (`user_userid` ASC) ;


-- -----------------------------------------------------
-- Table `ccdb`.`User_Loves_Tracks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccdb`.`User_Loves_Tracks` ;

CREATE  TABLE IF NOT EXISTS `ccdb`.`User_Loves_Tracks` (
  `user_userid` INT NOT NULL ,
  `tracks_trackid` INT NOT NULL ,
  PRIMARY KEY (`user_userid`, `tracks_trackid`) )
ENGINE = InnoDB;

CREATE INDEX `fk_fan_has_Tracks_Tracks2` ON `ccdb`.`User_Loves_Tracks` (`tracks_trackid` ASC) ;

CREATE INDEX `fk_fan_has_Tracks_fan2` ON `ccdb`.`User_Loves_Tracks` (`user_userid` ASC) ;


-- -----------------------------------------------------
-- Table `ccdb`.`User_Bans_Tracks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccdb`.`User_Bans_Tracks` ;

CREATE  TABLE IF NOT EXISTS `ccdb`.`User_Bans_Tracks` (
  `user_userid` INT NOT NULL ,
  `tracks_trackid` INT NOT NULL ,
  PRIMARY KEY (`user_userid`, `tracks_trackid`) )
ENGINE = InnoDB;

CREATE INDEX `fk_fan_has_Tracks_Tracks3` ON `ccdb`.`User_Bans_Tracks` (`tracks_trackid` ASC) ;

CREATE INDEX `fk_fan_has_Tracks_fan3` ON `ccdb`.`User_Bans_Tracks` (`user_userid` ASC) ;


-- -----------------------------------------------------
-- Table `ccdb`.`User_Shouts_Tracks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccdb`.`User_Shouts_Tracks` ;

CREATE  TABLE IF NOT EXISTS `ccdb`.`User_Shouts_Tracks` (
  `user_userid` INT NOT NULL ,
  `tracks_trackid` INT NOT NULL ,
  PRIMARY KEY (`user_userid`, `tracks_trackid`) )
ENGINE = InnoDB;

CREATE INDEX `fk_fan_has_Tracks_Tracks4` ON `ccdb`.`User_Shouts_Tracks` (`tracks_trackid` ASC) ;

CREATE INDEX `fk_fan_has_Tracks_fan4` ON `ccdb`.`User_Shouts_Tracks` (`user_userid` ASC) ;


-- -----------------------------------------------------
-- Table `ccdb`.`Tags`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccdb`.`Tags` ;

CREATE  TABLE IF NOT EXISTS `ccdb`.`Tags` (
  `tagid` INT NOT NULL ,
  `tag_text` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`tagid`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ccdb`.`Tracks_Has_Tags`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccdb`.`Tracks_Has_Tags` ;

CREATE  TABLE IF NOT EXISTS `ccdb`.`Tracks_Has_Tags` (
  `tracks_trackid` INT NOT NULL ,
  `tags_tagid` INT NOT NULL ,
  PRIMARY KEY (`tracks_trackid`, `tags_tagid`) )
ENGINE = InnoDB;

CREATE INDEX `fk_Tracks_has_Tags_Tags1` ON `ccdb`.`Tracks_Has_Tags` (`tags_tagid` ASC) ;

CREATE INDEX `fk_Tracks_has_Tags_Tracks1` ON `ccdb`.`Tracks_Has_Tags` (`tracks_trackid` ASC) ;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
