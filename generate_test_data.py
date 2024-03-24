import pandas as pd
import config


def generate_post_tag_test_data(configurations):
    ids = []
    creation_dates = []
    tags = []
    current_id = 1

    for config_item in configurations:
        year = config_item['year']
        tag_posts_dict = config_item['tag_posts_dict']

        for month in range(1, 13):
            for tag, posts_count in tag_posts_dict.items():
                for _ in range(posts_count):
                    ids.append(current_id)
                    creation_dates.append(f'{year}-{month:02d}')
                    tags.append(tag)
                    current_id += 1

    df = pd.DataFrame({
        'Id': ids,
        'CreationDate': creation_dates,
        'Tag': tags
    })

    return df


configurations = [
    {
        'year': 2020,
        'tag_posts_dict': {
            'a': 10,
            'b': 30,
            'c': 60
        }
    },
    {
        'year': 2021,
        'tag_posts_dict': {
            'a': 60,
            'b': 20,
            'c': 20
        }
    },
    {
        'year': 2021,
        'tag_posts_dict': {
            'a': 50,
            'b': 30,
            'c': 20
        }
    }
]

df_test_data = generate_post_tag_test_data(configurations)
file_path = config.get_file_path('posts_tag.csv')
df_test_data.to_csv(file_path, index=False)

print(f"Test data for specified configurations generated and saved to '{file_path}'")

#%%
