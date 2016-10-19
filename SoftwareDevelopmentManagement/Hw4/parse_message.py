"""
Syntax of messages.

<message>   ::=  <refmsg> <newline>  |  <playermsg> <newline>

<refmsg>    ::=  <colormsg>
            ::=  <move>
            ::=  <offerdraw>
            ::=  <declinedraw>
            ::=  <win>
            ::=  <lose>
            ::=  <draw>
            ::=  <badsyntax>
            ::=  <badmove>

<playermsg> ::=  <move>
            ::=  <offerdraw>
            ::=  <acceptdraw>
            ::=  <declinedraw>
            ::=  <surrender>

<colormsg>  ::=  "you are " <player>

<move>      ::=  <player> " moves " <piece> " from " <aposn> " to " <posn>

<offerdraw>     ::=  <player> " offers draw"
<acceptdraw>    ::=  <player> " accepts draw"
<declinedraw>   ::=  <player> " declines draw"
<surrender>     ::=  <player> " surrenders"

<win>           ::=  <player> " wins by reason of " <reason>
<lose>          ::=  <player> " loses by reason of " <reason>
<draw>          ::=  "the game is drawn"

<badsyntax>     ::=  "bad syntax"
<badmove>       ::=  "bad move"

<player>    ::=  "white"  |  "black"
<piece>     ::=  "K"  |  "Q"  |  "R"  |  "B"  | "N"  |  "P"
<aposn>     ::=  <board> " " <posn>
<board>     ::=  1  |  2
<posn>      ::=  <column> <row>



"""
import re






def reason_legal(ms):
    """
    <reason>    ::=  "checkmate"  |  "surrender"  |  "forfeit"
    :param message:
    :return: boolean
    """

    pat = "^(checkmate$|surrender$|forfeit)$"
    reg = re.compile(pat)
    if reg.match(ms): return True

    return False

#test
# print reason_legal("checkmate")
# print reason_legal("surrender")
# print reason_legal("forfeit")
# print reason_legal("Checkmate")
# print reason_legal("surrenderee")
# print reason_legal(" checkmate ")






def pos_legal(ms):
    """
        <column>    ::=  "a"  |  "b"  |  "c"  |  "d"  |  "e"  |  "f"  |  "g"  |  "h"
        :param message:
        :return: boolean
    """

    col_p = "^[a-h]$"

    col_r = re.compile(col_p)
    if col_r.match(ms): return True
    return False


def row_legal(ms):
    """
    <row>       ::=  "1"  |  "2"  |  "3"  |  "4"  |  "5"  |  "6"  |  "7"  |  "8"
    :param ms: string
    :return: boolean
    """

    p_row ="^[1-9]$"
    reg=re.compile(p_row)
    if reg.match(ms): return True

    return False

#test
# print row_legal("1")
# print row_legal("3")
# print row_legal("5")
# print row_legal("9")
# print row_legal("0")
# print row_legal("abc")
# print row_legal('21')
# print row_legal(" 1 ")

