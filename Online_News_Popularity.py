#Import pandas as pd 

import pandas as pd 

import numpy as np 

import matplotlib.pyplot as plt 

 

#Reading Data 

Data = pd.read_csv('OnlineNewsPopularity.csv') 

 

#Exploring Data - head displays first n rows; columns displays the names of all the columns;  

Data.head(5) 

Data.columns 

Data[[' timedelta']] 

 

 

#Removing leading blank space from all column names 

for col in Data.columns: 

    if col[0]==" ": 

        Data.rename(columns={col:col[1:]}, inplace = True) 

     

#---------------------Removing Outliers 

#Step1: Find Median, Q1F, Q3F, Interquartile range 

Sorted_shares = Data.sort_values('shares') 

median = Sorted_shares['shares'].median() 

first_quartile = Sorted_shares['shares'].quantile(q=0.25) 

third_quartile = Sorted_shares['shares'].quantile(q=0.75) 

interquartile_range = third_quartile-first_quartile 

#Find inner fences(minor outlier) and outer fences(major outlier)        

inner_boundary1 = first_quartile-(interquartile_range*1.5) #-1835.0 

inner_boundary2 = third_quartile+(interquartile_range*1.5) #5581.0 

outer_boundary1 = first_quartile-(interquartile_range*3)   #-4616.0 

outer_boundary2 = third_quartile+(interquartile_range*3)   #8362.0 

 

#Removing the outliers 

Data_without_outliers = Data[Data["shares"]<=8362] 

mean = Data_without_outliers['shares'].mean() #Without outlier treatment, mean was 3395. Removing outliers, we get 1916 

 

 

#Number of unique values(count of total number of keywords in title) in an article's title 

Data_without_outliers.n_tokens_title.unique() 

len(Data_without_outliers.n_tokens_title.unique()) 

 

#-------------------Checking for Length of title in words vs popularity 

    #Part 1: Finding out the number of shares per disntict keyword count 

#For each token, how many articles are there? 

Title_pop_df = Data_without_outliers.loc[:,["n_tokens_title", "shares"]] 

Title_pop_df_sorted = Title_pop_df.sort_values('n_tokens_title') 

distinct_heading_keywords_count=(Title_pop_df_sorted.n_tokens_title.unique()) 

 

NumberOfShares = {} 

for token in distinct_heading_keywords_count: 

    TempDf = Title_pop_df_sorted[Title_pop_df_sorted["n_tokens_title"]==token] 

    NumberOfShares[token] = len(TempDf.n_tokens_title) 

#2, 3, 4, 17, 18, 19, 20 and 23 (first 3 and last 5 tokens in NumberOfSHares) have less than 100 articles each 

#So, removing them from this specific analysis 

DelIndices = [0,1,2,15,16,17,18,19] 

distinct_heading_keywords_count = np.delete(distinct_heading_keywords_count, DelIndices) 

    

    #Part 2: Finding the min, max, range of shares for every title_token 

Min_Max_Range = {} 

for row in distinct_heading_keywords_count:     

    df_tokenwise =  Title_pop_df_sorted[Title_pop_df_sorted["n_tokens_title"]==row] 

    Min=(df_tokenwise["shares"]).min() 

    Max=(df_tokenwise["shares"]).max() 

    Range = Max-Min 

    Avg=df_tokenwise["shares"].mean() 

    Min_Max_Range[row]=[Min, Max, Range,Avg] 

     

#Par 3 - Line Chart 

Avg_list =[] 

for token in Min_Max_Range: 

    Avg_list=Avg_list + [Min_Max_Range[token][3]] 

#plt.subplot(2,3,1) 

plt.plot(distinct_heading_keywords_count,Avg_list, color='red') 

plt.xlabel('Number of Words in Title') 

plt.ylabel('Average Shares') 

plt.title('Popularity VS Lenght of Title') 

plt.show() 

 

     

     

     

#-------------------Checking for lenght of article vs popularity 

Title_cont_df = Data_without_outliers.loc[:,["n_tokens_content", "shares"]] 

Title_cont_df_sorted = Title_cont_df.sort_values('n_tokens_content') 

distinct_content_words_count=(Title_cont_df_sorted.n_tokens_content.unique()) 

 

NumberOfShares_content = {} 

for token in distinct_content_words_count: 

    TempDf = Title_cont_df_sorted[Title_cont_df_sorted["n_tokens_content"]==token] 

    NumberOfShares_content[token] = len(TempDf.n_tokens_content) 

    

     

#Part 2: Making buckets based on the data distribtion 

articles_per_content = np.array([0,0,0,0,0,0,0,0]) 

shares_per_bucket = np.array([0,0,0,0,0,0,0,0]) 

for row in distinct_content_words_count:     

    if row < 100: 

        df_tokenwise =  Title_cont_df_sorted[Title_cont_df_sorted["n_tokens_content"]==row] 

        articles_per_content[0] = articles_per_content[0] + len(df_tokenwise.n_tokens_content) 

        shares_per_bucket[0] = shares_per_bucket[0] + df_tokenwise['shares'].sum() 

    elif row < 200:  

        df_tokenwise =  Title_cont_df_sorted[Title_cont_df_sorted["n_tokens_content"]==row] 

        articles_per_content[1] = articles_per_content[1] + len(df_tokenwise.n_tokens_content) 

        shares_per_bucket[1] = shares_per_bucket[1] + df_tokenwise['shares'].sum() 

    elif row < 300:  

        df_tokenwise =  Title_cont_df_sorted[Title_cont_df_sorted["n_tokens_content"]==row] 

        articles_per_content[2] = articles_per_content[2] + len(df_tokenwise.n_tokens_content) 

        shares_per_bucket[2] = shares_per_bucket[2] + df_tokenwise['shares'].sum() 

    elif row < 400:  

        df_tokenwise =  Title_cont_df_sorted[Title_cont_df_sorted["n_tokens_content"]==row] 

        articles_per_content[3] = articles_per_content[3] + len(df_tokenwise.n_tokens_content) 

        shares_per_bucket[3] = shares_per_bucket[3] + df_tokenwise['shares'].sum() 

    elif row < 500:  

        df_tokenwise =  Title_cont_df_sorted[Title_cont_df_sorted["n_tokens_content"]==row] 

        articles_per_content[4] = articles_per_content[4] + len(df_tokenwise.n_tokens_content) 

        shares_per_bucket[4] = shares_per_bucket[4] + df_tokenwise['shares'].sum() 

    elif row < 750:  

        df_tokenwise =  Title_cont_df_sorted[Title_cont_df_sorted["n_tokens_content"]==row] 

        articles_per_content[5] = articles_per_content[5] + len(df_tokenwise.n_tokens_content) 

        shares_per_bucket[5] = shares_per_bucket[5] + df_tokenwise['shares'].sum() 

    elif row < 1000:  

        df_tokenwise =  Title_cont_df_sorted[Title_cont_df_sorted["n_tokens_content"]==row] 

        articles_per_content[6] = articles_per_content[6] + len(df_tokenwise.n_tokens_content) 

        shares_per_bucket[6] = shares_per_bucket[6] + df_tokenwise['shares'].sum() 

    else: 

        df_tokenwise =  Title_cont_df_sorted[Title_cont_df_sorted["n_tokens_content"]==row] 

        articles_per_content[7] = articles_per_content[7] + len(df_tokenwise.n_tokens_content) 

        shares_per_bucket[7] = shares_per_bucket[7] + df_tokenwise['shares'].sum() 

 

mean_shares_per_bucket = shares_per_bucket/articles_per_content 

     

     

#Par 3 - Line Chart 

#plt.subplot(2,3,2) 

plt.plot([1,2,3,4,5,6,7,8],mean_shares_per_bucket, color='blue') 

plt.xticks([1,2,3,4,5,6,7,8], ['<100','100-200','200-300','300-400','400-500','500-750','750-1000','>1000']) 

plt.xlabel('Number of Words in Article') 

plt.ylabel('Average Shares') 

plt.title('Popularity VS Length of Article') 

plt.show() 

plt.clf() 

plt.cla() 

 

 

 

 

 

#--------------------popularity vs number of images and videos in the article 

len(Data_without_outliers.num_imgs.unique()) 

len(Data_without_outliers.num_videos.unique()) 

 

Imgs_df = Data_without_outliers.loc[:,["num_imgs","shares"]] 

Videos_df = Data_without_outliers.loc[:,["num_videos","shares"]] 

Imgs_df_sorted = Imgs_df.sort_values('num_imgs') 

Videos_df_sorted = Videos_df.sort_values('num_videos') 

distinct_imgs_count=(Imgs_df_sorted.num_imgs.unique()) 

distinct_videos_count=(Videos_df_sorted.num_videos.unique()) 

 

 

NumberOfShares_imgs = {} 

for token in distinct_imgs_count: 

    TempDf = Imgs_df_sorted[Imgs_df_sorted["num_imgs"]==token] 

    NumberOfShares_imgs[token] = len(TempDf.num_imgs) 

     

NumberOfShares_videos = {} 

for token in distinct_videos_count: 

    TempDf = Videos_df_sorted[Videos_df_sorted["num_videos"]==token] 

    NumberOfShares_videos[token] = len(TempDf.num_videos) 

 

     

#Part 2I: Making buckets for images 

Imgs_per_content = np.array([0,0,0,0,0]) 

shares_per_bucket = np.array([0,0,0,0,0]) 

for row in distinct_imgs_count:     

    if row == 0: 

        df_tokenwise =  Imgs_df_sorted[Imgs_df_sorted["num_imgs"]==row] 

        Imgs_per_content[0] = Imgs_per_content[0] + len(df_tokenwise.num_imgs) 

        shares_per_bucket[0] = shares_per_bucket[0] + df_tokenwise['shares'].sum() 

    elif row == 1:  

        df_tokenwise =  Imgs_df_sorted[Imgs_df_sorted["num_imgs"]==row] 

        Imgs_per_content[1] = Imgs_per_content[1] + len(df_tokenwise.num_imgs) 

        shares_per_bucket[1] = shares_per_bucket[1] + df_tokenwise['shares'].sum() 

    elif row >1 and row <=10 :  

        df_tokenwise =  Imgs_df_sorted[Imgs_df_sorted["num_imgs"]==row] 

        Imgs_per_content[2] = Imgs_per_content[2] + len(df_tokenwise.num_imgs) 

        shares_per_bucket[2] = shares_per_bucket[2] + df_tokenwise['shares'].sum() 

    elif row >10 and row <=25:  

        df_tokenwise =  Imgs_df_sorted[Imgs_df_sorted["num_imgs"]==row] 

        Imgs_per_content[3] = Imgs_per_content[3] + len(df_tokenwise.num_imgs) 

        shares_per_bucket[3] = shares_per_bucket[3] + df_tokenwise['shares'].sum() 

    else: 

        df_tokenwise =  Imgs_df_sorted[Imgs_df_sorted["num_imgs"]==row] 

        Imgs_per_content[4] = Imgs_per_content[4] + len(df_tokenwise.num_imgs) 

        shares_per_bucket[4] = shares_per_bucket[4] + df_tokenwise['shares'].sum() 

 

mean_shares_per_bucket = shares_per_bucket/Imgs_per_content 

     

     

#Par 3I - Line Chart 

#plt.subplot(2,3,3) 

plt.plot([1,2,3,4,5],mean_shares_per_bucket, color='green') 

plt.xticks([1,2,3,4,5], ['0','1','1-10','10-25','>25']) 

plt.xlabel('Number of Images in Article') 

plt.ylabel('Average Shares') 

plt.title('Popularity VS Number of Images in Article') 

plt.show() 

 

 

 

#Part 2V: Making buckets for Videos 

Videos_per_content = np.array([0,0,0,0,0]) 

shares_per_bucket = np.array([0,0,0,0,0]) 

for row in distinct_videos_count:     

    if row == 0: 

        df_tokenwise =  Videos_df_sorted[Videos_df_sorted["num_videos"]==row] 

        Videos_per_content[0] = Videos_per_content[0] + len(df_tokenwise.num_videos) 

        shares_per_bucket[0] = shares_per_bucket[0] + df_tokenwise['shares'].sum() 

    elif row == 1:  

        df_tokenwise =  Videos_df_sorted[Videos_df_sorted["num_videos"]==row] 

        Videos_per_content[1] = Videos_per_content[1] + len(df_tokenwise.num_videos) 

        shares_per_bucket[1] = shares_per_bucket[1] + df_tokenwise['shares'].sum() 

    elif row >1 and row <=5 :  

        df_tokenwise =  Videos_df_sorted[Videos_df_sorted["num_videos"]==row] 

        Videos_per_content[2] = Videos_per_content[2] + len(df_tokenwise.num_videos) 

        shares_per_bucket[2] = shares_per_bucket[2] + df_tokenwise['shares'].sum() 

    elif row >5 and row <=10:  

        df_tokenwise =  Videos_df_sorted[Videos_df_sorted["num_videos"]==row] 

        Videos_per_content[3] = Videos_per_content[3] + len(df_tokenwise.num_videos) 

        shares_per_bucket[3] = shares_per_bucket[3] + df_tokenwise['shares'].sum() 

    else: 

        df_tokenwise =  Videos_df_sorted[Videos_df_sorted["num_videos"]==row] 

        Videos_per_content[4] = Videos_per_content[4] + len(df_tokenwise.num_videos) 

        shares_per_bucket[4] = shares_per_bucket[4] + df_tokenwise['shares'].sum() 

 

mean_shares_per_bucket = shares_per_bucket/Videos_per_content 

     

     

#Par 3V - Line Chart 

#plt.subplot(2,3,4) 

plt.plot([1,2,3,4,5],mean_shares_per_bucket, color='cyan') 

plt.xticks([1,2,3,4,5], ['0','1','1-5','5-10','>10']) 

plt.xlabel('Number of Videos in Article') 

plt.ylabel('Average Shares') 

plt.title('Popularity VS Number of Videos in Article') 

plt.show() 

 

 

 

#--------------------Popularity vs Category 

#There are 6 categories in the data - Lifestyle, Entertainment, Business, Social Media, Tech, World. All these articles are columns, and if an article belongs to any of these, we'll have a 1 under that. Otherwise, it will be 0 

Ctgr = ["data_channel_is_lifestyle","data_channel_is_entertainment","data_channel_is_bus","data_channel_is_socmed","data_channel_is_tech","data_channel_is_world"] 

 

Avg_per_category = [] 

for category in Ctgr: 

    Temp_df = Data_without_outliers.loc[:, [category,"shares"]] 

    Temp_df = Temp_df[Temp_df[category]==1] 

    Avg_per_category.append(Temp_df["shares"].mean()) 

 

#Plotting categories and popularity     

#plt.subplot(2,3,5) 

plt.plot([1,2,3,4,5,6],Avg_per_category, color='magenta') 

plt.xticks([1,2,3,4,5,6], ["Lifestyle","Entertainment","Business", "Social Media", "Tech", "World"]) 

plt.xlabel('Category of Article') 

plt.ylabel('Average Shares') 

plt.title('Popularity VS Category of Article') 

plt.show() 

 

 

 

#------------------------------------------------------popularity vs Weekday 

Days = ["weekday_is_monday","weekday_is_tuesday","weekday_is_wednesday","weekday_is_thursday","weekday_is_friday","weekday_is_saturday","weekday_is_sunday","is_weekend"] 

 

Avg_per_day = [] 

for day in Days: 

    Temp_df = Data_without_outliers.loc[:, [day,"shares"]] 

    Temp_df = Temp_df[Temp_df[day]==1] 

    Avg_per_day.append(Temp_df["shares"].mean()) 

 

#Plotting categories and popularity     

#plt.subplot(2,3,6) 

plt.plot([1,2,3,4,5,6,7,8],Avg_per_day, color='black') 

plt.xticks([1,2,3,4,5,6,7,8], ["Mon","Tue","Wed", "Thu", "Fri", "Sat","Sun","Wknd"]) 

plt.xlabel('Day of Publication of Article') 

plt.ylabel('Average Shares') 

plt.title('Popularity VS Day of Publication of Article') 

plt.show() 

plt.clf() 

 

 

 

 

##########----------------------------Show graphs 

#plt.tight_layout() 

#plt.show() 

#plt.clf() 