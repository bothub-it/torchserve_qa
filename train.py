from simplet5 import SimpleT5
import pandas as pd
from sklearn.model_selection import train_test_split
import re
import sys


def read_split_data(url):
    df = pd.read_csv(url)
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    train_df = train_df.to_csv('/content/train_df.csv')
    test_df = test_df.to_csv('/content/test_df.csv')
    return train_df, test_df

def train_model(url):
    train_df, test_df = read_split_data(url)
    model = SimpleT5()
    model.from_pretrained(model_type="t5", model_name="unicamp-dl/ptt5-base-portuguese-vocab")
    train_df = pd.read_csv('/content/train_df.csv')
    test_df = pd.read_csv('/content/test_df.csv')

    model.train(outputdir='qna2',
                train_df=train_df,
                eval_df=test_df,
                source_max_token_len=100,  
                target_max_token_len=100,
                batch_size=2, max_epochs=2, 
                use_gpu=False)

train_model(sys.argv[1])
