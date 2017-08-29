# WeiboSpider
WeiboSpider written in Python to get all original texts and images of an account

## running instructions

step0: follow the comments in WeiboSpider.py carefully to get cookies and user_id and paste them into the code or to change page_start and page_end (optional)

step1: pick a folder to store all the text files and weibo_image folder

step2: cd to the directory picked

step3: open terminal: python ..../WeiboSpider.py (just drag it into terminal) (some libs may need to be installed with pip)

every oripic url and picall url will be printed in terminal

all img urls failed to download will be recorded in a new txt file

END

id.txt and id_raw.txt are the same file with different names for further changes on id.txt may be needed to do data analysis

## inspired by dingmyu/weibo_analysis

1. invalid RegExps are updated

2. libs written in python(beautifulsoup etc.) are replaced by those written in C++(re, lxml etc.) to increase efficiency

3. a new method is implemented to extract img address accessible without cookies directly from oripic url to increase efficiency 

4. the first img url in picAll page is skipped since it was already extracted in previous page

## further developments

1. implement the code to analyze url with filter=0 (all weiboes)

2. optimize data analysis process

3. make it into a lib. users only need to call a function with several parameters to do all above
