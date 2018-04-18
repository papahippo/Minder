"""
module 'style' is a functional implementation of what might otherwise be achieved by
a style sheet (.css file).
"""
def Style():
    """
Style just returns a fixed set of styles; just enough styling to make data readable and
to make tables look like tables etc.
    """
    return ("""
td {
    border: 1px solid black;
    color: black;
    text-align: center;
    font-family: verdana;
    font-size: 12px;
}
th.input {
    background-color: #4C40CF;
    color: white;
    text-align: center;
    font-family: verdana;
    font-size: 12px;
}
th.output {
    background-color: #4CAF50;
    color: white;
    text-align: center;
    font-family: verdana;
    font-size: 12px;
}
    """)

