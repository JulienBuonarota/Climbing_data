SELECT * FROM boulder;

SELECT * FROM test;

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
