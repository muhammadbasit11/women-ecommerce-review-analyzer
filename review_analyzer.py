import pandas as pd
import matplotlib.pyplot as plt

class ReviewAnalyzer:
    def __init__(self,file_path):
        self.df=pd.read_csv(file_path)
        self.clean_data()
        self.analyze_data()
        self.analyze_text()
        self.visualize_data()

    def clean_data(self):
        print(f"BEFORE CLEANING:{self.df.shape}")
        data=self.df.copy()
        data=data.drop(columns=["Unnamed: 0"])
        data=data.dropna(subset=["Review Text","Division Name"])
        data["Title"]=data["Title"].fillna("No Title")
        data=data.drop_duplicates()
        print(f"AFTER CLEANING:{data.shape}")
        self.cleaned_df=data
    def analyze_data(self):
        #AVERAGE OF RATING
        self.avg_rating=self.cleaned_df["Rating"].mean()
        print(f"THE AVERAGE RATING IS {self.avg_rating}")

        # RATING RANGE

        self.rating_range=self.cleaned_df["Rating"].value_counts()
        self.rating_range=self.rating_range.reset_index()
        print(self.rating_range)

        ##AVERAGE RATING BY DEPARTMENT

        self.average_rating_department=self.cleaned_df.groupby("Department Name")["Rating"].mean().reset_index()
        print(self.average_rating_department) 
        
        #NUMBER OF PEOPLE RECOMMENDER VS NOT RECMENDED
        recommended=self.cleaned_df["Recommended IND"].value_counts()
        self.recommended_percentage=(int(recommended[1])/len(self.cleaned_df)*100)
        self.not_recommended_percentage=(int(recommended[0])/len(self.cleaned_df)*100)
        print(f"THE PERCENTAGE OF PEOPLE RECOMMENDED PRODUCTS:{self.recommended_percentage}%")
        print(f"THE PERCENTAGE OF PEOPLE NOT RECOMMENDED PRODUCTS:{self.not_recommended_percentage}%")

        #MOST REVIEWED GROUP AGES
        bins=[0,30,40,50,60,float("inf")]
        labels=["20s","30s","40s","50s","60+"]
        self.cleaned_df["Age Group"]=pd.cut(self.cleaned_df["Age"],bins=bins,labels=labels,right=False)
        self.review_by_age_group=self.cleaned_df.groupby("Age Group")["Review Text"].count()
        self.most_review_age=self.review_by_age_group.idxmax()
        print(f"THE MOST REVIEW GIVING AGE_GROUP IS:{self.most_review_age}")

    def analyze_text(self):
        # split the data into two groups:
        neg_data=self.cleaned_df[(self.cleaned_df["Rating"]>=1) & (self.cleaned_df["Rating"]<3)]
        pos_data=self.cleaned_df[(self.cleaned_df["Rating"]>=4) & (self.cleaned_df["Rating"]<=5)]
        # combine all review text in each group into one big string
        pos_reviews_text=pos_data["Review Text"]
        all_pos_text=" ".join(pos_reviews_text)
        neg_reviews_text=neg_data["Review Text"]
        all_neg_text=" ".join(neg_reviews_text)
        #convert to lowercase and split into individual words
        all_pos_text=all_pos_text.lower().split()
        all_neg_text=all_neg_text.lower().split()

        #  remove common useless words called stopwords
        print("before removing useless words",len(all_pos_text))
        stopwords ={"the","a","and","is","it","i","to","was","this",
                "my","in","of","for","so","but","are","with",
                "have","had","not","on","at","be","as","that","they"}

        clean_words_pos=[word for word in all_pos_text if word not in stopwords]
        clean_words_neg=[word for word in all_neg_text if word not in stopwords]
        print("AFTER removing useless words",len(clean_words_pos))

        #count word frequencies using a dictionary
        def word_frequency(clean_data):
            word_frequencies={}
            for word in clean_data:
                word_frequencies[word]=word_frequencies.get(word,0)+1
                    
            return word_frequencies
        self.pos_word_frequency=word_frequency(clean_words_pos)
        self.neg_word_frequency=word_frequency(clean_words_neg)

        #  top 10 words for positive reviews and top 10 for negative reviews
        self.sorted_frequencies_positive=sorted(self.pos_word_frequency.items(),key=lambda x:x[1],reverse=True)[0:10]
        self.sorted_frequencies_negative=sorted(self.neg_word_frequency.items(),key=lambda x:x[1],reverse=True)[0:10]
        #IT SORT BY THE COUNT
        print(f"THE POSITIVE REVIEWS WORD FREQUENCY IS\n{self.sorted_frequencies_positive}")
        print(f"\nTHE NAGATIVE REVIEWS WORD FREQUENCY IS\n{self.sorted_frequencies_negative}")


     
    def visualize_data(self):

        fig, axes = plt.subplots(2, 3, figsize=(18, 10)) 
        fig.suptitle("Women's E-Commerce Review Dashboard", fontsize=16)
        #Bar chart — Rating distribution (how many reviews per star rating)
        axes[0,0].bar(self.rating_range["Rating"],self.rating_range["count"])
        axes[0,0].set_xlabel("Rating")
        axes[0,0].set_ylabel("Count")
        axes[0][0].set_title("Rating Distribution")

        #Horizontal bar chart — Average rating by Department
        axes[0,1].barh(self.average_rating_department["Department Name"],self.average_rating_department["Rating"])
        axes[0,1].set_title("Average Rating by Department")
        axes[0,1].set_xlabel("RATINGS")
        axes[0,1].set_ylabel("DEPARTMENT")

        #Pie chart — Recommended vs Not Recommended percentage
        percentages=[self.not_recommended_percentage,self.recommended_percentage]
        labels=["NON-RECOMMENDED","RECOMMENDED"]
        axes[0,2].pie(percentages,labels=labels,autopct='%1.1f%%')
        axes[0,2].set_title("RECOMMENDED VS NOT-RECOMMENDED")

        #Bar chart — Review count by Age Group
        axes[1,0].bar(self.review_by_age_group.index,self.review_by_age_group.values)
        axes[1,0].set_title("Reviews by Age Group")
        axes[1,0].set_xlabel("AGE GROUP")
        axes[1,0].set_ylabel("NO.OF REVIEWS")
        

        #Bar chart — Top 10 positive words vs top 10 negative words side by side
        words,counts=zip(*self.sorted_frequencies_positive)

        axes[1,1].bar(words,counts)
        axes[1,1].set_title("Top Positive Words")
        axes[1,1].set_xlabel("WORDS")
        axes[1,1].set_ylabel("COUNT")
        axes[1,1].tick_params(axis='x', rotation=45)

        
        words,counts=zip(*self.sorted_frequencies_negative)
            
        axes[1,2].bar(words,counts)
        axes[1,2].set_title("Top Negative Words")   
        axes[1,2].set_xlabel("WORDS")
        axes[1,2].set_ylabel("COUNT")
        axes[1,2].tick_params(axis='x', rotation=45)

   
        plt.tight_layout()
        plt.show()
    

       
