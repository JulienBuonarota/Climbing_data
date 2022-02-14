-- Create the db : createdb -h localhost -p 5432 -U postgres testdb

SELECT * FROM boulder;

SELECT * FROM gym;

SELECT * FROM gym_map_section;

SELECT * FROM gym_image;

SELECT * FROM boulder_point;
SELECT * FROM boulder_like;

SELECT * FROM boulder_completion;

SELECT * FROM boulder_comment;

	
FROM boulder;
-- Get the list of created tables and indexes
SELECT *
FROM pg_catalog.pg_tables
WHERE schemaname = 'public';

SELECT *
FROM pg_catalog.pg_indexes
WHERE schemaname = 'public';

CREATE TABLE IF NOT EXISTS map_section
        (id serial PRIMARY KEY,
        gym_id int REFERENCES gym(id),
        map_section PATH);

-- Add values
INSERT INTO boulder
VALUES (12, 'purple', '2', 1, ((62, 46), (73, 46), (73, 52)), ('100%\xa0Volumes', 'Powerful'), '2021-12-21', Null, 0, 0, 700, 0, 'https://socialboulder.s3-eu-west-1.amazonaws.com/800/bouldersPics/cycKwGkY3oeqBPtpK.jpg');

-- Delete table
DROP TABLE boulders;

-- create table
CREATE TABLE IF NOT EXISTS boulder 
        (id serial   PRIMARY KEY,
        grade	     text,
        sub_grade    text,
        gym_id 	     smallint,
        map_section  path,
        tag 	     text[],
        date_opened  date,
        date_closed  date,
        nb_like      smallint,
        nb_comment   smallint,
        point 	     smallint,
        nb_completion smallint,
        img_url      text);
	
SELECT *
FROM boulder;

INSERT INTO boulder(grade, sub_grade, gym_id, map_section, tag, date_opened, date_closed, nb_like, nb_comment, point, nb_completion, img_url)
VALUES ('purple', '2', 1, CAST('((62, 46), (73, 46), (73, 52))' AS PATH),
'{"100%\xa0Volumes", "Powerful"}', '2021-12-21', Null, 0, 0, 700, 0,
'https://socialboulder.s3-eu-west-1.amazonaws.com/800/bouldersPics/cycKwGkY3oeqBPtpK.jpg');

CREATE TABLE IF NOT EXISTS gym
        (id serial PRIMARY KEY,
	gym_name    text,
        city 	    text,
        address     text
	scrape_on boolean);


SELECT *
FROM gym;


INSERT INTO gym(gym_name, city, address, social_boulder_url, scrape_on)
VALUES ('arkose_nation','paris','35 Rue des Grands Champs, Paris, FR 75020','https://www.sboulder.com/arkose/nation',TRUE);



INSERT INTO boulder(grade, sub_grade, gym_id, map_section, tag, date_opened, date_closed, nb_like, nb_comment, point, nb_completion, img_url)
VALUES
('purple',
'2',
(SELECT id FROM gym WHERE gym_name = 'arkose_nation'),
CAST('((62, 46), (73, 46), (73, 52))' AS PATH),
'{"100%\xa0Volumes", "Powerful"}',
'2021-12-21', Null, 0, 0, 700, 0,
'https://socialboulder.s3-eu-west-1.amazonaws.com/800/bouldersPics/cycKwGkY3oeqBPtpK.jpg');

INSERT INTO boulder(grade, sub_grade, gym_id, map_section_id, tag, date_opened, date_closed, img_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""

INSERT INTO gym_map_section(gym_id, map_section)
VALUES (1, '((47, 35), (37, 39))')
RAISE warning 'Duplicate user ID', USING ERRCODE = 'unique_constraint';


INSERT INTO gym_image(gym_id, img_url, os_path_to_img)
VALUES (1, 'https://socialboulder.s3-eu-west-1.amazonaws.com/800/bouldersPics/cycKwGkY3oeqBPtpK.jpg', NULL);


INSERT INTO boulder(grade, sub_grade, gym_id, map_section_id, tag, date_opened, date_closed, img_id)
VALUES ('purple', '2',
       (SELECT id FROM gym WHERE gym.gym_name = 'arkose_nation'),
       (SELECT id FROM gym_map_section WHERE gym_map_section.map_section = '((62, 46), (73, 46), (73, 52))'),
       '{"100%\xa0Volumes", "Powerful"}', '2021-12-21', NULL,
       (SELECT id FROM gym_image
       WHERE
         gym_image.gym_id = 1 AND gym_image.img_url = 'https://socialboulder.s3-eu-west-1.amazonaws.com/800/bouldersPics/cycKwGkY3oeqBPtpK.jpg'));


DELETE FROM boulder
WHERE grade = 'purple';

DELETE FROM gym_image
WHERE gym_id = 1;

DELETE FROM gym_map_section
WHERE gym_id = 1;





INSERT INTO boulder(grade, sub_grade, gym_id, map_section_id, tag, date_opened, date_closed, img_id)
                VALUES (%s, %s,
                       (SELECT id FROM gym WHERE gym.gym_name = %s),
                       (SELECT id FROM gym_map_section WHERE gym_map_section.map_section = %s),
                       %s, %s, %s,
                       (SELECT id FROM gym_image
                       WHERE
                         gym_image.gym_id = %s AND gym_image.img_url = %s));


INSERT INTO boulder(grade, sub_grade, gym_id, map_section_id, img_id)
SELECT
	'LOLpurple',
	'4',
	gym.id AS gym_id,
	gym_map_section.id AS gym_map_section_id,
	gym_image.id AS gym_image_id
FROM gym
INNER JOIN gym_map_section
      ON gym.id = gym_map_section.gym_id
INNER JOIN gym_image
      ON gym.id = gym_image.gym_id
WHERE
	gym.gym_name = 'arkose'
	AND gym_map_section.map_section = '((47, 35), (37, 39))'
	AND gym_image.img_url = 'https://socialboulder.s3-eu-west-1.amazonaws.com/800/bouldersPics/RWR7rcRpctRNsAinj.jpg';

SELECT id
FROM boulder
WHERE
	grade = 'purple'
	AND sub_grade = '4'
	AND gym_id = 1
	AND map_section_id = (SELECT id FROM gym_map_section WHERE gym_map_section.map_section = '((47, 35), (37, 39))')
	AND tag = '{Volumes, Complex, Technical}'
	AND date_opened = '2021-12-14'
	AND img_id = 24;

SELECT * FROM boulder_like;

DELETE FROM boulder_like
WHERE id = 1;

INSERT INTO boulder_like(boulder_id, registration_date, nb_like)
VALUES (8, '2022-02-14', 0);

	

	
