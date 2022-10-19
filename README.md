# Computer_Vision_HW1
[toc]
## HW1_1
1. 基本概念
- 相機拍攝的圖像會產生一定程度的失真，失真類型可分成 radial distortion 與 tangential distortion 兩種。
    - Radial distortion 會導致現實中的直線在圖片中呈現彎曲，且當點離圖像中心越遠，徑向畸變越大。以下圖為例，將圖中棋盤依兩邊緣連線後，可明顯觀察到圖的失真狀態。

        ![](https://playlab.computing.ncku.edu.tw:3001/uploads/upload_b508b147ee32c3e27bfa45d2d4e7cf81.png)
    
    - Tangential  distortion 導因於攝像鏡頭沒有與成像平面平行，導致圖像中的遠近無法被清楚表達。

- 兩種失真類型的公式分別如下:
    - Radial distortion:

        ![](https://playlab.computing.ncku.edu.tw:3001/uploads/upload_78df55a9bb19d03170fbff6802ace618.png)

    - Tangential distortion:
    
        ![](https://playlab.computing.ncku.edu.tw:3001/uploads/upload_9ef30e577a15cb9c80d1c5bf323e6efb.png)

- 為解決照片失真問題，我們需要考慮真實景像變成相機影像時的誤差，該誤差參數如下所述:

    - distortion coefficients
        
        ![](https://playlab.computing.ncku.edu.tw:3001/uploads/upload_03e9444963e90e7d37df1d6a3a3e5060.png)
    
    - intrinsic parameter
        > intrinsic parameter 是指一台相機拍攝時的一些特性，例如焦點長度與成像中心點。焦點長度與成像中心點可用於創建 camera matrix，該矩陣可用於消除特定相機鏡頭引起的失真。camera matrix 對於特定相機而言是唯一的，因此計算出的 camera matrix，可用於同一相機拍攝的其他圖像上。表示為一個  camera matrix 為一個 3x3 矩陣：

        ![](https://playlab.computing.ncku.edu.tw:3001/uploads/upload_ef2fac97d4ab22fc545fe8a90be74ba6.png)
    
    - extrinsic parameters 
        > extrinsic parameters 是指外部參數對應於將 3D 點的坐標轉換為坐標系的旋轉和平移向量。在多媒體的應用上，我們需要校正這些失真。為了找到這些參數，我們必須提供一些定義明確的圖案（例如棋盤）的樣本圖像。我們找到一些我們已經知道相對位置的特定點（例如棋盤中的方角），並且知道這些點在現實世界空間中的坐標。上述數組圖像坐標與現實座標的對應關係，可用於求解失真係數。為了獲得更好的結果，
