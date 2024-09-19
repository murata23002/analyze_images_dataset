## 概要
画像データセットを使用して画像のコンテキスト情報を生成および解析するためのものです。画像をOpenAI GPT APIに送信し、Bag of Words形式のキーワードとインスタンス、コンテキスト情報（時間、場所、オブジェクト、アクション）を抽出します。抽出された情報をJSON形式で保存し、後でデータの解析を行います。

## 機能

1. **画像のリサイズと圧縮**:
   - 各画像ファイルをリサイズし、指定されたファイルサイズ（500KB以下）になるよう圧縮します。

2. **Base64エンコーディング**:
   - 圧縮された画像をBase64形式にエンコードして、APIリクエストに使用します。

3. **画像コンテキストの生成**:
   - OpenAI GPT APIを使用して、Bag of Words（BoW）、インスタンス数、時間、場所、オブジェクト、アクションなど、画像のコンテキスト情報を取得し、JSONファイルに保存します。

4. **データの集計と可視化**:
   - 保存されたJSONファイルから、キーワードの頻度やコンテキスト情報を集計し、CSVファイルにエクスポートします。また、集計結果をコンソールで表示します。

## プロンプト
```
Analyze the given image and extract key information as structured JSON data. Ensure that:

The "keywords" array contains unique keywords or descriptive phrases (Bag of Words) that best represent the content of the image.

Each item in the array should be a string.
Exclude words or phrases that do not clearly fit the context.
All words should be written in lowercase.
Focus on nouns, adjectives, and key phrases that accurately describe the main elements and context of the image.
Properly distinguish between singular and plural forms of objects.
If applicable, the "instances" object should differentiate between single, few, and many instances of objects, with each entry in the following format:

"single": ["object1", "object2", ...]
"few": ["object1", "object2", ...]
"many": ["object1", "object2", ...]
Additionally, extract and clearly label contextual information in the "context" object, with entries for:

"time": "morning", "afternoon", "evening", "night" (or similar)
"location": "forest", "beach", "city street", etc.
"object": "car", "building", "river", etc."
"action": "running", "jumping", "sitting", etc." (if applicable)
If any contextual element is unclear or cannot be inferred, clearly label it as "unknown" in the "context" object.

The output should be a valid JSON object like the example below:

{
  "keywords": ["sky", "tree", "grass", "few clouds", "many rocks"],
  "instances": {
    "single": ["tree"],
    "few": ["clouds"],
    "many": ["rocks"]
  },
  "context": {
    "time": "evening",
    "location": "forest",
    "object": "campfire",
    "action": "burning"
  }
}

```
## 使用方法

### 必要条件

- **Python 3.x** インストール済み
- 必要なライブラリ：
  ```bash
  pip install openai pillow pandas
  ```

### 手順

1. **OpenAI APIキーの設定**:
   - `client = OpenAI(api_key="")` の部分にOpenAI APIキーを設定してください。
 ```python
# Initialize OpenAI client
client = OpenAI(api_key="")
 ```
2. **画像の保存先ディレクトリの設定**:
   - `image_directory` に画像が保存されているディレクトリパスを設定してください。

3. **JSONファイルの保存先ディレクトリの設定**:
   - JSONファイルは `json_output_directory` に保存されます。ディレクトリが存在しない場合は自動的に作成されます。

4. **画像コンテキスト生成スクリプトの実行**:
   - 画像データセットに対して、以下のコマンドを実行してください:
     ```bash
     python image_context_generator.py
     ```

5. **データ解析スクリプトの実行**:
   - JSONファイルからデータを集計し、CSV形式で出力するには以下のコマンドを実行してください:
     ```bash
     python analyze_json_data.py
     ```

### 出力

- 各画像のコンテキスト情報は、`json_outputs` ディレクトリ内に保存されます。
- 解析結果は、`output_csv` ディレクトリに保存され、以下のようなファイルが生成されます：
  - `keyword_frequency.csv`: キーワードの出現頻度
  - `context_time_frequency.csv`: コンテキスト内の時間の頻度
  - `context_location_frequency.csv`: コンテキスト内の場所の頻度
  - `context_action_frequency.csv`: コンテキスト内のアクションの頻度
  - `single_instances_frequency.csv`: 単一オブジェクトの頻度
  - `few_instances_frequency.csv`: 少数オブジェクトの頻度
  - `many_instances_frequency.csv`: 多数オブジェクトの頻度

## ディレクトリ構造

```
.
├── image_context_generator.py   # 画像コンテキスト生成スクリプト
├── analyze_json_data.py         # JSONデータ解析スクリプト
├── dist/                        # 画像データが保存されるディレクトリ
├── json_outputs/                # JSONファイルが出力されるディレクトリ
└── output_csv/                  # CSVファイルが保存されるディレクトリ
```

