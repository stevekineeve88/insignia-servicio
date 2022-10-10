CREATE TABLE action (
  id INT NOT NULL AUTO_INCREMENT,
  uuid BINARY(16) DEFAULT (uuid_to_bin(uuid())),
  const VARCHAR(100) NOT NULL,
  description VARCHAR(255) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE INDEX `action_const_UNIQUE` (`const` ASC),
  UNIQUE INDEX `action_uuid_UNIQUE` (`uuid` ASC)
);

CREATE TABLE role (
  id INT NOT NULL AUTO_INCREMENT,
  uuid BINARY(16) DEFAULT (uuid_to_bin(uuid())),
  const VARCHAR(100) NOT NULL,
  description VARCHAR(255) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE INDEX `role_const_UNIQUE` (`const` ASC),
  UNIQUE INDEX `role_uuid_UNIQUE` (`uuid` ASC)
);

CREATE TABLE role_group (
  id INT NOT NULL AUTO_INCREMENT,
  uuid BINARY(16) DEFAULT (uuid_to_bin(uuid())),
  const VARCHAR(100) NOT NULL,
  description VARCHAR(255) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE INDEX `role_group_const_UNIQUE` (`const` ASC),
  UNIQUE INDEX `role_group_uuid_UNIQUE` (`uuid` ASC)
);