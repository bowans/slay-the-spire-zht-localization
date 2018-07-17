## slay-the-spire-zht-localization
Slay the Spire 正體中文翻譯

    .
    ├── localization                    # beta branch 更新後從遊戲中取出最新翻譯
    │   ├── eng
    │   ├── zhs
    │   ├── zht
    │   ├── REFERENCES.txt              # 官方取名時的 reference
    │   ├── TRANSLATOR_README.txt       # 官方翻譯人員須知
    │   └── UPDATES.txt                 # 每次更新的 update note
    ├── zhs2zht                         # localization 中對 zhs 作簡轉繁，做為參考。
    ├── zht                             # 實際上 zht 更新翻譯的資料夾
    └── README.md

### 每次更新固定流程

1. 取出遊戲中的 localization ，更新 ```eng, zhs, zht, REFERENCES.txt, TRANSLATOR_README.txt, UPDATES.txt```。
2. 將最新的 ```localization\zhs``` 用繁化姬桌面版轉換，選項用台灣化，並移除每個檔案最下面因轉換而多出的空行。
3. Merge localization\zht 與實際上生新翻譯的 zht。
> 在上一次 update 給 dev 後，我們可能還有持續更新 zht。因此要做 Merge 來確保 localization\zht 的新內容與我們後來的更新都還在。
> 
> 若想要確認在上次給 dev 後做了哪些更新，可以點最新的 Release，會顯示與上次的 release 中相隔了那些 commit。

### 參考流程

以下直接是寫執行命令，如果是用其它工具的人，UI上應該會有對應的功能。

1. 點選 fork 將專案複製至自已的帳號底下，
2. 將你 fork 過去的專案，也就是你自己的專案 clone 到你的本地端
3. 在 clone 的專案下新建分支（branch），並切換到你的分支上，名稱可取為「trans」，命令為`git branch trans` + `git checkout trans`
4. 執行 `git remote add upstream https://github.com/bowans/slay-the-spire-zht-localization.git` 將本庫加為遠端庫
5. 執行 `git remote update` 更新
6. 執行 `git fetch upstream master` 拉取本庫更新到你的本地
7. 執行 `git rebase upstream/master` 將更新內容整併到你的分支

以上為初始化流程，如果 upstream 有更新請執行 5~7 即可，平時請在自己的分支上作業。
最後發 pull-request 將翻譯內容加回至本專案，每次發之前請務必確認是否同步了最新版。
（建議翻譯部份成果就可加回，太多可能導致重覆翻譯或衝突發生）

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

[[官方 Discord]] https://steamcommunity.com/linkfilter/?url=http://discord.gg/slaythespire
