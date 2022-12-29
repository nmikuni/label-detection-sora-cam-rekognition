# Label detection App with Soracom Cloud Camera Service and Amazon Rekognition

Soracom Cloud Camera Service (ソラカメ) の画像を SORACOM API で取得し、Amazon Rekognition で特定の label を検出し、結果を LINE Notify で通知するアプリケーションです。AWS Serverless Application Model (SAM) テンプレートを用いてデプロイできます。

**デフォルトで 1 分ごとに実行されるので注意してください。**

## 構成

1. Amazon EventBridge で定期的に AWS Lambda を呼び出す
2. ソラカメ API で静止画像をエクスポート
3. 静止画像を Amazon Rekognition でラベリング
4. ラベリングした結果を LINE Notify で通知

## 利用手順

以下の手順で利用できます。

### 事前準備

アカウントや環境を準備してください。

1. [Soracom Cloud Camera Service](https://soracom.jp/sora_cam/) 対応のカメラを用意する (API の利用にはライセンスの契約も必要です)
2. [LINE Notify](https://notify-bot.line.me/ja/) をセットアップする
3. [AWS](https://aws.amazon.com/jp/?nc2=h_lg) アカウントを用意する
4. [SORACOM SAM ユーザー](https://users.soracom.io/ja-jp/docs/sam/) の認証情報 (認証キー ID、認証キー) を準備する
5. [AWS Serverless Application Model](https://aws.amazon.com/jp/serverless/sam/) (SAM) をセットアップする

### アプリケーションのデプロイ

1. `label-detection-sora-cam-rekognition` のデプロイのため、必要な環境変数を準備します。
   - soracomAuthKeyId: SORACOM SAM ユーザーの認証キー ID
   - soracomAuthKey: SORACOM SAM ユーザーの認証キー
   - deviceId: ソラカメ対応カメラのデバイス ID
   - lineNotifyToken: LINE Notify のトークン
   - rekognitionRegion: Amazon Rekognition のリージョン
   - targetLabelName: 検知したいラベルの名前
   - targetConfidence: この信頼度以上の場合にラベルを検知します
2. `label-detection-sora-cam-rekognition` をビルド・デプロイします
   - `sam build` `sam deploy --guided --capabilities CAPABILITY_NAMED_IAM` を用います

### アプリケーションの削除

SAM でデプロイしたアプリケーションは `sam delete` コマンド、または AWS コンソールの CloudFormation メニューから削除できます。