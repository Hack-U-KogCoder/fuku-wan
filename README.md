# 腹話ロボット「ふくワン」

## ふくワンとは
```
ごめんなさいが言えないあなたへ。
腹話ロボット「ふくワン」がご主人の代わりに喋るワン！
言いたいことを手動入力またはAIを経由してふくワンに伝えてほしいワン！
> ふくワン「誠に申し訳ございません。」
```
つまり、本人の代わりに喋ってくれるデバイスです！

## 入力方法

ふくワンの口にあるコントローラーを操作して入力を行います。
コントローラーは上部に決定ボタンとモード切替ボタン、下部にジョイスティックがあります。

## 入力形式

- マニュアル入力
- プリセット入力
- 自動返答

### マニュアル入力

ガラケーでよく見る入力形式です。
「あかさたなはまらやわ」の子音の項目があり、押すたびに母音が変化します。

### プリセット入力

事前にキーワードを入力し、好きな時にすぐに再生できる入力形式です。

### 自動返答

内蔵されたマイクから相手の声を収集し、「生成AI」が適切な返答を提案します！

## インストール

```bash
git clone https://github.com/Hack-U-KogCoder/fuku-wan.git
cd fuku-wan
# 初回のみ実行が必須
./setup.sh
# 起動時に必要
./start.sh
python main.py
```

## その他 (アピールポイント)

- Gitを使った自動アップデート機能
- Textualを使った省リソースなTUI
- ほとんどの機能をパペット内で完結 (自動返答はインターネット接続が必須です)
