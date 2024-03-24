### Short description
Exploring top trending tags on StackOverflow by number of submitted questions, answers and votes.

### Introduction
TODO: 
- Motivation - broader picture then https://insights.stackoverflow.com/trends (not only questions)
- Source data : https://archive.org/download/stackexchange/ - various stack exchange dumps
- Implementation details are at the end; 

### Data model
TODO: 
- Data in the dump is pretty broad one, but we are interested in the following subset.
- Question - id, creation date and list of tags
- Answer - id, creation date and parent id (question id). Have no tags, but implicitly inherits them.
- Vote - up or down vote for certain post.

### Methodology

TODO:
- main metric is a tag share - inspired by "market share" (https://en.wikipedia.org/wiki/Market_share)
- Tag Rank is a position of a tag certain point of time based on its share. 
- idea is to find build trends based on speed of tag share grow over observable period of time.
- posts creation based trends - 
- votes creation based trends
- Sum up - join results find tags that ver top 20 fastest growing among two categories. 


### Posts creation trends
TODO:
- Based on posts (questions and answers) creation;
- Calculate tag share as `tag-share = tag-total-posts-created / total-posts-created * 100`
- Show sample data and charts 

### Votes trends
TODO:
- Based on posts (questions and answers) creation;
- Calculate tag share as `tag-share = tag-total-posts-created / total-posts-created * 100`
- Show sample data and charts 

### Trending tags
Bellow you can find list with details about the most trending tags for the past 3 years (tag, posts rank increase, votes rank increase)

### Implementation

100GB+ disk space.

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

### Conclusion
TODO:
- Might shed some light on tech landscape changes
- Is not a complete view.