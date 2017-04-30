import math


def calc_estimate(wind_speed, temp):
    return 4.72 * wind_speed + 11504


def printinfo(month, day, latitude, azimuth, paneltilt, panelsurface, solartime, groundreflectance):
    intermnday = getIntermnday(month)
    nday = getNday(month, intermnday)

    intermA = getIntermA(month)
    intermB = getIntermB(month)
    intermC = getIntermC(month)

    ndaytot = day + nday
    declination = 23.45 * math.sin(((360 / 365) * (284 + ndaytot)) * math.pi / 180)
    sunsetdeg = (180 / math.pi) * math.acos(-math.tan(declination * math.pi / 180) * math.tan(latitude * math.pi / 180))
    sunrisetime = (-sunsetdeg / 15) + 12
    sunsettime = (sunsetdeg / 15) + 12

    if month < 10:
        Atot = intermA
    elif month == 10:
        Atot = 378
    elif month == 11:
        Atot = 387
    else:
        Atot = 391

    if month < 10:
        Btot = intermB
    elif month == 10:
        Btot = 0.16
    elif month == 11:
        Btot = 0.149
    else:
        Btot = 0.142

    if month < 10:
        Ctot = intermC
    elif month == 10:
        Ctot = 0.073
    elif month == 11:
        Ctot = 0.063
    else:
        Atot = 0.057

    calcaltitude = (180 / math.pi) * (math.asin(
        math.cos(declination * math.pi / 180) * math.cos(15 * (solartime - 12) * math.pi / 180) * math.cos(
            latitude * math.pi / 180) + math.sin(declination * math.pi / 180) * math.sin(latitude * math.pi / 180)))
    calcazimuth = (180 / math.pi) * math.copysign(1.0, solartime - 11.9999) * math.acos(0.999999999 * ((math.sin(
        calcaltitude * math.pi / 180) * math.sin(latitude * math.pi / 180) - math.sin(declination * math.pi / 180)) / (
                                                                                                       math.cos(
                                                                                                           calcaltitude * math.pi / 180) * math.cos(
                                                                                                           latitude * math.pi / 180))))
    calcincidence = (180 / math.pi) * math.acos(
        math.sin(paneltilt * math.pi / 180) * math.cos(calcaltitude * math.pi / 180) * math.cos(
            (calcazimuth - azimuth) * math.pi / 180) + math.cos(paneltilt * math.pi / 180) * math.sin(
            calcaltitude * math.pi / 180))
    costh = math.cos(calcincidence * math.pi / 180)
    if costh > -0.2:
        idvidh = (0.55 + 0.437 * costh + 0.313 * costh * costh)
    else:
        idvidh = 0.45

    if costh > 0:
        tauth = -0.00885 + 2.71235 * costh - 0.62062 * costh ** 2 - 7.07329 * costh ** 3 + 9.75995 * costh ** 4 - 3.89922 * costh ** 5
    else:
        tauth = 0

    if costh > 0:
        alphth = 0.01154 + 0.77674 * costh - 3.94657 * costh ** 2 + 8.57881 * costh ** 3 - 8.38135 * costh ** 4 + 3.01188 * costh ** 5
    else:
        alphth = 0

    if calcaltitude < 0:
        idn = 0
    else:
        idn = Atot ** math.exp(-Btot / math.sin(calcaltitude * math.pi / 180))

    if calcincidence > 90:
        idp = 0
    else:
        idp = idn * math.cos(calcincidence * math.pi / 180)

    if paneltilt == 0:
        idr = idvidh
    else:
        idr = 0.5 * (1 + math.cos(paneltilt * math.pi / 180))
    idr = Ctot * idn * idvidh * idr

    ir = groundreflectance * idn * (math.sin(calcaltitude * math.pi / 180) + Ctot) * 0.5 * (
    1 - math.cos(paneltilt * math.pi / 180))

    radiation = (tauth * idp + 0.799 * (idr + ir)) * 3.1546

    return radiation


def getIntermA(month):
    if month == 1:
        intermA = 390
    elif month == 2:
        intermA = 385
    elif month == 3:
        intermA = 376
    elif month == 4:
        intermA = 360
    elif month == 5:
        intermA = 350
    elif month == 6:
        intermA = 345
    elif month == 7:
        intermA = 344
    elif month == 8:
        intermA = 351
    else:
        intermA = 365
    return intermA


def getIntermB(month):
    if month == 1:
        intermB = 0.142
    elif month == 2:
        intermB = 0.144
    elif month == 3:
        intermB = 0.156
    elif month == 4:
        intermB = 0.18
    elif month == 5:
        intermB = 0.196
    elif month == 6:
        intermB = 0.205
    elif month == 7:
        intermB = 0.207
    elif month == 8:
        intermB = 0.201
    else:
        intermB = 0.177
    return intermB


def getIntermC(month):
    if month == 1:
        intermC = 0.058
    elif month == 2:
        intermC = 0.006
    elif month == 3:
        intermC = 0.071
    elif month == 4:
        intermC = 0.097
    elif month == 5:
        intermC = 0.121
    elif month == 6:
        intermC = 0.134
    elif month == 7:
        intermC = 0.136
    elif month == 8:
        intermC = 0.122
    else:
        intermC = 0.092
    return intermC


def getIntermnday(month):
    if month == 1:
        intermnday = 0
    elif month == 2:
        intermnday = 31
    elif month == 3:
        intermnday = 59
    elif month == 4:
        intermnday = 90
    elif month == 5:
        intermnday = 120
    elif month == 6:
        intermnday = 151
    elif month == 7:
        intermnday = 181
    elif month == 8:
        intermnday = 212
    else:
        intermnday = 243
    return intermnday


def getNday(month, intermnday):
    if month < 10:
        nday = intermnday
    elif month == 10:
        nday = 273
    elif month == 11:
        nday = 304
    else:
        nday = 334
    return nday
