## slay-the-spire-zht-localization
[![Build Status](https://travis-ci.org/bowans/slay-the-spire-zht-localization.svg?branch=master)](https://travis-ci.org/bowans/slay-the-spire-zht-localization)

Slay the Spire 正體中文翻譯

    .
    ├── localization                    # beta branch 更新後從遊戲中取出最新翻譯
    │   ├── eng
    │   ├── zhs
    │   ├── zht
    │   ├── REFERENCES.txt              # 官方取名時的 reference
    │   ├── TRANSLATOR_README.txt       # 官方翻譯人員須知
    │   ├── UPDATES.txt                 # 每次更新的 update note
    │   └── validate_localization.py    # validation script
    ├── zhs2zht                         # localization 中對 zhs 作簡轉繁，做為參考。
    ├── zht                             # 實際上 zht 更新翻譯的資料夾
    ├── .travis.yml                     # file for Travis CI
    ├── README.md
    └── update_localization.py          # script for extraction and convertion of localization files

### 更新流程
純手動
1. 從```SlayTheSpire```資料夾找到```desktop-1.0.jar```，重新命名為```desktop-1.0.zip```
2. 解壓縮並複製出 ```localization```中的檔案：
   * ```eng```
   * ```zhs```
   * ```zht```
   * ```REFERENCES.txt```
   * ```TRANSLATOR_README.txt```
   * ```UPDATES.txt```
   * ```validate_localization.py```
3. 將最新的 ```localization\zhs``` 用繁化姬桌面版轉換至```zhs2zht```，選項用台灣化
4. 合併 ```localization\zht``` 與實際上更新翻譯的 ```zht```，檢查衝突

半自動
1. 執行 ```python update_localization.py -a [game_path]```
2. 合併 ```localization\zht``` 與實際上更新翻譯的 ```zht```，檢查衝突

### 協助翻譯

發現遊戲中翻譯有誤或是有翻譯的建議，可以直接發 issue 或是發 Pull Request。

以下是發 Pull Request 的參考流程，這邊直接 command line 指令，如果是用其它工具的人，UI上應該會有對應的功能。

1. 點選 fork 將專案複製至自已的帳號底下，
2. 將你 fork 過去的專案，也就是你自己的專案 clone 到你的本地端
3. 在 clone 的專案下新建分支（branch），並切換到你的分支上，名稱可取為「trans」，命令為`git branch trans` + `git checkout trans`
4. 執行 `git remote add upstream https://github.com/bowans/slay-the-spire-zht-localization.git` 將本庫加為遠端庫
5. 執行 `git remote update` 更新
6. 執行 `git fetch upstream master` 拉取本庫更新到你的本地
7. 執行 `git rebase upstream/master` 將更新內容整併到你的分支

以上為初始化流程，如果 upstream 有更新請執行 5~7 即可，平時請在自己的分支上作業。
最後發 Pull Request 將翻譯內容加回至本專案，每次發之前請務必確認是否同步了最新版。
（翻譯部份成果就可加回，太多可能導致重覆翻譯或衝突發生）
> Pull Request 有幾項準則：
> 1. 較小的 Pull Request。
> 2. 每個 Pull Request 只做一件事，例如「新增XX的翻譯」、「統一用詞：XX 換成 XX」。
> 3. 說明 Pull Request 做了什麼修改以及修改的理由。

### 翻譯和標點符號準則

符號一律使用全形符號，請參考[標點符號手冊](http://language.moe.gov.tw/001/Upload/FILES/SITE_CONTENT/M0001/HAU/haushou.htm)，
打不出來的符號，就直接複製此網頁上的符號，不要找相似的貼，有時樣子一樣但編碼不一樣，
套上字型的呈現到時會不同。

* 夾注號一律採用甲式。
* 書名號使用乙式第一種。
* 英文的單引號、雙引號一律改用中文引號「」，『』視情況使用。
* 英文的破折號 -，中文是──，是兩個不是一個。
* 刪節號……也是兩個全形，不是英文的六個點......。
* 英文和中文之間不需留空白，符號跟英文和中文之間也不需留空白。
* 遇到特殊變數(遊戲中會取代成圖案之類的)，變數前後要留空白。
* 遇到 1 of 5 這種顯示數量的地方，可以用 1/5，/是英文半形斜線，不需要用全形的。
* 其它待補充。

### 討論區

[官方 Discord](https://steamcommunity.com/linkfilter/?url=http://discord.gg/slaythespire) 頻道 chinese-traditional
