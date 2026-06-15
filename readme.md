<!-- DAC 數值轉換工具 使用說明 (readme.md) -->
# DAC 數值轉換工具 使用說明
==================================

## 功能簡介

本工具可根據用戶自訂的 DAC 轉換參數，將輸入的類比數值 (value) 轉換成對應的 digital code。

- 支援序列輸出 (`serial`)：逐位元排列，可選 MSB/LSB 方向
- 支援並列輸出 (`parallel`)：輸出 digital code 及二進位字串 (bit code)
- 支援限制 digital code 輸出範圍，並自動標示超出範圍的情形

## 安裝需求

- Python 3.6 以上（Anaconda 或原生 Python 皆可）
- **無需安裝額外套件**，僅用標準函式庫

## 使用方法

1. 編輯輸入檔案（假設為 `input.txt`）：

```
[condition]
resolution=16
+vref=5.0
-vref=0.0
output_format=serial # 可設為 serial 或 parallel
bit_order=msb # 僅 serial 模式下有效 (msb 或 lsb)

[outputlimit]
daccoderange=513:64741 # 輸出 digital code 的最小值:最大值(注意:value所對應的值都會加上 dac code min value)

[value]
0.5
1.0
2.0
2.5
7.5
8.0
```

2. 執行程式

打開終端機 (命令提示字元、PowerShell、Anaconda Prompt 皆可) 或執行 `run_script.bat`：

- 程式會讀取 `input.txt`，輸出結果到 `output.txt`
- 你也可以直接修改程式碼中的檔名設定

3. 查看輸出檔案

- 若 `output_format=serial`，每個 value 輸出一個區塊，每行一個 bit（排列順序依 `bit_order`）
- 若 `output_format=parallel`，每行輸出 `value, digital_code, bit_code, remark`

## 輸入檔案格式說明

1. `[condition]`
- `resolution`：DAC 精度（位元數），如 8、12、16、24
- `+vref` / `-vref`：正負參考電壓
- `output_format`：`serial` 或 `parallel`
- `bit_order`：bit 排列順序（僅 `serial` 模式下有效，可設 `msb` 或 `lsb`）

2. `[outputlimit]`
- `daccoderange=起始值:最大值`，例：`513:64741`

3. `[value]`
- 每行一個待轉換的類比數值

## 輸出檔案格式說明

1. Serial 模式範例

```
[result]
! value = 2.5
0
1
0
...

! value = 8.0, exceed daccoderange, digital_code=64741
1
1
1
1
1
0
1
0
...
```

- 若超出範圍，會在 value 標示行加上 `exceed daccoderange, digital_code=實際輸出值`
- 每個 value 一個區塊，區塊間有空行分隔

2. Parallel 模式範例

```
[result]
value,digital_code,bit_code,remark
2.5,33278,1000001000101110,
8.0,64741,1111110011110101,exceed daccoderange
```

- `bit_code` 為 MSB→LSB 排列
- 若超出範圍，`remark` 欄位標註 `exceed daccoderange`

## 注意事項

- 本工具僅使用 Python 內建模組（`re`、`csv` 皆為標準函式庫，無須安裝）
- 若 value 經轉換後加上 daccoderange 起始值超過最大值，將以最大值輸出，並自動標註 `exceed daccoderange`
- `serial` 模式預設 `bit_order=msb`，如需 `lsb` 可於 `[condition]` 區塊指定
- `parallel` 模式下 `bit_order` 參數不會作用
- 檔案編碼請使用 UTF-8

## 常見問題

Q1. 為什麼出現 `ImportError: No module named re`？

A1. 請確認你用的是標準 Python 3.x 環境，`re` 為內建模組，無需安裝。

Q2. 為什麼有的 value 被標註 `exceed daccoderange`？

A2. 代表該 value 對應的 digital code 超出你設定的最大值，程式自動用最大值替代並加註說明。

## 未來計畫
- [ ] 補上 code 下限檢查，避免出現負數或低於 'code_min' 的結果。  
- [ ] 把 input.txt / output.txt 改成可由外部指定。  
- [ ] 當某個 value 無法轉成數字時，可以印出提醒，方便除錯。  
