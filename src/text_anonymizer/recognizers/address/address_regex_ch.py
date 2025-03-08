"""
    Inspired by:
    - https://www.watson.ch/schweiz/leben/727369873-das-ist-der-haeufigste-strassenname-der-schweiz
    - https://de.wikipedia.org/wiki/Postleitzahl_(Schweiz)
    - https://stackoverflow.com/questions/9863630/regex-for-splitting-a-german-address-into-its-parts
    - https://regex101.com/library/jR3hA0
    - https://gist.github.com/0OZ/447ecddcbbe8e9bef546701822fb8cde
"""

REGEX_CH_POSTAL_CODE = r"""
(?P<postal_code>
    (?: (?<! \d) )
    (?P<Landkennung>CH-)?
    (?P<Leitregion>[1-9]{1})
    (?P<Leitbereich>[0-9]{3})
    (?: (?! \d ) )
)
"""

REGEX_CH_STANDARD_STREET_DE = r"""
(?P<standard_street_de>
    (?: (?<! [A-ZÄÖÜa-zäöüß] ) )

    ( [A-ZÄÖÜ] [a-zäüöß]+ [ ]{0,5} [-]? [ ]{0,5} ){0,3}
    [ ]?
    ([Aa]bfahrt|[AaÄä]cker|[Aa]llee|[Aa]lm|[Aa]nger|[Aa]nlage|[Bb]ach[l]?|[Bb]ad|[Bb]aum|[Bb]erg(en|l)?|[Bb]ichl|[Bb]lick|[Bb]oden|[Bb][oö]gen|[Bb]reite|[Bb]ruch|[Bb]rücke|[Bb]rühl|[Bb]runn(en)?|[Bb]ucht[l]?|[Bb]urg|[Bb]üh[e]?l|[Cc]haussee|[Dd]amm|[Dd]orf|[Dd]örfl|[Ee]ben|[Ee]ck|[Ee]gg|[Ee]ich|[Ee]splanade|[Ff]ahrt|[Ff]eld|[Ff]leck|[Ff]orst|[Gg][aä]rten|[Gg]artl|[Gg]asse|[Gg]a(ss|ß)l|[Gg]elände|[Gg]raben|[Gg]rub[e]?|[Gg]rund[e]?|[Gg]ründe|[Gg]ürtel|[Hh]afen|[Hh]agen|[Hh]ain|[Hh]alde|[Hh]ang|[Hh]aus|[Hh]äuser|[Hh]äusl|[Hh]eide|[Hh]eim|[Hh][oö]f(e|en)?|[Hh]öhe|[Hh]olz|[Hh]ölzl|[Hh]örn|[Hh]ügel|[Hh]ütte[n]?|[Jj]och|[Kk]ai|[Kk]anal|[kk]eller|[Kk]irch(en|e)?|[Kk]og[e]?l|[Kk]olonie|[Kk]reuz|[Ll]ach|[Ll][aä]nd[e]?|[Ll]eiten|[Ll]inden|[Mm]arkt|[Mm]itte|[Mm]ühl[e]?|[Nn]ord|[Oo]rt|[Öö]rtl|[Pp]ark|[Pp]assage|[Pp]fad|[Pp]latz[l]?|[Pp]romenade|[Rr]and|[Rr]ain|[Rr]edder|[Rr]eit|[Rr]euth|[Rr]ied|[Rr]ieg[e]?l|[Rr]ing|[Ss]chanz[e]?|[Ss]chlag|[Ss]chule|[Ss]chütt|[Ss]ee|[Ss]eite|[Ss]iedlung|[Ss]pitz|[Ss]tadl|[Ss]ta[dt]t|[Ss]tall|[Ss]te[e]?g|[Ss]teig[e]?|[Ss]tein|Steinbüchel|[Ss]tieg[e]?|[Ss]tift|[Ss]tr(|\.|a(ss|ß)e)|[Tt]al|[Tt]eich|[Tt]hurn|[Tt]or|[Tt]rift|[Tt]urm|[Uu]fer|[Vv]iertel|[Vv]öhde|[Ww]acht|[Ww]ald[e]?|[Ww]all|[Ww]art[e]?|[Ww]asser|[Ww]eg|[Ww]eide|[Ww]erk|[Ww]ies[e]?[n]?|[Ww]ink[e]?l|[Zz]eil[e]?|[Zz]ing|[Zz]ipf|[Zz]one)

    (?: (?! [A-ZÄÖÜa-zäöüß] ) )
)
"""

REGEX_CH_STANDARD_STREET_CH = r"""
(?P<standard_street_ch>
    (?: (?<! [A-ZÄÖÜa-zäöüß] ) )

    ( [A-ZÄÖÜ] [a-zäüöß]+ [ ]{0,5} [-]? [ ]{0,5} ){0,3}
    [ ]?
    ([Ww]egli|[Hh]üs(li|i)?)

    (?: (?! [A-ZÄÖÜa-zäöüß] ) )
)
"""

REGEX_CH_STANDARD_STREET_FR = r"""
(?P<standard_street_fr>
    (?:(?<![A-ZÄÖÜa-zäöüß]))
    
    (All(é|e)e|Au|Aux|Avenue|Boulevard|Champ[s]?|Ch(.|em[.]?|emin)?|Chez|Clos|Coin|Combe|C(ô|o)te|Cour|Cras|Cr(ê|e)t|Derri(è|e)re|Escalier|Ferme|Fin|Grand|Haut|Impasse|M(é|e)tairie|Moulin|Passage|Petit(e|es)?|Place|Pré|Prés|Promenade|Riva|Quai|Quartier|Route|RT[E]?|Rt[e]?|Rue|Ruelle|Sentier|Sous|Sur|Vers|Voie)
    [ ]
    ([A-ZÀ-ÝÑÄÖÜa-zà-ÿßñäöüß´`']+[ ]?){1,3}
    
    (?:(?![A-ZÄÖÜa-zäöüß]))
)
"""

REGEX_CH_STANDARD_STREET_IT = r"""
(?P<standard_street_it>
    (?:(?<![A-ZÄÖÜa-zäöüß]))
    
    (Alla|Ara|Car(a|á|à|aa)|Contrada|Corte|Gassa|Giassa|Piazza|Piazzetta|Ra|Salita|Sent(e|é|ée|ee)|Sentiero|Str(á|a)da|Str(é|e)cia|Str(è|e)da|Veia|Veja|Via|Viale|Vicolo|Vietta|Voa|Voia)
    [ ]
    ([A-ZÀ-ÝÑÄÖÜa-zà-ÿßñäöüß´`']+[ ]?){1,3}
    
    (?:(?![A-ZÄÖÜa-zäöüß]))
)
"""

REGEX_CH_OTHER_STREET = r"""
(?P<other_street>
    (?: (?<! [A-ZÄÖÜa-zäöüß] ) )
    ( [A-ZÄÖÜ] [a-zäüöß]+ [ ]{0,5} [-]? [ ]{0,5} ){1}
    (?: (?! [A-ZÄÖÜa-zäöüß] ) )
)
"""

REGEX_CH_STREET = r"""
(?P<street>
    {standard_street_de}
    |
    {standard_street_ch}
    |
    {standard_street_fr}
    |
    {standard_street_it}
)
""".format(
    standard_street_de=REGEX_CH_STANDARD_STREET_DE,
    standard_street_ch=REGEX_CH_STANDARD_STREET_CH,
    standard_street_fr=REGEX_CH_STANDARD_STREET_FR,
    standard_street_it=REGEX_CH_STANDARD_STREET_IT,
    other_street=REGEX_CH_OTHER_STREET,
)

REGEX_CH_STREET_NUMBER = r"""
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

REGEX_CH_CITY = r"""
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

REGEX_CH_REGION = r"""
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
REGEX_CH_ADDRESS = r"""
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
    street=REGEX_CH_STREET,
    street_number=REGEX_CH_STREET_NUMBER,
    postal_code=REGEX_CH_POSTAL_CODE,
    city=REGEX_CH_CITY,
    region=REGEX_CH_REGION,
)
