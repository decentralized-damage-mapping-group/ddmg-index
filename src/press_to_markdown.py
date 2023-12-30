#!/usr/bin/env python
# coding: utf-8

# In[83]:


import os
import pandas as pd
from tqdm import tqdm


# In[84]:


src_data = '/Users/coreyscher/Documents/GitHub/ddmg-index/src/etc/press.csv'
dest_dir = '/Users/coreyscher/Documents/GitHub/ddmg-index/content/press'


# In[92]:


# read in csv

df = pd.read_csv(src_data,  parse_dates= ['date'])

# list all subdirs in press directory

dirs = [x[0] for x in os.walk(dest_dir)][1:]


#add subsir column to df

df['datestr'] = df['date'].astype(str) + 'T00:00:00Z'
df['subdir'] = dest_dir + "/" + df['datestr'].str.split('T').str[0] + '-' + df['pub_short']

# filter dataframe for subdirs that are not already in the directory

filtered_df = df[df['subdir'].isin(dirs) == False]

print('Adding ' +str(len(filtered_df))+ ' new media articles')

# Markdown content template
markdown_content_template = """
---
title: "{title}"

date: '{date}'

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ['1']

# Publication name and optional abbreviated publication name.
publication: In *{pub}*
publication_short: In *{pub}*

abstract: {pub}

tags: [gaza]

# Display this page in the Featured widget?
featured: false

# Custom links (uncomment lines below)
links:
  - name: Article
    url: {url}

# url_pdf: ''
# url_code: ''
# url_dataset: ''
# url_poster: ''
# url_project: ''
# url_slides: ''
# url_source: ''
# url_video: ''

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.

# Associated Projects (optional).
#   Associate this publication with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `internal-project` references `content/project/internal-project/index.md`.
#   Otherwise, set `projects: []`.
projects: []
# projects:
#  - example

---
"""

# Iterate over rows and create Markdown files
for index, row in tqdm(filtered_df.iterrows()):
    title = row['title']
    url = row['url']
    date = row['datestr']
    pub = row['pub']
    pub_short = row['pub_short']
    subdir = row['subdir']

    # Format the date as needed
    # You may want to use datetime functions for more advanced date formatting

    # Fill out the Markdown content template
    markdown_content = markdown_content_template.format(title=title, 
                                                        url=url, 
                                                        date=date, 
                                                        pub= pub, 
                                                        pub_short = pub_short)

    # File path
    folder_path = f"{date + '-' + pub_short}" 
    
    try:
        # make the subdirectory
        os.makedirs(subdir)
        file_path = os.path.join(subdir, 'index.md')
        # Open the file in write mode and write the content
        with open(file_path, "w", encoding="utf-8") as markdown_file:
            markdown_file.write(markdown_content)
    except:
        continue


