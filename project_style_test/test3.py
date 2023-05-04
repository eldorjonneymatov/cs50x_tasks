import re
from helpers import *
import pandas as pd
import os
import datetime

# a = ['Londonning ICE birjasida Brent navli neftning narxi 31-martdan buyon ilk bor barreliga 78 dollarlik koʻrsatkichdan pastga tushdi.\n\n👉 @kunonline', '🇹🇷 Turkiya prezidenti maʼmuriyatining kommunikatsiyalar boshqarmasi shafeligi ostida tuzilgan dezinformatsiyaga qarshi kurashish markazi prezident Rajab Toyyib Erdoʻgʻanning infarktga uchragani va kasalxonaga yotqizilgani haqidagi maʼlumotlarni inkor etib chiqdi.\n\n👉 @kunonline', '🇹🇷 Turkiya prezidenti Rajab Toyyib Erdoʻgʻan 27-aprel kuni 4ta turk telekanallariga berishi rejalashtirilgan intervyusini bekor qildi.\n\n👉 @kunonline', 'Yevropada tabiiy gazning birja narxlari 2,5 foizga pasayib, 1000 kub metri uchun 442 dollargacha tushgan.\n\n👉 @kunonline', '🇬🇧 Britaniyalik deputatlar Rossiyaning “Vagner” xususiy harbiy kampaniyasini Sudandagi, Darfur muzofotidagi, shuningdek Burkina-Faso, Mali va Niger chegarasidagi buzgʻunchilik harakatlari uchun terrorchilik tashkiloti deb eʼlon qilishga chaqirishdi.\n\n👉 @kunonline', '🇧🇷 Braziliya sudi politsiya soʻroviga koʻra maʼlumotlarni toʻliq yetkazmayotgani uchun Telegram messenjeri ishini toʻxtatish haqida qaror chiqardi — Reuters\n\n👉 @kunonline', '🇨🇳 Mart oyida Xitoyda milliy valyuta yuan transchegaraviy pul oʻtkazmalarida AQSH dollaridan oʻzib, eng koʻp foydalanilgan valyutaga aylandi. Oʻtkazmalarda qariyb 550 mlrd dollarlik yuandan foydalanilgan.\n\n👉 @kunonline', '🇲🇩 “Men Moldova shu oʻn yillik oxirigacha Yevropa Ittifoqining toʻlaqonli aʼzosiga aylanishiga qattiq ishonaman” — Moldova prezidenti Mayya Sandu\n\n👉 @kunonline', '**Sharqiy Yevropa davlatlari Ukrainadagi urush fonida qarz miqdorining keskin oʻsishiga duchor boʻlishmoqda — Bloomberg.\n\n**Agentlikning maʼlumotlariga koʻra, Sharqiy Yevropa davlatlari hukumatlari dastlabki uch oyda 32 mlrd dollar qarz koʻtarishgan. Bu oʻtgan yilning shu davriga nisbatan uch barobar koʻp.\n\n👉 @kunonline', '**Jo Bayden agar AQSH va uning ittifoqchilariga yadroviy zarba berishga harakat qilsa, KXDRda “rejimni almashtirishi” bilan tahdid qildi\n\n**Bayden shuningdek KXDR bilan diplomatik sohada oʻsishga erishishga intilayotgani, biroq Vashingtonning Seul oldidagi yadroviy majburiyatlari daxlsiz ekanini ham qoʻshimcha qildi.\n\n👉 @kunonline', '“Gazprom media”ga qarashli Rutube videohostingiga texnik tomondan YouTubeʻga yetib olishi uchun 30 milliard rubl ajratilishi rejalashtirilmoqda.\n\n👉 @kunonline', '__“Men xorijiy kompaniyalar va tadbirkorlar bilan koʻproq muloqot qilishga intilaman. Sizlarning gʻoya, taklif va tashabbuslaringiz menga kuch-gʻayrat beradi, yangi islohotlarga undaydi. Shu bois, yangi-yangi investorlar bilan tez-tez uchrashuvlar oʻtkazishga, sizlarning yurtimizdagi yutuqlaringizni shaxsan kafolatlashga tayyorman”__, — dedi ikkinchi Toshkent xalqaro investitsiya forumida nutq soʻzlayotgan Shavkat Mirziyoyev.\n\n👉 @kunonline', '“Alohida taʼkidlab oʻtmoqchiman, Jahon savdo tashkiloti talablari islohotlarimiz mazmuniga toʻla mos va biz ushbu nufuzli tashkilotga tezroq aʼzo boʻlib kirishdan manfaatdormiz”, — dedi Shavkat Mirziyoyev.\n\n👉 @kunonline', '“Hech shubhasiz, yangi Konstitutsiya — biz boshlagan islohotlarni izchil davom ettirib, eng muhimi, ularga ortga qaytmaydigan tus berishi muqarrar”, — dedi Shavkat Mirziyoyev.\n\n👉 @kunonline', '**Bu yil Andijon, Namangan, Buxoro va Urganch aeroportlari boshqaruvi ham xususiy sektorga topshiriladi — Prezident\n\n**“Temiryo`l sohasida ham katta o`zgarishlarni boshlayapmiz va bunda investorlar faol ishtirok etishlarini so`rab qolaman”, – dedi Shavkat Mirziyoyev.\n\n👉 @kunonline', '🇹🇷 Turkiya prezidenti **Rajab Toyyib Erdoʻgʻan** “Aqquya” atom elektr stansiyasiga Rossiyadan yadroviy yonilg`i keltirib quyilishi marosimidagi efirga **Toshkent vaqti bilan soat 15:30 da** chiqishini maʼlum qildi.\n\n👉 @kunonline', "Rossiya mudofaa vaziri o'rinbosari general-polkovnik Mixail Mizinsyov ishdan olingani aytilmoqda.\n\n👉 @kunonline", "Ukraina xavfsizlik xizmati Donetsk viloyatida ukrain harbiylarining Limandagi pozitsiyalari haqida ruslarga ma'lumot bergan odamni ushladi.\n\n👉 @kunonline", '', '', "«Pele» so'zi portugal tili lug'atiga «eng yaxshi» so'zining ma'nodoshi sifatida kiritildi.\n\n👉 @kunonline", "Erdo'g'anning chiqishi «ba'zi sabablarga ko'ra» yarim soat keyinga surildi.\n\n👉 @kunonline", "**Turkiya prezident devoni: **Erdo'g'an mamlakatni hali uzoq vaqt boshqaradi, u favqulodda sog'lom.\n\n👉 @kunonline", '**🔺AQSH dollarining rasmiy kursi oshdi\n\n**Markaziy bank 28-apreldan xorijiy valutalarning o`zbek so`miga nisbatan yangi qiymatini belgiladi.\n\n🇺🇸 USD 11 390,24 so`m (+13,13)\n🇷🇺 RUB 139,74 so`m (+0,33)\n🇪🇺 EUR 12 572,55 so`m (+9,95)\n\n👉 @kunonline', '🇷🇺 Rossiya Davlat dumasiga “chet el agentlari”ga yordam beruvchilarni 300 ming rubl jarimaga tortish boʻyicha qonun loyihasi kiritildi.\n\n👉 @kunonline', 'Rossiya Mudofaa vazirligi shartnoma asosida xizmat qiluvchi 415 ming harbiyni yollamoqchi va ulardan 115 mingini Ukrainadagi urushga tashlamoqchi — AQSH razvedkasi\n\n👉 @kunonline']
# print(a)
# for b in a:
#     print('-'*100)
#     print(b)
#     print()
#     i = re.split(' |\n', b)
#     # print(i)
#     # print()
#     if len(i) < 2:
#         print("short")
#     elif i[-1] != "@kunonline" or i[-2] != '👉':
#         print(i)

# print(cyrillic_to_latin('ЁоЧИШҚИЧШ'))


DATA = 1
def f():
    DATA = 3

f()
print(DATA)