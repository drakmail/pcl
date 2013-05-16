SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';


-- -----------------------------------------------------
-- Table `users`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `users` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `login` VARCHAR(64) NOT NULL ,
  `email` VARCHAR(255) NOT NULL ,
  `screenname` VARCHAR(64) NULL ,
  `password` VARCHAR(255) NOT NULL ,
  `register_date` INT NOT NULL ,
  `real_name` VARCHAR(255) NULL ,
  `city` VARCHAR(255) NULL ,
  `country` TEXT NULL ,
  `os` TEXT NULL ,
  `pc_config` TEXT NULL ,
  `activated` TINYINT(1) NOT NULL DEFAULT False ,
  PRIMARY KEY (`id`) ,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tournaments`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `tournaments` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `tournament_name` VARCHAR(255) NOT NULL ,
  `tournament_type` SMALLINT NOT NULL ,
  `tournament_open_timestamp` INT NOT NULL ,
  `tournament_due_timestamp` INT NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tournaments_types`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `tournaments_types` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `tournament_type_name` VARCHAR(255) NOT NULL ,
  `starting_score` INT NOT NULL DEFAULT 5000 ,
  `won_score` SMALLINT NOT NULL DEFAULT 50 ,
  `deuce_score` SMALLINT NOT NULL DEFAULT 25 ,
  `loose_score` SMALLINT NOT NULL DEFAULT 0 ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `teams`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `teams` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `team_name` VARCHAR(255) NOT NULL ,
  `created_by_user` INT NOT NULL ,
  `team_tag` VARCHAR(20) NOT NULL ,
  `team_description` TEXT NOT NULL ,
  `team_http_address` VARCHAR(255) NOT NULL ,
  `team_irc_channel` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`id`) ,
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `tournaments_participation`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `tournaments_participation` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `tournament_id` INT NOT NULL ,
  `team_id` INT NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `users_teams_participation`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `users_teams_participation` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `team_id` INT NOT NULL ,
  `user_id` INT NOT NULL ,
  `participation_type` INT NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `users_team_participation_types`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `users_team_participation_types` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `type_name` VARCHAR(255) NOT NULL ,
  `can_invite` TINYINT(1) NOT NULL ,
  `can_war_arrange` TINYINT(1) NOT NULL ,
  `can_admin` TINYINT(1) NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `matches`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `matches` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `tournament_id` INT NOT NULL ,
  `team1` INT NOT NULL ,
  `team2` INT NOT NULL ,
  `map1` INT NOT NULL ,
  `map2` INT NOT NULL ,
  `map3` INT NULL DEFAULT NULL ,
  `score1` VARCHAR(255) NOT NULL ,
  `score2` VARCHAR(255) NOT NULL ,
  `score3` VARCHAR(255) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `demos`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `demos` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `match_id` INT NOT NULL ,
  `user_id` INT NOT NULL ,
  `demo_type` SMALLINT NOT NULL ,
  `demo_name` TEXT NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `demos_types`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `demos_types` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `name` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `maps`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `maps` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `name` VARCHAR(255) NOT NULL ,
  `desctription` TEXT NULL DEFAULT NULL ,
  `screenshot` TEXT NULL DEFAULT NULL ,
  `path` TEXT NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `users_groups`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `users_groups` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `group_name` VARCHAR(45) NULL ,
  `group_color` VARCHAR(45) NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `users_groups_permissions`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `users_groups_permissions` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `group_id` INT NOT NULL ,
  `can_admin` TINYINT(1) NOT NULL DEFAULT False ,
  `can_moderate` TINYINT(1) NOT NULL DEFAULT False ,
  `can_accept_matchresults` TINYINT(1) NOT NULL DEFAULT False ,
  `can_edit_matchresults` TINYINT(1) NOT NULL DEFAULT False ,
  `can_create_matches` TINYINT(1) NOT NULL DEFAULT False ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `activations`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `activations` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `user_id` INT NOT NULL ,
  `hash` VARCHAR(255) NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
