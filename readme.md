
# Spelling bee 聽打練習程式

## 程式說明

程式將會按照選取的單字檔案，與 index 亂數進行聽打練習

念單字的部分將由套件 pyttsx3 進行 讀取系統可發音的選項 進行亂數擇一撥放出來


Windows 11 下支援兩種
2024-11-17 16:46:50,745 - __main__ - INFO - 1: Microsoft Zira Desktop - English (United States)
2024-11-17 16:46:50,745 - __main__ - INFO - 2: Microsoft David Desktop - English (United States)

```
python go_to_test_app.py
```

## 設定檔說明
單字檔請放入 ./cfg/ 資料夾中，檔名格式為 *.json
```json
{"1": "arm",
 "2": "airplane",
 "3": "April",
 "4": "bakery",
 "5": "bottom",
 "6": "camera"}
```


## 打包指令(尚未完成)

```
pyinstaller --onefile --add-data "no.wav;." --add-data "yes.wav;." --add-data "r.jpg;." --add-data "w.jpg;." --add-data "1A.json;."  --add-data "1ARS.json;." --add-data "AL.json;."  go_to_test_app.py
```