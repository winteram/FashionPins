SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';


-- -----------------------------------------------------
-- Table `ccdb`.`Tracks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccdb`.`Tracks` ;

CREATE  TABLE IF NOT EXISTS `ccdb`.`Tracks` (
  `trackid` INT NOT NULL ,
  `is_crawled` INT NULL ,
  PRIMARY KEY (`trackid`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ccdb`.`artist`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccdb`.`artist` ;

CREATE  TABLE IF NOT EXISTS `ccdb`.`artist` (
  `artistid` INT NOT NULL ,
  PRIMARY KEY (`artistid`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ccdb`.`Tracks_has_artist`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccdb`.`Tracks_has_artist` ;

CREATE  TABLE IF NOT EXISTS `ccdb`.`Tracks_has_artist` (
  `Tracks_trackid` INT NOT NULL ,
  `artist_artistid` INT NOT NULL ,
  PRIMARY KEY (`Tracks_trackid`, `artist_artistid`) ,
  CONSTRAINT `fk_Tracks_has_artist_Tracks`
    FOREIGN KEY (`Tracks_trackid` )
    REFERENCES `ccdb`.`Tracks` (`trackid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Tracks_has_artist_artist1`
    FOREIGN KEY (`artist_artistid` )
    REFERENCES `ccdb`.`artist` (`artistid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_Tracks_has_artist_artist1` ON `ccdb`.`Tracks_has_artist` (`artist_artistid` ASC) ;

CREATE INDEX `fk_Tracks_has_artist_Tracks` ON `ccdb`.`Tracks_has_artist` (`Tracks_trackid` ASC) ;


-- -----------------------------------------------------
-- Table `ccdb`.`fan`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccdb`.`fan` ;

CREATE  TABLE IF NOT EXISTS `ccdb`.`fan` (
  `fanid` INT NOT NULL ,
  `fan_name` VARCHAR(45) NULL ,
  PRIMARY KEY (`fanid`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `ccdb`.`fan_listens_Tracks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccdb`.`fan_listens_Tracks` ;

CREATE  TABLE IF NOT EXISTS `ccdb`.`fan_listens_Tracks` (
  `fan_fanid` INT NOT NULL ,
  `Tracks_trackid` INT NOT NULL ,
  PRIMARY KEY (`fan_fanid`, `Tracks_trackid`) ,
  CONSTRAINT `fk_fan_has_Tracks_fan1`
    FOREIGN KEY (`fan_fanid` )
    REFERENCES `ccdb`.`fan` (`fanid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_fan_has_Tracks_Tracks1`
    FOREIGN KEY (`Tracks_trackid` )
    REFERENCES `ccdb`.`Tracks` (`trackid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_fan_has_Tracks_Tracks1` ON `ccdb`.`fan_listens_Tracks` (`Tracks_trackid` ASC) ;

CREATE INDEX `fk_fan_has_Tracks_fan1` ON `ccdb`.`fan_listens_Tracks` (`fan_fanid` ASC) ;


-- -----------------------------------------------------
-- Table `ccdb`.`fan_loves_Tracks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccdb`.`fan_loves_Tracks` ;

CREATE  TABLE IF NOT EXISTS `ccdb`.`fan_loves_Tracks` (
  `fan_fanid` INT NOT NULL ,
  `Tracks_trackid` INT NOT NULL ,
  PRIMARY KEY (`fan_fanid`, `Tracks_trackid`) ,
  CONSTRAINT `fk_fan_has_Tracks_fan2`
    FOREIGN KEY (`fan_fanid` )
    REFERENCES `ccdb`.`fan` (`fanid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_fan_has_Tracks_Tracks2`
    FOREIGN KEY (`Tracks_trackid` )
    REFERENCES `ccdb`.`Tracks` (`trackid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_fan_has_Tracks_Tracks2` ON `ccdb`.`fan_loves_Tracks` (`Tracks_trackid` ASC) ;

CREATE INDEX `fk_fan_has_Tracks_fan2` ON `ccdb`.`fan_loves_Tracks` (`fan_fanid` ASC) ;


-- -----------------------------------------------------
-- Table `ccdb`.`fan_bans_Tracks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccdb`.`fan_bans_Tracks` ;

CREATE  TABLE IF NOT EXISTS `ccdb`.`fan_bans_Tracks` (
  `fan_fanid` INT NOT NULL ,
  `Tracks_trackid` INT NOT NULL ,
  PRIMARY KEY (`fan_fanid`, `Tracks_trackid`) ,
  CONSTRAINT `fk_fan_has_Tracks_fan3`
    FOREIGN KEY (`fan_fanid` )
    REFERENCES `ccdb`.`fan` (`fanid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_fan_has_Tracks_Tracks3`
    FOREIGN KEY (`Tracks_trackid` )
    REFERENCES `ccdb`.`Tracks` (`trackid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_fan_has_Tracks_Tracks3` ON `ccdb`.`fan_bans_Tracks` (`Tracks_trackid` ASC) ;

CREATE INDEX `fk_fan_has_Tracks_fan3` ON `ccdb`.`fan_bans_Tracks` (`fan_fanid` ASC) ;


-- -----------------------------------------------------
-- Table `ccdb`.`fan_shouts_Tracks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccdb`.`fan_shouts_Tracks` ;

CREATE  TABLE IF NOT EXISTS `ccdb`.`fan_shouts_Tracks` (
  `fan_fanid` INT NOT NULL ,
  `Tracks_trackid` INT NOT NULL ,
  PRIMARY KEY (`fan_fanid`, `Tracks_trackid`) ,
  CONSTRAINT `fk_fan_has_Tracks_fan4`
    FOREIGN KEY (`fan_fanid` )
    REFERENCES `ccdb`.`fan` (`fanid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_fan_has_Tracks_Tracks4`
    FOREIGN KEY (`Tracks_trackid` )
    REFERENCES `ccdb`.`Tracks` (`trackid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_fan_has_Tracks_Tracks4` ON `ccdb`.`fan_shouts_Tracks` (`Tracks_trackid` ASC) ;

CREATE INDEX `fk_fan_has_Tracks_fan4` ON `ccdb`.`fan_shouts_Tracks` (`fan_fanid` ASC) ;


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
-- Table `ccdb`.`Tracks_has_Tags`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `ccdb`.`Tracks_has_Tags` ;

CREATE  TABLE IF NOT EXISTS `ccdb`.`Tracks_has_Tags` (
  `Tracks_trackid` INT NOT NULL ,
  `Tags_tagid` INT NOT NULL ,
  PRIMARY KEY (`Tracks_trackid`, `Tags_tagid`) ,
  CONSTRAINT `fk_Tracks_has_Tags_Tracks1`
    FOREIGN KEY (`Tracks_trackid` )
    REFERENCES `ccdb`.`Tracks` (`trackid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Tracks_has_Tags_Tags1`
    FOREIGN KEY (`Tags_tagid` )
    REFERENCES `ccdb`.`Tags` (`tagid` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

CREATE INDEX `fk_Tracks_has_Tags_Tags1` ON `ccdb`.`Tracks_has_Tags` (`Tags_tagid` ASC) ;

CREATE INDEX `fk_Tracks_has_Tags_Tracks1` ON `ccdb`.`Tracks_has_Tags` (`Tracks_trackid` ASC) ;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
