CREATE TABLE IF NOT EXISTS `users` (
	`id`	INTEGER(128) NOT NULL PRIMARY KEY AUTO_INCREMENT UNIQUE,
	`name`	TEXT(128) NOT NULL,
	`email`	TEXT(128) NOT NULL,
	`username`	TEXT(128) NOT NULL,
	`password`	TEXT(128) NOT NULL
);
INSERT INTO `users` VALUES (1,'Noam Annenberg','noam.annenberg@gmail.com','noamannenberg','$5$rounds=535000$c1.QS5zHPAbGAfLU$z7hUMpgmLmfarU4RaF1Yp3deVl6bOWP132LRVMHNT07');
INSERT INTO `users` VALUES (2,'David Friedenberg','friedenberg12@gmail.com','friedenberg12','$5$rounds=535000$6BVIwH1Yz9VBFEgy$6MirGjCAEZgzkM742jw/TZg8T5Hk2ivUJHlAPbhHZl4');
INSERT INTO `users` VALUES (3,'Jason Goolamadeen','GoolamadeenJ@gmail.com','JaceGrants','$5$rounds=535000$vGWXMKRI7sJ9Gq/L$dGdmUz6YOTLZR6bht78US4QJwtvk4G9PqLkRDTWTdgD');
INSERT INTO `users` VALUES (4,'Adam Berkowitz','adam@gmail.com','Adam B','$5$rounds=535000$QRc9z3deEHFjyuHq$szVi2KB7w.MhKvFvaE7H5oHEQWEQdAwPB.i6ASZiYV8');
INSERT INTO `users` VALUES (5,'Bobbyo Johnson','bob@johnson.com','bobby','$5$rounds=535000$r4XjiJP9p57sxXRv$MiPZc/JGtcQokoy8dGIgDQAEDQcDK4Njp66f66SIfO0');
CREATE TABLE IF NOT EXISTS `proposals` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
	`userid`	INTEGER NOT NULL,
	`title`	TEXT NOT NULL,
	`amount`	TEXT NOT NULL,
	`description`	TEXT NOT NULL,
	`tags`	TEXT NOT NULL,
	`location`	TEXT NOT NULL
);
INSERT INTO `proposals` VALUES (1,1,'Food for YuHacks','500','Yu Hacks needs more food','education','new york');
INSERT INTO `proposals` VALUES (2,1,'Raspberry Pi','1000','We want Raspberry pis!','hardware','new jersey');
INSERT INTO `proposals` VALUES (3,2,'Big Project','500','This is a big project you should do!','project math','Miami');
INSERT INTO `proposals` VALUES (4,3,'Building a school','400+','I want to build school for my village','education','Thailand');
INSERT INTO `proposals` VALUES (5,4,'Young people coding','250','We want to code and coffee costs money.','coding coffee money','New Jersey');
CREATE TABLE IF NOT EXISTS `grants` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
	`userid`	INTEGER NOT NULL,
	`amount`	INTEGER NOT NULL,
	`description`	TEXT NOT NULL,
	`tags`	TEXT NOT NULL,
	`location`	TEXT NOT NULL
);
INSERT INTO `grants` VALUES (1,1,500,'hi i like comp sci','computerscience','new york');
INSERT INTO `grants` VALUES (2,1,2000,'for yu hack food','education','new york');
INSERT INTO `grants` VALUES (5,2,100,'i like math','math','New York');
INSERT INTO `grants` VALUES (6,3,500,'Build a mini classroom out of clay','education','Thailand');
INSERT INTO `grants` VALUES (7,4,1000,'Young people willing to learn coding.','coding young people','New York');
INSERT INTO `grants` VALUES (8,5,1000,'I like hardware education and computers, so i''ll give you money!','hardware education computer','Georgia');
COMMIT;
