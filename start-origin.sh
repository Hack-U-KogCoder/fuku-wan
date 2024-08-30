#!/bin/bash

echo "リモートリポジトリの最新版を取得します..."
git pull -q
echo "リモートリポジトリの最新版を取得しました"

echo "コントローラーのスクリプトをバックグラウンドで実行します"
echo "パスワードの入力が求められる場合があります"
nohup sudo python input/controller.py &
echo "マイクのスクリプトをバックグラウンドで実行します"
nohup python input/microphone.py &
echo "python main.py を実行してください"
