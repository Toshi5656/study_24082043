import streamlit as st # フロントエンドを扱うstreamlitの機能をインポート
import speech_recognition as sr # 音声認識の機能をインポート

# 言語選択と、APIが認識する言語の変換リストを作成
set_language_list = {
    "日本語" : "ja",
    "英語" : "en-US",
}

# デフォルトの言語を設定
set_language = "日本語"

# 音声ファイルと音声認識の言語を引数に音声認識をする
def file_speech_to_text(audio_file, set_language):
    
    # 音声ファイルを読み込み
    with sr.AudioFile(audio_file) as source:
        audio =sr.Recognizer().record(source)   # sr.Recognizer().record(開いた音声ファイル）で認識準備

    try:
        text = sr.Recognizer().recognize_google(audio, language=set_language_list[set_language]) # sr.Recognizer().recoginze_google(音声データ, 言語)で音声認識して、textに代入
    except:
        text = "音声認識に失敗しました"
    return text # 認識した文字を返す

# 音声認識の言語を引数に音声認識をする
def mic_speech_to_text(set_language):

    #マイク入力を音声ファイルとして読み込み
    with sr.Microphone(device_index=1) as source:
        audio = sr.Recognizer().listen(source) # sr.Recognizer().listen(マイク入力)で認識準備
    
    try:
        text = sr.Recognizer().recognize_google(audio, language=set_language_list[set_language]) # sr.Recognizer().recognize_google(音声データ,言語)で音声認識して、textに代入
    except:
        text = "音声認識に失敗しました"
    return text #　認識した文字を返す

st.title("記事出力アプリ(テキスト/音声)") # タイトル
st.write("音声認識する言語を選んでください。") # 案内を表示
set_language = st.selectbox("音声認識する言語を選んでください", set_language_list.keys()) # 音声認識に使う言語を選択肢として表示
current_language_state = st.empty() # 選択肢を表示するための箱を準備
current_language_state.write("選択中の言語:" + set_language) # 選択肢を表示するための箱に選択した言語を表示


## file_upload = st.file_uploader("ここに音声認識したファイルをアップロードしてください。", type=["wav"]) # アップローダーを設定し、wavファイルだけ許可する設定にする

# ファイルアップロードされた場合、file_uploadがNoneではなくなる
## if (file_upload !=None):

##    st.write("音声認識結果：") # 案内表示
##    result_text = file_speech_to_text(file_upload, set_language) # アップロードされたファイルと選択した言語を元に音声認識開始
##    st.write(result_text) # メソッドから帰ってきた値を表示
##    st.audio(file_upload) # アップロードした音声をきける形で表示


    
st.write("マイクでの音声認識はこちらのボタンから") # 案内表示

result_text = ""

# ボタンが押された実行される
if st.button("音声認識開始"):
    state = st.empty() # マイク録音中を示すための箱を準備
    state.write("音声認識中") # 箱に案内表示書き込み
    result_text = mic_speech_to_text(set_language) # 選択した言語を元に音声開始
    # state.write("音声認識結果：") # 案内表示に変更
    # st.write(result_text)   # メソッドから返ってきた値を表示


# ここからGPT

from openai import OpenAI # openAIのchatGPTのAIを活用するための機能をインポート
import os # OSが持つ環境変数OPENAI_API_KEYにAPIを入力するためにosにｱｸｾｽするためのライブラリをインポート


# openAIの機能をclientに代入
client = OpenAI()

content_kind_of = [
    "中立的で客観的な文章",
    "分かりやすい、簡潔な文章",
    "親しみやすいトーンの文章",
    "専門用語をできるだけ使わない、一般読者向けの文章",
    "言葉の使い方に拘り、正確な表現を心掛けた文章",
    "ユーモアを交えた文章",
    "シンプルかつわかりやすい文法を使った文章",
    "面白く、興味深い内容を伝える文章",
    "具体的でイメージしやすい表現を使った文章",
    "人間味のある、感情や思いを表現する文章",
    "引用や参考文献を適切に挿入した、信頼性の高い文章",
    "読み手の興味を引き付けるタイトルやサブタイトルを使った文章",
    "統計データや図表を用いたわかりやすい文章",
    "独自の見解や考え方を示した、論理的な文章",
    "問題提起から解決策まで網羅した、解説的な文章",
    "ニュース性の高い、旬なトピックを取り上げた文章",
    "エンターテイメント性のある、軽快な文章",
    "読者の関心に合わせた、専門的な内容を深く掘り下げた文章",
    "人物紹介やインタビューを取り入れた、読み物的な文章",
]

# chatGTPにリクエストするためのメソッドを設定。引数には書いてほしい内容と文章のテイストと最大文字数を指定
def run_gpt(content_text_to_gpt, content_kind_of_to_gpt, content_maxStr_to_gpt):
    # リクエストの内容を決める
    request_to_gpt = content_text_to_gpt + "また、これを記事として読めるように、記事のﾀｲﾄﾙ、目次、内容の順番で出力してください。内容は" + content_maxStr_to_gpt + "文字以内で出力してください。" + "また、文章は" + content_kind_of_to_gpt + "にしてください"

    # 決めた内容を元にclient.chat.completions.createでchatGPTにリクエスト。オプションとしてmodelにAIモデル、messageに内容を指定
    response = client.chat.completions.create(
        # model="gpt-3.5-turbo",
        model= "gpt-4o-mini",
        messages=[
            {"role": "user", "content" : request_to_gpt },
        ],
    )

    # 返ってきたレスポンスの内容はresponse.choices[0].message.content.strip()に格納されているので、これをoutput_contentに代入
    output_content = response.choices[0].message.content.strip()
    return output_content # 返ってきたレススポンスの内容を返す

st.title("GPT出力") # タイトル

# 書かせたい内容
# content_text_to_gpt = st.sidebar.text_input("書かせたい内容を入力してください!")


# 入力ボックスにデフォルトで「GPTからの抽出」というテキストを表示
content_text_to_gpt = st.text_input("書かせたい内容を入力または上記音声認識してください!", result_text)

# 書かせたい内容のテイストを選択肢として表示する
content_kind_of_to_gpt = st.sidebar.selectbox("文章の種類", options=content_kind_of)

# chatGPTに出力される文字数
content_maxStr_to_gpt = str(st.sidebar.slider("記事の最大文字数", 100, 1000, 3000))

if content_text_to_gpt != "":
    output_content_text = run_gpt(content_text_to_gpt,content_kind_of_to_gpt,content_maxStr_to_gpt)
    st.write(output_content_text)



### ここから画像


    cocktail_prompt =output_content_text + " に関連する画像"


    response = client.images.generate(

    model="dall-e-3",

    prompt = cocktail_prompt,

    size="1024x1024",

    quality="standard",

    n=1,

    )

    image_url = response.data[0].url

    st.image(image_url)