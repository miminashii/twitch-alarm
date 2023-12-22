# twitch-alarm

とめる/koQchanが配信開始したらアラーム鳴らす。\
実行をctrl+cとかで止めない限り永遠と動く。

## 使う上での注意点

- Mac端末上でしか動作確認していません（Windowsだと動くかわからないです）

## 使い方

1. Python 3.11をインストール
2. 必要なパッケージをインストール

   ```bash
   pip install -r requirements.txt
   ```

3. 実行

   ```bash
   python twitch_alarm.py
   ```

## FYI

- `config.yaml`の`tomeru1`、`koqchan`を任意のチャンネルに変更すれば、そのチャンネルの配信開始を検知してアラームを鳴らせる。
- `config.yaml`の`alarm_filepath`を変更することで、好きなアラームの音を鳴らせる。
