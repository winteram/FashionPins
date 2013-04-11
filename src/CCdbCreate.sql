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
  `track_name` VARCHAR(255) NOT NULL ,
  `artist_name` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`trackid`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ccdb`.`User`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccdb`.`User` ;

CREATE  TABLE IF NOT EXISTS `ccdb`.`User` (
  `userid` INT NOT NULL AUTO_INCREMENT ,
  `user_name` VARCHAR(255) NOT NULL ,
  `is_crawled` INT NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`userid`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ccdb`.`user_listens_tracks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccdb`.`user_listens_tracks` ;

CREATE  TABLE IF NOT EXISTS `ccdb`.`user_listens_tracks` (
  `user_userid` INT NOT NULL ,
  `tracks_trackid` INT NOT NULL ,
  PRIMARY KEY (`user_userid`, `tracks_trackid`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ccdb`.`user_loves_tracks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccdb`.`user_loves_tracks` ;

CREATE  TABLE IF NOT EXISTS `ccdb`.`user_loves_tracks` (
  `user_userid` INT NOT NULL ,
  `tracks_trackid` INT NOT NULL ,
  `lovedate` DATE NULL ,
  PRIMARY KEY (`user_userid`, `tracks_trackid`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ccdb`.`user_bans_tracks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccdb`.`user_bans_tracks` ;

CREATE  TABLE IF NOT EXISTS `ccdb`.`user_bans_tracks` (
  `user_userid` INT NOT NULL ,
  `tracks_trackid` INT NOT NULL ,
  `bandate` DATE NULL ,
  PRIMARY KEY (`user_userid`, `tracks_trackid`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ccdb`.`user_shouts_tracks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccdb`.`user_shouts_tracks` ;

CREATE  TABLE IF NOT EXISTS `ccdb`.`user_shouts_tracks` (
  `user_userid` INT NOT NULL ,
  `tracks_trackid` INT NOT NULL ,
  PRIMARY KEY (`user_userid`, `tracks_trackid`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ccdb`.`Tags`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccdb`.`Tags` ;

CREATE  TABLE IF NOT EXISTS `ccdb`.`Tags` (
  `tagid` INT NOT NULL ,
  `tag_text` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`tagid`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ccdb`.`tracks_has_tags`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccdb`.`tracks_has_tags` ;

CREATE  TABLE IF NOT EXISTS `ccdb`.`tracks_has_tags` (
  `tracks_trackid` INT NOT NULL AUTO_INCREMENT ,
  `tags_tagid` INT NOT NULL ,
  PRIMARY KEY (`tracks_trackid`, `tags_tagid`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ccdb`.`user_has_friends`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccdb`.`user_has_friends` ;

CREATE  TABLE IF NOT EXISTS `ccdb`.`user_has_friends` (
  `User_userid` INT NOT NULL ,
  `User_userid1` INT NOT NULL ,
  PRIMARY KEY (`User_userid`, `User_userid1`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ccdb`.`user_recent_tracks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccdb`.`user_recent_tracks` ;

CREATE  TABLE IF NOT EXISTS `ccdb`.`user_recent_tracks` (
  `User_userid` INT NOT NULL ,
  `Tracks_trackid` INT NOT NULL ,
  `date` DATE NULL )
ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
