from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import time
import os

# Chrome WebDriverを初期化
options = webdriver.ChromeOptions()
options.add_argument("executable_path=path/to/chromedriver")
driver = webdriver.Chrome(options=options)

# AtCoderにログインする
login_url = "https://atcoder.jp/login"
driver.get(login_url)

# ユーザー名とパスワードをゆっくり入力してログイン
username = "ner2298"
password = "naonao.2298"

username_input = driver.find_element(By.NAME, "username")
password_input = driver.find_element(By.NAME, "password")
login_button = driver.find_element(By.CLASS_NAME, "btn-primary")

for char in username:
    username_input.send_keys(char)
    time.sleep(0.3)  # 0.5秒待機

for char in password:
    password_input.send_keys(char)
    time.sleep(0.3)  # 0.5秒待機

login_button.click()
time.sleep(3)

# questions = "abc310"
# question = "abc310_c"

x = 737

while x <= 800:
    try:
        questions_url = "https://kenkoooo.com/atcoder/#/table/"
        driver.get(questions_url)
        time.sleep(3)

        questions_url = driver.find_elements(By.CLASS_NAME, "btn-secondary")
        ARC_button = questions_url[2]
        ARC_button.click()
        time.sleep(3)

        question_urls = driver.find_elements(
            By.CSS_SELECTOR, f"a[href^='https://atcoder.jp/contests/']"
        )
        question_url = question_urls[x].get_attribute("href")

        # コンテスト名と問題名を抽出する正規表現パターン
        pattern = r"https://atcoder.jp/contests/(\w+)/tasks/(\w+)"

        # 正規表現パターンに一致する部分を抽出
        match = re.match(pattern, question_url)

        # コンテスト名と問題名を取得
        questions = match.group(1)
        question = match.group(2)

        # 問題ページにアクセスする
        contest_url = f"https://atcoder.jp/contests/{questions}/tasks/{question}"
        driver.get(contest_url)
        time.sleep(3)
        # テキストファイルに保存する文字列を格納する変数を初期化
        text_to_save = f"問題リンク: {contest_url}\n\n"

        # 入力例・出力例の取得
        sample_elements = driver.find_elements(
            By.CSS_SELECTOR, ".part pre[id^='pre-sample']"
        )

        # 入力例・出力例を保存
        for i in range(len(sample_elements) // 2):
            input_elem_index = i * 2
            output_elem_index = i * 2 + 1

            input_elem = sample_elements[input_elem_index]
            output_elem = sample_elements[output_elem_index]

            if input_elem.text.strip() and output_elem.text.strip():
                text_to_save += f"入力例{i + 1}: \n{input_elem.text.strip()}\n"
                text_to_save += f"出力例{i + 1}: \n{output_elem.text.strip()}\n\n"

        # 提出結果画面にアクセスする
        submissions_url = f"https://atcoder.jp/contests/{questions}/submissions?f.Task={question}&f.LanguageName=&f.Status="
        driver.get(submissions_url)
        time.sleep(3)

        a = 1
        id = 1
        page = 1

        # ACかつPythonのコード・実行時間を取得・保存
        while a <= 19 and page <= 10:
            elements = driver.find_elements(By.TAG_NAME, "tr")
            if "Python (3.8.2)" in elements[a].text and "AC" in elements[a].text:
                code_urls = driver.find_elements(
                    By.CSS_SELECTOR, f"a[href^='/contests/{questions}/submissions/']"
                )
                code_url = code_urls[a + 1].get_attribute("href")
                driver.get(code_url)
                time.sleep(3)
                code = driver.find_element(By.ID, "submission-code").text
                tds = driver.find_elements(By.TAG_NAME, "td")
                code_time = tds[7].text
                text_to_save += f"code{id}: 実行時間: {code_time}\n"
                text_to_save += f"{code}\n\n"
                id += 1
                a += 1
                driver.get(
                    f"https://atcoder.jp/contests/{questions}/submissions?f.LanguageName=&f.Status=&f.Task={question}&f.User=&page={page}"
                )
                time.sleep(3)
                if a == 19:
                    # 次のページへのリンクを見つけてクリックする
                    page += 1
                    driver.get(
                        f"https://atcoder.jp/contests/{questions}/submissions?f.LanguageName=&f.Status=&f.Task={question}&f.User=&page={page}"
                    )
                    time.sleep(3)
                    a = 1
            else:
                a += 1
                if a == 19:
                    # 次のページへのリンクを見つけてクリックする
                    page += 1
                    driver.get(
                        f"https://atcoder.jp/contests/{questions}/submissions?f.LanguageName=&f.Status=&f.Task={question}&f.User=&page={page}"
                    )
                    time.sleep(3)
                    a = 1

        # 保存先のディレクトリパスを指定
        save_directory = r"C:\Users\naoto\Desktop\AtCoderAI\codedata"

        # ファイル名を指定（question変数は事前に定義していると仮定）
        file_name = f"{question}code.txt"

        # ファイルのフルパスを生成
        file_path = os.path.join(save_directory, file_name)

        # テキストファイルに保存
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text_to_save)

        time.sleep(3)

        x += 1
        print(x)

    except IndexError:
        # エラーが発生した場合はテキストを保存してループに戻る
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text_to_save)

        x += 1
        print(x)
        continue

    except AttributeError:
        # エラーが発生した場合はループに戻る
        x += 1
        print(x)
        continue

# ブラウザを閉じる
driver.quit()
