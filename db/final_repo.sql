-- 創建名為「users」的用戶表格
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    user_type VARCHAR(20) NOT NULL
);

-- 創建名為「training_datasets」的訓練資料集表格
CREATE TABLE training_datasets (
    dataset_id SERIAL PRIMARY KEY,
    dataset_name VARCHAR(100) NOT NULL,
    teacher_id INTEGER REFERENCES users(user_id),
    training_data_path VARCHAR(255) NOT NULL,
    validation_data_path VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 創建名為「models」的模型表格
CREATE TABLE models (
    model_id SERIAL PRIMARY KEY,
    model_name VARCHAR(100) NOT NULL,
    student_id INTEGER REFERENCES users(user_id),
    dataset_id INTEGER REFERENCES training_datasets(dataset_id),
    model_path VARCHAR(255) NOT NULL,
    accuracy FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 創建名為「scores」的成績表格
CREATE TABLE scores (
    score_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES users(user_id),
    model_id INTEGER REFERENCES models(model_id),
    score FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
