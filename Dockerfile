# ベースイメージの指定
FROM python:3.9-slim

# 作業ディレクトリの設定
WORKDIR /app

# 必要なファイルをコピー
COPY requirements.txt .
COPY application.py .
COPY misc ./misc

# 必要なライブラリのインストール
RUN pip install --no-cache-dir -r requirements.txt

# Flaskのデフォルトポート番号を設定
EXPOSE 5000

# アプリケーションの起動コマンド
CMD [ "python", "app.py" ]
