import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score

from joblib import dump, load
#拆分資料集
def SplitData():
    # 1. 載入數據
    data_path = 'E:\大四雲端運算期末作品\資料集\完整\MatchTimelinesFirst15.csv'
    data = pd.read_csv(data_path)
    # 计算分割的索引位置
    split_index = int(len(data) / 10)

    # 分割数据
    test_data = data[:split_index]  # 1/10的数据
    train_data = data[split_index:]  # 9/10的数据

    # 5. 匯出訓練集和測試集到CSV文件
    train_data_path = 'E:\大四雲端運算期末作品\資料集\訓練\MatchTimelinesFirst15_train_data.csv'
    test_data_path = 'E:\大四雲端運算期末作品\資料集\測試\MatchTimelinesFirst15_test_data.csv'

    train_data.to_csv(train_data_path, index=False)
    test_data.to_csv(test_data_path, index=False)

    print(f'訓練集已匯出到: {train_data_path}')
    print(f'測試集已匯出到: {test_data_path}')


#匯入模型
def UseModel():
    # 1. 從資料夾中匯入Naive Bayes模型和TF-IDF向量化器
    model_path = 'E:/大四雲端運算期末作品/模型/MatchTimelinesFirst15_model.joblib'
    
    model = load(model_path)

    # 2. 載入測試數據
    test_data_path = 'E:/大四雲端運算期末作品/資料集/測試/MatchTimelinesFirst15_test_data.csv'
    
    test_data = pd.read_csv(test_data_path)
    # 分離特徵和標籤
    features = list(test_data.columns[:14])
    X_test = test_data[features]
    y_test = test_data['status']

    pred = model.predict(X_test)

    # 5. 計算準確率
    accuracy = accuracy_score(y_test, pred)
    print(f'模型的準確率是: {accuracy:.2f}')