# refer: https://blog.csdn.net/weixin_42763614/article/details/103051262

import math, ephem

yuefen = ["正月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
nlrq = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十", "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八",
        "十九", "二十", "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十"]
tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
gz = [''] * 60  # 六十甲子表
for i in range(60):
    gz[i] = tiangan[i % 10] + dizhi[i % 12]


def EquinoxSolsticeJD(year, angle):
    if 0 <= angle < 90:
        date = ephem.next_vernal_equinox(year)
    elif 90 <= angle < 180:
        date = ephem.next_summer_solstice(year)
    elif 180 <= angle < 270:
        date = ephem.next_autumn_equinox(year)
    else:
        date = ephem.next_winter_solstice(year)
    JD = ephem.julian_date(date)
    return JD


# 计算二十四节气
def SolarLongitube(JD):
    date = ephem.Date(JD - 2415020)
    s = ephem.Sun(date)  # date应为UT时间
    sa = ephem.Equatorial(s.ra, s.dec, epoch=date)
    se = ephem.Ecliptic(sa)
    L = se.lon / ephem.degree / 180 * math.pi
    return L


def SolarTerms(year, angle):
    if angle > 270: year -= 1  # 岁首冬至
    if year == 0: year -= 1  # 公元0改为公元前1
    JD = EquinoxSolsticeJD(str(year), angle)  # 初值
    if angle >= 270:
        JD0 = EquinoxSolsticeJD(str(year), (angle - 90) % 360)
        if JD < JD0:  # 非年末冬至
            JD = EquinoxSolsticeJD(str(year + 1), angle)  # 转入次年
    JD1 = JD
    while True:
        JD2 = JD1
        L = SolarLongitube(JD2)
        JD1 += math.sin(angle * math.pi / 180 - L) / math.pi * 180
        if abs(JD1 - JD2) < 0.00001:
            break  # 精度小于1 second
    return JD1  # UT


def EvenTerms(year, angle):  # 十二节
    if 225 <= angle <= 270: year -= 1  # 岁首冬至改为立冬
    JD = SolarTerms(year, angle)
    return JD


def DateCompare(JD1, JD2):  # 输入ut，返回ut+8的比较结果
    JD1 += 0.5 + 8 / 24
    JD2 += 0.5 + 8 / 24
    if math.floor(JD1) >= math.floor(JD2):
        return True
    else:
        return False


def dzs_search(year):  # 寻找年前冬至月朔日
    if year == 1: year -= 1  # 公元0改为公元前1
    dz = ephem.next_solstice((year - 1, 12))  # 年前冬至
    jd = ephem.julian_date(dz)
    # 可能的三种朔日
    date1 = ephem.next_new_moon(ephem.Date(jd - 2415020 - 0))
    jd1 = ephem.julian_date(date1)
    date2 = ephem.next_new_moon(ephem.Date(jd - 2415020 - 29))
    jd2 = ephem.julian_date(date2)
    date3 = ephem.next_new_moon(ephem.Date(jd - 2415020 - 31))
    jd3 = ephem.julian_date(date3)
    if DateCompare(jd, jd1):  # 冬至合朔在同一日或下月
        return date1
    elif DateCompare(jd, jd2) and (not DateCompare(jd, jd1)):
        return date2
    elif DateCompare(jd, jd3):  # 冬至在上月
        return date3


def Solar2LunarCalendar(date):  # 默认输入ut+8时间
    JD = ephem.julian_date(date) - 8 / 24  # ut
    year = ephem.Date(JD + 8 / 24 - 2415020).triple()[0]
    shuo = []  # 存储date
    shuoJD = []  # 存储JD
    # 判断所在年
    shuo.append(dzs_search(year))  # 本年冬至朔
    next_dzs = dzs_search(year + 1)  # 次年冬至朔
    this_dzsJD = ephem.julian_date(shuo[0])
    next_dzsJD = ephem.julian_date(next_dzs)
    nian = year  # 农历年
    if DateCompare(JD, next_dzsJD):  # 该日在次年
        shuo[0] = next_dzs  # 次年冬至朔变为本年
        next_dzs = dzs_search(year + 2)
        nian += 1
    if not DateCompare(JD, this_dzsJD):  # 该日在上年
        next_dzs = shuo[0]  # 本年冬至朔变为次年
        shuo[0] = dzs_search(year - 1)
        nian -= 1
    next_dzsJD = ephem.julian_date(next_dzs)
    shuoJD.append(ephem.julian_date(shuo[0]))  # 找到的年前冬至朔
    # 查找所在月及判断置闰
    szy = 0
    i = -1  # 中气序
    j = -1  # 计算连续两个冬至月中的合朔次数
    zry = 99  # 无效值
    flag = False
    while not DateCompare(shuoJD[j], next_dzsJD):  # 从冬至月起查找，截止到次年冬至朔
        i += 1
        j += 1
        # 查找所在月，起冬至朔
        if DateCompare(JD, shuoJD[j]):
            szy += 1  # date所在月
            newmoon = shuoJD[j]
        shuo.append(ephem.next_new_moon(shuo[j]))  # 次月朔
        shuoJD.append(ephem.julian_date(shuo[j + 1]))
        # 查找本月中气，若无则置闰
        if j == 0: continue  # 冬至月一定含中气，从次月开始查找
        angle = (-90 + 30 * i) % 360  # 本月应含中气，起冬至
        qJD = SolarTerms(nian, angle)
        # 不判断气在上月而后气在后月的情况，该月起的合朔次数不超过气数，可省去
        if DateCompare(qJD, shuoJD[j + 1]) and flag == False:  # 中气在次月，则本月无中气
            zry = j + 1  # 置闰月
            i -= 1
            flag = True  # 仅第一个无中气月置闰
    # 判断置闰
    if j == 12 and zry != 99:  # 有无中气月但合朔仅12次
        zry = 99
    if szy >= zry % 12 and zry != 99:
        szy -= 1  # 置闰后的月序名
    # 以正月开始的年干支
    if szy < 3: nian -= 1  # 正月前属上年
    if nian < 0: nian += 1
    rq = math.floor(JD + 8 / 24 + 0.5) - math.floor(newmoon + 8 / 24 + 0.5)  # 日干支
    # return date + ' 为农历：' + yuefen[(szy - 3) % 12] + nlrq[rq] + '\n'
    return "%02d-%02d" % ((szy - 3) % 12 + 1, rq + 1), str(yuefen[(szy - 3) % 12] + nlrq[rq])


# date = "2020-06-28"  # "1993-06-27"
# print(Solar2LunarCalendar(date))

