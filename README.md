# Usage

    >>> Gs_minor.triads
    [GsMin, AsDim, BMaj, CsMin, DsMin, EMaj, FsMaj]
    >>> GsMin + m7
    GsMin7
    >>> GsMin7 in Gs_minor
    True
    >>> print GsMin7.inverted(2)
      #   #     #   #   #     #   #     #   #   #     #   #     #   #   #   
      #   #     #   #   #     #   #     #   #   #     #   #     #   #   #   
      |   |     |   |   |     |   |     |   |   |     |   |     |   |   |   
    c | d | e f | g | a | b c | d | e f | g | a | b c | d | e f | g | a | b 
                                  x     x   x     x
