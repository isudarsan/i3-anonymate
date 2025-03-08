"""
    Inspired by: 
    - wikipedia
    - the python library "pyap" (https://pypi.org/project/pyap/, https://github.com/vladimarius/pyap)
"""

"""Numerals from one to nine
Note: here and below we use syntax like '[Oo][Nn][Ee]'
instead of '(one)(?i)' to match 'One' or 'oNe' because
Python Regexps don't seem to support turning On/Off
case modes for subcapturing groups.
"""
REGEX_EN_ZERO_TO_NINETEEN = r"""
                                (?:
                                    [Zz][Ee][Rr][Oo]\ |[Oo][Nn][Ee]\ |[Tt][Ww][Oo]\ |
                                    [Tt][Hh][Rr][Ee][Ee]\ |[Ff][Oo][Uu][Rr]\ |
                                    [Ff][Ii][Vv][Ee]\ |[Ss][Ii][Xx]\ |
                                    [Ss][Ee][Vv][Ee][Nn]\ |[Ee][Ii][Gg][Hh][Tt]\ |
                                    [Nn][Ii][Nn][Ee]\ |[Tt][Ee][Nn]\ |
                                    [Ee][Ll][Ee][Vv][Ee][Nn]\ |
                                    [Tt][Ww][Ee][Ll][Vv][Ee]\ |
                                    [Tt][Hh][Ii][Rr][Tt][Ee][Ee][Nn]\ |
                                    [Ff][Oo][Uu][Rr][Tt][Ee][Ee][Nn]\ |
                                    [Ff][Ii][Ff][Tt][Ee][Ee][Nn]\ |
                                    [Ss][Ii][Xx][Tt][Ee][Ee][Nn]\ |
                                    [Ss][Ee][Vv][Ee][Nn][Tt][Ee][Ee][Nn]\ |
                                    [Ee][Ii][Gg][Hh][Tt][Ee][Ee][Nn]\ |
                                    [Nn][Ii][Nn][Ee][Tt][Ee][Ee][Nn]\ 
                                )
"""

# Numerals - 10, 20, 30 ... 90
REGEX_EN_TEN_TO_NINETY = r"""
                                (?:
                                    [Tt][Ee][Nn]\ |[Tt][Ww][Ee][Nn][Tt][Yy]\ |
                                    [Tt][Hh][Ii][Rr][Tt][Yy]\ |
                                    [Ff][Oo][Rr][Tt][Yy]\ |
                                    [Ff][Oo][Uu][Rr][Tt][Yy]\ |
                                    [Ff][Ii][Ff][Tt][Yy]\ |[Ss][Ii][Xx][Tt][Yy]\ |
                                    [Ss][Ee][Vv][Ee][Nn][Tt][Yy]\ |
                                    [Ee][Ii][Gg][Hh][Tt][Yy]\ |
                                    [Nn][Ii][Nn][Ee][Tt][Yy]\ 
                                )
"""

# One hundred
REGEX_EN_HUNDRED = r"""
                                (?:
                                    [Hh][Uu][Nn][Dd][Rr][Ee][Dd]\ 
                                )
"""

# One thousand
REGEX_EN_THOUSAND = r"""
                                (?:
                                    [Tt][Hh][Oo][Uu][Ss][Aa][Nn][Dd]\ 
                                )
"""

REGEX_EN_NAME_STANDARD_W_LOOKAROUND = r"""
(?P<name_standard_w_lookaround>
    (?: (?<! [A-ZÄÖÜa-zäöüß] ) )

    [A-ZÄÖÜ][a-zäöüß]+
    (
        [ ]{0,5} (-|\\|/|\.)? [ ]{0,5}
        [A-ZÄÖÜ][a-zäöüß]+
    ){0,3}

    (?: (?! [A-ZÄÖÜa-zäöüß] ) )
)
"""

REGEX_EN_NAME_STANDARD_WO_LOOKAROUND = r"""
(?P<name_standard_wo_lookaround>
    [A-ZÄÖÜ][a-zäöüß]+
    (
        [ ]{0,5} (-|\\|/|\.)? [ ]{0,5}
        [A-ZÄÖÜ][a-zäöüß]+
    ){0,3}
)
"""

REGEX_EN_NAME_W_NUMBERS_W_LOOKAROUND = r"""
(?P<name_w_numbers_w_lookaround>
    (?: (?<! [A-ZÄÖÜa-zäöüß0-9] ) )

    [A-ZÄÖÜ0-9][a-zäöüß0-9]+
    (
        [ ]{0,5} (-|\\|/|\.)? [ ]{0,5}
        [A-ZÄÖÜ0-9][a-zäöüß0-9]+
    ){0,3}

    (?: (?! [A-ZÄÖÜa-zäöüß0-9] ) )
)
"""

REGEX_EN_NAME_W_NUMBERS_WO_LOOKAROUND = r"""
(?P<name_w_numbers_wo_lookaround>
    [A-ZÄÖÜ0-9][a-zäöüß0-9]+
    (
        [ ]{0,5} (-|\\|/|\.)? [ ]{0,5}
        [A-ZÄÖÜ0-9][a-zäöüß0-9]+
    ){0,3}
)
"""

REGEX_PART_DIVIDER = r"""
(
    (
        ( [^\d\n\r] {1,5} (\r\n|\r|\n)? )
        |
        (\r\n|\r|\n) 
    )
)
"""

REGEX_PART_DIVIDER_CITY = r"""
(
    (
        ( [^\d\n\r] {1,20} (\r\n|\r|\n)? ) 
        |
        (\r\n|\r|\n)
    )
)
"""

REGEX_SPACE_PATTERN = r"""
(
    [ ] {1,5}
)
"""

"""
Regexp for matching street number.
Street number can be written 2 ways:
1) Using letters - "One thousand twenty two"
2) Using numbers
   a) - "1022"
   b) - "85-1190"
   c) - "85 1190"
"""
REGEX_GB_STREET_NUMBER = r"""
                    (?P<street_number>
                        (?:
                            (?:
                                [Nn][Uu][Mm][Bb][Ee][Rr]|
                                [Nn][RrOo]\.?|
                                [Nn][Uu][Mm]\.?
                            )
                            {space}?
                        )?
                        (?:
                            (?:
                                [Aa][Nn][Dd]\ 
                                |
                                {thousand}
                                |
                                {hundred}
                                |
                                {zero_to_nineteen}
                                |
                                {ten_to_ninety}
                            ){from_to}
                            |
                            (?:
                                \d{from_to} 
                                (?: {space}? [A-Za-z] (?![A-Za-z\d]]) )? 
                                (?!\d)
                                (?:{space}?\-{space}?\d{from_to} (?: {space}? [A-Za-z] (?![A-Za-z\d]) )? )?
                            )
                        )
                        {space}?
                    )  # end street_number
""".format(
    thousand=REGEX_EN_THOUSAND,
    hundred=REGEX_EN_HUNDRED,
    zero_to_nineteen=REGEX_EN_ZERO_TO_NINETEEN,
    ten_to_ninety=REGEX_EN_TEN_TO_NINETY,
    space=REGEX_SPACE_PATTERN,
    from_to="{1,5}",
)

REGEX_GB_POST_DIRECTION = r"""
                    (?P<post_direction>
                        (?:
                            [Nn][Oo][Rr][Tt][Hh]\ |
                            [Ss][Oo][Uu][Tt][Hh]\ |
                            [Ee][Aa][Ss][Tt]\ |
                            [Ww][Ee][Ss][Tt]\ 
                        )
                        |
                        (?:
                            NW\ |NE\ |SW\ |SE\ 
                        )
                        |
                        (?:
                            N\.?\ |S\.?\ |E\.?\ |W\.?\ 
                        )
                    )  # end post_direction
"""

# Regexp for matching street type
REGEX_GB_STREET_TYPE = r"""
                    (?:
                        (?P<street_type>
                            # Street
                            [Ss][Tt][Rr][Ee][Ee][Tt]|S[Tt]\.?|
                            # Boulevard
                            [Bb][Oo][Uu][Ll][Ee][Vv][Aa][Rr][Dd]|[Bb][Ll][Vv][Dd]\.?|
                            # Highway
                            [Hh][Ii][Gg][Hh][Ww][Aa][Yy]|H[Ww][Yy]\.?|
                            # Broadway
                            [Bb][Rr][Oo][Aa][Dd][Ww][Aa][Yy]|
                            # Freeway
                            [Ff][Rr][Ee][Ee][Ww][Aa][Yy]|
                            # Causeway
                            [Cc][Aa][Uu][Ss][Ee][Ww][Aa][Yy]|C[Ss][Ww][Yy]\.?|
                            # Expressway
                            [Ee][Xx][Pp][Rr][Ee][Ss][Ss][Ww][Aa][Yy]|
                            # Way
                            [Ww][Aa][Yy]|
                            # Walk
                            [Ww][Aa][Ll][Kk]|
                            # Lane
                            [Ll][Aa][Nn][Ee]|L[Nn]\.?|
                            # Road
                            [Rr][Oo][Aa][Dd]|R[Dd]\.?|
                            # Avenue
                            [Aa][Vv][Ee][Nn][Uu][Ee]|A[Vv][Ee]\.?|
                            # Circle
                            [Cc][Ii][Rr][Cc][Ll][Ee]|C[Ii][Rr]\.?|
                            # Cove
                            [Cc][Oo][Vv][Ee]|C[Vv]\.?|
                            # Drive
                            [Dd][Rr][Ii][Vv][Ee]|D[Rr]\.?|
                            # Parkway
                            [Pp][Aa][Rr][Kk][Ww][Aa][Yy]|P[Kk][Ww][Yy]\.?|
                            # Park
                            [Pp][Aa][Rr][Kk]|
                            # Court
                            [Cc][Oo][Uu][Rr][Tt]|C[Tt]\.?|
                            # Square
                            [Ss][Qq][Uu][Aa][Rr][Ee]|S[Qq]\.?|
                            # Loop
                            [Ll][Oo][Oo][Pp]|L[Pp]\.?|
                            # Place
                            [Pp][Ll][Aa][Cc][Ee]|P[Ll]\.?|
                            # Parade
                            [Pp][Aa][Rr][Aa][Dd][Ee]|P[Ll]\.?|
                            # Estate
                            [Ee][Ss][Tt][Aa][Tt][Ee]|
                            # Mundells
                            [Mm]undells
                        )
                        (?![A-Za-z])
                    )  # end street_type
"""

"""
Regexp for matching street name.
In "Hoover Boulevard", "Hoover" is a street name
Seems like the longest US street is 'Northeast Kentucky Industrial Parkway' - 31 charactors
https://atkinsbookshelf.wordpress.com/tag/longest-street-name-in-us/
"""
REGEX_GB_STANDARD_STREET = r"""
(?P<standard_street>
    {name_standard_wo_lookaround}
    [ ]?
    {street_type}
)
""".format(
    name_standard_wo_lookaround=REGEX_EN_NAME_STANDARD_WO_LOOKAROUND,
    street_type=REGEX_GB_STREET_TYPE,
)

REGEX_GB_FLOOR = r"""
                    (?P<floor>
                        (?:
                        \d+[A-Za-z]{0,2}\.?\ [Ff][Ll][Oo][Oo][Rr]\ 
                        )
                        |
                        (?:
                            [Ff][Ll][Oo][Oo][Rr]\ \d+[A-Za-z]{0,2}\ 
                        )
                    )  # end floor
"""

REGEX_GB_BUILDING = r"""
                    (?P<building_id>
                        (?:
                            (?:[Bb][Uu][Ii][Ll][Dd][Ii][Nn][Gg])
                            |
                            (?:[Bb][Ll][Dd][Gg])
                        )
                        \ 
                        (?:
                            (?:
                                [Aa][Nn][Dd]\ 
                                |
                                {thousand}
                                |
                                {hundred}
                                |
                                {zero_to_nineteen}
                                |
                                {ten_to_ninety}
                            ){{1,5}}
                            |
                            \d{{0,4}}[A-Za-z]?
                        )
                        \ ?
                    )  # end building_id
""".format(
    thousand=REGEX_EN_THOUSAND,
    hundred=REGEX_EN_HUNDRED,
    zero_to_nineteen=REGEX_EN_ZERO_TO_NINETEEN,
    ten_to_ninety=REGEX_EN_TEN_TO_NINETY,
)

REGEX_GB_OCCUPANCY = r"""
                    (?P<occupancy>
                        (?:
                            (?:
                                # Suite
                                [Ss][Uu][Ii][Tt][Ee]|[Ss][Tt][Ee]\.?
                                |
                                # Studio
                                [Ss][Tt][Uu][Dd][Ii][Oo]|[Ss][Tt][UuDd]\.?
                                |
                                # Apartment
                                [Aa][Pp][Tt]\.?|[Aa][Pp][Aa][Rr][Tt][Mm][Ee][Nn][Tt]
                                |
                                # Room
                                [Rr][Oo][Oo][Mm]|[Rr][Mm]\.?
                                |
                                # Flat
                                [Ff][Ll][Aa][Tt]
                                |
                                \#
                            )
                            {space}?
                            (?:
                                [A-Za-z\#\&\-\d]{{1,7}}
                            )?
                        )
                        {space}?
                    )  # end occupancy
""".format(
    space=REGEX_SPACE_PATTERN,
)

REGEX_GB_PO_BOX = r"""
                    (?:
                        [Pp]\.? {space}? [Oo]\.? {space}? ([Bb][Oo][Xx]{space}?)?\d+
                    )
""".format(
    space=REGEX_SPACE_PATTERN,
)

REGEX_GB_FULL_STREET = r"""
        (?:
            (?P<full_street>
                (?:
                    {po_box} {part_divider}
                )?
                (?:
                    {floor} {part_divider}
                )?
                (?:
                    {occupancy} {part_divider}
                )?
                (?:
                    {building} {part_divider}
                )?
                (?:
                    (?: {street_number} {space} )
                    #|             # uncomment to make street number optionally
                    #(?! \d{{}} )  # uncomment to make street number optionally
                )
                {standard_street}
            )
        )  # end full_street
""".format(
    street_number=REGEX_GB_STREET_NUMBER,
    standard_street=REGEX_GB_STANDARD_STREET,
    post_direction=REGEX_GB_POST_DIRECTION,
    floor=REGEX_GB_FLOOR,
    building=REGEX_GB_BUILDING,
    occupancy=REGEX_GB_OCCUPANCY,
    po_box=REGEX_GB_PO_BOX,
    part_divider=REGEX_PART_DIVIDER,
    space=REGEX_SPACE_PATTERN,
)

# region1 is actually a "state"
REGEX_GB_REGION1 = REGEX_EN_NAME_STANDARD_W_LOOKAROUND

REGEX_GB_CITY = REGEX_EN_NAME_STANDARD_W_LOOKAROUND

REGEX_GB_POSTAL_CODE = r"""
        (?P<postal_code>
            (?:
                (?:[gG][iI][rR] {0,}0[aA]{2})|
                (?:
                    (?:
                        [aA][sS][cC][nN]|
                        [sS][tT][hH][lL]|
                        [tT][dD][cC][uU]|
                        [bB][bB][nN][dD]|
                        [bB][iI][qQ][qQ]|
                        [fF][iI][qQ][qQ]|
                        [pP][cC][rR][nN]|
                        [sS][iI][qQ][qQ]|
                        [iT][kK][cC][aA]
                    )
                    \ {0,}1[zZ]{2}
                )|
                (?:
                    (?:
                        (?:[a-pr-uwyzA-PR-UWYZ][a-hk-yxA-HK-XY]?[0-9][0-9]?)|
                        (?:
                            (?:[a-pr-uwyzA-PR-UWYZ][0-9][a-hjkstuwA-HJKSTUW])|
                            (?:[a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y][0-9][abehmnprv-yABEHMNPRV-Y])
                        )
                    )
                    \ {0,}[0-9][abd-hjlnp-uw-zABD-HJLNP-UW-Z]{2}
                )
            )
        )  # end postal_code
"""

REGEX_GB_COUNTRY = r"""
        (?<![A-ZÄÖÜa-zäöüß])
        (?P<country>
            (?:[Tt][Hh][Ee][ ]?)?[Uu][Nn][Ii][Tt][Ee][Dd][ ]?[Kk][Ii][Nn][Gg][Dd][Oo][Mm][ ]?[Oo][Ff][ ]?(?:[Gg][Rr][Ee][Aa][Tt][ ]?)?[Bb][Rr][Ii][Tt][Aa][Ii][Nn](?:[ ]?[Aa][Nn][Dd][ ]?[Nn][Oo][Rr][Tt][Hh][Ee][Rr][Nn][ ]?[Ii][Rr][Ee][Ll][Aa][Nn][Dd])?|
            (?:[Gg][Rr][Ee][Aa][Tt][ ]?)?[Bb][Rr][Ii][Tt][Aa][Ii][Nn](?:[ ]?[Aa][Nn][Dd][ ]?[Nn][Oo][Rr][Tt][Hh][Ee][Rr][Nn][ ]?[Ii][Rr][Ee][Ll][Aa][Nn][Dd])?|
            (?:[Tt][Hh][Ee][ ]?)?[Uu][Nn][Ii][Tt][Ee][Dd][ ]?[Kk][Ii][Nn][Gg][Dd][Oo][Mm]|
            (?:[Nn][Oo][Rr][Tt][Hh][Ee][Rr][Nn][ ]?)?[Ii][Rr][Ee][Ll][Aa][Nn][Dd]|
            [Ee][Nn][Gg][Ll][Aa][Nn][Dd]|
            [Ss][Cc][Oo][Tt][Ll][Aa][Nn][Dd]|
            [Ww][Aa][Ll][Ee][Ss]|
            [Cc][Yy][Mm][Rr][Uu]|
            [Gg][Bb]|
            [Uu][Kk]|  
            [Nn]\.?[ ]?[Ii]\.?
        )  # end country
        (?![A-ZÄÖÜa-zäöüß])
"""

REGEX_GB_ADDRESS_STANDARD = r"""
(?P<address_standard>
    {full_street} 

    (?P<city> {part_divider_city} {city} )?

    (?: {part_divider} {region1} )?

    (?(street_type) # conditional on street type (currently without effect since street type is mandatory)
        (?(city) # conditional on city
            (?: {part_divider} {postal_code} )? |
            (?: {part_divider} {postal_code} )
        ) |     
        (?: {part_divider} {postal_code} )
    )

    (?: {part_divider} {country} )?
)  # end full_address
""".format(
    full_street=REGEX_GB_FULL_STREET,
    part_divider=REGEX_PART_DIVIDER,
    part_divider_city=REGEX_PART_DIVIDER_CITY,
    city=REGEX_GB_CITY,
    region1=REGEX_GB_REGION1,
    country=REGEX_GB_COUNTRY,
    postal_code=REGEX_GB_POSTAL_CODE,
)


REGEX_EN_FORM_VALUE_SIGNAL = r"""
(
    [ ]{0,5} \: [ ]{0,5}
)
"""

REGEX_EN_FORM_VALUE = r"""
(
    [^\:] {0,20}
)
"""

REGEX_GB_ADDRESS_FORM = r"""
(?P<address_form>
    (?: ([Ss][Tt][Rr][Ee][Ee][Tt]) {form_value_signal} ( {value} | ) {part_divider} )
    (?: ([Nn][Uu][Mm][Bb][Ee][Rr]) {form_value_signal} ( {value} | ) {part_divider} )
    (?: (Additional\ information) {form_value_signal} ( {value} | ) {part_divider} )
    (?: (PO\ Box) {form_value_signal} ( {value} | ) {part_divider} )
    (?: ([Cc][Oo][Uu][Nn][Tt][Rr][Yy]) {form_value_signal} ( {value} | ) {part_divider} )
    (?: ([Pp][Oo][Ss][Tt][Aa][Ll]\ [Cc][Oo][Dd][Ee]) {form_value_signal} ( {value} | ) {part_divider} )
    (?: ([Ss][Tt][Aa][Tt][Ee]) {form_value_signal} ( {value} | ) {part_divider} )
    (?: ([Cc][Ii][Tt][Yy]) {form_value_signal} ( {value} | ) )
)
""".format(
    form_value_signal=REGEX_EN_FORM_VALUE_SIGNAL,
    value=REGEX_EN_FORM_VALUE,
    part_divider=REGEX_PART_DIVIDER,
)

REGEX_GB_ADDRESS = r"""
(?x)
(?P<address>
    {address_standard} |
    {address_form}
)
""".format(
    address_standard=REGEX_GB_ADDRESS_STANDARD, address_form=REGEX_GB_ADDRESS_FORM
)
