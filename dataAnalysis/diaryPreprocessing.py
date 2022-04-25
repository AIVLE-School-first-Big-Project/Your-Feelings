import re
from hanspell import spell_checker # 오타, 띄어쓰기 보정
import pandas as pd
from sklearn.pipeline import Pipeline

# 커스텀 변환기: 하이퍼파라미터 튜닝 메서드(get_params, set_params)와 fit_trainsform 메서드를 상속받기 위해
from sklearn.base import BaseEstimator, TransformerMixin


class SpellModify(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.strip()
        X = re.sub(r"[\n]+", " ", X) # 줄바꿈 -> 띄어쓰기로 수정

        # 오타, 띄어쓰기 수정
        X_check = spell_checker.check(X)
        X_spell = X_check.checked

        return X_spell


# 신조어 변환
class NeologismChange(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        neologism_df = pd.read_csv("data/new_word.csv")
        for _, row in neologism_df.iterrows():
            X = X.replace(row['word'], row['mean'])
        return X


diary_pipeline = Pipeline([
        ('newly', NeologismChange()), # 신조어 처리
        ('spelling', SpellModify()), # 일기 오타, 띄어쓰기 전처리
])


# 사용방법
# from diaryPreprocessing import *
# diary_pipeline.fit_transform("text")