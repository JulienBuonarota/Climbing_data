library(DBI)
con <- dbConnect(RPostgres::Postgres(),dbname = 'ClimbingGymDB', 
                 host = 'localhost',
                 port = 5432,
                 user = 'climbing_data',
                 password = 'admin')


query <- "
SELECT
	*
FROM
	boulder
WHERE
	gym_id !=1
	or (gym_id = 1 and date_opened > '2022-01-01')
ORDER BY
  gym_id,
  CASE
	WHEN grade = 'yellow' THEN 1
	WHEN grade = 'green' THEN 2
	WHEN grade = 'blue' THEN 3
	WHEN grade = 'red' THEN 4
	WHEN grade = 'black' THEN 5
	ELSE 6
	END;"
res <- dbSendQuery(con, query)
boulders <- dbFetch(res)

library(ggplot2)
# color palet corresponding to boulder difficulties
# lock grade color order
grade_order <- rev(c("yellow", "green", "blue", "red", "black", "purple"))
boulders$factor_grade <- factor(boulders$grade, levels=grade_order)

ggplot(data=boulders) + 
  geom_bar(mapping=aes(x=gym_id, fill=factor_grade)) + 
  scale_fill_manual(values=grade_order)
