CREATE TABLE edits ( e_item INT, e_property INT, e_value VARCHAR(255), e_datatype INT, e_source INT, e_job INT, e_status INT);
/*
e_datatype
  1 - wikibase-item
  2 - string
  3 - commonsMedia
*/
/*
e_status
  0 - pending
  1 - done
  2 - already done
  -1 - error
*/
ALTER TABLE `edits` ADD id MEDIUMINT PRIMARY KEY NOT NULL AUTO_INCREMENT FIRST;
CREATE TABLE sources ( s_property INT, s_value VARCHAR(255), s_datatype INT);
ALTER TABLE `sources` ADD id MEDIUMINT PRIMARY KEY NOT NULL AUTO_INCREMENT FIRST;
CREATE TABLE jobs (j_properties VARCHAR(225), j_values VARCHAR(255), j_source VARCHAR(3000), j_raw VARCHAR(3000), j_user VARCHAR(255), j_timestamp TIMESTAMP, j_status INT);
ALTER TABLE `jobs` ADD id MEDIUMINT PRIMARY KEY NOT NULL AUTO_INCREMENT FIRST;
/*
j_status
  -1 - deleted/rejected
  0 - pending approval
  1 - in progress
  2 - done
*/