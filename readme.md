# Overview
This project implements an LSTM Model to predict BTC prices in the future. The default number of hours is hardcoded to 4 for now but the project and the model can be tweaked to improve it further and make it configurable.

Each individual value is considered to be within the past ***n*** hours where ***n*** is the size of each list. The lists should all be of equal size. 

# API
**Endpoint**
*http://{{BASE_URL}}/api*

**Sample Request Data**
All arguments here are required.
```json
{
    "close_price": [
        6350.0,
        6356.48,
        6361.93,
        6368.78,
        6456.0,
        6365.43,
        6327.94,
        6326.98,
        6339.5,
        6333.05
    ],
    "polarity": [
        0.10265670748614598,
        0.09800395297609978,
        0.0966881579841847,
        0.10399680386738332,
        0.09438312650721571,
        0.10083589375817453,
        0.1119643429977597,
        0.1058881862567765,
        0.10811700734669419,
        0.10666706633974722
    ],
    "sensitivity": [
        0.21614845947129513,
        0.21861239516350178,
        0.23134226427071872,
        0.21773906718462835,
        0.19525553005949395,
        0.22307632548845868,
        0.19504306787217293,
        0.20993930342403333,
        0.20800324193424663,
        0.21723050559221563
    ],
    "tweet_vol": [
        4354.0,
        4432.0,
        3980.0,
        3830.0,
        3998.0,
        12435.0,
        3843.0,
        3831.0,
        3743.0,
        3480.0
    ],
    "volume_btc": [
        986.73,
        126.46,
        259.1,
        81.54,
        124.55,
        141.5,
        141.3,
        162.37,
        58.62,
        74.75
    ]
}
```