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
username = "XXXXXX"
password = "XXXXXX"

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

x = 1

while x <= 200:
    try:
        questions_url = "https://kenkoooo.com/atcoder/#/table/"
        driver.get(questions_url)
        time.sleep(3)

        questions_url = driver.find_elements(By.CLASS_NAME, "btn-secondary")
        ABC_button = questions_url[1]
        ABC_button.click()
        # ARC_button = questions_url[2]
        # ARC_button.click()
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

        # 問題文を取得
        problem_statement = driver.find_element(By.TAG_NAME, "section").text

        # コードを保存
        text_to_save += f"問題文: \n{problem_statement}\n\n"

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

        a = 1
        b = 0
        id = 1
        page = 1

        # 提出結果画面にアクセスする
        submissions_url = f"https://atcoder.jp/contests/{questions}/submissions?f.Task={question}&f.LanguageName=Python&f.Status=AC&f.User="
        driver.get(submissions_url)
        time.sleep(3)

        # ページが500エラーを返すかどうかを確認
        if "500 Internal Server Error" in driver.page_source:
            # エラーが発生した場合、URLを変更
            e_submissions_url = f"https://atcoder.jp/contests/{questions}/submissions?f.Task={question}&f.LanguageName=&f.Status=&f.User="
            submissions_url = e_submissions_url
            b += 1
            driver.get(submissions_url)
            time.sleep(3)

        if b == 0:
            # ACかつPythonのコード・実行時間を取得・保存
            while a <= 19 and id <= 20:
                elements = driver.find_elements(By.TAG_NAME, "tr")
                if "Python" in elements[a].text and "AC" in elements[a].text:
                    code_urls = driver.find_elements(
                        By.CSS_SELECTOR,
                        f"a[href^='/contests/{questions}/submissions/']",
                    )
                    code_url = code_urls[a + 1].get_attribute("href")
                    driver.get(code_url)
                    time.sleep(3)
                    code = driver.find_element(By.CLASS_NAME, "ace_text-layer").text
                    tds = driver.find_elements(By.TAG_NAME, "td")
                    code_time = tds[7].text
                    text_to_save += f"code{id}: 実行時間: {code_time}\n"
                    text_to_save += f"{code}\n\n"
                    id += 1
                    a += 1
                    driver.get(
                        f"https://atcoder.jp/contests/{questions}/submissions?f.LanguageName=Python&f.Status=AC&f.Task={question}&f.User=&page={page}"
                    )
                    time.sleep(3)
                    if a == 19:
                        # 次のページへのリンクを見つけてクリックする
                        page += 1
                        driver.get(
                            f"https://atcoder.jp/contests/{questions}/submissions?f.LanguageName=Python&f.Status=AC&f.Task={question}&f.User=&page={page}"
                        )
                        time.sleep(3)
                        a = 1
                else:
                    a += 1
                    if a == 19:
                        # 次のページへのリンクを見つけてクリックする
                        page += 1
                        driver.get(
                            f"https://atcoder.jp/contests/{questions}/submissions?f.LanguageName=Python&f.Status=AC&f.Task={question}&f.User=&page={page}"
                        )
                        time.sleep(3)
                        a = 1

        else:
            # ACかつPythonのコード・実行時間を取得・保存
            while a <= 19 and id <= 20:
                elements = driver.find_elements(By.TAG_NAME, "tr")
                if "Python" in elements[a].text and "AC" in elements[a].text:
                    code_urls = driver.find_elements(
                        By.CSS_SELECTOR,
                        f"a[href^='/contests/{questions}/submissions/']",
                    )
                    code_url = code_urls[a + 1].get_attribute("href")
                    driver.get(code_url)
                    time.sleep(3)
                    code = driver.find_element(By.CLASS_NAME, "ace_line").text
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
        save_directory = r"C:\Users\naoto\Desktop\AtCoderAI\codedata1"

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
        # 保存先のディレクトリパスを指定
        save_directory = r"C:\Users\naoto\Desktop\AtCoderAI\codedata1"

        # ファイル名を指定（question変数は事前に定義していると仮定）
        file_name = f"{question}code.txt"

        # ファイルのフルパスを生成
        file_path = os.path.join(save_directory, file_name)
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
