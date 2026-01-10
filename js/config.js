// Fallback list of files (used if auto-discovery fails)
// GitHub Pages 不支持目录浏览，必须显式列出所有数据文件
export const DATA_FILES = [
    '8756.json',
    '8758.json',
    '8765.json',
    '8767.json',
    '8770.json',
    '8774.json',
    '8777.json',
    '8781.json',
    '8785.json',
    '8789.json',
    '8793.json',
    '8795.json',
    '8799.json',
    '8805.json',
    '8807.json',
    '8810.json',
    '8812.json',
    '8815.json',
    '8817.json',
    '8819.json',
    '8825.json',
    '8828.json'
];

export const AUTH_KEY = 'vps2026';

export const COUNTRY_DICT = {
    // -------------------- 北美洲 --------------------
    'United States': [
        'US', 'USA', 'America', 'United States', '美国',
        'Los Angeles', '洛杉矶', 'New York', '纽约',
        'Chicago', '芝加哥', 'Houston', '休斯顿',
        'Phoenix', '菲尼克斯', 'Philadelphia', '费城',
        'San Antonio', '圣安东尼奥', 'San Diego', '圣迭戈',
        'Dallas', '达拉斯', 'San Jose', '圣荷西',
        'Austin', '奥斯汀', 'Seattle', '西雅图',
        'Denver', '丹佛', 'Washington', '华盛顿',
        'Boston', '波士顿', 'Miami', '迈阿密',
        'Atlanta', '亚特兰大', 'Portland', '波特兰',
        'Las Vegas', '拉斯维加斯'
    ],
    'Canada': [
        'CA', 'Canada', '加拿大',
        'Toronto', '多伦多', 'Vancouver', '温哥华',
        'Montreal', '蒙特利尔', 'Calgary', '卡尔加里',
        'Ottawa', '渥太华', 'Edmonton', '埃德蒙顿',
        'Winnipeg', '温尼伯', 'Quebec City', '魁北克城',
        'Hamilton', '汉密尔顿'
    ],
    // -------------------- 中美洲、加勒比 --------------------
    'Mexico': [
        'MX', 'Mexico', '墨西哥',
        'Mexico City', '墨西哥城', 'Guadalajara', '瓜达拉哈拉',
        'Monterrey', '蒙特雷', 'Puebla', '普埃布拉',
        'Tijuana', '蒂华纳', 'Cancún', '坎昆'
    ],

    // -------------------- 南美洲 --------------------
    'Brazil': [
        'BR', 'Brazil', 'Brasil', '巴西',
        'São Paulo', '圣保罗', 'Rio de Janeiro', '里约热内卢',
        'Brasília', '巴西利亚', 'Salvador', '萨尔瓦多',
        'Fortaleza', '福塔雷萨', 'Belo Horizonte', '贝洛奥里藏特'
    ],
    'Argentina': [
        'AR', 'Argentina', '阿根廷',
        'Buenos Aires', '布宜诺斯艾利斯', 'Córdoba', '科尔多瓦',
        'Rosario', '罗萨里奥', 'Mendoza', '门多萨'
    ],

    // -------------------- 欧洲 --------------------
    'United Kingdom': [
        'GB', 'UK', 'United Kingdom', 'Great Britain', 'England', '英国',
        'London', '伦敦', 'Manchester', '曼彻斯特',
        'Birmingham', '伯明翰', 'Glasgow', '格拉斯哥',
        'Leeds', '利兹', 'Liverpool', '利物浦',
        'Edinburgh', '爱丁堡'
    ],
    'Germany': [
        'DE', 'Germany', 'Deutschland', '德国',
        'Berlin', '柏林', 'Munich', '慕尼黑',
        'Frankfurt', '法兰克福', 'Hamburg', '汉堡',
        'Cologne', '科隆', 'Stuttgart', '斯图加特',
        'Düsseldorf', '杜塞尔多夫'
    ],
    'France': [
        'FR', 'France', '法国',
        'Paris', '巴黎', 'Marseille', '马赛',
        'Lyon', '里昂', 'Toulouse', '图卢兹',
        'Nice', '尼斯', 'Bordeaux', '波尔多',
        'Lille', '里尔'
    ],
    'Netherlands': [
        'NL', 'Netherlands', 'Holland', '荷兰',
        'Amsterdam', '阿姆斯特丹', 'Rotterdam', '鹿特丹',
        'The Hague', '海牙', 'Utrecht', '乌得勒支',
        'Eindhoven', '埃因霍温'
    ],
    'Russia': [
        'RU', 'Russia', 'Russian Federation', '俄罗斯',
        'Moscow', '莫斯科', 'Saint Petersburg', '圣彼得堡',
        'Novosibirsk', '新西伯利亚', 'Yekaterinburg', '叶卡捷琳堡'
    ],
    // -------------------- 亚洲 --------------------
    'China': [
        // 基础代号/别名
        'CN', 'China', 'PRC', '中华人民共和国', '中国',

        // ----- 直辖市 -----
        'Beijing', '北京', 'Shanghai', '上海',
        'Tianjin', '天津', 'Chongqing', '重庆',
        'Beijing Municipality', '京津冀地区', // 兼容常见写法

        // ----- 省份（含省会） -----
        // 北京、天津、上海、重庆 已在直辖市列出，这里列出其余省份及省会
        'Hebei', '河北', 'Shijiazhuang', '石家庄',
        'Shanxi', '山西', 'Taiyuan', '太原',
        'Liaoning', '辽宁', 'Shenyang', '沈阳',
        'Jilin', '吉林', 'Changchun', '长春',
        'Heilongjiang', '黑龙江', 'Harbin', '哈尔滨',
        'Jiangsu', '江苏', 'Nanjing', '南京',
        'Zhejiang', '浙江', 'Hangzhou', '杭州',
        'Anhui', '安徽', 'Hefei', '合肥',
        'Fujian', '福建', 'Fuzhou', '福州',
        'Jiangxi', '江西', 'Nanchang', '南昌',
        'Shandong', '山东', 'Jinan', '济南',
        'Henan', '河南', 'Zhengzhou', '郑州',
        'Hubei', '湖北', 'Wuhan', '武汉',
        'Hunan', '湖南', 'Changsha', '长沙',
        'Guangdong', '广东', 'Guangzhou', '广州',
        'Guangxi', '广西', 'Nanning', '南宁',
        'Hainan', '海南', 'Haikou', '海口',
        'Sichuan', '四川', 'Chengdu', '成都',
        'Guizhou', '贵州', 'Guiyang', '贵阳',
        'Yunnan', '云南', 'Kunming', '昆明',
        'Tibet', '西藏', 'Lhasa', '拉萨',
        'Shaanxi', '陕西', 'Xi\'an', '西安',
        'Gansu', '甘肃', 'Lanzhou', '兰州',
        'Qinghai', '青海', 'Xining', '西宁',
        'Ningxia', '宁夏', 'Yinchuan', '银川',
        'Xinjiang', '新疆', 'Urumqi', '乌鲁木齐',
        'Inner Mongolia', '内蒙古', 'Hohhot', '呼和浩特',

        // ----- 经济特区 & 开发区 -----
        'Shenzhen', '深圳', 'Zhuhai', '珠海',
        'Xiamen', '厦门', 'Fujian', '福州',

        // ----- 主要城市（除省会外） -----
        'Suzhou', '苏州', 'Wuxi', '无锡', 'Ningbo', '宁波',
        'Dalian', '大连', 'Qingdao', '青岛', 'Xian', '西安',
        'Changchun', '长春', 'Harbin', '哈尔滨',
        'Zhangjiakou', '张家口', 'Yantai', '烟台',
        'Sanya', '三亚', 'Kunshan', '昆山',
        'Foshan', '佛山', 'Dongguan', '东莞',
        'Zhengzhou', '郑州', 'Changsha', '长沙',
        'Wenzhou', '温州', 'Zibo', '淄博',
        'Lanzhou', '兰州', 'Urumqi', '乌鲁木齐',

        // ----- 两个特别行政区 -----
        // 香港
        'Hong Kong', 'HongKong', '香港', 'HK', 'Hong Kong Island', '香港岛',
        'Kowloon', '九龙', 'New Territories', '新界',
        // 澳门
        'Macau', 'Macau', '澳门', 'MO', 'Macao', 'Macao SAR',
        'Peninsula', '澳门半岛', 'Taipa', '氹仔', 'Cotai', '路氹城'
    ],

    // 仍保留独立条目，若不需要可自行删除
    'Hong Kong': [
        'HK', 'Hong Kong', 'HongKong', '香港',
        'Hong Kong Island', '香港岛', 'Kowloon', '九龙', 'New Territories', '新界'
    ],
    'Macau': [
        'MO', 'Macau', 'Macao', '澳门',
        'Macau Peninsula', '澳门半岛', 'Taipa', '氹仔', 'Cotai', '路氹城'
    ],

    'Japan': [
        'JP', 'Japan', 'Nippon', '日本',
        'Tokyo', '东京', 'Osaka', '大阪',
        'Kyoto', '京都', 'Nagoya', '名古屋',
        'Sapporo', '札幌', 'Fukuoka', '福冈',
        'Kobe', '神户', 'Hiroshima', '广岛'
    ],
    'South Korea': [
        'KR', 'Korea', 'South Korea', 'Republic of Korea', '韩国',
        'Seoul', '首尔', 'Busan', '釜山',
        'Incheon', '仁川', 'Daegu', '大邱',
        'Daejeon', '大田', 'Gwangju', '光州'
    ],
    'Taiwan': [
        'TW', 'Taiwan', 'Republic of China', '台湾',
        'Taipei', '台北', 'Kaohsiung', '高雄',
        'Taichung', '台中', 'Tainan', '台南',
        'Taoyuan', '桃园'
    ],

    // -------------------- 大洋洲 --------------------
    'Australia': [
        'AU', 'Australia', '澳大利亚', '澳洲',
        'Sydney', '悉尼', 'Melbourne', '墨尔本',
        'Brisbane', '布里斯班', 'Perth', '珀斯',
        'Adelaide', '阿德莱德', 'Canberra', '堪培拉',
        'Gold Coast', '黄金海岸'
    ],
    'New Zealand': [
        'NZ', 'New Zealand', '新西兰',
        'Auckland', '奥克兰', 'Wellington', '惠灵顿',
        'Christchurch', '基督城', 'Hamilton', '汉密尔顿'
    ],

    // -------------------- 非洲 --------------------
    'South Africa': [
        'ZA', 'South Africa', 'RSA', '南非',
        'Johannesburg', '约翰内斯堡', 'Cape Town', '开普敦',
        'Durban', '德班', 'Pretoria', '比勒陀利亚'
    ],
    'Nigeria': [
        'NG', 'Nigeria', '尼日利亚',
        'Lagos', '拉各斯', 'Abuja', '阿布贾',
        'Kano', '卡诺', 'Ibadan', '伊巴丹'
    ],

    // -------------------- 其他地区（示例） --------------------
    'Singapore': [
        'SG', 'Singapore', '新加坡', '狮城'
    ],
    'Malaysia': [
        'MY', 'Malaysia', '马来西亚',
        'Kuala Lumpur', '吉隆坡', 'George Town', '乔治市',
        'Johor Bahru', '新山', 'Ipoh', '怡保',
        'Kota Kinabalu', '亚庇'
    ]
};