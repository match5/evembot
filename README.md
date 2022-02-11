# evembot

EVE手游脚本（仅用于学习交流）

- 安装步骤

1. 安装 python3.7 (勾选安装pip 和 添加环境变量)
2. 安装 tesseract-ocr(勾选中文数据包)
3. 运行 setup.bat

- 使用方法

1. 在模拟器中运行游游戏
2. 修改配置文件
3. 模拟器分辨率设置为 1280x720
4. 游戏设置 打开 自动攻击 自动环绕
4. 设置总览 显示 怪 异常 空间站 军堡 星门
5. 点开本地
3. 运行 run.bat

- 配置说明

 ```json
 {
    "window_title": "雷电模拟器",           // 模拟器窗口名
    "tesseract_path": "C:/Program Files/Tesseract-OCR/tesseract.exe",   // Tesseract 安装路径
    /*
        省略...
    */
    "spot_filter": ["小", "中"],            // 异常名称过滤
    "equipments": {
        "rect": [785, 570, 1270, 735],
        "buttons": [
            {                               // 战斗装备 比如 武提 网子 吸电
                "idx": 0,                   // 装备按钮位置编号:
                                            //  0  1  2  3  4  5
                                            //  6  7  8  9  10 11
                "available_states": {
                    "Fight": true           // 启动状态(战斗)
                }
            },
            {                               // 回复装备
                "idx": 1,                   
                "condition": "shield<85"    // 启动条件(盾小于85%)
                                            // 可用于判断的属性: shield:盾 armour:甲 structure:结构 energy:电
            },
            {                               // 逃跑装备 比如 圣光
                "idx": 2,
                "available_states": {
                    "Escape": true          // 启动状态(逃跑)
                }                     
            },
        ]
    },
    "avoid_players": {                      // 规避本地玩家
        "red": true,                        // 红名
        "criminal": true,                   // 罪犯
        "white": true                       // 白名
    },
    "escape_condition": "shield<30"         // 逃跑条件
 }
 ```