import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from wordcloud import WordCloud

# 현재 스크립트 파일의 디렉토리 경로를 가져옵니다.
current_dir = os.path.dirname(__file__)

# 한글 폰트 설정
font_path = os.path.join(current_dir, 'HMFMPYUN.TTF')
font_name = fm.FontProperties(fname=font_path).get_name()
plt.rc('font', family=font_name)


def extract_conversations(text):
    if text[0] == '[':
        return text
    
    
def conversations_split(text):
    text = text.replace('[', '').split(']')
    text = [t.strip() for t in  text]
    return text


def get_df(df):
    df.columns = ['내용']
    
    df['내용'] = df['내용'].apply(extract_conversations)
    
    df = df.dropna()
    df = df.reset_index(drop=True)
    
    df['내용'] = df['내용'].apply(conversations_split)
    
    name = []
    date = []
    messages = []

    for i in df['내용']:
        if len(i) == 3:
            name.append(i[0])
            date.append(i[1])
            messages.append(i[2])
            
    data = {'이름': name,
            '날짜': date,
            '내용': messages}

    df = pd.DataFrame(data)
    
    return df


def get_bar(df):
    message_cnt = df.groupby('이름')['내용'].count()

    plt.bar(message_cnt.index, message_cnt, )

    for index, value in enumerate(message_cnt):
        plt.text(index, value, str(value), ha='center')
        
    plt.title('사용자별 대화 수')

    # 그래프를 Streamlit 애플리케이션에 출력
    st.pyplot(plt)


def get_wc(df, name, max_words):
    if name == '전체':
        text = ' '.join(df['내용'])
    else:
        text = ' '.join(df[df['이름'] == name]['내용'])

    # 워드클라우드 객체 생성
    wordcloud = WordCloud(font_path=font_path,
                          background_color="white",
                          width=1000,
                          height=1000,
                          max_words=max_words,
                          max_font_size=300).generate(text)

    # 워드클라우드 표시
    st.image(wordcloud.to_array())


def main():
    st.title('카톡 대화 분석')
    st.write(font_name)

    # 파일 업로드 컴포넌트 생성
    uploaded_file = st.file_uploader("파일 업로드 (업로드된 파일은 서버에 저장되지 않습니다)", type=['txt'])

    # 파일이 업로드된 경우 데이터프레임으로 변환하여 출력
    if uploaded_file is not None:
        # 업로드된 파일을 데이터프레임으로 읽어오기
        df = pd.read_csv(uploaded_file, sep='\t')
        df = get_df(df)

        get_bar(df)

        # 셀렉트 박스 생성
        selects = ['전체']
        names = list(df['이름'].unique())
        selects += names

        name = st.selectbox(
            '이름을 선택해주세요', (selects)
            )
        
        st.write(name, '이(가) 선택되었습니다.')

        # 볼륨 바 생성
        max_words = st.slider('키워드 수 조정 (기본: 50)', 1, 100, 50)
        get_wc(df, name, max_words)



if __name__ == '__main__':
    main()
