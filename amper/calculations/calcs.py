# coding: utf-8

# In[ ]:

import math

# Gsc = Solar constant
# 
# φ = Latitude 
# 
# L = Longitude 
# 
# δ = Declination -> **-23.45°≤δ≤23.45°** 
# 
# ω = Hour angle -> **-180°≤ω≤180°** 
# 
# hs = Sun altitude 
# 
# γ = Solar azimuth 
# 
# θz = Zenith Angle -> **0° ≤ θz ≤ 90°** 
# 
# Gon = Exact irradiation incident on a surface θ outside the atmosphere 
# 
# τb = Transmision Beam radiation 
# 
# τd = Transmision diffuse radiation 
# 
# Gcb = Beam radiation 
# 
# 

# Solar constant
# 
# ![title](http://i.imgur.com/UqAn4ZB.png)
# 
# 
# σ = 5.67*10^-8 W/m^2.k^4 Stefan Boltzmann constant
# 
# R = 696*10^6m Sun radiuses
# 
# D = 150 * 10^9 is the avg distance between sun and earth

# In[ ]:

solar_constant = 1367  # W/m^2


def cos(x):
    return math.cos(x)


def sin(x):
    return math.sin(x)


def asin(x):
    return math.asin(x)


# Sun position
# 
# => α=90-Φ+δ

# In[7]:

def fun_sun_position(latitude, declination):
    return 90 - latitude + declination


# 

# Where declination is calculated as
# 
# => δ= 23.45° ⋅ Sin[ 360/365 (284+d)] 
# 
# and 284 is an adjustation value as declination not being zero on January 

# In[8]:

def fun_declination(day):
    return 23.45 * sin((360 / 365) * (284 + day))


# The hour angle is the derivation of the sun's angle from south:
# 
# => ω = 15° ⋅ (SolarTime - 12)

# In[9]:

def fun_hour_angle(solar_time):
    return 15 * (solar_time - 12)


# Where solar time is calculated as:
# 
# => E = 229.2 ⋅ (0.000075 + 0.001868 cosB − 0.032077 ⋅ sinB−0.014615 ⋅  cos2B − 0.04089 ⋅ sin2B)
# 
# => B = (n - 1) ⋅ 360/365
# 
# => SolarTime = StandardTime + 4(Lst - Lloc) + E
# 
# Lst = Standard meridian for the local timezone
# Lloc = Longitude of the location
# 
# Reference: https://en.wikipedia.org/wiki/Equation_of_time

# In[1]:

def fun_e(day):
    B = (day - 1) * 360 / 365
    return 229.2 * (0.000075 + 0.001868 * cos(B) * sin(B) - 0.014615
                    * cos(2 * B) - 0.04089 * sin(2 * B))


def fun_solar_time(std_time, std_meridian, longitude, day):
    return std_time + ((4 * (std_meridian - longitude) + fun_e(day)) / 60)


# Solar altitude:
# 
# => hs = Arcsin[cos(φ) * cos(δ) * cos(ω) + sin(φ)*sin(δ)]

# In[ ]:

def fun_sun_altitude(latitude, declination, hour_angle):
    return asin(
        cos(latitude) * cos(declination) * cos(hour_angle) + sin(latitude) * sin(declination))


# Solar azimuth:
# 
# => γ = Arcsin[(cos(δ) ⋅ sin(ω))/cos(hs)]

# In[ ]:

def fun_azimuth(declination, hour_angle, sun_altitude):
    return asin((cos(declination) * sin(hour_angle)) / cos(sun_altitude))


# Zenith angle:
# 
# => cosθz = cosφ⋅cosδ⋅cosω+sinφ⋅sinδ

# In[ ]:

def fun_zenith_angle(latitude, declination, hour_angle):
    return cos(latitude) * cos(declination) * cos(hour_angle) + sin(latitude) * sin(
        declination)


# Radiation outside atmosphere:
# 
# => Gon = Gsc * (1 + 0.033 ⋅ cos((360⋅n)/365))

# In[ ]:

def fun_radiation_outside_atmosphere(day):
    return solar_constant * (1 + 0.033 * cos((360 * day) / 365))


# Thau beam:
# 
# => τb = Gcb / Go = a0 + a1 ⋅ e^(-K/cosθz)
# 
# Beam radiation:
# 
# => Gcb = τb ⋅ Gon ⋅ (cosφ ⋅ cosδ ⋅ cosω + sinφ ⋅ sinδ)
# 
# Let's define some constants:
# 
# a0 = 0,4237 - 0.00821 ⋅ (6-A)^2
# a1 = 0,5055 - 0.00595 ⋅ (6.5-A)^2
# k = 0.2711 + 0.01858 ⋅ (2.5-A)^2
# 
# Where A is the altitude above the sea level (in km).

# In[ ]:

def fun_transmission_beam(altitude, zenith_angle):
    a0 = 0.4237 - 0.00821 * (6 - altitude) ** 2
    a1 = 0.5055 - 0.00595 * (6.5 - altitude) ** 2
    k = 0.2711 + 0.01858 * (2.5 - altitude) ** 2

    return a0 + a1 * (math.e ** (-k / cos(zenith_angle)))


def fun_beam_radiation(t_beam, rad_outside_atmosphere, latitude, declination, hour_angle):
    return t_beam * rad_outside_atmosphere * (
        cos(latitude) * cos(declination) * cos(hour_angle) + sin(latitude) * sin(
            declination))


# Transimion diffuse radiation:
# 
# => τd = 0.271 - 0.294 ⋅ τb
# 
# Diffuse Radiation:
# 
# => Gcd = τd ⋅ Gon ⋅ (cosφ ⋅ cosδ ⋅ cosω + sinφ ⋅ sinδ)

# In[2]:

def fun_transmission_diffuse_radiation(transmission_beam):
    return 0.271 - 0.294 * transmission_beam


def fun_diffuse_radiation(t_diffuse_radiation, rad_outside_atmosphere, latitude, declination, hour_angle):
    return t_diffuse_radiation * rad_outside_atmosphere * (cos(latitude) * cos(declination)
                                                           * cos(hour_angle) + sin(latitude)
                                                           * sin(declination))


# Total radiation received on horizontal at ground surface at a clear day:
# 
# => Gc = (τb +τd)⋅Gsc⋅(1+0.033⋅cos(360⋅n)/365)⋅(cosφ⋅cosδ⋅cosω+sinφ⋅sinδ)

# In[5]:

def fun_total_radiation_day(transmission_beam, transmission_diffuse_radiation, latitude, declination, hour_angle, day):
    transmissions_sum = transmission_beam + transmission_diffuse_radiation

    return transmissions_sum * solar_constant * (
        1 + 0.033 * cos((360 * day) / 365) * (cos(latitude) * cos(declination)
                                              * cos(hour_angle) + sin(latitude)
                                              * sin(declination)))


def radiation_day(latitude, longitude, altitude, day, current_time, gtm):
    declination = fun_declination(day=day)
    print("Declination " + str(declination))

    radiation_outside_atmosphere = fun_radiation_outside_atmosphere(day=day)
    print("Radiation outside atmosphere " + str(radiation_outside_atmosphere))

    solar_time = fun_solar_time(std_time=current_time, std_meridian=gtm, longitude=longitude, day=day)
    print("Solar time " + str(solar_time))

    hour_angle = fun_hour_angle(solar_time=solar_time)
    print("Hour angle " + str(hour_angle))

    zenith_angle = fun_zenith_angle(latitude=latitude, declination=declination, hour_angle=hour_angle)
    print("Zenith angle " + str(zenith_angle))

    transmission_beam = fun_transmission_beam(altitude=altitude, zenith_angle=zenith_angle)
    print("Transmission beam " + str(transmission_beam))

    transmission_diffuse_radiation = fun_transmission_diffuse_radiation(transmission_beam=transmission_beam)
    print("Transmission diffuse radiation " + str(transmission_diffuse_radiation))

    beam_radiation = fun_beam_radiation(t_beam=transmission_beam, rad_outside_atmosphere=radiation_outside_atmosphere,
                                        latitude=latitude, declination=declination,
                                        hour_angle=hour_angle)
    print("Beam radiation " + str(beam_radiation))

    diffuse_radiation = fun_diffuse_radiation(t_diffuse_radiation=transmission_diffuse_radiation,
                                              rad_outside_atmosphere=radiation_outside_atmosphere, latitude=latitude,
                                              declination=declination, hour_angle=hour_angle)
    print("Diffuse radiation " + str(diffuse_radiation))

    return fun_total_radiation_day(transmission_beam=transmission_beam,
                                   transmission_diffuse_radiation=transmission_diffuse_radiation, latitude=latitude,
                                   declination=declination, hour_angle=hour_angle, day=day)


# Energy received taking into acount the inclinationg of the surface
# 
# => G (inclined) = G(horizontal) * Sin (α+β) / Sinα
# 
# β is the ° of the surface

# In[6]:

def fun_radiation_with_angle_simple(raw_radiation, sun_position, panel_angle):
    return raw_radiation * sin(sun_position + panel_angle) / sin(sun_position)

#
