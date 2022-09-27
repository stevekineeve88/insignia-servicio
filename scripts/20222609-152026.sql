CREATE TABLE role_group_role (
  id INT NOT NULL AUTO_INCREMENT,
  role_group_id INT NOT NULL,
  role_id INT NOT NULL,
  uuid BINARY(16) DEFAULT (uuid_to_bin(uuid())),
  PRIMARY KEY (id),
  UNIQUE INDEX `role_group_role_role_group_id_role_id_UNIQUE` (`role_group_id` ASC, `role_id` ASC),
  UNIQUE INDEX `role_group_role_uuid_UNIQUE` (`uuid` ASC),
  INDEX `role_group_role_role_group_id_fk` (`role_group_id` ASC),
  CONSTRAINT `role_group_role_role_group_id_fk`
    FOREIGN KEY (`role_group_id`)
    REFERENCES `role_group` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  INDEX `role_group_role_role_id_fk` (`role_id` ASC),
  CONSTRAINT `role_group_role_role_id_fk`
    FOREIGN KEY (`role_id`)
    REFERENCES `role` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE role_group_role_action (
  id INT NOT NULL AUTO_INCREMENT,
  role_group_role_id INT NOT NULL,
  action_id INT NOT NULL,
  uuid BINARY(16) DEFAULT (uuid_to_bin(uuid())),
  PRIMARY KEY (id),
  UNIQUE INDEX `role_group_role_action_role_group_role_id_action_id_UNIQUE` (`role_group_role_id` ASC, `action_id` ASC),
  UNIQUE INDEX `role_group_role_action_uuid_UNIQUE` (`uuid` ASC),
  INDEX `role_group_role_action_role_group_role_id_fk` (`role_group_role_id` ASC),
  CONSTRAINT `role_group_role_action_role_group_role_id_fk`
    FOREIGN KEY (`role_group_role_id`)
    REFERENCES `role_group_role` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  INDEX `role_group_role_action_action_id_fk` (`action_id` ASC),
  CONSTRAINT `role_group_role_action_action_id_fk`
    FOREIGN KEY (`action_id`)
    REFERENCES `action` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);