## Introduction

### Why
https://insights.stackoverflow.com/trends?tags=r%2Cstatistics shows statistics but it is not complete and only 
for tags that chosen by user. We want to have broader picture. 

### What we are going to do?
Calculate SO tags trends for long (-3y), mid (-2y) and short (-1y) term perspective. Based on them trying to predict further development for
next period or calculate trajectory (e.g. via linear regression).
SO trends could be a helpful source of understanding of tech industry development and trends.

### How we are going to do?
Methodology
get treds for certain tag (technology, topic etc) by number of created posts and upvotes count.
https://insights.stackoverflow.com/trends?tags=r%2Cstatistics - calculate only relative size questions.
Questions might not complete whole history:
- Answers show interests;
- Up-votes show interest around those who is looking for them;

To compare apples to apples we can introduce trend score as average of relative sizes for all three signals.

Describe how we are going to calculate trends. Describe what are the options (e.g. count by posts, views, votes etc)
and why the path was chosen.

Post data - use creation date (for questions and answers) to aggregate number of posts created per month and year and tag.
then calculate relative position, relative size of each tag per all created posts till that point.
Choose top 10 tags that increased over time the most.

Votes data - similarly to Posts - join with posts to get tags info.
then agg by month, year and tag. Choose top 10 tags that increased over time the most.
Choose top 10 tags that increased over time the most.

Explain why view count and favorites are not taken into account:
- For simplicity()
- Correlates (show);


## Get the data

### Environment
Any in theory. This one was executed in Vertex AI GCP Notebooks workbench on instance type `n2d-standard-2`. 

### Download the data
Check available disk space: 
```shell
! df . -h
```

You need to have 100GB+ disk space.

Source: https://archive.org/download/stackexchange/
Download posts :
```shell
wget https://archive.org/download/stackexchange/stackoverflow.com-Posts.7z/
```

Download votes :
```shell
wget https://archive.org/download/stackexchange/stackoverflow.com-Votes.7z
```

Download read me with documentation:
```shell
wget https://archive.org/download/stackexchange/readme.txt
```

Install tool to unpack 7z archive:
```shell
sudo apt-get update
sudo apt-get install p7zip-full
```

Unpack posts archive:
```shell
7z x stackoverflow.com-Posts.7z
```

Unpack votes archive:
```shell
7z x stackoverflow.com-Votes.7z
```

## Prepare raw data 
TODO :
- For pandas we need csv and not xml;
- we need only certain attributes so others will be filtered.
- convert one to another and filter data we don't need;
put code of a whole notebook;

## Trends by the number of created posts
TODO turn tags to list 
Filter - deleted, closed + shows % for each to understand how many data we filter out.
remove DeletionDate, ClosedDate columns
split posts dataframe on answers dataframe (has tags) and questions (no tags)
Parse - tags as a list
explode dataframe by tags
join questions with answers based on question.ParentId and answer.Id
select for questions all fields with tag
union questions and answers
create dataframe by tag count - aggregate by creation month-year and tag, count
create dataframe total count - aggregate by creation month-year, count
calculate relative size for each tag at each month-year.
calculate rank for each tag and each month-year. (window - year month, sort by relative size - function rank for tag)
Aggregate by tag and collect list of relative sizes, ranks and total count per each year month (sorted chronologically)
Find those tags for each change in three periods (-3y, -2y, -1y) is the biggest in terms of relative size.
print them


## Trends by the number of up-votes

## Wrap up
Overlaps between categories
save all calculations to the file and give access on the github


## Summary
TODO CODE LINK CODE TO DATA
SHOW HOW OTHERS CAN EXPLORE TRENDS FOR THEIR TAG OR TAGS 