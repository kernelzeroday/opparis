#
#  _____ ______          _____   _____ _    _   _______ ______ _____  __  __  _____ 
# / ____|  ____|   /\   |  __ \ / ____| |  | | |__   __|  ____|  __ \|  \/  |/ ____| ®
#| (___ | |__     /  \  | |__) | |    | |__| |    | |  | |__  | |__) | \  / | (___   ©
# \___ \|  __|   / /\ \ |  _  /| |    |  __  |    | |  |  __| |  _  /| |\/| |\___ \ 
# ____) | |____ / ____ \| | \ \| |____| |  | |    | |  | |____| | \ \| |  | |____) |
#|_____/|______/_/    \_\_|  \_\\_____|_|  |_|    |_|  |______|_|  \_\_|  |_|_____/ 
                                                                                   

#This is an instructable on using the correct search terms to find ISIS-related links. If you follow
#it correctly and verify that the sites you have found are related to ISIS, please submit them, thx!


#------------
#Instructions
#------------
#1. Get Python at  https://www.python.org/downloads/  unless you already have it (Mac does)

#2. Open Terminal (or Command Prompt for Windows) and type (without quotes) "python"

#3. Copy and paste everything below the words White Villain into your interpreter

#6. Paste the generated search phrase in  https://www.google.iq  and analyze the new results
#   To translate pages, it is recommended to use Google Chrome, which has integrated translation

#7. Submit any valid ones to one of the channel operators and we will deal with the info accordingly


#THANKS FOR READING
#PLEASE PARTICIPATE

#White Villain
import random

str1= "وسائل إعلام المجاهدين"
str2= " إعلام البلاتفورم"
str3= " إعلام الزهراء"
str4= " القاعدة في المغرب الاسلامي"
str5= " منتدى اليقظة الإسلامي"
str6= " إعلام أجناد الدولة الإسلامية"
str7= " الدولة الإسلامية"
str8= " مجلس شورى المجاهدين"
str9= " المجاهدين"
str10= " أسود"
str11= " الجهاد"
str12= " كافر"
str13= " استشهاد"
str14= "  إسمـعـوا منّا إن أردتم الإنصاف"
str15= "  جهـادنا لتحكيـم الشريـعة"
str16= "  مُــــحَــــمْــــدا وَ صــحـبَــه دولة الإسلام"
str17= "  إمــارة الـعـراق - حيث مصارع الرجال"
str18 = "تقرير"
str19 = "#داعش"
str20 = "عبوة أخرى"
str21 = "الخلافة الاسلامية"
str22 = "وهلاك وإصابة"
str23 = "الموت للغرب"
str24 = "الإخوة"
str25 = "دمى"

terrorTalk = [str1,str2,str3,str4,str5,str6,str7,str8,str9,str10,str11,str12,str13,str14,str15,str16,str17,str18,str19,str20,str21,str22,str23,str24,str25]

strI1 = "media Mujahideen"
strI2 = "Media Alblattform"
strI3 = "Media Zahra"
strI4 = "Al-Qaeda in the Islamic Maghreb"
strI5 = "Islamic awakening forum"
strI6 = "inform the hosts of the Islamic state"
strI7 = "Islamic state"
strI8 = "Mujahideen Shura Council"
strI9 = "mujahideen"
strI10 = "black"
strI11 = "Jihad"
strI12 = "infidel"
strI13 = "martyrdom"
strI14 = "Hear us if you want fairness"
strI15 = "jihad of the arbitration law"
strI16 = "Muhammad and his companions state of Islam"
strI17 = "loyalty to the Muslims and disavowal of the infidels"
strI18 = "Report"
strI19 = "#Daash"
strI20 = "another explosive device"
strI21 = "Islamic Caliphate"
strI22 = "killed and injured"
strI23 = "death to the west"
strI24 = "brothers"
strI25 = "puppets"

infidelTalk = [strI1,strI2,strI3,strI4,strI5,strI6,strI7,strI8,strI9,strI10,strI11,strI12,strI13,strI14,strI15,strI16,strI17,strI18,strI19,strI20,strI21,strI22,strI23,strI24,strI25]

one = random.randrange(0,len(terrorTalk))
two = random.randrange(0,len(terrorTalk))
three = random.randrange(0,len(terrorTalk))

DONT = random.randrange(0,len(infidelTalk))
UNDERESTIMATE = random.randrange(0,len(infidelTalk))
ME = random.randrange(0,len(infidelTalk))

searchPhrase = (terrorTalk[one]+(" ")+terrorTalk[two]+(" ")+terrorTalk[three])
translation = (infidelTalk[DONT]+(" ")+infidelTalk[UNDERESTIMATE]+(" ")+infidelTalk[ME])

print (searchPhrase)
print (translation)
