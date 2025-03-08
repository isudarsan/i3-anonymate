from enum import Enum


class CreditCardNumbers(Enum):
    visa_with_gaps = "4539 1488 0343 6467"
    visa_no_gaps = "4539148803436467"
    mastercard_with_gaps = "5555 3412 4444 1115"
    mastercard_no_gaps = "5555341244441115"
    american_express_with_gaps = "3714 496353 98431"
    american_express_no_gaps = "371449635398431"
    visa_short = "4222222222222"


credit_card_test_cases = [credit_card.value for credit_card in CreditCardNumbers]
credit_card_test_case_ids = [credit_card.name for credit_card in CreditCardNumbers]


class CreditCardNumbers_invalid(Enum):
    visa = "4539 1488 0443 6467"
    visa_short = "4222222222223"
    mastercard = "5555 3412 4484 1115"
    american_express = "378282246310002"
    diners_club_international = "30569309025902"


invalid_credit_card_test_cases = [credit_card.value for credit_card in CreditCardNumbers_invalid]
invalid_credit_card_test_case_ids = [credit_card.name for credit_card in CreditCardNumbers_invalid]

class USDriverLicenseNumbers(Enum):
    alabama = "1234567"
    arizona = "D08954796"
    arkansas = "999999999"
    colorado = "15-239-1250"
    florida = "S514-172-80-844-0"
    idaho = "TC100001G"
    illinois = "P142-4558-7924"
    iowa = "123XX6789"
    washington = "WDLABCD456DG"
    # california = "I1234568"  # not recognized
    # michigan = "800 000 224 322"  # last 3 digits not recognized
    # new_jersey = "X9999 99999 99999"  # first part not detected


us_driver_license_test_cases = [license.value for license in USDriverLicenseNumbers]
us_driver_license_test_case_ids = [license.name for license in USDriverLicenseNumbers]


email_test_cases = [
    "user@mail.example.com",
    "user+label@example.com",
    "first.last@example.com",
    "user@example-company.com",
    "user123@example.com",
    "123user@example.com",
    "user_name@example.com",
    "user-name@example.com",
    # "user@mailserver",
    # "user@xn--dmin-mari.com",
    "a_really_long_username_matching_the_maximum_length@example.com",
    "austria@example.at",
    "switzerland@example.ch",
    "germany@example.de",
    "united_kingdom@example.co.uk",
]


class IBANExamples(Enum):
    AUSTRIA = "AT61 1904 3002 3457 3201"
    FRANCE = "FR76 3000 6000 0112 3456 7890 189"
    GERMANY = "DE89 3704 0044 0532 0130 00"
    ITALY = "IT60 X054 2811 1010 0000 0123 456"
    SPAIN = "ES91 2100 0418 4502 0005 1332"
    SWITZERLAND = "CH93 0076 2011 6238 5295 7"
    UK = "GB29 NWBK 6016 1331 9268 19"


iban_test_cases = [iban.value for iban in IBANExamples]
iban_test_case_ids = [iban.name for iban in IBANExamples]


class AddressExamples(Enum):
    AUSTRIA: dict[str, str] = {
        "AUSTRIA_1": "Mariahilfer Straße 123, 1060 Wien", # countries are not recognized
        #"AUSTRIA_2": "Schönbrunner Allee 45, Stiege 2, Top 8, 1120 Wien", # Stiegennr. und Topnr. werden nicht erkannt
        "AUSTRIA_3": "Haupt-Platz 7, 8010 Graz",
        "AUSTRIA_4": "Dorfstraße 12a, A-6020 Innsbruck",
        "AUSTRIA_5": "Landstraße 20 in 4020 Linz",
        #"AUSTRIA_6": "Postfach 20, 4020 Linz", # Postfachlogik wird nicht erkannt
    }
    SWITZERLAND: dict[str, str] = {
        "SWITZERLAND_1": "Bahnhofstrasse 12, 8001 Zürich",
        #"SWITZERLAND_2": "Rue de Lausanne 45, 1202 Genève", # accents nicht erkannt
        "SWITZERLAND_3": "Industriestrasse 27, CH-3052 Zollikofen",
        #"SWITZERLAND_4": "Postfach, 4001 Basel", # Postfachnummer muss nicht zwangsläufig angegeben werden
        #"SWITZERLAND_5": "Postfach 123, 4001 Basel",
        "SWITZERLAND_6": "Untere Hauptgasse 14 in 3600 Thun",
    }
    GERMANY: dict[str, str] = {
        "GERMANY_1": "Berliner Straße 98, 10115 Berlin",
        "GERMANY_2": "Hauptplatz 17 in 80331 München",
        "GERMANY_3": "Am Kirchplatz 5, D-69117 Heidelberg",
        "GERMANY_4": "Rathaus-berg 13, 68159 Mannheim",
        "GERMANY_5": "E5 6, 68159 Mannheim",
        #"GERMANY_6": "Postfach 3456, 53115 Bonn", #Postfachlogik nicht abgedeckt
        #"GERMANY_7": "Guimaráes-Platz 3, 67655 Kaiserslautern", # akztente nicht abgedeckt
    }
    SPAIN: dict[str, str] = {
        "SPAIN_1": "Calle Mayor 24, 28013 Madrid",
        "SPAIN_2": "Carrer de Balmes, 51, 08007 Barcelona",
        "SPAIN_3": "Plaza del Ayuntamiento, 10, 46002 Valencia",
        "SPAIN_4": "Avenida de Andalucía 12, 29001 Málaga",
        #"SPAIN_5": "Paseo de la Castellana 120, Esc. A, 28046 Madrid", # Treppenaufstiege (Escalera) nicht gematched
    }
    UK: dict[str, str] = {
        "UK_1": "221B Baker Street, London NW1 6XE",
        "UK_2": "10 Downing Street, Westminster, SW1A 2AA",
        "UK_3": "34 George Street, Edinburgh EH2 2LR",
        #"UK_4": "County Road, John O'Groats KW1 4YR", # missing street number
    }
    US: dict[str, str] = {
        #"US_1": "1600 Pennsylvania Avenue NW, Washington, DC 20500", # 
        "US_2": "123 Elm Street, Apt. 4B, New York, NY 10001",
        "US_3": "742 Evergreen Terrace, Springfield, IL 62701",
        "US_4": "1 Infinite Loop, Cupertino, CA 95014",
        "US_5": "350 Fifth Avenue, Suite 3800, New York, NY 10118",
    }


address_at_test_cases = list(AddressExamples.AUSTRIA.value.values())
address_at_test_case_ids = list(AddressExamples.AUSTRIA.value.keys())
address_ch_test_cases = list(AddressExamples.SWITZERLAND.value.values())
address_ch_test_case_ids = list(AddressExamples.SWITZERLAND.value.keys())
address_de_test_cases = list(AddressExamples.GERMANY.value.values())
address_de_test_case_ids = list(AddressExamples.GERMANY.value.keys())
address_es_test_cases = list(AddressExamples.SPAIN.value.values())
address_es_test_case_ids = list(AddressExamples.SPAIN.value.keys())
address_uk_test_cases = list(AddressExamples.UK.value.values())
address_uk_test_case_ids = list(AddressExamples.UK.value.keys())
address_us_test_cases = list(AddressExamples.US.value.values()) 
address_us_test_case_ids = list(AddressExamples.US.value.keys())


class VinExamples(Enum):
    HONDA   = "1HGBH41JXMN109186" # Honda
    SUZUKI  = "LJCPCBLCX11000237" # motor cycle
    PORSCHE = "WP0ZZZ99ZTS392124" # Porsche
    AUDI    = "WAUZZZ8CZRA166666" # Audi80
    MB_1    = "WDB2110611A189066" # Mercedes
    MB_2    = "WDD1760012J220412" # Mercedes
    MB_3    = "WDDZF6EB7JA400545" # Mercedes
    MB_4    = "WDC2533641F249044" # Mercedes


vin_test_cases = [vin.value for vin in VinExamples]
vin_test_cases_ids = [vin.name for vin in VinExamples]


class ImeiExamples(Enum):
    IPHONE_11       = "356656420759143"
    IPHONE_07       = "353816087037570"
    IPAD_AIR19      = "353193101561377"
    SAMSUNG_S23     = "350925378856300"
    SAMSUNG_A12     = "353411573285477"
    REDMI_12C       = "864792066725562"
    GOOGLE_PIXEL7   = "354449800418262"
    HUAWEI_P30      = "860998045323254"
    OPPO_A3         = "869311034496886"
    VIVO_V20        = "865551059948659"
    EALME_GT2       = "861943053106786"
    MOTOROLA_G53    = "352790348046574"
    LG_G6           = "355403083327657"
    NOKIA_1100      = "010510000707477"
    ONEPLUS_9       = "866522055827402"
    HONOR_90        = "863432066896581"
    INFINIX_G96     = "352844812831332"
    LENOVO_TABE10   = "869619046443567"
    ALCATEL_1S      = "355130108187952"
    ZUTE_A725G      = "860703065673749"
    SONY_XZ3        = "351739090429182"
    ASUS_ZENFONE5   = "357001067758968"
    TCL_40XL        = "357822955933581"
    # NOKIA_6030_1    = "010928/00/389023/3" # separators not recognized
    # NOKIA_6030_2    = "010928-00-389023-3" # separators not recognized
    # NOKIA_6030_3    = "01/092800/389023/3" # separators not recognized
    # NOKIA_6030_4    = "01-092800-389023-3" # separators not recognized


imei_test_cases = [imei.value for imei in ImeiExamples]
imei_test_case_ids = [imei.name for imei in ImeiExamples]

class ImeiExamples_invalid(Enum):
    IPHONE_11       = "356656420759141"
    SAMSUNG_S23     = "350925378856302"
    GOOGLE_PIXEL7   = "354449800418263"

invalid_imei_test_cases = [imei.value for imei in ImeiExamples_invalid]
invalid_imei_test_cases_ids = [imei.name for imei in ImeiExamples_invalid]

class PhoneNumberExamples_AT(Enum):
    
    SPACING_1_1   = "06641234567"
    SPACING_1_2   = "0664 1234567"
    SPACING_1_3   = "0664 123 4567"
    SPACING_1_4   = "0664 12 34 567"

    SPACING_2_1   = "+4301718605879"
    SPACING_2_2   = "+43171 860 587 9"
    SPACING_2_3   = "+43171 86 05 87 9"
    SPACING_2_4   = "+43171 86 05 879"
    SPACING_2_5   = "+43 171 860 587 9"

    SPACING_3_1   = "+43(0)1718605879"
    SPACING_3_2   = "+43(0)171 860 587 9"
    SPACING_3_3   = "+43(0)171 86 05 87 9"
    SPACING_3_4   = "+43(0)171 86 05 879"
    
    SPACING_4_1   = "+43(0) 171 860 587 9"
    SPACING_4_2   = "+43(0) 171 86 05 87 9"
    SPACING_4_3   = "+43(0) 171 86 05 879"
    
    SPACING_5_1   = "+43 (0) 171 860 587 9"
    SPACING_5_2   = "+43 (0) 171 86 05 87 9"
    SPACING_5_3   = "+43 (0) 171 86 05 879"
    
    SPACING_6_1   = "+43 (0)171 860 587 9"
    SPACING_6_2   = "+43 (0)171 86 05 87 9"
    SPACING_6_3   = "+43 (0)171 86 05 879"

    SPACING_7_1   = "00431718605879"     
    #SPACING_7_2   = "0043 171 860 587 9" 
    #SPACING_7_3   = "0043 171 86 05 87 9"
    #SPACING_7_4   = "0043 171 86 05 879" 

    SPACING_8_1   = "0316 345 6789"    
    SPACING_8_2   = "01 234 5678"    

    #CONTEXT_01   = "phone 0567841891235"
    #CONTEXT_02   = "Tel. 0567841891235"

phonenumber_at_test_cases = [pn.value for pn in PhoneNumberExamples_AT]
phonenumber_at_test_cases_ids = [pn.name for pn in PhoneNumberExamples_AT]


class PhoneNumberExamples_CH(Enum):
    
    SPACING_1_1   = "0312345678"
    SPACING_1_2   = "044 567 89 01"
    SPACING_1_3   = "079 123 45 67"

    SPACING_2_1a   = "+41312345678"
    SPACING_2_2a   = "+41 312345678"
    SPACING_2_3a   = "+41 312 345 678"
    SPACING_2_4a   = "+41 79 123 45 67"

    # +4175 for lichtenstein until end of 1999
    #SPACING_2_1b   = "+417501718605879"
    SPACING_2_2b   = "+4175171 860 587 9"
    SPACING_2_3b   = "+4175171 86 05 87 9"
    SPACING_2_4b   = "+4175171 86 05 879"
    SPACING_2_5b   = "+4175 171 860 587 9"

    SPACING_3_1   = "+41(0)312345678"
    SPACING_3_2   = "+41(0)312 345 678"
    SPACING_3_3   = "+41(0)31 23 45 678"
    
    SPACING_4_1   = "+41(0) 312345678"
    SPACING_4_2   = "+41(0) 312 345 678"
    SPACING_4_3   = "+41(0) 31 23 45 678"

    SPACING_5_1   = "+41 (0) 312345678"
    SPACING_5_2   = "+41 (0) 312 345 678"
    SPACING_5_3   = "+41 (0) 31 23 45 678"

    SPACING_6_1   = "0041312345678"
    #SPACING_6_2   = "0041 312 345 678"
    #SPACING_6_3   = "0041 31 23 45 678"
        
    #CONTEXT_01   = "phone 312345678"
    #CONTEXT_02   = "Tel. 0567841891235"

phonenumber_ch_test_cases = [pn.value for pn in PhoneNumberExamples_CH]
phonenumber_ch_test_cases_ids = [pn.name for pn in PhoneNumberExamples_CH]

class PhoneNumberExamples_DE(Enum):
    
    SPACING_1_1   = "0176 12345678" 
    SPACING_1_2   = "089 98765"
    SPACING_1_3   = "030 12345678" 
    SPACING_1_4   = "0151 98765432" 
    SPACING_1_5   = "01718304026"

    SPACING_2_1   = "+4901718605879"
    SPACING_2_2   = "+49171 860 587 9"
    SPACING_2_3   = "+49171 86 05 87 9"
    SPACING_2_4   = "+49171 86 05 879"
    SPACING_2_5   = "+49 171 860 587 9"

    SPACING_3_1   = "+49(0)1718605879"
    SPACING_3_2   = "+49(0)171 860 587 9"
    SPACING_3_3   = "+49(0)171 86 05 87 9"
    SPACING_3_4   = "+49(0)171 86 05 879"
    
    SPACING_4_1   = "+49(0) 171 860 587 9"
    SPACING_4_2   = "+49(0) 171 86 05 87 9"
    SPACING_4_3   = "+49(0) 171 86 05 879"
    
    SPACING_5_1   = "+49 (0) 171 860 587 9"
    SPACING_5_2   = "+49 (0) 171 86 05 87 9"
    SPACING_5_3   = "+49 (0) 171 86 05 879"
    
    SPACING_6_1   = "+49 (0)171 860 587 9"
    SPACING_6_2   = "+49 (0)171 86 05 87 9"
    SPACING_6_3   = "+49 (0)171 86 05 879"

    SPACING_7_1   = "00491724431392"     
    SPACING_7_2   = "0049 172 443 1392"
    SPACING_7_3   = "00492677526"      
    SPACING_7_4   = "0049 2677 526"    

    SPACING_8_1   = "(02677) 8605879"
    #SPACING_8_2   = "(02677) 860 587 9"
    #SPACING_8_3   = "(02677) 86 05 87 9"   
    SPACING_8_4   = "(02677) 86 05 879"      

    #CONTEXT_01   = "phone 0567841891235"
    #CONTEXT_02   = "Tel. 0567841891235"

phonenumber_de_test_cases = [pn.value for pn in PhoneNumberExamples_DE]
phonenumber_de_test_cases_ids = [pn.name for pn in PhoneNumberExamples_DE]

class PhoneNumberExamples_ES(Enum):
    
    SPACING_1_1   = "912 345 678"
    SPACING_1_2   = "912345678"

    SPACING_2_1   = "+34917186058"
    SPACING_2_2   = "+34 612 345 678"
    SPACING_2_3   = "+34871 860 587"

    SPACING_3_1   = "+34 931234567"
    SPACING_3_2   = "+34 93 123 4567"
    SPACING_3_3   = "+3493 1234567"

    SPACING_4_1   = "0034671860587"   
    #SPACING_4_2   = "0034 771 860 587"

    #CONTEXT_01   = "phone 917186058"
    #CONTEXT_02   = "Tel. 917186058"

phonenumber_es_test_cases = [pn.value for pn in PhoneNumberExamples_ES]
phonenumber_es_test_cases_ids = [pn.name for pn in PhoneNumberExamples_ES]

class PhoneNumberExamples_UK(Enum):
    
    SPACING_1_1   = "(0)7400 123456"
    SPACING_1_2   = "07400 123456"
    SPACING_1_3   = "07400123456"

    SPACING_2_1   = "+4420 8605879"
    SPACING_2_2   = "+4420 860 587 9"
    SPACING_2_3   = "+4420 86 05 87 9"
    SPACING_2_4   = "+4420 86 05 879"
    SPACING_2_5   = "+4420  860 587 9"

    SPACING_3_1   = "+44(0)20 605879"
    SPACING_3_2   = "+44(0)20 860 587 9"
    SPACING_3_3   = "+44(0)20 86 05 87 9"
    SPACING_3_4   = "+44(0)20 86 05 879"
    
    SPACING_4_1   = "+44 (0)20 17186058"
    SPACING_4_2   = "+44 (0)20 1718 6058"
    SPACING_4_3   = "+44 (0)20 171 860 58"
    SPACING_4_4   = "+44 (0)20 171 86 05 8"
    
    SPACING_5_1   = "+44 (0) 20 17186058"
    SPACING_5_2   = "+44 (0) 20 1718 6058"
    SPACING_5_3   = "+44 (0) 20 171 860 58"
    SPACING_5_4   = "+44 (0) 20 171 86 05 8"

    SPACING_6_1   = "+44 (0)7400 123456"
    SPACING_6_2   = "+44 (0)7400 1234 56"
    SPACING_6_3   = "+44 (0)7400 171 605"
    SPACING_6_4   = "+44 (0)7400 1718 60"

    SPACING_7_1   = "+44 (0) 7400 123456"
    SPACING_7_2   = "+44 (0) 7400 1234 56"
    SPACING_7_3   = "+44 (0) 7400 171 605"
    SPACING_7_4   = "+44 (0) 7400 1718 60"
    
    SPACING_8_1   = "+44 (0) 800 860 587 9"
    SPACING_8_2   = "+44 (0)800 8605879"
    #SPACING_8_3   = "+44(0)800 8605 8759"
    
    SPACING_9_1   = "00442018605879"
    SPACING_9_2   = "0044 20 8606 5879"
    SPACING_9_3   = "0044 (0)20 8605 8769"

    #CONTEXT_01   = "phone 20605879"
    #CONTEXT_02   = "Tel. 20605879"

phonenumber_uk_test_cases = [pn.value for pn in PhoneNumberExamples_UK]
phonenumber_uk_test_cases_ids = [pn.name for pn in PhoneNumberExamples_UK]


class PhoneNumberExamples_US(Enum):
    
    #SPACING_1_1   = "555-1234"

    SPACING_2_1   = "+11718605879"
    SPACING_2_2   = "+1171 860 587 9"
    SPACING_2_3   = "+1171 86 05 87 9"
    SPACING_2_4   = "+1171 86 05 879"
    SPACING_2_5   = "+1 171 860 587 9"

    SPACING_3_1   = "+1(205)171-8605"
    SPACING_3_2   = "+1(907)171 8605"
    
    SPACING_4_1   = "+1(229) 171-8605"
    SPACING_4_2   = "+1(808) 171 8605"

    SPACING_5_1   = "+1 (339) 171-8605" # default phone number
    SPACING_5_2   = "+1 (413) 171 8605"

    SPACING_6_1   = "+1 (218)171-8605"
    SPACING_6_2   = "+1 (218)171 8605"

    #SPACING_7_1   = "001 684 860-5879"        
    #SPACING_7_2   = "001 171 860 5879" 

    SPACING_8_1   = "(218) 860-5879"   
    SPACING_8_2   = "(413) 860 5879" 

    #CONTEXT_01   = "phone 0567841891235"
    #CONTEXT_02   = "Tel. 0567841891235"

phonenumber_us_test_cases = [pn.value for pn in PhoneNumberExamples_US]
phonenumber_us_test_cases_ids = [pn.name for pn in PhoneNumberExamples_US]

