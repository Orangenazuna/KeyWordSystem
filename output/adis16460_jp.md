

{0}------------------------------------------------

![](_page_0_Picture_2.jpeg)

# ANALOG 小型、高精度 6 DOF (自由度) 慣性 DEVICES センサー

-タシート

**ADIS16460** 

#### <span id="page-0-0"></span>特長

3 軸デジタル・ジャイロ・センサー

測定範囲: ±100°/sec (最小値)

動作中のパイアス安定性: 8°/hr (代表値)

x 軸の角度ランダム・ウォーク: 0.12°/√hr (代表値)

3 軸デジタル加速度センサーのダイナミック・レンジ: ±5 g

自律動作とデータ収集

外部設定コマンド不要

短い起動時間

感度、パイアス、軸アライメントを工場出荷時にキャリブレー

ション

補正温度範囲: 0 °C ≤ T<sub>A</sub> ≤ 70 °C

シリアル・ペリフェラル・インターフェース(SPI) データ通

データ・アクイジション同期用データ・レディ信号

温度センサー内蔵

プログラマブルな動作と制御

自動と手動のバイアス補正制御

パートレット・ウィンドウの有限インパルス応答(FIR)フ

ィルタ、可変タップ数

外部サンプル・クロック・オプション: 直接

シングル・コマンドのセルフ・テスト

単電源動作: 3.15 V ~ 3.45 V

2000 g の衝撃耐性

動作温度範囲: -25 °C ~ +85 °C

#### <span id="page-0-1"></span>アプリケーション

スマート農業/建設機械

無人航空機(UAV)/ドローン、ナビゲーション、積載物の安

定化

ロボット装置

<span id="page-0-3"></span>工場/工業用オートメーション、社員/資産の管理

#### <span id="page-0-2"></span>概要

ADIS16460 iSensor® デバイスは、3 軸ジャイロ・センサーと 3 軸加速度センサーを備えた全機能内蔵型の慣性システムです。 ADIS16460 内の各センサーには、業界最先端の iMEMS® 技術と 動的性能を最適化するシグナル・コンディショニングが組み合 わされています。工場出荷時のキャリブレーションで、感度、 バイアス、アライメントについて各センサーの特性が評価され ています。その結果、各センサーは個別の動的補正式を備え、 高精度なセンサー計測を行うことができます。

ADIS16460 は、高精度の多軸慣性センシングを工業用システム に組み込むためのシンプルで費用対効果に優れたソリューショ ンを提供します。これは、とりわけディスクリート部品を使用 した設計と比較して、複雑さや費用面でメリットがあります。 すなわち、製品に必要なモーション・テストと補正が全て工場で の製造工程に組み込まれているため、システムを統合する時間 を大幅に短縮できます。厳密な直交アライメントにより、ナビ ゲーション・システムの慣性フレーム・アライメントが容易にな ります。SPIとレジスタ構造により、データ収集と設定制御のた めのインターフェースが簡単です。

ADIS16460 は、約 22.4 mm×22.4 mm×9 mm のアルミニウム・ モジュール・パッケージに収容され、14 ピンのコネクタ・イン ターフェースを備えています。

#### 機能ブロック図

![](_page_0_Figure_41.jpeg)

アナログ・デバイセズ社は、提供する情報が正確で信頼できるものであることを期していますが、その情報の利用に関して、あるいは利用によって 生じる第三者の特許やその他の権利の侵害に関して一切の責任を負いません。また、アナログ・デバイセズ社の特許または特許の権利の使用を明示 的または暗示的に許諾するものでもありません。仕様は、予告なく変更される場合があります。本紙記載の商標および登録商標は、それぞれの所有 者の財産です。※日本語版資料は REVISION が古い場合があります。最新の内容については、英語版をご参照ください。

©2017 Analog Devices, Inc. All rights reserved

{1}------------------------------------------------

グローバル・コマンド......19

## 目次

| アプリケーション1                                                                               | ソフトウェア・リセット                                                | 19 |
|-----------------------------------------------------------------------------------------|------------------------------------------------------------|----|
| 概要1                                                                                     | フラッシュ・メモリ・テスト                                              | 19 |
| 機能ブロック図1                                                                                | マニュアル・フラッシュ更新                                              | 19 |
| 改訂履歴2                                                                                   | 自動セルフ・テスト                                                  | 19 |
| 仕様3                                                                                     | 入出力の設定                                                     | 19 |
| タイミング仕様5                                                                                | データ・レディ (DR) ピンの設定                                         | 19 |
| 絶対最大定格6                                                                                 | SYNC ピンの設定                                                 | 20 |
| ESD に関する注意6                                                                             | デジタル処理の設定                                                  | 21 |
| ピン配置およびピン機能説明7                                                                          | ジャイロ・センサー/加速度センサー                                          | 21 |
| 代表的な性能特性8                                                                               | キャリブレーション                                                  | 22 |
| 動作原理10                                                                                  | ジャイロ・センサー                                                  | 22 |
| センサー・データの読出し10                                                                          | 加速度センサー                                                    | 22 |
| デバイスの設定11                                                                               | 工場出荷時キャリブレーション値の復元                                         | 23 |
| ユーザ・レジスタ12                                                                              | アプリケーション情報                                                 | 24 |
| 出力データ・レジスタ13                                                                            | 実装上のポイント                                                   | 24 |
| 回転13                                                                                    | 電源に関する考慮事項                                                 | 24 |
| 加速度センサー15                                                                               | ブレークアウト・ボード                                                | 24 |
| 内部温度17                                                                                  | PC ベースの評価ツール                                               | 25 |
| 製品の識別17                                                                                 | 外形寸法                                                       | 26 |
| ステータス/エラー・フラグ17                                                                         | オーダー・ガイド                                                   | 26 |
| システム機能19                                                                                |                                                            |    |
| 改訂履歴                                                                                    | 8/2016—Rev. 0 to Rev. A                                    | 1  |
| 6/2017—Rev. A to Rev. B                                                                 | Changes to Features Section                                |    |
| Changed ML-14-5 to ML-14-6Universal                                                     | Changes to t <sub>NV</sub> Parameter, Table 2              |    |
| Change to Gryoscope/Misalignment/Axis to Axis Parameter, Table 1 .3 Changes to Figure 6 | Changed Acceleration (Shock) Parameter to Mechanical Shock |    |
| Changes to Figure 6                                                                     | Survival Parameter, Table 3                                |    |
| Changes to Figure 28                                                                    | Changes to Burst Read Function Section and Figure 21       |    |
| Changes to Figure 32                                                                    | Change to Dit /, Table 77                                  | 17 |
| Undated Outline Dimensions 26                                                           | 1/2016 Pavision 0. Initial Varsian                         |    |

-2/26-

<span id="page-1-0"></span>Changes to Ordering Guide ....................................

{2}------------------------------------------------

## <span id="page-2-0"></span>仕様

特に指定のない限り、T<sup>A</sup> = 25 °C、VDD = 3.3 V、角速度 = 0°/sec、± 1 *g*、MSC\_CTRL = 0x00C1。

<span id="page-2-4"></span><span id="page-2-3"></span><span id="page-2-2"></span><span id="page-2-1"></span>表 1.

| Parameter                           | Test Conditions/Comments                | Min  | Typ         | Max | Unit          |
|-------------------------------------|-----------------------------------------|------|-------------|-----|---------------|
| GYROSCOPES                          |                                         |      |             |     |               |
| Dynamic Range                       |                                         | ±100 |             |     | °/sec         |
| Initial Sensitivity                 | 16-bit data format1                     |      | 0.005       |     | °/sec/LSB     |
|                                     | 1<br>32-bit data format                 |      | 7.63 × 10−8 |     | °/sec/LSB     |
| Repeatability2                      | 0°C ≤ TA ≤ 70°C                         |      |             | 1   | %             |
| Sensitivity Temperature Coefficient | 0°C ≤ TA ≤ 70°C                         |      | ±20         |     | ppm/°C        |
| Misalignment                        | Axis to axis                            |      | ±0.05       |     | Degrees       |
|                                     | Axis to frame (package)                 |      | ±1          |     | Degrees       |
| Nonlinearity                        | Best fit straight line                  |      | 0.5         |     | % of FS       |
| Bias Repeatability2, 3              | 0°C ≤ TA ≤ 70°C, 1 σ                    |      | 0.5         |     | °/sec         |
| In-Run Bias Stability               | 1 σ                                     |      | 8           |     | °/hr          |
| Angle Random Walk                   | 1 σ, x-axis                             |      | 0.12        |     | °/√hr         |
|                                     | 1 σ, y-axis, z-axis                     |      | 0.17        |     | °/√hr         |
| Bias Temperature Coefficient        | 0°C ≤ TA ≤ 70°C                         |      | ±0.007      |     | °/sec/°C      |
| Linear Acceleration Effect on Bias  | Any axis, 1 σ                           |      | ±0.01       |     | °/sec/g       |
| Vibration Rectification Error       | 20 Hz to 2000 Hz, 5 g rms               |      | ±0.0004     |     | °/sec/g2      |
| Bias Supply Sensitivity             | 3.15 V ≤ VDD ≤ 3.45 V                   |      | 0.037       |     | °/sec/V       |
| Output Noise                        | No filtering                            |      | 0.075       |     | °/sec rms     |
| Rate Noise Density                  | 10 Hz to 40 Hz, no filtering            |      | 0.004       |     | °/sec/√Hz rms |
| −3 dB Bandwidth                     |                                         |      | 375         |     | Hz            |
| Sensor Resonant Frequency           |                                         |      | 65          |     | kHz           |
| ACCELEROMETERS                      | Each axis                               |      |             |     |               |
| Dynamic Range                       |                                         | ±5   |             |     | g             |
| Initial Sensitivity                 | 16-bit data format4                     |      | 0.25        |     | mg/LSB        |
|                                     | 32-bit data format4                     |      | 3.81 × 10−6 |     | mg/LSB        |
| Repeatability2                      | 0°C ≤ TA ≤ 70°C                         |      |             | 1   | %             |
| Sensitivity Temperature Coefficient | 0°C ≤ TA ≤ 70°C                         |      | ±15         |     | ppm/°C        |
| Misalignment                        | Axis to axis                            |      | ±0.05       |     | Degrees       |
|                                     | Axis to frame (package)                 |      | ±1          |     | Degrees       |
| Nonlinearity                        | Best fit straight line                  |      | ±0.1        |     | % of FS       |
| Bias Repeatability2, 3              | 0°C ≤ TA ≤ +70°C, 1 σ                   |      | ±15         |     | mg            |
| In-Run Bias Stability               | 1 σ                                     |      | 0.2         |     | mg            |
| Velocity Random Walk                | 1 σ                                     |      | 0.09        |     | m/sec/√hr     |
| Bias Temperature Coefficient        | 0°C ≤ TA ≤ 70°C                         |      | ±0.05       |     | mg/°C         |
| Vibration Rectification Error       | 20 Hz to 2000 Hz, 1 g rms               |      | 0.08        |     | mg/g2         |
| Bias Supply Sensitivity             | 3.15 V ≤ VDD ≤ 3.45 V                   |      | 72          |     | mg/V          |
| Output Noise                        | No filtering                            |      | 4.5         |     | mg rms        |
| Noise Density                       | 10 Hz to 40 Hz, no filtering            |      | 0.2         |     | mg/√Hz rms    |
| −3 dB Bandwidth                     |                                         |      | 350         |     | Hz            |
| Sensor Resonant Frequency           |                                         |      | 5.5         |     | kHz           |
| TEMPERATURE                         |                                         |      |             |     |               |
|                                     |                                         |      |             |     |               |
| Sensitivity                         | See 内部温度の測定データは TEMP_OUT                |      | 0.05        |     | °C/LSB        |
|                                     | レジスタにロードされます(表 37 参                     |      |             |     |               |
|                                     | 照)。温度データのフォーマットを表                       |      |             |     |               |
|                                     | 38 に示します。この温度は内部温度の                     |      |             |     |               |
|                                     | 測定値であり、外部の状態を正確に表                       |      |             |     |               |
|                                     | すものではないことに注意してくださ                       |      |             |     |               |
|                                     | い。TEMP_OUT の使用目的は温度の<br>相対変化をモニタすることです。 |      |             |     |               |
| LOGIC INPUTS5                       |                                         |      |             |     |               |
| Input High Voltage, VIH             |                                         | 2.0  |             |     | V             |
| Input Low Voltage, VIL              |                                         |      |             | 0.8 | V             |
|                                     |                                         |      |             |     |               |
| Logic 1 Input Current, IIH          | VIH = 3.3 V                             |      | ±0.2        | ±10 | µA            |

<span id="page-2-5"></span>Rev. B - 3/26 -

{3}------------------------------------------------

| Parameter                  | Test Conditions/Comments         | Min    | Typ  | Max  | Unit   |
|----------------------------|----------------------------------|--------|------|------|--------|
| Logic 0 Input Current, IIL | VIL = 0 V                        |        |      |      |        |
| All Pins Except RST        |                                  |        | 40   | 60   | µA     |
| RST Pin                    |                                  |        | 1    |      | mA     |
| Input Capacitance, CIN     |                                  |        | 10   |      | pF     |
| DIGITAL OUTPUTS5           |                                  |        |      |      |        |
| Output High Voltage, VOH   | ISOURCE = 1.6 mA                 | 2.4    |      |      | V      |
| Output Low Voltage, VOL    | ISINK = 1.6 mA                   |        |      | 0.4  | V      |
| FLASH MEMORY               | Endurance6                       | 10,000 |      |      | Cycles |
| Data Retention7            | TJ = 85°C                        | 20     |      |      | Years  |
| FUNCTIONAL TIMES8          | Time until new data is available |        |      |      |        |
| Power-On Start-Up Time     |                                  |        | 290  |      | ms     |
| Reset Recovery Time9, 10   |                                  |        | 222  |      | ms     |
| Reset Initiation Time11    |                                  | 10     |      |      | μs     |
| CONVERSION RATE            |                                  |        |      |      |        |
| x_GYRO_OUT, x_ACCL_OUT     |                                  |        | 2048 |      | SPS    |
| Clock Accuracy             |                                  |        |      | ±3   | %      |
| Sync Input Clock12         | MSC_CTRL[3:2] = 01               | 0.8    |      | 2000 | Hz     |
| PPS Input Clock            | MSC_CTRL[3:2] = 10               |        |      | 128  | Hz     |
| POWER SUPPLY               | Operating voltage range, VDD     | 3.15   | 3.3  | 3.45 | V      |
| Power Supply Current       | VDD = 3.15 V                     |        | 44   | 55   | mA     |

<sup>1</sup> X\_GYRO\_LOW(表 10)、Y\_GYRO\_LOW(表 12)、Z\_GYRO\_LOW(表 14)の各レジスタには、ユーザ設定可能なフィルタに関連するビットの増加分 が取り込まれます。

Rev. B - 4/26 -

<sup>2</sup> 再現性の仕様は、以下のドリフトの要因と条件に基づく分析的な予測を表しています。これらは、温度ヒステリシス(0 °C ~ 70 °C)、電子回路のドリフ ト(高温動作時の寿命テスト: 85 °C、500 時間)、温度サイクルによるドリフト(JESD22、Method A104-C、Method N、500 サイクル、−40 °C ~ +85 °C)、レート・ランダム・ウォーク(10 年予測)、およびブロードバンド・ノイズです。

<sup>3</sup> バイアス再現性は、さまざまな条件での長期的な動作特性を表します。短期再現性は、動作中のバイアス安定度とノイズ密度の仕様に関係しています。

<sup>4</sup> X\_ACCL\_LOW(表 24)、Y\_ACCL\_LOW(表 26)、Z\_ACCL\_LOW(表 28)の各レジスタには、ユーザ設定可能なフィルタに関連するビットの増加分が 取り込まれます。

<sup>5</sup> デジタル I/O 信号は 3.3 V の内部電源で駆動され、入力は 5 V を許容します。

<sup>6</sup> 書換え回数は JEDEC 規格 22 Method A117 に準拠し、−40 °C、+25 °C、+85 °C、+125 °C で測定しています。

<sup>7</sup> 等価データ保持寿命は、JEDEC 規格 22 Method A117 に準拠した 85 °C のジャンクション温度(TJ)での値です。データ保持寿命はジャンクション温度に ともなって短くなります。

<sup>8</sup> これらの時間には、全体の精度に影響を与える可能性がある、熱安定時間と内部フィルタ応答時間(375 Hz 帯域幅)は含まれていません。

<sup>9</sup> このパラメータは、リセット・サイクル開始前に全起動シーケンスが完了していると仮定しています。

<sup>10</sup> このパラメータは、RST ラインの立上がりから DR ラインのパルスがオンに戻る(通常動作に戻る)までの時間を表します。

<sup>11</sup> このパラメータは、リセット動作を確実に開始する RST ラインのパルス時間を表します。

<sup>12</sup> 規定された最小値を下回る同期入力クロックでも動作しますが、性能レベルは低下します。

{4}------------------------------------------------

#### <span id="page-4-0"></span>タイミング仕様

特に指定のない限り、T<sup>A</sup> = 25 °C、VDD = 3.3 V。

<span id="page-4-2"></span><span id="page-4-1"></span>表 2.

|                |                                           |          | Normal Mode |      |      | Burst Read |      |      |
|----------------|-------------------------------------------|----------|-------------|------|------|------------|------|------|
| Parameter      | Description                               | 1<br>Min | Typ         | Max  | Min1 | Typ        | Max  | Unit |
| fSCLK          | Serial clock                              | 0.1      |             | 2.0  | 0.1  |            | 1.0  | MHz  |
| tSTALL         | Stall period between data                 | 16       |             |      | N/A2 |            |      | µs   |
| tREADRATE      | Read rate                                 | 24       |             |      |      |            |      | µs   |
| tCS            | Chip select to SCLK edge                  | 200      |             |      | 200  |            |      | ns   |
| tDAV           | DOUT valid after SCLK edge                |          |             | 25   |      |            | 25   | ns   |
| tDSU           | DIN setup time before SCLK rising edge    | 25       |             |      | 25   |            |      | ns   |
| tDHD           | DIN hold time after SCLK rising edge      | 50       |             |      | 50   |            |      | ns   |
| tSCLKR, tSCLKF | SCLK rise/fall times                      |          | 5           | 12.5 |      | 5          | 12.5 | ns   |
| tDR, tDF       | DOUT rise/fall times                      |          | 5           | 12.5 |      | 5          | 12.5 | ns   |
| tSFS           | CS high after SCLK edge                   | 0        |             |      | 0    |            |      | ns   |
| t1             | Input sync positive pulse width           | 25       |             |      | 25   |            |      | µs   |
| tSTDR          | Input sync to data ready valid transition |          | 636         |      |      | 636        |      | µs   |
| tNV            | Data invalid time                         |          | 47          |      |      | 47         |      | µs   |
| t2             | Input sync period                         | 500      |             |      | 500  |            |      | µs   |

<sup>1</sup> 仕様については出荷テストを行っていませんが、設計と特性評価により保証しています。

#### タイミング図

![](_page_4_Figure_8.jpeg)

Rev. B - 5/26 -

<sup>2</sup> バースト読出しモードを使用する場合、待ち時間は適用されません。

{5}------------------------------------------------

## <span id="page-5-0"></span>絶対最大定格

表 3.

| Parameter                     | Rating                 |
|-------------------------------|------------------------|
| Mechanical Shock Survival     |                        |
| Any Axis, Unpowered           | 2000 g                 |
| Any Axis, Powered             | 2000 g                 |
| VDD to GND                    | −0.3 V to +3.45 V      |
| Digital Input Voltage to GND  | −0.3 V to +5.3 V       |
| Digital Output Voltage to GND | −0.3 V to +VDD + 0.3 V |
| Temperature                   |                        |
| Operating Range               | −25°C to +85°C         |
| Storage Range                 | −65°C to +125°C1, 2    |

<sup>1</sup> −25 °C ~ +8 °C の規定温度の範囲外に長時間放置すると、工場出荷時 のキャリブレーションの精度に悪影響を与える可能性があります。こ の精度を維持するには、デバイスを −25 °C ~ +85 °C の規定動作温度範 囲内で保管する必要があります。

上記の絶対最大定格を超えるストレスを加えると、デバイスに 恒久的な損傷を与えることがあります。この仕様規定は定格の みを指定するものであり、この仕様の動作のセクションに記載 する規定値以上でデバイスが動作することを意味するものでは ありません。長時間にわたり絶対最大定格を超える状態で動作 させると、デバイスの信頼性に影響を与えることがあります。

#### 表 4. パッケージ特性

| Package Type | θJA (°C/W) | θJC (°C/W) | Mass (grams) |
|--------------|------------|------------|--------------|
| ML-14-6      | 36.5       | 16.9       | 15           |

#### <span id="page-5-1"></span>**ESD** に関する注意

![](_page_5_Picture_10.jpeg)

#### **ESD**(静電放電)の影響を受けやすいデバイスです。

電荷を帯びたデバイスや回路ボードは、検知されない まま放電することがあります。本製品は当社独自の特 許技術である ESD 保護回路を内蔵してはいますが、 デバイスが高エネルギーの静電放電を被った場合、損 傷を生じる可能性があります。したがって、性能劣化 や機能低下を防止するため、ESD に対する適切な予防 措置を講じることをお勧めします。

Rev. B - 6/26 -

<sup>2</sup> デバイスは 150 °C の温度に短時間放置しても支障ありませんが、長時 間放置すると機械内部の品質に問題が生じるおそれがあります。

{6}------------------------------------------------

**ADIS16460** 

## <span id="page-6-0"></span>ピン配置およびピン機能説明

ADIS16460 TOP VIEW (Not to Scale)

![](_page_6_Figure_3.jpeg)

- NOTES
  1. THIS REPRESENTS THE PIN ASSIGNMENTS WHEN LOOKING DOWN AT THE CONNECTOR. SEE FIGURE 6.
  2. MATING CONNECTOR: SAMTEC CLM-107-02 SERIES OR EQUIVALENT.
  3. DNC = DO NOT CONNECT.

図 5.ピン配置

![](_page_6_Picture_10.jpeg)

表 5. ピン機能の説明

| Pin No. | Mnemonic | Туре           | Description                              |
|---------|----------|----------------|------------------------------------------|
| 1       | DR       | Output         | データ・レディ・インジケータ。                          |
| 2       | SYNC     | Input/Output   | 外部同期の入出力(MSC_CTRLによる)。表 50 を参照してください。    |
| 3       | SCLK     | Input          | SPIシリアル・クロック。                            |
| 4       | DOUT     | Output         | SPI データ出力。このピンは SCLK の立下がりエッジでクロック出力します。 |
| 5       | DIN      | Input          | SPI データ入力。このピンは SCLK の立上がりエッジでクロック入力します。 |
| 6       | CS       | Input          | SPIチップ・セレクト。                             |
| 7       | DNC      | Not applicable | 接続なし。このピンには接続しないでください。                   |
| 8       | RST      | Input          | リセット。                                    |
| 9       | DNC      | Not applicable | 接続なし。このピンには接続しないでください。                   |
| 10      | DNC      | Not applicable | 接続なし。このピンには接続しないでください。                   |
| 11      | VDD      | Supply         | 電源。                                      |
| 12      | DNC      | Not applicable | 接続なし。このピンには接続しないでください。                   |
| 13      | GND      | Supply         | 電源グラウンド。                                 |
| 14      | DNC      | Not applicable | 接続なし。このピンには接続しないでください。                   |

Rev. B -7/26-

{7}------------------------------------------------

13390-007

## <span id="page-7-0"></span>代表的な性能特性

![](_page_7_Figure_2.jpeg)

図 7. ジャイロ・センサーのルート・アラン分散

![](_page_7_Figure_4.jpeg)

図 8. 低温から高温への温度変化対ジャイロ・センサーの 感度誤差

![](_page_7_Figure_6.jpeg)

図 9. 低温から高温への温度変化対ジャイロ・センサーの バイアス誤差

![](_page_7_Figure_8.jpeg)

図 10. 加速度センサーのルート・アラン分散

13390-008

![](_page_7_Figure_10.jpeg)

図 11. 高温から低温への温度変化対ジャイロ・センサーの 感度誤差

![](_page_7_Figure_12.jpeg)

図 12. 高温から低温への温度変化対ジャイロ・センサーの バイアス誤差

Rev. B - 8/26 -

{8}------------------------------------------------

![](_page_8_Figure_1.jpeg)

図 13. 低温から高温への温度変化対加速度センサーの感度誤差

![](_page_8_Figure_3.jpeg)

図 14. 低温から高温への温度変化対加速度センサーの バイアス誤差

![](_page_8_Figure_5.jpeg)

図 15. 高温から低温への温度変化対加速度センサーの感度誤差

![](_page_8_Figure_7.jpeg)

図 16. 高温から低温への温度変化対加速度センサーの バイアス誤差

Rev. B - 9/26 -

{9}------------------------------------------------

## <span id="page-9-0"></span>動作原理

ADIS16460 は初期化が不要な自律センサー・システムです。 VDD ピンと GND ピンの間に適正な電源が供給されると、この デバイスは自身で初期化を行い、2048 SPS のサンプル・レート でセンサー・データのサンプリング、処理、出力レジスタへの ロードを開始します。各サンプリング・サイクルが完了する と、DR ピン(図 5 参照)のパルスがハイ・レベルになりま す。SPI インターフェースにより、多くの組み込みプロセッサ のプラットフォームと容易に統合することができます(図 17 (電気的接続)と表 6(ピンの機能)を参照)。

![](_page_9_Picture_3.jpeg)

図 17. 電気的接続図

表 6. 一般的なマスター・プロセッサのピン名と機能

| Pin Name | Function                   |
|----------|----------------------------|
| SS       | Slave select               |
| SCLK     | Serial clock               |
| MOSI     | Master output, slave input |
| MISO     | Master input, slave output |
| IRQ      | Interrupt request          |

ADIS16460 の SPI インターフェースは、全二重シリアル通信 (同時送受信)に対応し、図 20 に示すビット・シーケンスを使 用します。ADIS16460 と通信するプロセッサのシリアル・ポー トを初期化する際に注意を要する一般的な設定項目のリストを 表 7 に示します。

表 7. 一般的なマスター・プロセッサの SPI 設定

| Processor Setting | Description                           |
|-------------------|---------------------------------------|
| Master            | The ADIS16460 operates as a slave     |
| SCLK Rate1        | Maximum serial clock rate, see 表 2    |
| SPI Mode 3        | CPOL = 1 (polarity), CPHA = 1 (phase) |
| MSB First         | Bit sequence, see 図 20                |
| 16-Bit Length     | Shift register/data length            |

<sup>1</sup> バースト読出しの場合、SCLK レート は 1 MHz 以内です。

#### <span id="page-9-1"></span>センサー・データの読出し

ADIS16460 では、センサー・データを取得するために、シング ル・レジスタとバースト・レジスタの 2 つのオプションを備えて います。シングル・レジスタ読出しには 2 つの 16 ビット SPI サ イクルを必要とします。最初のサイクルで、図 20 のビット割り 当てを使ってレジスタの値が要求されます。読出しではビット DC7 ~ ビット DC0 はドント・ケアになり、2 番目のシーケンス では DOUT に出力レジスタ値が続きます。連続する 3 つのシン グル・レジスタ読出しを図 18 に示します。

この例では、最初に DIN = 0x0600 で X\_GYRO\_OUT の値を要求 し、続いて 0x0A00 で Y\_GYRO\_OUT の値を、0x0E00 で Z\_GYRO\_OUT の値を要求しています。全二重動作では、プロ セッサが DIN による次のデータ・セットを要求しながら、同じ 16 ビット SPI サイクルを使って DOUT からデータを読み出すこ とができます。繰返しパターンで X\_GYRO\_OUT を読み出すと きの 4 つの SPI 信号の例を図 19 に示します。

![](_page_9_Figure_14.jpeg)

図 19. SPI 読出しの例、2 番目のシーケンス

![](_page_9_Figure_16.jpeg)

**NOTES**

- **1. THE DOUT BIT PATTERN REFLECTS THE ENTIRE CONTENTS OF THE REGISTER IDENTIFIED BY [A6:A0]**
- **IN THE PREVIOUS 16-BIT DIN SEQUENCE WHEN R/W = 0.**
- <span id="page-9-2"></span>**2. IF R/W = 1 DURING THE PREVIOUS SEQUENCE, DOUT IS NOT DEFINED.**

図 20. SPI 通信のビット・シーケンス

13390-012

Rev. B - 10/26 -

{10}------------------------------------------------

#### パースト読出し機能

バースト読出し機能では、1つの連続したビット・ストリーム内の全てのデータを読み出すことができ、各 16 ビット・セグメントの間に待ち時間がありません。図 21 に示すように、このモードは、はじめに DIN = 0x3E00 と設定し、続いて  $\overline{CS}$  をローに保持したまま、DIAG STAT、X GYRO OUT、

Y GYRO OUT, Z GYRO OUT, X ACCL OUT,

Y\_ACCL\_OUT、Z\_ACCL\_OUT、TEMP\_OUT、SMPL\_CNTR、チェックサムの各レジスタを読み出します。次式を使用してチェックサム値を確認します。なお、式中、各バイトを独立した符号なしの8ビット数として扱います。

 $f = y / f + \Delta = DIAG\_STAT [15:8] + DIAG\_STAT [7:0] + X\_GYRO\_OUT [15:8] + X\_GYRO\_OUT [7:0] + Y\_GYRO\_OUT [15:8] + Y\_GYRO\_OUT [7:0] + Z\_GYRO\_OUT [15:8] + Z\_GYRO\_OUT [7:0] + X\_ACCL\_OUT [15:8] + X\_ACCL\_OUT [7:0] + Y\_ACCL\_OUT [15:8] + Y\_ACCL\_OUT [7:0] + Z\_ACCL\_OUT [15:8] + Z\_ACCL\_OUT [7:0] + TEMP\_OUT [15:8] + TEMP\_OUT [7:0] + SMPL\_CNTR [15:8] + SMPL\_CNTR [7:0]$ 

![](_page_10_Figure_6.jpeg)

図 21. バースト読出しシーケンス

#### SPI 読出しのテスト・シーケンス

SPI 通信をテストするためのテスト・パターンを図 22 に示します。このパターンでは、繰返しパターンで DIN ラインに 0x5600 を書き込み、各 16 ビット・シーケンスの待ち時間条件(表 2 参照)を満たした時点でチップ・セレクトを立ち上げます。 DOUT は、2 番目の 16 ビット・シーケンスから開始して、PROD ID レジスタの値 0x404C を生成します(表 41 参照)。

![](_page_10_Figure_10.jpeg)

図 22. SPI 読出しのテスト・パターン(DIN = 0x5600、DOUT = 0x404C)

#### <span id="page-10-0"></span>デバイスの設定

表 8 のコントロール・レジスタを使ってさまざまな設定を選択することができます。SPIでは、図 20 のビット割り当てを使って、一度に 1 バイトずつこれらのレジスタにアクセスします。各レジスタは 16 ビットで、ビット [7:0] は下位アドレスに対応し、ビット [15:8] は上位アドレスに対応します。アドレス0x3Eに 0x01 を書き込む例を図 23 に示します(GLOB\_CMD [1]、DIN=0xBE01 を使用)。

![](_page_10_Figure_14.jpeg)

図 23. SPI 書込みシーケンスの例

#### デュアル・メモリ構造

設定データをコントロール・レジスタに書き込むと、その SRAM (揮発性メモリ) の内容が更新されます。システム内の 関連する各コントロール・レジスタの設定値を最適化したら、 GLOB\_CMD [3] = 1 (DIN = 0xBE08) に設定して、これらの設定値を不揮発性フラッシュ・メモリにコピーします。フラッシュ更新処理では、全処理時間の間、適正な電源レベルを必要とします(表 44 参照)。ユーザ・レジスタのメモリ・マップを表 8 に示します。この表にはフラッシュ・バックアップ情報の欄があります。この欄が「yes」の場合は、そのレジスタにフラッシュのミラー・ロケーションがあることを示しており、適正にバックアップされると、起動中やリセット後に自動的に復元されます。動作の管理や重要なユーザ設定値の保存に使用するデュアル・メモリ構造を図 24 に示します。

![](_page_10_Figure_18.jpeg)

図 24. SRAM とフラッシュ・メモリの図

Rev. B — 11/26 —

{11}------------------------------------------------

## <span id="page-11-0"></span>ユーザ・レジスタ

表 8. ユーザ・レジスタのメモリ・マップ<sup>1</sup>

| Name       | R/W | Flash Backup | Address2         | Default | Function                                | Bit Assignments |
|------------|-----|--------------|------------------|---------|-----------------------------------------|-----------------|
| FLASH_CNT  | R   | Yes          | 0x00             | N/A     | Flash memory write count                | See Table 49    |
| DIAG_STAT  | R   | No           | 0x02             | 0x0000  | Diagnostic and operational status       | See Table 43    |
| X_GYRO_LOW | R   | No           | 0x04             | N/A     | X-axis gyroscope output, lower word     | See Table 10    |
| X_GYRO_OUT | R   | No           | 0x06             | N/A     | X-axis gyroscope output, upper word     | See Table 11    |
| Y_GYRO_LOW | R   | No           | 0x08             | N/A     | Y-axis gyroscope output, lower word     | See Table 12    |
| Y_GYRO_OUT | R   | No           | 0x0A             | N/A     | Y-axis gyroscope output, upper word     | See Table 13    |
| Z_GYRO_LOW | R   | No           | 0x0C             | N/A     | Z-axis gyroscope output, lower word     | See Table 14    |
| Z_GYRO_OUT | R   | No           | 0x0E             | N/A     | Z-axis gyroscope output, upper word     | See Table 15    |
| X_ACCL_LOW | R   | No           | 0x10             | N/A     | X-axis accelerometer output, lower word | See Table 24    |
| X_ACCL_OUT | R   | No           | 0x12             | N/A     | X-axis accelerometer output, upper word | See Table 25    |
| Y_ACCL_LOW | R   | No           | 0x14             | N/A     | Y-axis accelerometer output, lower word | See Table 26    |
| Y_ACCL_OUT | R   | No           | 0x16             | N/A     | Y-axis accelerometer output, upper word | See Table 27    |
| Z_ACCL_LOW | R   | No           | 0x18             | N/A     | Z-axis accelerometer output, lower word | See Table 28    |
| Z_ACCL_OUT | R   | No           | 0x1A             | N/A     | Z-axis accelerometer output, upper word | See Table 29    |
| SMPL_CNTR  | R   | No           | 0x1C             | N/A     | Sample counter, MSC_CTRL[3:2] = 11      | See Table 52    |
| TEMP_OUT   | R   | No           | 0x1E             | N/A     | Temperature (internal, not calibrated)  | See Table 37    |
| Reserved   | N/A | N/A          | 0x20, 0x22       | N/A     | Reserved, do not use                    | N/A             |
| X_DELT_ANG | R   | No           | 0x24             | N/A     | X-axis delta angle output               | See Table 18    |
| Y_DELT_ANG | R   | No           | 0x26             | N/A     | Y-axis delta angle output               | See Table 19    |
| Z_DELT_ANG | R   | No           | 0x28             | N/A     | Z-axis delta angle output               | See Table 20    |
| X_DELT_VEL | R   | No           | 0x2A             | N/A     | X-axis delta velocity                   | See Table 32    |
| Y_DELT_VEL | R   | No           | 0x2C             | N/A     | Y-axis delta velocity                   | See Table 33    |
| Z_DELT_VEL | R   | No           | 0x2E             | N/A     | Z-axis delta velocity                   | See Table 34    |
| Reserved   | N/A | N/A          | 0x30             | N/A     | Reserved, do not use                    | N/A             |
| MSC_CTRL   | R/W | Yes          | 0x32             | 0x00C1  | Miscellaneous control                   | See Table 50    |
| SYNC_SCAL  | R/W | Yes          | 0x34             | 0x7FFF  | Sync input scale control                | See Table 51    |
| DEC_RATE   | R/W | Yes          | 0x36             | 0x0000  | Decimation rate control                 | See Table 53    |
| FLTR_CTRL  | R/W | Yes          | 0x38             | 0x0500  | Filter control, autonull record time    | See Table 54    |
| Reserved   | N/A | N/A          | 0x3A, 0x3C       | N/A     | Reserved, do not use                    | N/A             |
| GLOB_CMD   | W   | No           | 0x3E             | N/A     | Global commands                         | See Table 44    |
| X_GYRO_OFF | R/W | Yes          | 0x40             | 0x0000  | X-axis gyroscope bias offset factor     | See Table 55    |
| Y_GYRO_OFF | R/W | Yes          | 0x42             | 0x0000  | Y-axis gyroscope bias offset factor     | See Table 56    |
| Z_GYRO_OFF | R/W | Yes          | 0x44             | 0x0000  | Z-axis gyroscope bias offset factor     | See Table 57    |
| X_ACCL_OFF | R/W | Yes          | 0x46             | 0x0000  | X-axis acceleration bias offset factor  | See Table 58    |
| Y_ACCL_OFF | R/W | Yes          | 0x48             | 0x0000  | Y-axis acceleration bias offset factor  | See Table 59    |
| Z_ACCL_OFF | R/W | Yes          | 0x4A             | 0x0000  | Z-axis acceleration bias offset factor  | See Table 60    |
| Reserved   | N/A | N/A          | 0x4C, 0x4E, 0x50 | N/A     | Reserved, do not use                    | N/A             |
| LOT_ID1    | R   | Yes          | 0x52             | N/A     | Lot Identification Number 1             | See Table 39    |
| LOT_ID2    | R   | Yes          | 0x54             | N/A     | Lot Identification Number 2             | See Table 40    |
| PROD_ID    | R   | Yes          | 0x56             | 0x404C  | Product identifier                      | See Table 41    |
| SERIAL_NUM | R   | Yes          | 0x58             | N/A     | Lot specific serial number              | See Table 42    |
| CAL_SGNTR  | R   | N/A          | 0x60             | N/A     | Calibration memory signature value      | See Table 46    |
| CAL_CRC    | R   | N/A          | 0x62             | N/A     | Calibration memory CRC values           | See Table 48    |
| CODE_SGNTR | R   | N/A          | 0x64             | N/A     | Code memory signature value             | See Table 45    |
| CODE_CRC   | R   | N/A          | 0x66             | N/A     | Code memory CRC values                  | See Table 47    |

<sup>1</sup> N/A は適用なしを表します。

Rev. B - 12/26 -

<sup>2</sup> 各レジスタは 2 バイトで構成されます。示されているアドレスは下位バイトのものです。上位バイトのアドレスは下位バイトのアドレスに 1 を足した値で す。

{12}------------------------------------------------

## <span id="page-12-0"></span>出力データ・レジスタ

出力データ・レジスタには、慣性センサー(ジャイロ・センサ ー、加速度センサー)の測定値、角度変化の計算値、速度変化 の計算値、相対温度のモニタ値などが含まれています。

#### <span id="page-12-1"></span>回転

ADIS16460 は、*i*MEMS ジャイロ・センサーを用い、角速度と角 度変位(角度変化)の 2 つの異なるフォーマットを使って、3 つの直交軸周りで回転慣性測定を行います。それぞれの出力レ ジスタ(表 9 参照)の正の応答に対応する軸割り当てと回転の 方向を図 26 に示します。

#### 角速度のデータ

回転角速度のデータは、3 軸 MEMS ジャイロ・センサーからの 補正された応答を表します。6 個のレジスタにより、これらの 測定値にリアルタイムでアクセスすることができます。各軸に はプライマリ・レジスタとセカンダリ・レジスタ の 2 つの専用 レジスタがあります。図 26 の 3 つの軸(ωX、ωY、ωZ)のそれ ぞれに対するレジスタ割り当てを表 9 に示します。

表 9. 回転角速度のデータ・レジスタ

| Axis | Primary Register      | Secondary Register    |
|------|-----------------------|-----------------------|
| ωX   | X_GYRO_OUT (see Table | X_GYRO_LOW (see Table |
|      | 11)                   | 10)                   |
| ωY   | Y_GYRO_OUT(see Table  | Y_GYRO_LOW (see Table |
|      | 13)                   | 12)                   |
| ωZ   | Z_GYRO_OUT (see       | Z_GYRO_LOW (see       |
|      | Table 15)             | Table 14)             |

プライマリ・レジスタは、16 ビットの 2 の補数を供給します。 ここで、スケール・ファクタ(KG)は 0.005°/sec/LSB に等しい 値です。セカンダリ・レジスタは、ユーザ設定可能なデジタ ル・フィルタ(表 53 と表 54 を参照)の加算関数に関連するビ ットの増加分を捕捉できるようにします。X 軸周りの回転角速 度に対して最大 32 ビットのデジタル分解能のデジタル値を生成 するための、プライマリ・レジスタ(X\_GYRO\_OUT)とセカ ンダリ・レジスタ(X\_GYRO\_LOW)の組み合わせ方を、図 25 に示します。

![](_page_12_Figure_10.jpeg)

図 25. 32 ビット・ジャイロ・センサーのデータ・フォーマット

表 10. X\_GYRO\_LOW(ベース・アドレス = 0x04)、読出し専 用

| Bits   | Description                          |
|--------|--------------------------------------|
| [15:0] | X-axis, gyroscope, output data       |
|        | Bit growth from X_GYRO_OUT data path |

表 11. X\_GYRO\_OUT(ベース・アドレス = 0x06)、読出し専 用

| Bits   | Description                                        |
|--------|----------------------------------------------------|
| [15:0] | X-axis, gyroscope output data, 0.005°/sec/LSB (KG) |
|        | 0°/sec = 0x0000, twos complement format            |

表 12. Y\_GYRO\_LOW(ベース・アドレス = 0x08)、読出し専 用

| Bits   | Description                          |
|--------|--------------------------------------|
| [15:0] | Y-axis, gyroscope, output data       |
|        | Bit growth from Y_GYRO_OUT data path |

表 13. Y\_GYRO\_OUT(ベース・アドレス = 0x0A)、読出し専 用

| Bits   | Description                                        |
|--------|----------------------------------------------------|
| [15:0] | Y-axis, gyroscope output data, 0.005°/sec/LSB (KG) |
|        | 0°/sec = 0x0000, twos complement format            |

表 14. Z\_GYRO\_LOW(ベース・アドレス =0x0C)、読出し専 用

| Bits   | Description                          |  |
|--------|--------------------------------------|--|
| [15:0] | Z-axis, gyroscope, output data       |  |
|        | Bit growth from Z_GYRO_OUT data path |  |

表 15. Z\_GYRO\_OUT(ベース・アドレス = 0x0E)、読出し専 用

| Bits   | Description                                        |
|--------|----------------------------------------------------|
| [15:0] | Z-axis, gyroscope output data, 0.005°/sec/LSB (KG) |
|        | 0°/sec = 0x0000, twos complement format            |

![](_page_12_Picture_24.jpeg)

Rev. B - 13/26 -

{13}------------------------------------------------

16 ビット測定にプライマリ・レジスタのみを使う場合の、デジ タル・データ・フォーマットの 7 つの例を表 16 に示します。

表 16. 回転速度、16 ビットの例

| Rotation     |         |        |                     |
|--------------|---------|--------|---------------------|
| Rate (°/sec) | Decimal | Hex    | Binary              |
|              |         |        |                     |
| +100         | 20,000  | 0x4E20 | 0100 1110 0010 0000 |
| +0.01        | +2      | 0x0002 | 0000 0000 0000 0010 |
| +0.005       | +1      | 0x0001 | 0000 0000 0000 0001 |
| 0            | 0       | 0x0000 | 0000 0000 0000 0000 |
| −0.005       | −1      | 0xFFFF | 1111 1111 1111 1111 |
| −0.01        | −2      | 0xFFFE | 1111 1111 1111 1110 |
| −100         | −20,000 | 0xB1E0 | 1011 0001 1110 0000 |

全てではないとしても、多くの場合、センサーの主要な性能基 準を維持するために、アプリケーションが 32 ビットのデジタル 分解能の全てを必要とすることはありません。データ幅を小さ いビット数に切り詰める場合、以下の式を使って最下位ビット に対するスケール・ファクタを計算します。

$$1 LSB = K_G \times \frac{1}{2^{N-16}}$$

ここで、N は全ビット数です。

例えば、システムが X\_GYRO\_LOW レジスタの 4 ビットを使用 する場合、データ幅は 20 ビットになり、LSB の重みは 0.0003215°/sec に等しい値になります。

$$1 LSB = 0.005^{\circ} / sec \times \frac{1}{2^{20-16}}$$

$$1 LSB = 0.005^{\circ} / sec \times \frac{1}{16} = 0.0003125^{\circ} / sec$$

プライマリ・レジスタとセカンダリ・レジスタを使って回転角 速度に対する 20 ビット数を生成する場合の、デジタル・デー タ・フォーマットの 7 つの例を表 17 に示します。

表 17. 回転速度、20 ビットの例

| Rotation<br>Rate |          |         |                          |
|------------------|----------|---------|--------------------------|
| (°/sec)          | Decimal  | Hex     | Binary                   |
| +100             | +320,000 | 0x4E200 | 0100 1110 0010 0000 0000 |
| +0.000625        | +2       | 0x00002 | 0000 0000 0000 0000 0010 |
| +0.0003125       | +1       | 0x00001 | 0000 0000 0000 0000 0001 |
| 0                | 0        | 0x00000 | 0000 0000 0000 0000 0000 |
| −0.0003125       | −1       | 0xFFFFF | 1111 1111 1111 1111 1111 |
| −0.000625        | −2       | 0xFFFFE | 1111 1111 1111 1111 1110 |
| −100             | −320,000 | 0xB1E00 | 1011 0001 1110 0000 0000 |

#### 角度変化のデータ

角度変化の測定値(図 26 の ΔθX、ΔθY、ΔθZ)は、各データ処理 サイクルでのそれぞれの軸周りの角度変位を表します。各軸 (x、y、z)には専用のレジスタがあり、その 3 つのレジスタに よって、これらの測定値にリアルタイムでアクセスできます。 X\_DELT\_ANG(表 18 参照)は x 軸の出力データ・レジスタ (図 26 の ΔθX)、Y\_DELT\_ANG(表 19 参照)は y 軸の出力デ ータ・レジスタ(図 26 の ΔθY)、Z\_DELT\_ANG(表 20 参照) は z 軸の出力データ・レジスタ(図 26 の ΔθZ)です。これらの レジスタのスケール・ファクタは、ジャイロ・センサーのスケ ール・ファクタ(表 11 参照、K<sup>G</sup> = 0.005°/sec/LSB)、 MSC\_CTRL[3:2](表 50 参照)に関連するサンプル・クロッ ク(fSAMPLE)、およびデシメーション・レートの設定値 (DEC\_RATE、表 53 参照)に依存します。

表 18. X\_DELT\_ANG(ベース・アドレス = 0x24)、読出し専 用

| Bits   | Description                                                |
|--------|------------------------------------------------------------|
| [15:0] | X-axis, delta angle output data                            |
|        | 0° = 0x0000, twos complement format                        |
|        | 1 LSB = KG × (DEC_RATE + 1)/fSAMPLE (degrees)              |
|        | fSAMPLE = 2048 Hz when MSC_CTRL[3:2] = 00                  |
|        | fSAMPLE is the external clock rate when MSC_CTRL[3:2] ≠ 00 |

表 19.Y\_DELT\_ANG(ベース・アドレス = 0x26)、読出し専用

| Bits   | Description                                                |
|--------|------------------------------------------------------------|
| [15:0] | Y-axis, delta angle output data                            |
|        | 0° = 0x0000, twos complement format                        |
|        | 1 LSB = KG × (DEC_RATE + 1)/fSAMPLE (degrees)              |
|        | fSAMPLE =2048 Hz when MSC_CTRL[3:2] = 00                   |
|        | fSAMPLE is the external clock rate when MSC_CTRL[3:2] ≠ 00 |

表 20. Z\_DELT\_ANG(ベース・アドレス = 0x28)、読出し専 用

| Bits                                      | Description                                                |
|-------------------------------------------|------------------------------------------------------------|
| [15:0]<br>Z-axis, delta angle output data |                                                            |
|                                           | 0° = 0x0000, twos complement format                        |
|                                           | 1 LSB = KG × (DEC_RATE + 1)/fSAMPLE (degrees)              |
|                                           | fSAMPLE = 2048 Hz when MSC_CTRL[3:2] = 00                  |
|                                           | fSAMPLE is the external clock rate when MSC_CTRL[3:2] ≠ 00 |

MSC\_CTRL[3:2]= 00(fSAMPLE = 2048 Hz)、DEC\_RATE = 0x0000 のときの数値による角度変化のデータ・フォーマットの 例を表 21 に示します。

表 21. x\_DELT\_ANG データ・フォーマット、例 1

| Angle (°)1    | Decimal | Hex    | Binary                 |
|---------------|---------|--------|------------------------|
| +0.079998     | +32,767 | 0x7FFF | 0111 1111 1111 1111    |
| +0.0000048828 | +2      | 0x0002 | 0000 0000 0000<br>0010 |
| +0.0000024414 | +1      | 0x0001 | 0000 0000 0000<br>0001 |
| 0             | 0       | 0x0000 | 0000 0000 0000<br>0000 |
| −0.0000024414 | −1      | 0xFFFF | 1111 1111 1111 1111    |
| −0.0000048828 | −2      | 0xFFFE | 1111 1111 1111 1110    |
| −0.080000     | −32,768 | 0x8000 | 1000 0000 0000<br>0000 |

<sup>1</sup> MSC\_CTRL[3:2]= 00、fSAMPLE = 2048 Hz、DEC\_RATE = 0x0000。 MSC\_CTRL[3:2]= 01、外部クロック・レート(fSAMPLE)= 2000 Hz、DEC\_RATE = 0x0009 のときの数値による角度変化の データ・フォーマットの例を表 22 に示します。

表 22. x\_DELT\_ANG データ・フォーマット、例 2

| Angle (°)1 | Decimal | Hex    | Binary              |
|------------|---------|--------|---------------------|
| +0.81918   | +32,767 | 0x7FFF | 0111 1111 1111 1111 |
| +0.000050  | +2      | 0x0002 | 0000 0000 0000 0010 |
| +0.000025  | +1      | 0x0001 | 0000 0000 0000 0001 |
| 0          | 0       | 0x0000 | 0000 0000 0000 0000 |
| −0.000025  | −1      | 0xFFFF | 1111 1111 1111 1111 |
| −0.000050  | −2      | 0xFFFE | 1111 1111 1111 1110 |
| −0.81920   | −32,768 | 0x8000 | 1000 0000 0000 0000 |

<sup>1</sup> MSC\_CTRL[3:2]= 01、fSAMPLE = 2000 Hz、DEC\_RATE = 0x0009。

Rev. B - 14/26 -

{14}------------------------------------------------

#### <span id="page-14-0"></span>加速度センサー

ADIS16460 は、*i*MEMS 加速度センサーを用い、線形加速度と速 度変化の 2 つの異なるフォーマットを使って、3 つの直交軸に 沿って線形慣性を測定します。軸割り当てと、それぞれの出力 レジスタ(表 9 参照)の正の応答に対応する線形加速度の方向 を図 28 に示します。

#### 線形加速度

線形加速度の測定値は、3 軸 MEMS 加速度センサーからの補正 された応答を表します。6 個のレジスタにより、これらの測定 値にリアルタイムでアクセスすることができます。各軸にはプ ライマリ・レジスタとセカンダリ・レジスタ の 2 つの専用レジ スタがあります。図 28 の 3 つの軸(aX、aY、aZ)のそれぞれに 対するレジスタ割り当てを表 23 に示します。

表 23. 線形加速度のデータ・レジスタ

| Axis | Primary Register      | Secondary Register    |
|------|-----------------------|-----------------------|
| aX   | X_ACCL_OUT (see Table | X_ACCL_LOW (see Table |
|      | 25)                   | 24)                   |
| aY   | Y_ACCL_OUT (see Table | Y_ACCL_LOW (see Table |
|      | 27)                   | 26)                   |
| aZ   | Z_ACCL_OUT (see       | Z_ACCL_LOW (see       |
|      | Table 29)             | Table 28)             |

プライマリ・レジスタは、16 ビットの 2 の補数を与えます。こ こで、スケール・ファクタ(KA)は 0.25 m*g*/LSB に等しい値で す。セカンダリ・レジスタは、ユーザ設定可能なデジタル・フ ィルタ(表 53 と表 54 を参照)の加算関数に関連するビットの 増加分を捕捉できるようにします。プライマリ・レジスタ

(X\_ACCL\_OUT)とセカンダリ・レジスタ(X\_ACCL\_LOW) をどのように組み合わせて、X 軸に沿った線形加速度に対して 最大 32 ビットのデジタル分解能のデジタル値を生成するかを図 27 に示します。

![](_page_14_Figure_9.jpeg)

図 27. 32 ビット加速度センサーのデータ・フォーマット

表 24. X\_ACCL\_LOW(ベース・アドレス = 0x10)、読出し専 用

|  | Bits   | Description                          |
|--|--------|--------------------------------------|
|  | [15:0] | X-axis, accelerometer, output data   |
|  |        | Bit growth from X_ACCL_OUT data path |

表 25. X\_ACCL\_OUT(ベース・アドレス = 0x12)、読出し専 用

| Bits   | Description                                          |
|--------|------------------------------------------------------|
| [15:0] | X-axis, accelerometer output data, 0.25 mg /LSB (KA) |
|        | 0 mg = 0x0000, twos complement format                |

表 26. Y\_ACCL\_LOW(ベース・アドレス = 0x14)、読出し専 用

| Bits   | Description                          |  |
|--------|--------------------------------------|--|
| [15:0] | Y-axis, accelerometer, output data   |  |
|        | Bit growth from Y_ACCL_OUT data path |  |

表 27. Y\_ACCL\_OUT(ベース・アドレス = 0x16)、読出し専 用

| Bits   | Description                                         |  |
|--------|-----------------------------------------------------|--|
| [15:0] | Y-axis, accelerometer output data, 0.25 mg/LSB (KA) |  |
|        | 0 mg = 0x0000, twos complement format               |  |

表 28. Z\_ACCL\_LOW(ベース・アドレス = 0x18)、読出し専 用

| Bits<br>Description |                                      |  |
|---------------------|--------------------------------------|--|
| [15:0]              | Z-axis, accelerometer, output data   |  |
|                     | Bit growth from Z_ACCL_OUT data path |  |

表 29. Z\_ACCL\_OUT(ベース・アドレス = 0x1A)、読出し専 用

| Bits   | Description                                         |  |
|--------|-----------------------------------------------------|--|
| [15:0] | Z-axis, accelerometer output data, 0.25 mg/LSB (KA) |  |
|        | 0 mg = 0x0000, twos complement format               |  |

![](_page_14_Figure_23.jpeg)

Rev. B - 15/26 -

{15}------------------------------------------------

16 ビット測定にプライマリ・レジスタのみを使う場合の、デジ タル・データ・フォーマットの 7 つの例を表 30 に示します。

表 30. 加速度、2 の補数フォーマット

| Acceleration (mg) | Decimal | Hex    | Binary              |
|-------------------|---------|--------|---------------------|
| +5000             | 20,000  | 0x4E20 | 0100 1110 0010 0000 |
| +0.5              | +2      | 0x0002 | 0000 0000 0000 0010 |
| +0.25             | +1      | 0x0001 | 0000 0000 0000 0001 |
| 0                 | 0       | 0x0000 | 0000 0000 0000 0000 |
| −0.25             | −1      | 0xFFFF | 1111 1111 1111 1111 |
| −0.5              | −2      | 0xFFFE | 1111 1111 1111 1110 |
| −5000             | −20,000 | 0xB1E0 | 1011 0001 1110 0000 |

全てではないとしても、多くの場合、センサーの主要な性能基 準を維持するために、アプリケーションが 32 ビットのデジタル 分解能の全てを必要とすることはありません。データ幅を小さ いビット数に切り詰める場合、以下の式を使って最下位ビット に対するスケール・ファクタを計算します。

$$1 LSB = K_A \times \frac{1}{2^{N-16}}$$

ここで、N は全ビット数です。

例えば、システムが X\_ACCL\_LOW レジスタから 2 ビットを使 用する場合、データ幅は 18 ビットになり、LSB の重みは 0.0625 m*g* に等しい値になります。

$$1 LSB = 0.25 mg \times \frac{1}{2^{18-16}}$$

$$1 LSB = 0.25 mg \times \frac{1}{4} = 0.0625 mg$$

プライマリ・レジスタとセカンダリ・レジスタを使って回転角 速度に対する 18 ビット数を生成する場合の、デジタル・デー タ・フォーマットの 7 つの例を表 31 に示します。

表 31. 加速度、18 ビットの例

| Acceleration |         |         |                        |
|--------------|---------|---------|------------------------|
| (mg)         | Decimal | Hex     | Binary                 |
| +5000        | 80,000  | 0x13880 | 01 0011 1000 1000 0000 |
| +0.125       | +2      | 0x00002 | 00 0000 0000 0000 0010 |
| +0.0625      | +1      | 0x00001 | 00 0000 0000 0000 0001 |
| 0            | 0       | 0x00000 | 00 0000 0000 0000 0000 |
| −0.0625      | −1      | 0x3FFFF | 11 1111 1111 1111 1111 |
| −0.125       | −2      | 0x3FFFE | 11 1111 1111 1111 1110 |
| −5000        | −80,000 | 0x2C780 | 10 1100 0111 1000 0000 |

#### 速度変化のデータ

速度変化の測定値(図 28 の ΔVX、ΔVY、ΔVZ)は、各データ処 理サイクルでのそれぞれの軸に沿った速度変化を表します。各 軸(x、y、z)には専用のレジスタがあり、その 3 つのレジスタ によって、これらの測定値にリアルタイムでアクセスできま す。X\_DELT\_VEL(表 32 参照)は x 軸の出力データ・レジス タ(図 28 の ΔVX)、Y\_DELT\_VEL(表 33 参照)は y 軸の出力 データ・レジスタ(図 28 の ΔVY)、Z\_DELT\_VEL(表 34 参 照)は z 軸の出力データ・レジスタ(図 28 の ΔVZ)です。これ らのレジスタのスケール・ファクタは、加速度センサーのスケ ール・ファクタ(表 25 参照、K<sup>A</sup> = 0.25 m*g*/sec/LSB)、 MSC\_CTRL[3:2](表 50 参照)に関連するサンプル・クロッ ク(fSAMPLE)、およびデシメーション・レートの設定値 (DEC\_RATE、表 53 参照)に依存します。

表 32. X\_DELT\_VEL(ベース・アドレス = 0x2A)、読出し専用

| Bits                                              | Description                                                |  |
|---------------------------------------------------|------------------------------------------------------------|--|
| [15:0]                                            | X-axis, delta velocity output data                         |  |
|                                                   | 0° = 0x0000, twos complement format                        |  |
| 1 LSB = KA × 10 × (DEC_RATE + 1)/fSAMPLE (mm/sec) |                                                            |  |
|                                                   | fSAMPLE = 2048 Hz when MSC_CTRL[3:2] = 00                  |  |
|                                                   | fSAMPLE is the external clock rate when MSC_CTRL[3:2] ≠ 00 |  |

表 33. Y\_DELT\_VEL(ベース・アドレス = 0x2C)、読出し専 用

| Bits   | Description                                                |  |
|--------|------------------------------------------------------------|--|
| [15:0] | Y-axis, delta velocity output data                         |  |
|        | 0° = 0x0000, twos complement format                        |  |
|        | 1 LSB = KA × 10 × (DEC_RATE + 1)/fSAMPLE (mm/sec)          |  |
|        | fSAMPLE = 2048 Hz when MSC_CTRL[3:2] = 00                  |  |
|        | fSAMPLE is the external clock rate when MSC_CTRL[3:2] ≠ 00 |  |

表 34. Z\_DELT\_VEL(ベース・アドレス = 0x2E)、読出し専用

| Bits   | Description                                                |  |  |
|--------|------------------------------------------------------------|--|--|
| [15:0] | Z-axis, delta velocity output data                         |  |  |
|        | 0° = 0x0000, twos complement format                        |  |  |
|        | 1 LSB = KA × 10 × (DEC_RATE + 1)/fSAMPLE (mm/sec)          |  |  |
|        | fSAMPLE =2048 Hz when MSC_CTRL[3:2] = 00                   |  |  |
|        | fSAMPLE is the external clock rate when MSC_CTRL[3:2] ≠ 00 |  |  |

MSC\_CTRL[3:2]= 00、fSAMPLE = 2048 Hz、DEC\_RATE = 0x0000 のときの数値による速度変化のデータ・フォーマットの 例を表 35 に示します。

表 35. x\_\_DELT\_VEL データ・フォーマット、例 1

| Velocity<br>1<br>(mm/sec) | Decimal | Hex    | Binary              |
|---------------------------|---------|--------|---------------------|
| +39.999                   | +32,767 | 0x7FFF | 0111 1111 1111 1111 |
| +0.0024414                | +2      | 0x0002 | 0000 0000 0000 0010 |
| +0.0012207                | +1      | 0x0001 | 0000 0000 0000 0001 |
| 0                         | 0       | 0x0000 | 0000 0000 0000 0000 |
| −0.0012207                | −1      | 0xFFFF | 1111 1111 1111 1111 |
| −0.0024414                | −2      | 0xFFFE | 1111 1111 1111 1110 |
| −40                       | −32,768 | 0x8000 | 1000 0000 0000 0000 |

<sup>1</sup> MSC\_CTRL[3:2]= 00、fSAMPLE = 2840 Hz、DEC\_RATE = 0x0000。

Rev. B - 16/26 -

{16}------------------------------------------------

MSC\_CTRL[3:2]= 01、fSAMPLE = 2000 Hz、DEC\_RATE = 0x0009 のときの数値による速度変化のデータ・フォーマットの 例を表 36 に示します。

表 36. x\_\_DELT\_VEL データ・フォーマット、例 2

| Velocity<br>(mm/sec)1 | Decimal | Hex    | Binary              |
|-----------------------|---------|--------|---------------------|
| +409.59               | +32,767 | 0x7FFF | 0111 1111 1111 1111 |
| +0.0250               | +2      | 0x0002 | 0000 0000 0000 0010 |
| +0.0125               | +1      | 0x0001 | 0000 0000 0000 0001 |
| 0                     | 0       | 0x0000 | 0000 0000 0000 0000 |
| −0.0125               | −1      | 0xFFFF | 1111 1111 1111 1111 |
| −0.0250               | −2      | 0xFFFE | 1111 1111 1111 1110 |
| −409.6                | −32,768 | 0x8000 | 1000 0000 0000 0000 |

<sup>1</sup>MSC\_CTRL[3:2]= 01、fSAMPLE = 2000 Hz、DEC\_RATE = 0x0009。

#### <span id="page-16-0"></span>内部温度

<span id="page-16-3"></span>内部温度の測定データは TEMP\_OUT レジスタにロードされま す(表 37 参照)。温度データのフォーマットを表 38 に示しま す。この温度は内部温度の測定値であり、外部の状態を正確に 表すものではないことに注意してください。TEMP\_OUT の使用 目的は温度の相対変化をモニタすることです。

表 37. TEMP\_OUT(ベース・アドレス = 0x1E)、読出し専用

| Bits   | Description                                |
|--------|--------------------------------------------|
| [15:0] | Twos complement, 0.05°C/LSB, 25°C = 0x0000 |

表 38. 温度、2 の補数フォーマット

| Temperature (°C) | Decimal | Hex    | Binary              |
|------------------|---------|--------|---------------------|
| +105             | +1600   | 0x0640 | 0000 0110 0100 0000 |
| +85              | +1200   | 0x04B0 | 0000 0100 1011 0000 |
| +25.1            | +2      | 0x0002 | 0000 0000 0000 0010 |
| +25.05           | +1      | 0x0001 | 0000 0000 0000 0001 |
| +25              | 0       | 0x0000 | 0000 0000 0000 0000 |
| +24.95           | −1      | 0xFFFF | 1111 1111 1111 1111 |
| +24.90           | −2      | 0xFFFE | 1111 1111 1111 1110 |
| −40              | −1300   | 0xFAEC | 1111 1010 1110 1100 |

#### <span id="page-16-1"></span>製品の識別

PROD\_ID レジスタには、16,460 に相当する 2 進数が含まれてい ます(表 41 参照)。このレジスタは、システム・ソフトウェア で製品固有の変数を追跡する必要のあるシステムに、この変数 を提供します。LOT\_ID1 レジスタと LOT\_ID2 レジスタとが組 み合わされて、固有の 32 ビット・ロット識別コードが提供され ます(表 39 と表 40 を参照)。

SERIAL\_NUM レジスタには、デバイス・ラベルのシリアル・ナ ンバーを表す 2 進数が含まれています(表 42 参照)。 SERIAL\_NUM に割り当てられたシリアル・ナンバーは、ロット に固有のものです。

表 39. LOT\_ID1(ベース・アドレス = 0x52)、読出し専用

| Bits   | Description                     |
|--------|---------------------------------|
| [15:0] | Lot identification, binary code |

#### 表 40. LOT\_ID2(ベース・アドレス = 0x54)、読出し専用

| Bits   | Description                     |
|--------|---------------------------------|
| [15:0] | Lot identification, binary code |

#### 表 41. PROD\_ID(ベース・アドレス = 0x56)、読出し専用

| Bits   | Description (Default = 0x404C)           |
|--------|------------------------------------------|
| [15:0] | Product identification = 0x404C (16,460) |

#### 表 42. SERIAL\_NUM(ベース・アドレス = 0x58)、読出し専 用

| Bits    | Description                      |
|---------|----------------------------------|
| [15:12] | Reserved, values can vary        |
| [11:0]  | Serial number, 1 to 4094 (0xFFE) |

#### <span id="page-16-2"></span>ステータス/エラー・フラグ

表 43 の DIAG\_STAT レジスタには、フラッシュ更新、通信、オ ーバーレンジ、セルフ・テスト、メモリの完全性に対するエラ ー・フラグとして機能する各種ビットが含まれています。この レジスタを読み出すことにより、各フラグの状態にアクセス し、その後の動作のモニタリングのために全てのビットをゼロ にリセットすることができます。エラー状態が継続した場合、 次のサンプル・サイクルの終了時にエラー・フラグが 1 に戻り ます。

#### 表 43. DIAG\_STAT(ベース・アドレス = 0x02)、読出し専用

| Bits   | Description (Default = 0x0000)              |
|--------|---------------------------------------------|
| [15:8] | Not used, always zero                       |
| [9:8]  | Reserved, values can vary (not always zero) |
| 7      | Input clock out of sync                     |
|        | 1 = fail, 0 = pass                          |
| 6      | Flash memory test                           |
|        | 1 = fail, 0 = pass                          |
| 5      | Self test diagnostic error flag             |
|        | 1 = fail, 0 = pass                          |
| 4      | Sensor overrange                            |
|        | 1 = overrange, 0 = normal                   |
| 3      | SPI communication failure                   |
|        | 1 = fail, 0 = pass                          |
| 2      | Flash update failure                        |
|        | 1 = fail, 0 = pass                          |
| [1:0]  | Not used, always zero                       |

#### マニュアル・フラッシュ更新

GLOB\_CMD[3]= 1(DIN = 0xBE08、表 44 参照)に設定する と、マニュアル・フラッシュ更新(MFU)ルーチンがトリガさ れ、ユーザ・レジスタの設定値がマニュアル・フラッシュ・メ モリにコピーされます。これにより、不揮発性バックアップが 行われ、リセットまたはパワーオン・プロセス時にレジスタに ロードされます。このルーチンの完了後、DIAG\_STAT[2]に合 否の結果が入ります。このビットがエラー状態(1)に設定され ると、再度 MFU がトリガされ、MFU の完了後に DIAG\_STAT [2]が再度チェックされます。このフラグがゼロのままの場 合、最新の更新が完了していて、その後の処置が不要なことを 示します。このエラー・フラグが出続ける場合、フラッシュ・ メモリの不具合を示している可能性があります。

Rev. B - 17/26 -

{17}------------------------------------------------

#### **SPI** 通信エラー

フラグ(DIAG\_STAT[3])は、チップ・セレクト(CS)ライ ンがロー・レベルの間の SCLK パルスの総数が 16 の整数倍に等 しくなかったことを示します。このフラグは通信エラーを示し ている可能性があるので、前のコマンドを繰り返すプロセス、 またはデータの完全性の検証をトリガすることができます。

#### センサー・オーバーレンジ

このエラー・フラグ(DIAG\_STAT[4])は、慣性センサーの 1 つが測定範囲を超えた状態になったことを示します。

#### セルフ・テスト・エラー

DIAG\_STAT[5]ビットは、GLOB\_CMD[2](表 44 参照)に 関係する自動セルフ・テスト機能の結果を示します。このビッ トがエラー状態(1)に設定されると、再度自動セルフ・テスト (AST)がトリガされ、AST の完了後に DIAG\_STAT[5]が再

度チェックされます。このフラグがゼロのままの場合、最新の チェックが完了していて、その後の処置が不要なことを示しま す。このエラー・フラグが出続ける場合、1 個または複数の慣 性センサーの不具合を示している可能性があります。

#### フラッシュ・テスト・エラー

DIAG\_STAT[6](表 43 参照)には、GLOB\_CMD[4]= 1 (DIN = 0xBE10、表 44 参照)に設定した後に実行されるメモ リ・テストの結果が含まれています。

#### 入力クロック同期エラー

このエラー・フラグ(DIAG\_STAT[7]= 1)は、SYNC ピンの 信号の周波数に対して SYNC\_SCAL の値が適切でないことを示 します。

Rev. B - 18/26 -

{18}------------------------------------------------

## <span id="page-18-0"></span>システム機能

## <span id="page-18-1"></span>グローバル・コマンド

GLOB\_CMD レジスタは、複数のグローバル・コマンドに対し てトリガ・ビットを提供します。これらのルーチンを開始する には、対応するビットを 1 に設定し、実行時間(表 44 参照)が 経過してから SPI ポートでその後の通信を始めます。

表 44. GLOB\_CMD(ベース・アドレス = 0x3E)、書込み専用

| Bits   | Description                 | Execution Time (Max) |
|--------|-----------------------------|----------------------|
| [15:8] | Not used                    | Not applicable       |
| 7      | Software reset              | 222 ms               |
| [6:5]  | Not used                    | Not applicable       |
| 4      | Flash memory test           | 36                   |
| 3      | Manual flash update         | 70                   |
| 2      | Automated self test (AST)   | 7                    |
| 1      | Factory calibration restore | 75 ms                |
| 0      | Gyroscope bias correction   | 1 output data cycle1 |

<sup>1</sup> この時間は、DEC\_RATE(表 53 参照)と MSC\_CTRL[3:2](表 50 参 照)で設定されます。

#### <span id="page-18-2"></span>ソフトウェア・リセット

GLOB\_CMD レジスタを使い、GLOB\_CMD[7]= 1(DIN = 0xBE80)に設定することにより、プロセッサのリセットを開始 することができます。

#### <span id="page-18-3"></span>フラッシュ・メモリ・テスト

ADIS16460 の工場出荷時の設定では、プログラム・コードとキ ャリブレーションのメモリ・バンクに対して、IEEE-802.3 CRC32 イーサネット規格の方法を使った巡回冗長検査(CRC) が行われています。この処理により、これら 2 つのメモリ・バ ンクのシグネチャ値が生成され、これらが CODE\_SGNTR(表 45 参照)と CAL\_SGNTR(表 46 参照)のレジスタに設定され ます。

表 45. CODE\_SGNTR(ベース・アドレス = 0x64)、読出し専 用

| Bits   | Description                            |
|--------|----------------------------------------|
| [15:0] | Program code signature value, constant |

#### 表 46. CAL\_SNGTR(ベース・アドレス = 0x60)、読出し専用 Bits Description

[15:0] Calibration signature value, constant

GLOB\_CMD レジスタを使い、GLOB\_CMD[4]= 1(DIN = 0xBE10、表 44 参照)に設定することにより、どの時点でもフ ラッシュ・メモリ・テストを開始することができます。このテ ストでは、プログラム・コードとキャリブレーションのメモ リ・バンクに対して同じ CRC 処理を行い、その結果を CODE\_CRC(表 47 参照)と CAL\_CRC(表 48 参照)のレジス タに書き込みます。このテストが終了すると、合否の結果が

DIAG\_STAT[6](表 43 参照)にロードされます。合格結果 (DIAG\_STAT[6]= 0)になるには以下の条件が必要です。

- CODE\_CRC = CODE\_SNGTR
- CAL\_CRC = CAL\_SGNTR

表 47. CODE\_CRC(ベース・アドレス = 0x66)、読出し専用

| Bits   | Description                            |
|--------|----------------------------------------|
| [15:0] | Program code CRC, updates continuously |

表 48. CAL\_CRC(ベース・アドレス = 0x62)、読出し専用

| Bits   | Description                                 |
|--------|---------------------------------------------|
| [15:0] | Calibration CRC value, updates continuously |

#### <span id="page-18-4"></span>マニュアル・フラッシュ更新

GLOB\_CMD レジスタを使い、GLOB\_CMD[3]= 1(DIN = 0xBE08、図 24 も参照)に設定することにより、ユーザ設定値 を不揮発性フラッシュ・メモリに保存することができます。 FLASH\_CNT レジスタ(表 49 参照)によって、フラッシュ更新 の実行回数が提供され、定格に基づく書換え回数の管理が容易 になります(表 1 参照)。GLOB\_CMD[0]と GLOB\_CMD [1](表 44 参照)のコマンドを開始すると、フラッシュ・メ モリも更新されるので、FLASH\_CNT レジスタのカウントがイ ンクリメントされることに注意してください。

表 49. FLASH\_CNT(ベース・アドレス = 0x00)、読出し専用

| Bits   | Description    |  |
|--------|----------------|--|
| [15:0] | Binary counter |  |

#### <span id="page-18-5"></span>自動セルフ・テスト

ADIS16460 の各慣性センサーはセルフ・テスト機能を備えてお り、その物理的な構成素子に静電気力を加え、回転運動(ジャ イロ・センサー)と直線運動(加速度センサー)に対する応答 をシミュレーションするようにこれらを動かします。この動き によって各センサーの出力に予測可能で観測可能な応答が生 じ、これにより、各センサーとそれらに関連するシグナル・チ ェーンの基本機能を検証することができます。GLOB\_CMD レ ジスタにより、このセンサー・レベルの機能を使って各センサ ーが作動中であることを検証する自動処理を開始することがで きます。GLOB\_CMD[2]= 1(DIN = 0xBE04、表 44 参照)に 設定してこの AST 機能をトリガします。この機能は、通常のデ ータ生成を停止し、各センサーのセルフ・テスト機能を作動さ せ、それらの応答を通常応答の範囲と比較してから、通常のデ ータ・サンプリングを再開します。このルーチンの完了後、 DIAG\_STAT[5](表 43 参照)に合否の結果が入ります。

#### <span id="page-18-6"></span>入出力の設定

ADIS16460 には、サンプリングとデータ・アクイジションを管 理する SYNC と DR の 2 本のピンがあります(図 5 参照)。 MSC\_CTRL レジスタには、これらのピンを設定するためのいく つかのビットが備わっています(表 50 参照)。

#### <span id="page-18-7"></span>データ・レディ(**DR**)ピンの設定

DR ピンは、出力レジスタに新しいデータが用意されたことを 示すデータ・レディ信号を提供して、処理の遅延を最小限に抑 え、データの衝突を防止するのに役立ちます(図 5 参照)。こ のピンをシステム・プロセッサの割込み要求(IRQ)ピンに接 続する例を図 17 に示します。MSC\_CTRL[0](表 50 参照) を使って極性を設定し、システム・レベルの割込みサービス・ ルーチン(ISR)をこの信号の適切なエッジでトリガできるよう にします。例えば、MSC\_CTRL[0]= 1 の例を図 4 に示しま す。

Rev. B - 19/26 -

{19}------------------------------------------------

この場合、パルスの立上がりエッジでトリガする IRQ ピンに対して適正に機能します。信号の立下がりエッジでトリガする IRQ を DR で駆動する場合には、DIN = 0xB2C3(MSC\_CTRL [7:0] = 0xC3)に設定します。このコードは、線形 g 補償(MSC\_CTRL [7])と振動ポイント(MSC\_CTRL [6])の工場出荷時のデフォルト設定値も保持しています。このデバイスが GLOB\_CMD レジスタ(表 44 参照)に関係するグローバル・コマンドの実行中は、データ・レディ信号が停止することに注意してください。

#### <span id="page-19-0"></span>SYNC ピンの設定

MSC\_CTRL [3:2] (表 50 参照) により、SYNC ピン (図 5 参照) の機能がサポートする 4 つのモード (内部サンプル・クロック、外部同期 (直接サンプル制御)、データ・カウンタによる高精度入力同期、サンプル・タイム・インジケータ)の1つを選択するためのユーザ設定可能な制御を行うことができます。MSC\_CTRL [1] は、SYNC ピンのアクティブ状態の極性を(動作中のモードに関係なく)設定します。

表 50. MSC\_CTRL(ベース・アドレス = 0x32)、読出し/書 込み

| Description (Default = 0x00C1)                  |
|-------------------------------------------------|
| Not used                                        |
| Linear-g compensation control                   |
| 1 = enabled                                     |
| 0 = disabled (no linear- $g$ compensation)      |
| Point of percussion, see 図 32                   |
| 1 = enabled                                     |
| 0 = disabled (no point of percussion alignment) |
| Not used, always set to zero                    |
| SYNC function setting                           |
| 11 = sample time indicator (output)             |
| 10 = precision input sync with data counter     |
| 01 = direct sample control (input)              |
| 00 = disabled (internal sample clock)           |
| SYNC polarity (input or output)                 |
| 1 = rising edge triggers sampling               |
| 0 = falling edge triggers sampling              |
| DR polarity                                     |
| 1 = active high when data is valid              |
| 0 = active low when data is valid               |
|                                                 |

#### サンプル・タイム・インジケータ

MSC\_CTRL [3:2] = 11 (表 50 参照) の場合、ADIS16460 は内部サンプル・クロック(2048 SPS)を使ってデータのサンプリングと処理を行い、SYNC ピンはパルス信号を出力します。この信号の立上がりエッジが慣性センサーのサンプル・タイムを示します。ADIS16460 をこのモードに設定するには、DIN = 0xB2CD に設定しますが、MSC\_CTRL レジスタの他のデフォルト設定値は保持します。

#### データ・カウンタによる高精度入力同期

MSC\_CTRL [3:2] = 10 (表 50 参照) の場合、出力レジスタの 更新レートは入力クロック周波数 ( $f_{SYNC}$ ) と SYNC\_SCAL レジスタ (表 51 参照) のスケール・ファクタ ( $H_{SS}$ ) の積に等しく なります。このモードにより、GPS (全地球測位システム) の

PPS (パルス毎秒) 信号やビデオ同期信号など、低速のクロック入力リファレンスに対応することができます。ADIS16460をこのモードに設定するには DIN = 0xB2C9 に設定しますが、MSC\_CTRL レジスタの他のデフォルト設定値は保持します。このモードでは、次式を使ってスケール・ファクタ (HSS) の値を計算し、SYNC\_SCAL レジスタに書き込みます。

$$H_{SS} = \text{floor} \left( \frac{32,768}{f_{SYNC}} - 1 \right)$$

例えば、60 Hz のビデオ同期信号を使用する場合、DIN = 0 xB421 および DIN = 0 xB502 に設定することにより、 $\text{H}_{SS}$  を 545 に等しい値(SYNC SCAL = 0 x0221)に設定します。

$$H_{SS} = floor\left(\frac{32,768}{60} - 1\right) = floor(545.13333) = 545$$

1 Hz (PPS) の信号を使用する場合は、このレジスタのデフォルト値 (0x7FFF) がこのモードに対応します。SYNC\_SCAL がデフォルト値でない場合には、DIN = 0xB4FF および DIN = 0xB57F に設定することにより、SYNC\_SCAL = 0x7FFF に設定します。

$$H_{SS} = \text{floor}\left(\frac{32,768}{1} - 1\right) = \text{floor}(32,767) = 32,767$$

fsync を公称値に設定する場合、次の関係式が成り立つことを確認してください。

 $1945 \text{ Hz} \le H_{SS} \times f_{SYNC} \le 2048$ 

この条件の範囲外で動作させると、データ・サンプリングの入力制御ループが入力周波数にロックしない可能性があります。 DIAG\_STAT [7] = 1 (表 43 参照) がこの状態を示します。この場合、入力同期信号はサンプル・タイムに影響しなくなります。

表 51. SYNC\_SCAL(ベース・アドレス = 0x34)、読出し/書 込み

| <u>~ ·                                     </u> |                                                                                                              |
|-------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| Bits                                            | Description (Default = 0x7FFF)                                                                               |
| 15                                              | Not used                                                                                                     |
| [14:0]                                          | Input sync scale factor, H <sub>SS</sub> , when MSC_CTRL[3:2] = 10.<br>Binary format, range = 255 to 32,767. |

MSC\_CTRL [3:2] = 10 の場合、SMPL\_CNTR レジスタは、各入力クロック・パルスが 24576 Hz のレートで生成した全カウント数を提供します。SMPL\_CNTR レジスタは、各同期入力信号の立上がりエッジで 0x0000 にリセットされます。

表 52. SMPL\_CNTR(ベース・アドレス = 0x1C)、読出し/書 込み

| Bits   | Description                                                                                                                                                             |
|--------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [15:0] | Data counter for the number of samples since the last input clock pulse, binary format, 0x0000 = 0 µs, 40.69 µs/LSB, each input clock pulse resets this value to 0x0000 |

#### 直接サンプル制御

MSC\_CTRL [3:2] = 01 (表 50 参照) の場合、SYNC ピンのクロック信号によって出力レジスタの更新レートが制御されます。ADIS16460 をこのモードに設定するには、DIN = 0xB2C5 に設定しますが、MSC\_CTRL レジスタの他のデフォルト設定値は保持します。

Rev. B — 20/26 —

{20}------------------------------------------------

## <span id="page-20-0"></span>デジタル処理の設定

#### <span id="page-20-1"></span>ジャイロ・センサー/加速度センサー

ジャイロ・センサーと加速度センサーの信号処理全体を説明する図を図 30 に示します。内部サンプル・クロックを使用する場合(MSC\_CTRL [3:2] = 00、表 50 参照)、内部サンプリング・システムが 2048 SPS のレートで新しいデータを生成します。DEC\_RATE レジスタ(表 53 参照)はユーザ設定可能な入力を提供し、これにより、出力レジスタの更新レートに対するデシメーション・レートを制御します。例えば、DEC\_RATE = 0x0009 (DIN = 0xB609、次に DIN = 0xB700) に設定して、デシメーション係数を 10 に設定します。この設定により更新レートが 204.8 SPS に低減され、ジャイロ・センサー、加速度センサー、温度の出力レジスタに反映されます。

表 53. DEC\_RATE(ベース・アドレス = 0x36)、読出し/書込み

| Bits    | Description (Default = 0x0000)                    |
|---------|---------------------------------------------------|
| [15:11] | Not used, always zero                             |
| [10:0]  | D, decimation rate setting, linear, see Figure 30 |

#### デジタル・フィルタ処理

FLTR\_CTRL レジスタ (表 54 参照) により、デジタル・ローパス・フィルタを制御することができます。このフィルタは、バートレット・ウィンドウの FIR フィルタ応答を提供する 2 つのカスケード式平均化フィルタで構成されています (図 29 参照)。例えば、FLTR\_CTRL [2:0] = 100 (DIN = 0xB804) に設定し、各段を 16 タップに設定します。 2048 SPS のデフォルト・サンプル・レートとゼロ・デシメーション (DEC\_RATE = 0x00) で使用すると、この値によりセンサーの帯域幅は約 41 Hz に減少します。

![](_page_20_Figure_8.jpeg)

図 29. バートレット・ウィンドウの FIR フィルタの周波数応答 (位相遅延 = N サンプル)

表 54. FLTR\_CTRL(ベース・アドレス = 0x38)、読出し/書 込み

| Bits   | Description (Default = 0x0500)                             |
|--------|------------------------------------------------------------|
| [15:9] | Reserved                                                   |
| [10:8] | Sensor bias estimation time factor (NBE)                   |
|        | Setting range = 0 to 6                                     |
|        | Estimation time = $(1/2048) \times 2^{(NBE+11)}$ (seconds) |
| [7:3]  | Reserved                                                   |
| [2:0]  | Filter Size Variable B, setting range = 0 to 6             |
|        | Number of taps in each stage; $N_B = 2^B$                  |
|        | See Figure 29 for the filter response                      |

![](_page_20_Figure_12.jpeg)

図 30. センサーのサンプリングと周波数応答のブロック図

Rev. B — 21/26 —

{21}------------------------------------------------

## <span id="page-21-0"></span>キャリブレーション

ADIS16460 は、温度サイクル、衝撃、振動、その他の環境条件に曝された後でも、その機械的構造とアセンブリ工程により、各センサーの位置とアライメントは安定しています。工場出荷時のキャリブレーションには、各ジャイロ・センサーと加速度センサーの温度に対する動的特性評価が含まれており、センサー固有の補正式が生成されます。

#### <span id="page-21-1"></span>ジャイロ・センサー

 $X_GYRO_OFF$ (表 55 参照)、 $Y_GYRO_OFF$ (表 56 参照)、 $Z_GYRO_OFF$ (表 57 参照)の各レジスタは、ジャイロ・センサーのx 軸、y 軸、z 軸のユーザ設定可能なバイアス調整機能をそれぞれ提供します。図 31 は、これらのレジスタのそれぞれのバイアス補正係数が、各センサーの出力レジスタのデータに直接影響を与えることを示しています。

![](_page_21_Figure_5.jpeg)

図 31. ジャイロ・センサーと加速度センサーのキャリブレーション

表 55. X\_GYRO\_OFF(ベース・アドレス = 0x40)、読出し/ 書込み

| Bits   | Description (Default = 0x0000)                                                      |
|--------|-------------------------------------------------------------------------------------|
| [15:0] | X-axis, gyroscope offset correction factor, twos                                    |
|        | complement, 1 LSB = $0.000625^{\circ}/\text{sec}$ , $0^{\circ}/\text{sec} = 0x0000$ |

表 56. Y\_GYRO\_OFF(ベース・アドレス = 0x42)、読出し/ 書込み

| Bits   | Description (Default = 0x0000)                                                                      |
|--------|-----------------------------------------------------------------------------------------------------|
| [15:0] | Y-axis, gyroscope offset correction factor, twos complement, 1 LSB = 0.000625°/sec, 0°/sec = 0x0000 |

表 57. Z\_GYRO\_OFF(ベース・アドレス = 0x44)、読出し/ 書込み

| Bits   | Description (Default = 0x0000)                                                                      |
|--------|-----------------------------------------------------------------------------------------------------|
| [15:0] | Z-axis, gyroscope offset correction factor, twos complement, 1 LSB = 0.000625°/sec, 0°/sec = 0x0000 |

#### ジャイロ・センサーのバイアス誤差の計算

システム・レベルのキャリブレーションでは、バイアス誤差の計算から始める必要があります。バイアス誤差の計算では、通常、ADIS16460 が静的慣性状態で動作しているときのジャイロ・センサーのデータの時間記録の収集と平均化を行います。この計算に関係する時間記録の長さは、精度の目標値によって異なります。アラン分散の関係(図7参照)から、バイアス測定の平均化時間と期待精度の間のトレードオフの関係が与えられます。振動、温度勾配、電源の不安定性が、このプロセスの精度に影響を与える可能性があります。

#### ジャイロ・センサーのバイアス補正係数

バイアス計算が完了したら、計算値に -1 を掛けて極性を変え、オフセット補正レジスタ (表 55、表 56、表 57 を参照) に対応するデジタル・フォーマットに変換し、補正レジスタに補正係数を書き込みます。例えば、X\_GYRO\_OFF = 0xFFF6 (DIN = 0xC1FF、0xC0F6) に設定して、x 軸のバイアスを 10 LSB (0.00625°/sec) だけ下げます。

#### シングル・コマンドのバイアス補正

GLOB\_CMD [0] = 1 (DIN = 0xBE01、表 44 参照)に設定する と、ADIS16460 は X\_GYRO\_OFF、Y\_GRYO\_OFF、Z\_GYRO\_OFF の各レジスタに、バックワード・ルッキング連続 バイアス・エスティメータ (CBE) の値を自動的にロードしま す。CBE の記録長および記録時間は、FLTR\_CTRL [10:8] のビット(表 54 参照)に関係しています。この計算の精度は、FLTR\_CTRL [10:8] の計算時間中に回転運動が生じないことを前 提としています。

#### <span id="page-21-2"></span>加速度センサー

 $X\_ACCL\_OFF$  (表 58 参照)、 $Y\_ACCL\_OFF$  (表 59 参照)、 $Z\_ACCL\_OFF$  (表 60 参照) の各レジスタは、加速度センサーのx 軸、y 軸、z 軸のユーザ設定可能なバイアス調整機能をそれぞれ提供します。図 31 は、これらのレジスタのそれぞれのバイアス補正係数が、各センサーの出力レジスタのデータに直接影響を与えることを示しています。

表 58. X\_ACCL\_OFF(ベース・アドレス = 0x46)、読出し/ 書込み

| Bits   | Description (Default = 0x0000)                                              |  |
|--------|-----------------------------------------------------------------------------|--|
|        | 1 (,                                                                        |  |
| [15:0] | X-axis, accelerometer offset correction factor,                             |  |
|        | twos complement, $0.03125 \text{ mg/LSB}$ , $0 \text{ g} = 0 \text{x} 0000$ |  |

表 59. Y\_ACCL\_OFF(ベース・アドレス = 0x48)、読出し/ 書込み

| Bits    | Description (Default = 0x0000)                                                                |
|---------|-----------------------------------------------------------------------------------------------|
| [15:14] | Not used                                                                                      |
| [13:0]  | Y-axis, accelerometer offset correction factor, twos complement, 0.03125 mg/LSB, 0 g = 0x0000 |

表 60. Z\_ACCL\_OFF(ベース・アドレス = 0x4A)、読出し/書込み

| Bits Description (Default = 0x0000) |         | Description (Default = 0x0000)                                                                |
|-------------------------------------|---------|-----------------------------------------------------------------------------------------------|
|                                     | [15:14] | Not used                                                                                      |
|                                     | [13:0]  | Z-axis, accelerometer offset correction factor, twos complement, 0.03125 mg/LSB, 0 g = 0x0000 |

#### 加速度センサーのバイアス誤差の計算

静止状態で、各加速度センサーを重力に対する反応が予測可能な方向に設定します。一般的な方法では、各加速度センサーの応答がピークになる方向に置かれているときの応答を測定します。つまり、 $\pm 1\,g$  になるときが最適な測定位置になります。次に、 $\pm 1\,g$  と  $\pm 1\,g$  の加速度センサーの測定値を平均して残留バイアス誤差を計算します。回転のポイントを増やすことにより、応答の精度を向上させることができます。

#### 加速度センサーのバイアス補正係数

バイアス計算が完了したら、計算値に -1 を掛けて極性を変え、オフセット補正レジスタ (表 58、表 59、表 60 を参照) に対応するデジタル・フォーマットに変換し、補正レジスタに補正係数を書き込みます。

例えば、 $Y\_ACCL\_OFF = 0xFFF4$  (DIN = 0xC7FF、0xC6F4) に 設定して、y 軸のバイアスを 12 LSB (0.375 mg) だけ小さくします。

{22}------------------------------------------------

#### 振動ポイント・アライメント

MSC\_CTRL[6]= 1(DIN = 0xB2C1、表 50 参照)に設定し て、この機能をイネーブルし、DR ピンと SYNC ピンの工場出 荷時のデフォルト設定値を維持します。この機能により、振動 ポイントは図 32 に示すポイントに移動されます。MSC\_CTRL の詳細については表 50 を参照してください。

<span id="page-22-1"></span>![](_page_22_Picture_3.jpeg)

図 32. 振動ポイントの物理的な基準

#### <span id="page-22-0"></span>工場出荷時キャリブレーション値の復元

GLOB\_CMD[1]= 1(DIN = 0xBE02、表 44 参照)に設定し て、工場出荷時キャリブレーション値の復元機能を実行しま す。これにより、ジャイロ・センサーと加速度センサーのオフ セット・レジスタが 0x0000 に、全てのセンサー・データが 0 に リセットされます。この処理はフラッシュ・メモリを自動更新 することにより完了し、通常のデータ・サンプリングとデータ 処理に戻ります。

Rev. B - 23/26 -

{23}------------------------------------------------

## <span id="page-23-0"></span>アプリケーション情報実装上のポイント

<span id="page-23-1"></span>ADIS16460 のパッケージは、3 本の M2 (2-56) マシン・ネジを使用して、20 インチ・オンス~40 インチ・オンスのトルクで、プリント回路ボード (PCB) や固定筐体に実装することができます。ADIS16460 の機械的インターフェースを設計する際には、電気的コネクタに不要な並進応力がかからないようにします。この応力がかかると、慣性センサーのバイアス再現性に影響を与える可能性があります。同じ PCB に接続用コネクタがある場合、実装ネジ用の貫通穴が必要になる可能性があります。CLM-107-02 ファミリーのコネクタ・タイプの1つを使ったPCB パッド設計の詳細図を図 33 に示します。

![](_page_23_Picture_3.jpeg)

図 33. 接続用コネクタの設計詳細

#### <span id="page-23-2"></span>電源に関する考慮事項

起動時、VDD が 1.6 V に達すると、内部電力変換システムが電流を流し始めます。VDD が 2.35 V に等しくなると、内部プロセッサが初期化を開始します。プロセッサの起動後、VDD は 128 ms 以内に 2.7 V に達する必要があります。また、内部プロセッサを確実にシャットダウンさせるには、電源が 1.6 V を下回るようにする必要があります。VDD と GND の間に 10  $\mu$ F 以上の容量を配置します。ADIS16460 のコネクタのできるだけ近くに高品質の積層セラミック・コンデンサを配置すると、最良の結果が得られます。このコンデンサを使用すると、センサーに最適なノイズ性能が得られます。

#### <span id="page-23-3"></span>ブレークアウト・ボード

ADIS16IMU4/PCBZ ブレークアウト・ボードは、組み込みプロセッサ開発システムへの接続をシンプルにするためのリボン・ケーブル・インターフェースを備えています。このブレークアウト・ボードの回路図を図 34 に、上面図を図 35 に示します。 J2 は ADIS16460 のコネクタに直接接続でき、J1 は 1 mm のリボン・ケーブル・システムに容易に接続できます。

![](_page_23_Picture_9.jpeg)

図 34. ADIS16IMU4/PCBZ の回路図

![](_page_23_Picture_11.jpeg)

図 35. ADIS16IMU4/PCBZ の上面図

|     | J <sup>,</sup> | 1  |      |          |
|-----|----------------|----|------|----------|
| RST | 1              | 2  | SCLK |          |
| cs  | 3              | 4  | DOUT |          |
| DNC | 5              | 6  | DIN  |          |
| GND | 7              | 8  | GND  |          |
| GND | 9              | 10 | VDD  |          |
| VDD | 11             | 12 | VDD  |          |
| DR  | 13             | 14 | SYNC | 3390-029 |
| NC  | 15             | 16 | NC   | 13390    |

図 36. ADIS16IMU4/PCBZ の J1 のピン配置

Rev. B — 24/26 —

{24}------------------------------------------------

### <span id="page-24-0"></span>**PC** ベースの評価ツール

ADIS16IMU4/PCBZ は、ADIS16460 を EVAL-ADIS 評価システ ムに接続するためのシンプルな方法を提供します。これによ り、基本的な機能と性能を PC ベースで評価することができま す。詳細については、ウィキ・ガイド ADIS1646X/AD24000 Evaluation on a PC を参照してください。

#### 関連ビット数の計算

プライマリ出力データ・レジスタは、各慣性センサーに対して 16 ビットの分解能を備えています。この分解能は、内部フィル タを使用しない場合や、ADIS16460 が出力レジスタにロードす る全てのサンプルを収集する場合に、主要なセンサー動作を維 持するのに十分な値です。内部フィルタを使用するシステムで は、これらのフィルタの累積機能によって生じるビットの増加 分がセカンダリ出力データ・レジスタに取り込まれます。この ビットの増加分の大きさは、これら両方のレジスタの設定値に よって決まります。可変設定値(表 53 の D、表 54 の B)と以 下の式を使って、加算関数の総数(NS)とともに、データ・パ スの関連ビットの増加分(NBG)を計算します。

*NS* = *D* + *2 B NBG* = *NS*

例えば、B = 5、D = 4 の場合、内部データ・パスのビットの増 加分は 6 ビットになります。すなわち、各セカンダリ・レジス タの上位 6 ビット(X\_GYRO\_LOW[15:10]など)のみが適用 されます。

*NS* = *D* + *2 <sup>B</sup>* = 4 + 2<sup>5</sup> = 36 サンプル

*NBG* = *NS* = 36 = 6 ビット

システム・プロセッサのデータ・パスに繰り上げるビット数を 決める場合、各センサーの安定性能も考慮するべきです。例え ば、ジャイロ・センサーのセカンダリ・レジスタを上位 6 ビッ トに維持すると、0.000078125°/sec(0.28°/hour)のデジタル分解 能が得られます。これは、ADIS16460 ジャイロ・センサーの動 作中のバイアス安定度よりも大幅に小さい値です。

Rev. B - 25/26 -

{25}------------------------------------------------

## <span id="page-25-0"></span>外形寸法

![](_page_25_Figure_2.jpeg)

![](_page_25_Figure_3.jpeg)

図 37. コネクタ・インターフェース付き 14 ピン・モジュール [MODULE] (ML-14-6) 寸法: mm

## <span id="page-25-1"></span>オーダー・ガイド

| Model <sup>1</sup> | Temperature Range | Package Description                              | Package Option |
|--------------------|-------------------|--------------------------------------------------|----------------|
| ADIS16460AMLZ      | −25°C to +85°C    | 14-Lead Module with Connector Interface [MODULE] | ML-14-6        |

<sup>1</sup> Z = RoHS 準拠製品

Rev. B — 26/26 —