# Blog: Exploring Stack overflow tags trends

###  Introduction
This repository contains complete code for "Exploring Stack overflow tags trends" blog post.
It consists of the following Jupyter notebooks:
- [#1_convert_xml_to_csv.ipynb](%231_convert_xml_to_csv.ipynb) - convert raw data from XML to CSV format.
- [#2_explore_data.ipynb](%232_explore_data.ipynb) - data evaluation and features selection. 
- [#3_pre_process_data.ipynb](%233_pre_process_data.ipynb) - initial calculation, like `ActivityScore`. 
- [#4_calculate_trends.ipynb](%234_calculate_trends.ipynb) - trends calculation and storage.
- [#5_show_trends.ipynb](%235_show_trends.ipynb) - trends visualisation.

### Local setup
Setup venv
`python3 -m venv exploring_so_tags_trends`

Activate venv
`source exploring_so_tags_trends/bin/activate`

Install dependencies:
`pip3 install -r requirements.txt`

### Download and unpack raw data
To reproduce analysis results, follow instructions to download raw data first.
Make sure you have ~100 GB of available disk space.  

Download archives with data dump:
```
wget https://archive.org/download/stackexchange/stackoverflow.com-Comments.7z
wget https://archive.org/download/stackexchange/stackoverflow.com-Posts.7z
wget https://archive.org/download/stackexchange/stackoverflow.com-Votes.7z
```

Install `7z` package to un-archive data:
```
sudo apt-get install p7zip-full
```

Un-archive downloaded data: 
```
7z x stackoverflow.com-Comments.7z
7z x stackoverflow.com-Posts.7z
7z x stackoverflow.com-Votes.7z
```

### How to run
Some calculations are pretty memory intensive, make sure you have at least 64 Gb of available memory.
Run notebooks one by one to get results.
