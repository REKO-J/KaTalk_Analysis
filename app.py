import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 한글 폰트 설정
plt.rc('font', family='NanumBarunGothic')

def generate_wordcloud(text):
    wordcloud = WordCloud(font_path=None, width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot()

def main():
    st.title('한글 워드클라우드 생성')

    # 워드클라우드를 생성할 텍스트 입력
    text = st.text_area('텍스트 입력', '여기에 텍스트를 입력하세요.')

    if st.button('워드클라우드 생성'):
        generate_wordcloud(text)

if __name__ == "__main__":
    main()
