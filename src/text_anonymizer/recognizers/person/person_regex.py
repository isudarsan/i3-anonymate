#################
# regex for all languages
#################

REGEX_NAME_WORD = r"""
(?P<name>
    (?P<initials>[A-ZÀ-ÝÑ][a-zà-ÿßñ]?\.)|
    (?P<standard_name>[A-ZÀ-ÝÑÄÖÜ][a-zà-ÿßñäöü]+)(?![a-zA-Z])|
    (?P<apostrophe_name>[A-ZÀ-ÝÑ][‘`´'][A-ZÀ-Ý][a-zà-ÿßñ]+)(?![a-zA-Z])
    #|
    # upper case name word; leave commented or FPs grow because of regex for greeting and goodbye phrases.
    #(?P<uppercase_name>[A-ZÄÖÜß]+)
    #|
    # lower case name word; leave commented or <<der>> in "Assistent <<der>> Geschäftsleitung" is recognized
    #(?P<lowercase_name>[a-zäöüß]+) 
)
"""

REGEX_NAME_WORD_W_LOWERCASE = r"""
(?P<name>
    (?P<initials>[A-ZÀ-ÝÑ][a-zà-ÿßñ]?\.)|
    (?P<standard_name>[A-ZÀ-ÝÑÄÖÜ][a-zà-ÿßñäöü]+)(?![a-zA-Z])|
    (?P<apostrophe_name>[A-ZÀ-ÝÑ][‘`´'][A-ZÀ-ÝÑ][a-zà-ÿßñ]+)(?![a-zA-Z])|
    (?P<lowercase_name>[a-zà-ÿßñ]+)(?![a-zA-Z])
)
"""

REGEX_NAME_WORD_W_UPPERCASE = r"""
(?P<name>
    (?P<initials>[A-ZÀ-Ý][a-zà-ÿßñ]?\.)|
    (?P<standard_name>[A-ZÀ-ÝÑ][a-zà-ÿßñ]+)(?![a-zA-Z])|
    (?P<apostrophe_name>[A-ZÀ-ÝÑ][‘`´'][A-ZÀ-ÝÑ][a-zà-ÿßñ]+)(?![a-zA-Z])|
    (?P<uppercase_name>[A-ZÀ-ÝÑ]+)(?![a-zA-Z])
)
"""

REGEX_FULL_NAME = r"""
(?P<full_name>
    {name_word}
    (?P<optional_part>
        (?P<optional_nobiliary_particle>
            (?P<sep_before_particle>[ ]) {{1,5}}
            (?P<particle>
                [Vv][Oo][Nn]|
                [Zz][Uu]
            )
        )?
        (?P<more_names>
            ([ ] {{1,5}} | [ ] {{0,5}} \- [ ] {{0,5}})
            {name_word}
        ){{1,2}}
    )?
)
""".format(
    name_word=REGEX_NAME_WORD
)

REGEX_FULL_NAME_W_UPPERCASE = r"""
(?P<full_name_w_uppercase>
    {name_word_w_uppercase}
    (?P<optional_part>
        (?P<optional_nobiliary_particle>
            (?P<sep_before_particle>[ ]) {{1,5}}
            (?P<particle>
                [Vv][Oo][Nn]|
                [Zz][Uu]
            )
        )?
        (?P<more_names>
            ([ ] {{1,5}} | [ ] {{0,5}} \- [ ] {{0,5}} | (\.))
            {name_word_w_uppercase}
        ){{1,2}}
    )?
)
""".format(
    name_word_w_uppercase=REGEX_NAME_WORD_W_UPPERCASE
)

REGEX_COMMA_SEPARATED_NAME = r"""
(?P<comma_separated_name>
    (?P<optional_nobiliary_particle>
        (?P<particle>
            [Vv][Oo][Nn]|
            [Zz][Uu]
        )
    )?
    (?P<last_names>
        (?P<seperator>[\- ]){{0,5}}
        {name_word}
    ){{1,4}}
    (?P<optional_first_name_part>
        (?P<comma>
            [ ]{{0,5}},[ ]{{0,5}}
        )
        {name_word}
    )?
)    
""".format(
    name_word=REGEX_NAME_WORD
)

#################
# LANGUAGE_CODE_DE
#################

REGEX_DE_TITLED_PERSON = r"""
(?x)
(?:
    (?<! [A-ZÀ-Ýa-zà-ÿß] )
    (?:
        (?: 
            H[Rr]?\.|
            H[Ee][Rr][Rr][Nn]?|
            F[Rr]\.|
            F[Rr][Aa][Uu]|
            P[Rr][Oo][Ff](\.)?([Ee][Ss][Ss][Oo][Rr])?|
            D[Oo][Kk][Tt][Oo][Rr]|
            D[Rr](\.)?
        )
        [ ] {{1,5}}
    ) {{1,5}}
    {full_name_w_uppercase}
)
""".format(
    full_name_w_uppercase=REGEX_FULL_NAME_W_UPPERCASE
)

REGEX_DE_GREETED_PERSON = r"""
(?x)
(?<=
    (?:
        # uncomment if needed
        #(?:[Gg][Uu][Tt][Ee][Nn][ ][Tt][Aa][Gg])
        (?:[Gg][Uu][Tt][Ee][Nn][ ][Mm][Oo][Rr][Gg][Ee][Nn])
        |
        (?:[Gg][Rr](ue|[Üü])(ß|[Ss]{{1,2}})[ ][Gg][Oo][Tt]{{1,2}})

        # Uncomment if needed.
        #|
        #(?:[Hh][Aa][Ll]{{1,2}}[Oo])
    )
    (?:[ ] {{1,5}} )
)
{full_name}
""".format(
    full_name=REGEX_FULL_NAME
)


REGEX_DE_GOODBYE_PERSON = r"""
(?x)
(?<=
    (?:
        ([Gg][Rr]([UuÜü]|(ue))(ß|[Ss]{{1,2}})([Ee][Nn]?|[Tt])?)| # can't end with "Gott" (Grüß Gott)
        [Mm]\.?[Ff]\.?[Gg]\.?|
        [Rr][Ee][Gg][Aa][Rr][Dd][Ss]|
        [VvBbLlFf][Gg]|
        [Bb][Ee][Ss][Tt][Ee][Nn] [ ] {{1,5}} [Dd][Aa][Nn][Kk]|
        [Cc][Oo][Rr][Dd][Ii][Aa][Ll][Ee][Mm][Ee][Nn][Tt]
    )
    (?:[,])?
    (?: ( [^\S\n\r] {{1,5}} ) | ( [ ] {{0,5}} (\r\n|\r|\n) ) )
    # [^\S\n\r] -> a single whitespace but a line break
    # (\r\n|\r|\n) -> a single line break regardless of platform)
)
{full_name_w_uppercase}
""".format(
    full_name_w_uppercase=REGEX_FULL_NAME_W_UPPERCASE
)

# Regex that matches the first person after a person indicator in an email form.
# Multiple succeeding persons are not matched (as you would expect in emails (Cc: person1 .. person2 .. ..).
# An attempt to match multiple succeeding persons was made but commented below.
# The downside is lower precision for PERSON and lower recall for other entities like EMAIL, because the regex matches anything between person names.
REGEX_DE_FORM_EMAIL_PERSON = r"""
(?x)
(?<=
    (?:
        [Vv][Oo][Nn]:|
        From:|
        To:|
        An:|
        Cc:|
        Bcc:
    )
    (?: ( [^\d\n\r] {{0,5}} (\r\n|\r|\n)? )? )
)
(
    {comma_separated_name}|
    {full_name}
)
#(
#    ( .{{0,30}}? < .{{1,30}}? @ .{{1,30}}? > .{{0,10}}? )
#    ( \; )
#    ( ( [^\d\n\r] {{0,5}} (\r\n|\r|\n)? )? )
#    (
#        comma_separated_name|
#        full_name
#    )
#){{0,5}}
""".format(
    comma_separated_name=REGEX_COMMA_SEPARATED_NAME, full_name=REGEX_FULL_NAME
)

# Regex that matches persons after a person indicator in a form.
REGEX_DE_FORM_GENERAL_PERSON = r"""
(?x)
(?<=
    (?:
        firstname:|
        lastname:|
        z.H.|z.H|zH|
        i.A.|
        Ansprechpartner:|
        Geschäftsführer:|
        Bearbeiter:
    )
    (?: ( [^\d\n\r] {{0,5}} (\r\n|\r|\n)? )? )
)
(
    {full_name_w_uppercase}
)
(
    (?P<comma> [ ]{{0,5}},[ ]{{0,5}})
    (
        {full_name_w_uppercase}
    )
){{0,3}}
""".format(
    full_name_w_uppercase=REGEX_FULL_NAME_W_UPPERCASE
)

#################
# LANGUAGE_CODE_EN
#################

REGEX_EN_GOODBYE_PERSON = r"""
(?x)
(?<=
    (?:
        [Tt][Hh][Aa][Nn][Kk][Ss]|
        [Rr][Ee][Gg][Aa][Rr][Dd][Ss]|
        [Cc][Hh][Ee][Ee][Rr][Ss]
    )
    (?:[,])?
    (?: ( [^\S\n\r] {{1,5}} ) | ( [ ] {{0,5}} (\r\n|\r|\n) ) )
    # [^\S\n\r] -> a single whitespace but a line break
    # (\r\n|\r|\n) -> a single line break regardless of platform)
)
(
    {full_name}|
    {name_word_w_lowercase}
)
""".format(
    full_name=REGEX_FULL_NAME, name_word_w_lowercase=REGEX_NAME_WORD_W_LOWERCASE
)

REGEX_EN_TITLED_PERSON = r"""
(?x)
(?:
    (?<! [A-ZÀ-Ýa-zà-ÿß] )
    (?:
        (?:
            M[Rr][Ss]?(\.)?|
            M[Ss](\.)?|
            M[Ii][Ss][Ss](\.)?|
            P[Rr][Oo][Ff](\.)?([Ee][Ss][Ss][Oo][Rr])?|
            D[Oo][Kk][Tt][Oo][Rr]|
            D[Rr](\.)?
        )
        [ ] {{1,5}}
    ) {{1,5}}
    {full_name_w_uppercase}
)
""".format(
    full_name_w_uppercase=REGEX_FULL_NAME_W_UPPERCASE
)

#################
# LANGUAGE_CODE_ES
#################

REGEX_ES_GREETED_PERSON = r"""
(?x)
(?<=
    (?:
        (?:
            [D][i][s][t][i][n][g][u][i][d][o]|
            [D][i][s][t][i][n][g][u][i][d][a]|
            [H][o][l][a]|
            [E][s][t][i][m][a][d][o]|
            [E][s][t][i][m][a][d][a]
        )
    )
    (?:[ ]) {{1,5}}
)
{full_name}
""".format(
    full_name=REGEX_FULL_NAME
)

REGEX_ES_GOODBYE_PERSON = r"""
(?x)
(?<=
    (?:
        [A][t][e][n][t][a][m][e][n][t][e]|
        [Cc][o][r][d][i][a][l][e][s]|
        [C][o][r][d][i][a][l][m][e][n][t][e]|
        [Rr][Ee][Cc][Uu][Er][Rr][Dd][Oo][Ss]|
        [Rr][Ee][Gg][Aa][Rr][Dd][Ss]|
        [Ss][Aa][Ll][Uu][Dd][Oo]([Ss])?
    )
    (?:[,])?
    (?: ( [^\S\n\r] {{1,5}} ) | ( [ ] {{0,5}} (\r\n|\r|\n) ) )
    # [^\S\n\r] -> a single whitespace but a line break
    # (\r\n|\r|\n) -> a single line break regardless of platform)
)
{full_name_w_uppercase}
""".format(
    full_name_w_uppercase=REGEX_FULL_NAME_W_UPPERCASE
)

REGEX_ES_TITLED_PERSON = r"""
(?x)
(?:
    (?<! [A-ZÀ-Ýa-zà-ÿß] )
    (?:
        (?: 
            [S][Ee][Ññ][Oo][Rr]([Aa])?|
            [S][Rr](\.)?|
            [S][Rr][Ee][Ss](\.)?|
            [S][Rr][Aa](\.)?|
            [S][Rr][Aa][Ss](\.)?|
            [D][Oo][Nn]|
            [D][Oo][Ññ][Aa]
        )
        [ ] {{1,5}}
    ) {{1,5}}
    {full_name_w_uppercase}
)
""".format(
    full_name_w_uppercase=REGEX_FULL_NAME_W_UPPERCASE
)
