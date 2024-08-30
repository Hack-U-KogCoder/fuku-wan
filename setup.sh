#!/bin/bash

echo "外部パッケージをインストールします..."
pip install keyboard pyaudio textual python-dotenv openai gpiozero
echo "外部パッケージをインストールしました"

cp ./start-origin.sh ./start.sh
echo "start.sh を作成しました"
chmod +x ./start.sh
echo "./start.sh を実行してください"
