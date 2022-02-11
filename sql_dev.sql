-- Create the db : createdb -h localhost -p 5432 -U postgres testdb

SELECT * FROM boulder;

SELECT * FROM gym;

-- Get the list of created tables and indexes
SELECT *
FROM pg_catalog.pg_tables
WHERE schemaname = 'public';

SELECT *
FROM pg_catalog.pg_indexes
WHERE schemaname = 'public';


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
