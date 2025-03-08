"""
    Inspired by:
    https://www.laputa.it/spanish-street-types/?lang=en
"""

REGEX_ES_POSTAL_CODE = r"""
(?P<postal_code>
    (?: (?<! \d) )
    (?P<province>[0]{1}[1-9]{1}|[1-5]{1}[0-9]{1})
    (?P<remainder>[0-9]{3})
    (?: (?! \d ) )
)
"""

REGEX_ES_STANDARD_STREET = r"""
(?P<standard_street>
    (?: (?<! [A-ZÀ-ÝÑÄÖÜa-zà-ÿßñäöüß] ) )

    (Avenida|Avenue|Autovía|Avda[.]?|Avd[.]?|Avda[.]?|Av.|Barriada|Barrio|Bulevar|[Cc]alle|Carril|Circunvalación|Corredera|[Cc][./]|[Cc]arrer|Carretera|[Cc]rta.|Camino|Plaça|Plaza|Pl\.|Pza\.|Paseo|Pso.|Pasaje|Pje.|Rúa|Rbla.|Rambla|Ronda|Senda|Vía)
    [ ]{0,2}
    ( [A-ZÀ-ÝÑÄÖÜa-zà-ÿßñäöüß´`']+ [ ]? ){0,4}
    
    (?: (?! [A-ZÀ-ÝÑÄÖÜa-zà-ÿßñäöüß] ) )
)
"""

REGEX_ES_STREET = r"""
(?P<street>
    {standard_street}
)
""".format(
    standard_street=REGEX_ES_STANDARD_STREET
)

REGEX_ES_STREET_NUMBER = r"""
(?P<street_number>
    (?: (?<! \d) )
    ([Nn])? (º)?
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

REGEX_ES_CITY = r"""
(?P<city>
    (?: (?<! [A-ZÀ-ÝÑÄÖÜa-zà-ÿßñäöüß] ) )
    [A-ZÀ-ÝÑ] [a-zà-ýßñ]+
    ( [A-ZÀ-ÝÑÄÖÜa-zà-ÿßñäöüß´`']+ [ ]? ){0,3}
    (?: (?! [A-ZÀ-ÝÑÄÖÜa-zà-ÿßñäöüß] ) )
)
"""

REGEX_ES_REGION = r"""
(?P<region>
    (?: (?<! [A-ZÀ-ÝÑÄÖÜa-zà-ÿßñäöüß] ) )

    [A-ZÀ-ÝÑ] [a-zà-ýßñ]+
    [ ]?
    ( [A-ZÀ-ÝÑÄÖÜa-zà-ÿßñäöüß´`']+ [ ]? ){0,3}

    (?: (?! [A-ZÀ-ÝÑÄÖÜa-zà-ÿßñäöüß] ) )
)
"""

# Details of an appartment like floor, stairwell etc.
# Written in a generic way and using separators to be used as a placeholder or separator for appartment details,
# e.g. between the street number and the remainder of the address.
REGEX_ES_APPARTMENT_DETAILS_W_SEPARATOR = r"""
(?P<appartment_details>
    ([°º A-Z a-z 0-9 , .]|[ ]){1,4}?
)
"""

"""
Addresses match when they
1) contain a street name and a street number
2) end with a city, postal code or both OR start with a postal code and optionally a city
"""
REGEX_ES_ADDRESS = r"""
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
        (?P<sep_street_street_no> ([,]|[ ]) {{1,5}})
        {street_number}
        |
        {street_number}
        (?P<sep_street_no_street> ([,]|[ ]) {{1,5}})
        {street}
    )
    # after street and street number
    (?(before_street)
        |
        # optional part for appartment details, contains separators for the following already
        # {appartment_details}?
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
    street=REGEX_ES_STREET,
    street_number=REGEX_ES_STREET_NUMBER,
    appartment_details=REGEX_ES_APPARTMENT_DETAILS_W_SEPARATOR,
    postal_code=REGEX_ES_POSTAL_CODE,
    city=REGEX_ES_CITY,
    region=REGEX_ES_REGION,
)
