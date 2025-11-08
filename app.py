from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.messages import SystemMessage, HumanMessage  ← 修正点1: この行を削除またはコメントアウト
from langchain_core.output_parsers import StrOutputParser

# --- 関数の定義 ---

# 【条件】「入力テキスト」と「ラジオボタンでの選択値」を引数として受け取り、
# LLMからの回答を戻り値として返す関数
def get_llm_response(user_input, expertise_choice):
    """
    LLMからの回答を取得します。
    """
    
    # 【条件】ラジオボタンでの選択値に応じてLLMに渡すプロンプトのシステムメッセージを変える
    # 専門家の種類は「健康アドバイザー」と「キャリアコンサルタント」とします。
    if expertise_choice == "健康アドバイザー":
        system_message_content = "あなたは優秀な健康アドバイザーです。ユーザーの質問に対して、健康的で実践的なアドバイスを簡潔に提供してください。"
    elif expertise_choice == "キャリアコンサルタント":
        system_message_content = "あなたは経験豊富なキャリアコンサルタントです。ユーザーのキャリアに関する悩みや質問に対し、具体的で前向きな助言を簡潔に行ってください。"
    else:
        system_message_content = "あなたは親切なアシスタントです。"

    # 【条件】Lesson8を参考にLangChainのコードを記述
    
    # 1. LLMモデルの初期化
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7) 

    # 2. プロンプトテンプレートの作成 (← 修正点2: タプル記法に変更)
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message_content),
        ("human", "{user_question}")
    ])

    # 3. 出力パーサー
    output_parser = StrOutputParser()

    # 4. チェーンの作成
    chain = prompt | llm | output_parser
    
    # 5. LLMの実行と回答の取得
    try:
        response = chain.invoke({"user_question": user_input})
        return response
    except Exception as e:
        # APIキーがない場合や他のエラーをキャッチ
        st.error(f"AIの呼び出し中にエラーが発生しました: {e}")
        st.error("【開発者向け】: .envファイルにOPENAI_API_KEYが正しく設定されているか確認してください。")
        return None

# --- Streamlit アプリのUI ---

st.title("🧑‍🏫 専門家チャットボット")
st.markdown("""
このアプリは、あなたの質問や悩みに専門家が回答するチャットボットです。
""")

st.info("**【操作方法】**\n1. 相談したい専門家を選んでください。\n2. 質問を入力し、「送信」ボタンを押してください。")

# --- UIコンポーネント ---

expertise = st.radio(
    "相談する専門家を選んでください:",
    ("健康アドバイザー", "キャリアコンサルタント"),
    key="expertise_choice"
)

user_query = st.text_area("質問を入力してください:", "", height=150)

if st.button("送信"):
    if user_query:
        st.info(f"**あなたの質問:**\n{user_query}")
        st.info(f"**選択した専門家:** {expertise}")
        
        with st.spinner("AIが回答を生成中です..."):
            answer = get_llm_response(user_query, expertise)
            
            if answer:
                st.success(f"**{expertise}からの回答:**\n{answer}")
    else:
        st.warning("質問を入力してください。")