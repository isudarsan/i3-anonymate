"""
    Inspired by:
    - https://de.wikipedia.org/wiki/Postleitzahl_(Deutschland)
    - https://de.wikipedia.org/wiki/Liste_der_Postleitregionen_in_Deutschland#F%C3%BCnfstelliges_System_seit_1993
    - https://de.wikipedia.org/wiki/Stra%C3%9Fenname
    - https://de.wikipedia.org/wiki/Stra%C3%9Fe#Namenszus%C3%A4tze
    - https://de.wikipedia.org/wiki/Wohnadresse
    - https://de.wikipedia.org/wiki/Geb%C3%A4udeadresse
    - https://www.focus.de/regional/nordrhein-westfalen/von-koeln-nach-pulheim-1501-das-ist-die-hoechste-hausnummer-deutschlands_id_5671032.html
    - https://de.wikipedia.org/wiki/Quadratestadt
    - https://stackoverflow.com/questions/9863630/regex-for-splitting-a-german-address-into-its-parts
    - https://regex101.com/library/jR3hA0
    - https://gist.github.com/0OZ/447ecddcbbe8e9bef546701822fb8cde
"""

REGEX_DE_POSTAL_CODE = r"""
(?P<postal_code>
    (?: (?<! \d) )
    (?P<Code>[D][ ]{0,1}[-][ ]{0,1})?
    (?P<Leitregion>[0]{1}[1-9]{1}|[1-9]{1}[0-9]{1})
    (?P<Leitbereich>[0-9]{3})
    (?: (?! \d ) )
)
"""

REGEX_DE_STANDARD_STREET = r"""
(?P<standard_street>
    (?: (?<! [A-ZÄÖÜa-zäöüß] ) )

    ( [A-ZÄÖÜ] [a-zäüöß]+ [ ]{0,5} [-]? [ ]{0,5} ){0,3}
    [ ]?
    ([Cc]haussee|[Aa]llee|[Ss]tr(|\.|a(ss|ß)e)|[Rr]ing|berg|gasse|grund|hörn|Nord|graben|[Mm]arkt|[Uu]fer|[Ss]tieg[e]?|[Ss]teig[e]?|[Ll]inden|[Dd]amm|[Pp]latz|brücke|Steinbüchel|Burg|[Ww]eg|rain|park|[Ww]eide|[Hh][oö]f|pfad|garten|turm|halde|[Ww]all|redder|[Ee]splanade|[Bb]ruch|[Vv]öhde)

    (?: (?! [A-ZÄÖÜa-zäöüß] ) )
)
"""

REGEX_DE_OTHER_STREET = r"""
(?P<other_street>
    (?: (?<! [A-ZÄÖÜa-zäöüß] ) )
    ( [A-ZÄÖÜ] [a-zäüöß]+ [ ]{0,5} [-]? [ ]{0,5} ){1}
    (?: (?! [A-ZÄÖÜa-zäöüß] ) )
)
"""

REGEX_DE_MANNHEIM_STREET = r"""
(?P<mannheim_street>
    (?: (?<! \w ) )
    [A-IK-U][1-7]
    (?: (?! \d ) )
)
"""

REGEX_DE_STREET = r"""
(?P<street>
    {standard_street}
    |
    {mannheim_street}
)
""".format(
    standard_street=REGEX_DE_STANDARD_STREET,
    other_street=REGEX_DE_OTHER_STREET,
    mannheim_street=REGEX_DE_MANNHEIM_STREET,
)

REGEX_DE_STREET_NUMBER = r"""
(?P<street_number>
    (?: (?<! \d) )

    (\d{1,4})
    ([a-zA-Z]{0,3})
    (
        ( [ ]{0,5} (–|-|/)? [ ]{0,5} )
        \d{1,3}
        [a-zA-Z]?
    )?
    
    (?: (?! \d ) )
)
"""

REGEX_DE_CITY = r"""
(?P<city>
    (?: (?<! [A-ZÄÖÜa-zäöüß] ) )

    [A-ZÄÖÜ][a-zäöüß]+
    (
        [ ]{0,5} (-|\\|/|am|an\ der)? [ ]{0,5}
        [A-ZÄÖÜ][a-zäöüß]+
    )?

    (?: (?! [A-ZÄÖÜa-zäöüß] ) )
)
"""

REGEX_DE_REGION = r"""
(?P<region>
    (?: (?<! [A-ZÄÖÜa-zäöüß] ) )

    [A-ZÄÖÜ][A-ZÄÖÜa-zäöüß]+
    (
        [ ]{0,5} (-|\\|/|\(|\))? [ ]{0,5}
        [A-ZÄÖÜ][A-ZÄÖÜa-zäöüß]+
    ){0,2}
    [ \) ] ?

    (?: (?! [A-ZÄÖÜa-zäöüß] ) )
)
"""

"""
Addresses match when they
1) contain a street name followed by a street number
2) end with a city, postal code or both OR start with a postal code and optionally a city
"""
REGEX_DE_ADDRESS = r"""
(?x)
(?P<address>
    # before street and street number
    (?P<before_street>
        (?: # postal code mandatory and city optionally
            (?:
                {city}
            )?
            (?:
                (?(city)
                    (?P<sep_before_postal_code> (( [^\d\n\r] {{1,5}} (\r\n|\r|\n)? ) )|(\r\n|\r|\n))
                    |
                )
                {postal_code}
            )
            (?(city)
                |
                (?:
                    (?P<sep_before_city> (( [^\d\n\r] {{1,5}} (\r\n|\r|\n)? ) )|(\r\n|\r|\n))
                    {city}
                )?
            )
        )
    )?
    (?(before_street)
        (?P<sep_before_street> (( [^\d\n\r] {{1,5}} (\r\n|\r|\n)? ) )|(\r\n|\r|\n))
        |
    )
    (?: # street and street number
        {street}
        (?P<sep_before_street_number> [ ] {{1,5}})
        {street_number}
    )
    # after street and street number
    (?(before_street)
        |
        (?P<after_street>
            (?: # postal code mandatory and city optionally
                (?:
                    (?P<sep_before_city> (( [^\d\n\r] {{1,6}} (\r\n|\r|\n)? ) )|(\r\n|\r|\n))
                    {city}
                )?
                (?:
                    (?P<sep_before_postal_code> (( [^\d\n\r] {{1,5}} (\r\n|\r|\n)? ) )|(\r\n|\r|\n))
                    {postal_code}
                )
                (?(city)
                    |
                    (?:
                        (?P<sep_before_city> (( [^\d\n\r] {{1,5}} (\r\n|\r|\n)? ) )|(\r\n|\r|\n))
                        {city}
                    )?
                )
            )
            |
            (?: # city mandatory and postal code optionally
                (?:
                    (?P<sep_before_postal_code> (( [^\d\n\r] {{1,5}} (\r\n|\r|\n)? ) )|(\r\n|\r|\n))
                    {postal_code}
                )?
                (?:
                    (?P<sep_before_city> (( [^\d\n\r] {{1,5}} (\r\n|\r|\n)? ) )|(\r\n|\r|\n))
                    {city}
                )
                (?:
                    (?P<sep_before_region> (( [^\d\n\r] {{1,5}} (\r\n|\r|\n)? ) )|(\r\n|\r|\n))
                    {region}
                )?
                (?(postal_code)
                    |
                    (?:
                        (?P<sep_before_postal_code> (( [^\d\n\r] {{1,5}} (\r\n|\r|\n)? ) )|(\r\n|\r|\n))
                        {postal_code}
                    )?
                )
            )
        )
        (?P<closing_chars> [ \) ] )?
    )
)
""".format(
    street=REGEX_DE_STREET,
    street_number=REGEX_DE_STREET_NUMBER,
    postal_code=REGEX_DE_POSTAL_CODE,
    city=REGEX_DE_CITY,
    region=REGEX_DE_REGION,
)
