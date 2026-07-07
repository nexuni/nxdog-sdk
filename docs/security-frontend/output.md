# **0. 開始**

首次進入介面後，系統會提供引導介面讓使用者建立帳號，如圖1。
根據引導填入管理者的帳號密碼即可。

![][embedded-image-1]

**圖 1**

# **1. 快速開始指南**

0. 先至 **Map > General** 設置地圖與Home Point
1. **設定 Home Point（原點）**  
   進入系統後，前往 **Map > General**，點擊 **Home Point** 來設定機器狗的起始位置。  
2. **建立巡檢路線**  
   設定好 Home Point 後，前往 **Map > Route** 建立所需的巡檢路線。  
3. **建立巡檢計畫**  
   接著前往 **Map > Plan**，將已建立的路線組合成巡檢計畫。  
4. **開始巡檢**  
   完成上述設定後，機器狗將會自動開始執行巡檢計畫。



# **2. 首頁**

如圖 2 所示，從側邊欄選擇 **Home** 可開啟首頁，你也可以在側邊欄切換頁面。

![][image2]

**圖 2**

## Dashboard

如圖 3 所示，你可以在 Dashboard 執行非排程的即時操作。可在此暫停、恢復或清除機器狗目前的任務。  
你也可以直接命令機器狗前往或執行預先定義的 Goal、Route 或 Patrol Plan，或命令它返回 Home。  
此外，也可控制機器狗頭燈、切換運作模式、開啟麥克風，以及播放預設音效。

| 圖示 | 功能說明 |
| :---- | :---- |
| ![][image3] | 顯示即將進行的巡檢排程。點擊後可查看機器狗未來三天的巡檢計畫，並可略過或恢復目前巡檢計畫。 |
| ![][image4] | 點擊可預覽或下載最新巡檢報告，內容包含本次巡檢中所有 AI 偵測事件。 |
| ![][image5] | 點擊切換為手動模式。當機器狗閒置時，可透過搖桿進行控制。 |
| ![][image6] | 顯示機器狗目前使用的地圖。點擊可切換並預覽其他地圖。 |
| ![][image7] | 清除機器狗目前任務。 |
| ![][image8]/![][image9] | 暫停或恢復機器狗目前任務。 |
| ![][image10] | 命令機器狗返回 Home。 |
| ![][image11] | 點擊後可在地圖上選取目的地，確認後機器狗會移動至該位置。 |
| ![][image12] | 點擊後可選擇預先定義的 Route，確認後機器狗會立刻執行。 |
| ![][image13] | 點擊後可選擇預先定義的 Goal，確認後機器狗會立刻前往。 |
| ![][image14] | 點擊後可開啟對話框選擇預設巡檢計畫。可於對話框中預覽巡檢路線，選擇從最近點開始或執行完整計畫，也可決定完成後是否返回 Home。確認後機器狗會立即執行選定計畫。 |
| ![][image15] | 點擊後可開啟控制面板，啟用麥克風、播放預設音效、調整頭燈，以及切換行為模式。 |

![][image16]

**圖 3**

## 系統總覽

如圖 4 所示，此區塊提供系統資訊總覽。

### Recent Events

Recent Events 面板會顯示機器狗近期活動，包括系統錯誤、AI 偵測事件及緊急事件。點擊右上角可查看更多事件。

### Task List

Task List 面板顯示最新任務執行結果。點擊右上角可查看更多紀錄與詳細資訊。

### Status

Status 面板顯示機器狗目前狀態，包括電量、充電狀態、馬達最高溫度、目前速度，以及緊急按鈕狀態。

![][image17]

**圖 4**

## 即時影像

如圖 5 所示，你可以在此區查看主鏡頭與左右側鏡頭的即時影像，也可以透過右上角按鈕重新整理或暫停影像。

![][image18]

**圖 5**

# **3. 地圖頁面**

## Home Position 設定

1. 如圖 6 所示，從側邊欄選擇 **Map** 以開啟地圖設定頁。  
2. 如圖 7 所示，從上方選單選擇 **General** 以開啟一般設定頁。  
3. 點擊 **Home Point** 開啟設定對話框，如圖 8。  
4. 從左下角選擇一張地圖。  
5. 地圖顯示後，點擊地圖以設定 Home 位置。  
6. 在右側調整朝向，使其面向充電座。

![][image19]

**圖 6**

![][image20]

**圖 7**

![][image21]

**圖 8**

## Initial Pose

在定位跑掉的情況下，你可以點擊 **Initial Pose** 按鈕（如圖六所示），並選擇當前位置，如圖所示。

![][image-init-pose]

**圖 image-init-pose**

## Goal 管理

1. 在地圖設定頁中，如圖 9 所示，從上方選單選擇 **Goal** 以開啟 Goal 設定頁。  
2. 點擊右上角 **"+"** 按鈕，會跳出 Goal 設定對話框，如圖 10。  
3. 選擇地圖、輸入名稱，並輸入或選擇群組名稱。  
4. 地圖顯示後，點擊地圖設定 Goal 位置。  
5. 設定下方的 **Degree**，用來定義巡檢時機器狗面向方向。
6. 你可以點擊卡片進入修正頁面，並可以在此頁面對Goal進行編輯或刪除操作，如圖goal-edit所示。

![][image22]

**圖 9**

![][image23]

**圖 10**

![][goal-edit]

**圖 goal-edit**



## Route 管理

1. 在地圖設定頁中，如圖 11 所示，從上方選單選擇 **Route** 以開啟 Route 設定頁。  
2. 點擊右上角 **"+"** 按鈕，會跳出 Route 設定對話框，如圖 12。  
3. 選擇地圖、輸入名稱、選擇 AI 偵測模式與事件類型，並設定該路線的速度等級。  
4. 地圖顯示後，依序點擊地圖上的多個點位以定義路線，再於右側調整 **Degree**，設定機器狗在各點位的朝向。
5. 你可以點擊卡片進入修正頁面，並可以在此頁面對Route進行編輯或刪除操作，如圖route-edit所示。

![][image24]

**圖 11**

![][image25]

**圖 12**

![][embedded-image-2]

**圖 route-edit**



## Patrol Plan 管理

1. 在地圖設定頁中，如圖 13 所示，從上方選單選擇 **Schedule** 以開啟排程設定頁。  
2. 點擊右上角 **"+"** 按鈕，會跳出排程設定對話框，如圖 14。  
3. 在對話框中，使用右上角 **Select a route** 區塊加入巡檢路線，並可在左側預覽選擇的路線。接著輸入巡檢計畫名稱、選擇啟用星期，並設定開始時間、結束時間與巡檢間隔。最後可選擇完成後是否返回 Home。點擊 **Save** 後，系統會依設定開始執行巡檢計畫。  
4. 巡檢計畫設定完成後，會如圖 15 顯示於列表中，摘要呈現巡檢資訊。你也可以點擊 Enabled 欄位，在 Active 與 Inactive 間切換，並可以點擊 Edit 來編輯或刪除計畫，如圖 plan-edit 所示。

![][image26]

**圖 13**

![][image27]

**圖 14**

![][image28]

**圖 15**

![][plan-edit]

**圖 plan-edit**



# **4. NVR 回放頁面**

如圖 16 所示，從側邊欄選擇 **Replay** 可開啟回放頁面。

1. 使用上方日曆（如圖 17）選擇年份與月份。有錄影資料的日期會以綠色勾號標示。  
2. 選擇 **Single** 模式（指定單一鏡頭）或 **Triple** 模式進行回放。  
3. 選擇日期後，如圖 18 所示，下方時間軸會以藍色標示可回放的時間區段。移到藍色區段即可直接開始回放。

![][image29]![][image30]

**圖 16 / 圖 17**

![][image31]

**圖 18**

按鈕說明：

| ![][image32] | ![][image33] | ![][image34] | ![][image35] | ![][image36] | ![][image37] | ![][image38] |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| Fast Backward | Step Backward | Play | Step Forward | Fast Forward | Zoom Out | Zoom In |

# **5. 紀錄**

如圖 19 所示，從側邊欄選擇 **Logs** 可開啟紀錄頁面。

在這裡可以查看 AI 偵測事件、緊急事件、完整巡檢任務報告，以及使用者操作紀錄。

![][image39]

**圖 19**

## AI Event

如圖 20 所示，此頁可查看巡檢期間由 AI 偵測到的事件。你也可使用篩選功能快速找到需要的資訊，並將報告下載為 PDF。

![][image40]

**圖 20**

按鈕說明：

| ![][image41] | ![][image42] | ![][image43] | ![][image44] |
| :---- | :---- | :---- | :---- |
| Display images | Show event location | Add filter conditions | Download as PDF |

## Emergency Event

如圖 21 所示，此頁可查看機器狗的緊急事件，包括網路中斷、人為位移，以及任務執行中的突發狀況。

![][image45]

**圖 21**

## Task Report

如圖 22 所示，此頁左側可查看所有手動執行或排程執行的巡檢報告。每份報告都會顯示摘要，包括巡檢名稱、成功或失敗狀態、失敗原因（若有）、耗時與耗電量、AI 事件數量，以及特殊 AI 事件。

點擊某一份巡檢報告後，右側會顯示其所有 waypoint 與偵測到的事件圖片。

![][image46]

**圖 22**

## User Action Log

如圖 23 所示，此頁可查看系統中的使用者操作活動。

![][image47]

**圖 23**

# **6. Health**

如圖 27 所示，此頁顯示系統健康狀態，包含以下資訊：

1. **Server status**
2. **CPU usage**
3. **Memory usage**
4. **Swap usage**
5. **Disk usage**
6. **Motor temperatures**
7. **Network read/write speed**

![][image51]

**圖 27**

# **7.設定**

進入設定後，上方會有子選項可以選擇，如圖所示。

![][embedded-image-3]

1. General

在這個頁面底下，可以讓你選擇系統設定和Licenses設定，在System底下，你可以設定地圖/上傳地圖/上傳罐頭音效，而在license底下
你則可以更新license資訊

![][embedded-image-4]

2. AI

在此頁面底下，你可以設定緊急AI事件，緊急AI事件可以在篩選器中作為一個群組去顯示。

![][embedded-image-5]

3. Notifications

在此頁面你可以設定通知項目，包括：
1. telegram: 輸入你的 **Telegram ID** 到 **Telegram Subscribers** 欄位。
2. Email: 輸入 **Email Receiver Address List**、**Sender Address** 與 **Sender Password**。

![][embedded-image-6]

4. Engineering

內部設定，你通常不需要設定此項目。

5. User

你可以在此使用者，按下action後，可以讓你刪除使用者/修改使用者資訊，或是修改使用者密碼。

![][embedded-image-7]

[goal-edit]: goal-edit.png

[image1]: image1.png

[image2]: image2.png

[plan-edit]: plan-edit.png

[image3]: image3.png

[image4]: image4.png

[image5]: image5.png

[image6]: image6.png

[image7]: image7.png

[image8]: image8.png

[image9]: image9.png

[image10]: image10.png

[image11]: image11.png

[image12]: image12.png

[image13]: image13.png

[image14]: image14.png

[image15]: image15.png

[image-init-pose]: image-init-pose.png

[image-edit]: image-edit.png

[image16]: image16.png

[image17]: image17.png

[image18]: image18.png

[image19]: image19.png

[image20]: image20.png

[image21]: image21.png

[image22]: image22.png

[image23]: image23.png

[image24]: image24.png

[image25]: image25.png

[image26]: image26.png

[image27]: image27.png

[image28]: image28.png

[image29]: image29.png

[image30]: image30.png

[image31]: image31.png

[image32]: image32.png

[image33]: image33.png

[image34]: image34.png

[image35]: image35.png

[image36]: image36.png

[image37]: image37.png

[image38]: image38.png

[image39]: image39.png

[image40]: image40.png

[image41]: image41.png

[image42]: image42.png

[image43]: image43.png

[image44]: image44.png

[image45]: image45.png

[image46]: image46.png

[image47]: image47.png

[image48]: image48.png

[image49]: image49.png

[image50]: image50.png

[image51]: image51.png

[embedded-image-1]: embedded-image-1.png
[embedded-image-2]: embedded-image-2.png
[embedded-image-3]: embedded-image-3.png
[embedded-image-4]: embedded-image-4.png
[embedded-image-5]: embedded-image-5.png
[embedded-image-6]: embedded-image-6.png
[embedded-image-7]: embedded-image-7.png
