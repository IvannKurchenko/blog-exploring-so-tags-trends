## Exploring StackOverflow tags trends

### Short description
Exploring top trending tags on StackOverflow by number of submitted questions, answers and votes.

### Introduction
[Stackoverflow Trends](https://insights.stackoverflow.com/trends) is a great place to see how progress of certain tag
over time. However, it provides possibility to show trends for requested tags. Primary motivation of this post is to
explore and compare all tags trends between each other for past several years, to find the most rapidly growing.

For this we are going to use ["Stack Exchange Data Dump" published to Internet Archive](https://archive.org/details/stackexchange)
that contains various data dumps for whole "Stack Exchange" websites family. In particular, we are going to use posts and votes data.
First we will start with some high level ideas, then proceed to data explosion, later show found results and cover some implementation details at the end.   
All analysis was done using Python, Jupyter, Pandas, NumPy and matplotlib. In the most important parts of code are present, but unnecessary details are omitted for readability. 

### Available data
Stack Exchange data dump is a pretty broad one and covers all sorts of data related to users, activity etc. 
For more details, you can see the data set description at [readme.txt](https://ia904700.us.archive.org/6/items/stackexchange/readme.txt) file.

First of all, we need to choose data that will be used to gain understanding about tags popularity.
Tag popularity can be identified as a summary of all activity related to a tag. For instance, asking a question,
answering a question, commenting on a post and voting for a post.

At first glance, we can consider the following data files and fields as candidates for such analysis:
`Posts.xml` - posts data. Following fields can be used:   
```
- Id 
- PostTypeId
  - 1: Question
  - 2: Answer
- ParentId (only present if PostTypeId is 2)
- CreationDate 
- DeletionDate
- ClosedDate, e.g.:"2009-03-11T12:51:01.480" 
- Tags
- Score
- ViewCount
- AnswerCount
- CommentCount
- FavoriteCount
```

`Votes.xml` - post votes data. Following fields can be used:
``` 
- Id 
- PostId 
- VoteTypeId
  - 1: AcceptedByOriginator
  - 2: UpMod (upvote)
  - 3: DownMod (downvote)
  - 4: Offensive
  - 5: Favorite - if VoteTypeId = 5 UserId will be populated
  - 6: Close
  - 7: Reopen
  - 8: BountyStart
  - 9: BountyClose
  - 10: Deletion
  - 11: Undeletion
  - 12: Spam
  - 13: InformModerator
  - 15: ModeratorReview
  - 16: ApproveEditSuggestion
- CreationDate
```

`Comments.xml` - posts comments data. Following fields can be used:
```
- Id
- PostId 
- Score 
- CreationDate, e.g.:"2008-09-06T08:07:10.730" 
```

It is easy to notice that supplied data has some redundancy:
- `Posts.xml - Score` - is a sum of all votes that are also stored in `Votes.xml` file.
- `Posts.xml - AnswerCount` - is a sum of all answer posts (e.g. `PostTypeId = 2`) for a question, that contains in same file.
- `Posts.xml - CommentCount` - is a sum of all comments that are also stored in `Comments.xml` file.

We can use either history of some activity, like voting via `Votes.xml` or its result in `Posts.xml - Score`.
Later in the post, we will find that using resulting numbers could be an option to go. 

### Initial data selection
It looks like a lot of dimensions to use for further analysis. Let's try to discover whether we can reduce its number.  

We can begin from finding proportion of `Posts` which are marked as favorite, have comments, views and have scores.
In other words, find number of posts which fields `FavoriteCount`, `CommentCount`, `ViewCount`, `Score` are greater than 0.
Aside note: `Score` less than 0, means that it received votes, but negative one. Nonetheless, for simplicity lets consider positively voted posts only.

Calculations logic looks in the following way: 
```python
posts_size = posts_df.size
favorited_posts_size = posts_df[posts_df['FavoriteCount'] > 0.0].size
commented_posts_size = posts_df[posts_df['CommentCount'] > 0.0].size
viewed_posts_size = posts_df[posts_df['ViewCount'] > 0.0].size
scored_posts_size = posts_df[posts_df['Score'] > 0.0].size

favorited_posts_proportion = favorited_posts_size / posts_size
commented_posts_proportion = commented_posts_size / posts_size
viewed_posts_proportion = viewed_posts_size / posts_size
scored_posts_proportion = scored_posts_size / posts_size

print(f"All Posts: {posts_size:,}")
print(f"Favorited Posts: {favorited_posts_size:,} ({favorited_posts_proportion:.2%})")
print(f"Commented Posts: {commented_posts_size:,} ({commented_posts_proportion:.2%})")
print(f"Viewed Posts: {viewed_posts_size:,} ({viewed_posts_proportion:.2%})")
print(f"Scored Posts: {scored_posts_size:,} ({scored_posts_proportion:.2%})")
```

And results are:
```
All Posts: 657,239,539
Favorited Posts: 1,518 (0.00%)
Commented Posts: 331,794,034 (50.48%)
Viewed Posts: 264,899,404 (40.30%)
Scored Posts: 358,470,134 (54.54%)
```
`FavoriteCount` does not look like a strong signal, and it can be easily neglected.

One more approach for dimensionality reduction is to find correlation.
```python
posts_df[['CommentCount', 'ViewCount', 'Score']].corr().to_markdown()
```

Bellow is the correlation matrix between three remaining fields:

|              |   CommentCount |   ViewCount |     Score |
|:-------------|---------------:|------------:|----------:|
| CommentCount |     1          |  0.00796425 | 0.0839743 |
| ViewCount    |     0.00796425 |  1          | 0.761194  |
| Score        |     0.0839743  |  0.761194   | 1         |

As you can see, `Score` and `ViewCount` has pretty strong correlation of slightly more than 76%, which means that one of them can be ignored.
Since there is a historical data for `Score` in `Votes.xml` file, but not for `ViewCount`, the former field can be eliminated.\

### Result numbers versus history
As a result of previous steps, we have the following signals to use for tag trend:
- Posts creation - present in `Posts.xml` file and `CreationDate` field;
- Votes creation - present in: 
  - `Votes.xml` file and `CreationDate` field;
  - `Posts.xml` file and `Score` field that reflects the sum all votes;
- Comments creation - present in: 
  - `Comments.xml` file and `CreationDate` field;
  - `Posts.xml` file and `CommentCount` field that number of all comments;

There is an overlap in between votes and comments history and summary numbers in the scope of a post.
So which one shall the history of voting or commenting be taken into account?

Let's begin with votes and see what is the dynamics of voting. To make it we can calculate the date difference between post `CreationDate` and votes `CreationDate`:
```python
posts_votes_df = pd.merge(posts_creation_df, votes_creation_df, left_on='Id', right_on='PostId', suffixes=('_post', '_vote'))
votes_months_difference_seq = ((posts_votes_df['CreationDate_vote'] - posts_votes_df['CreationDate_post']).dt.days / 30).round()
months_difference_counts = months_difference_seq.value_counts(normalize=True) * 100
print(months_difference_counts.head(10))
```

Results are following:
```
-0.0     31.868489
 1.0      1.590028
 2.0      1.144887
 4.0      1.003856
 3.0      0.978432
 6.0      0.962302
 8.0      0.926534
 10.0     0.920690
 5.0      0.913960
 12.0     0.903898
```

Which also can visualise via `matplotlib`:
![votes_creation_duration.png](images%2Fvotes_creation_duration.png)
Not a lot of surprise to see [long tail](https://en.wikipedia.org/wiki/Long_tail) in this distribution. 
Nearly `30%` of votes were given in the first month of post existence.

Now we can discover dynamics for posts commenting.
```python
posts_comments_df = pd.merge(posts_creation_df, comments_creation_df, left_on='Id', right_on='PostId', suffixes=('_post', '_comment'))
comments_months_difference_seq = ((posts_comments_df['CreationDate_comment'] - posts_comments_df['CreationDate_post']).dt.days / 30).round()
comments_months_difference_counts = comments_months_difference_seq.value_counts(normalize=True) * 100
print(comments_months_difference_counts.head(10))
```

Prints the following:
```
0.0     90.935936
1.0      0.911582
2.0      0.438805
3.0      0.318881
4.0      0.291622
5.0      0.244062
6.0      0.240956
8.0      0.210341
7.0      0.209174
10.0     0.192652
```
And visualise all numbers by using `matplotlib`:
![comments_creation_duration.png](images%2Fcomments_creation_duration.png)

A pretty similar picture can be seen for comments. A major `90%` of comments were created in the first month.

Bottom line:  to take votes and comments into account `CommentCount` and `Score` fields from `Posts.xml` file are going to be used instead of respective history for each activity.

### Methodology

#### Metrics
Since we selected data to work with, we can proceed to actual trend calculations.
The main idea is to build trends based on the speed of tag growth over some observable period, for instance, 3 years.

#### Activity score
First, let's introduce a notion of the main metric which will be used to identify tag growth as 
```
ActivityScore = Score + CommentCount + 1
```
where `Score`, `CommentCount` are fields from `Posts.xml` and `+1` identifies a fact of created posts (to cover the case of a post without votes and comments).
`ActivityScore` as the name and definition say, sums up all activity around the tag in the scope of a post.

#### Tag share
At this step, we can proceed to describe to main metric for which trend or trajectory will be calculated. The naive approach might be to calculate the sum of `ActivityScore` over time for a certain tag.
However, absolute numbers do not reflect comparison. That's why we need some relative metric, which can be called tag-share, similar to well-known [Market share](https://en.wikipedia.org/wiki/Market_share) definition.
In terms of `ActivityScore` it can be expressed as:
```
TagShare = TagTotlaActivityScore / TotalActivityScore * 100
```
where `TagTotalActivityScore` is a cumulative sum of `ActivityScore` for a certain tag and `TotalActivityScore` is a cumulative sum of `ActivityScore` for all posts up until a certain point in time.

#### Tag rank
Although `TagShare` reflects relative tag activity another helpful metric could `TagRank` ,which is a position of a tag certain point in time based on its `TagShare`.
It is [available in Pandas](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.core.window.rolling.Rolling.rank.html) so pretty easy to calculate.

#### Trending tags
Now we can proceed to the most interesting part and see the top 20 most trending tags for the past 3 years in terms of `TagShare` increase:

| Tag                  | StartTagShare | EndTagShare | TagShareDelta | StartTagRank | EndTagRank | TagRankDelta |
|----------------------|---------------|-------------|---------------|--------------|------------|--------------|
| python               | 8.810830      | 9.339611    | 0.528781      | 2.0          | 2.0        | -0.0         |
| reactjs              | 1.241718      | 1.588594    | 0.346876      | 28.0         | 20.0       | 8.0          |
| flutter              | 0.436962      | 0.641511    | 0.204549      | 80.0         | 57.0       | 23.0         |
| typescript           | 0.805759      | 0.961976    | 0.156217      | 42.0         | 38.0       | 4.0          |
| pandas               | 0.952074      | 1.098120    | 0.146046      | 37.0         | 33.0       | 4.0          |
| r                    | 1.613965      | 1.758538    | 0.144573      | 19.0         | 19.0       | -0.0         |
| node.js              | 1.796068      | 1.894887    | 0.098818      | 18.0         | 18.0       | -0.0         |
| dart                 | 0.304894      | 0.399665    | 0.094771      | 121.0        | 90.0       | 31.0         |
| python-3.x           | 0.982737      | 1.077354    | 0.094617      | 36.0         | 34.0       | 2.0          |
| dataframe            | 0.502394      | 0.594033    | 0.091639      | 64.0         | 59.0       | 5.0          |
| kotlin               | 0.289945      | 0.374375    | 0.084430      | 130.0        | 97.0       | 33.0         |
| spring-boot          | 0.384552      | 0.460593    | 0.076042      | 92.0         | 71.0       | 21.0         |
| next.js              | 0.032364      | 0.101599    | 0.069234      | 1107.0       | 354.0      | 753.0        |
| react-native         | 0.379365      | 0.447968    | 0.068603      | 95.0         | 78.0       | 17.0         |
| docker               | 0.609848      | 0.677211    | 0.067362      | 57.0         | 53.0       | 4.0          |
| amazon-web-services  | 0.477610      | 0.543093    | 0.065484      | 70.0         | 63.0       | 7.0          |
| visual-studio-code   | 0.274666      | 0.335564    | 0.060898      | 136.0        | 111.0      | 25.0         |
| vue.js               | 0.299155      | 0.358858    | 0.059704      | 126.0        | 103.0      | 23.0         |
| firebase             | 0.389395      | 0.442814    | 0.053419      | 89.0         | 81.0       | 8.0          |
| swiftui              | 0.096526      | 0.148999    | 0.052473      | 398.0        | 253.0      | 145.0        |


`TagShare` dynamics over time looks following:
![tag_share_trends.png](images%2Ftag_share_trends.png)

`TagRank` timeline for these tags: 
![tag_rank_trends.png](images%2Ftag_rank_trends.png)

### Conclusion
Stackoverflow tags trends might shad some light on tech trends using numbers. 
If you want to explore trend for your favorite topic, you can find data set with calculated metrics at [Kaggle](https://www.kaggle.com/datasets/ivankurchenko/stackoverflow-tags-trends)
and the complete code with instructions at [GitHub](https://github.com/IvannKurchenko/blog-exploring-so-tags-trends).