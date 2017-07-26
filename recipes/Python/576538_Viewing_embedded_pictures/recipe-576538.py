'''Function allowing to view docstrings with embedded
images.  The images are encoded in base 64.

(c) 2008 Andre Roberge
License: MIT License
'''

import os
import re
import sys
import webbrowser

html_template = "<html><head></head><body><pre>%s</pre></body></html>"

def view(obj):
    """
    Allows viewing docstring with embedded images.

    To see a normal docstring, use help(object).
    To see a docstring with embedded images, use docpicture.view(object).
    It is assumed that the images are included (encoded in base 64) in
    your Python module.

    The result will be an html file displayed in your default browser,
    with the images inserted.

    For example: docpicture = python_powered_w.png

    Limitation: the filename must be a valid Python identifier.
    Note that this works with gif images  docpicture=python_g.gif

    as well as jpeg images docpicture = python_j.jpg

    All that is required is for the filename (without the extension) be a
    unique value.  Note that the same image can appear twice.

    docpicture = python_powered_w.png
    """
    source_module = sys.modules[obj.__module__]

    docpicture_pattern = re.compile("\s*(docpicture\s*=\s*.+?)\s")
    image_name_pattern = re.compile("\s*docpicture\s*=\s*(.+?)\s")

    docstring = obj.__doc__
    image_filename = image_name_pattern.search(obj.__doc__)
    while image_filename is not None:
        filename = image_filename.groups()[0]
        base_name, ext = filename.split('.')
        image = getattr(source_module, base_name).decode("base64")

        image_file = open(filename, "wb")
        image_file.write(image)
        image_file.close()
        docstring = docpicture_pattern.sub("</pre><img src=%s><pre>" % filename,
                                    docstring, count=1)
        image_filename = image_name_pattern.search(docstring)

    html_file = open("test.html", 'w')
    html_file.write(html_template % docstring)
    html_file.close()
    url = os.path.join(os.getcwd(), "test.html")
    webbrowser.open(url)

python_powered_w = """\
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
AElFTkSuQmCC

"""

python_g = """\
R0lGODlhMgAtAPcAAAAAADdqlDdrljdrmDZsmDZtmzZtnDZunDZvnzxtljZwoDdxojdypDdzpjd0
pjd1qDd1qjd2qTd2qjd2rDd4rTd4rjpzpTt1pjx3pzl3qzp4qzl4rTh5rz14qzd5sDd6sDp7sTh7
sjh7tDh8tDh8tjp+tjh+uDh/ukd7pkd/rVB8oDiAujiAvDuDvTiCvjyAuT2EvjiDwDqFwTiFwkuA
rUKCt0ODuECFvUOGvUeJvkmJvk2Ju1+IqV+KrlGItVCLu1eMuFuLtFyOuGCHqGCOtW2Zv3CUsnGa
vXGbvnWdvkGJw0eKwEqNw06OwWecym6dxG6fyXegw3CjzHulx3ijyHilyXqpz32oy3+s0/+2Iv+5
J/+7KP64Lf+8Kf68Kv++K/68Lf65NPy9Mf29NP/ALf/BLv/CL/3BMv7DNP/EMf/FMv/GNP7GN//B
Pf/GOP/INf/JN/7IOv/KOP/LOv7LPf/MO//MPP7NPv/OPf/PPv/QP/vCRP/DQv/HQfrBTP/MTP/G
U/zLV//NU//OVP/QQP7QQv/SQf/SQv7SRf/UQ//URP/WRf/XRv/YSP7YSv/aSv/aTP/cTf/dTv/e
T/vTUf/RV/zWUv/UWf/UXP3YU/7bUf/eUPzbXPvLZ/vVZfzQY//SYf3SZv/Wb/zZYPrRdPvVcP/Q
c/nRfvnVefnbcP/gUf/gUv/iU//jVP/kVf/kVv/lWP/mWP7kXP/oW//qXf/sX/7rYP/tYPzqbfzr
b4ihr4erx4msyI+00pm1zZu2zp25z5a20pS62ZS725S73Je93Jq61Ju92r/GrKTB2L3P37fO4cPK
sd3avu/ajvbUivrSgP/ajfjdkuDaovrggvLmn//hl/vqm+njqvbqqPbrqvburfburvrmoP/kqfnu
ov3ooP/toffis/vpuPvwpP/wo//ypsDLzc7f7d3m8OXiyOPj0OPk0ePk0vXoxf/uxefn5+np6ens
7+zr6+3t7f/14PHx8fTz8/X09PD1+fX4/Pj39/n4+P/9+gAAAAAAACH5BAEAAP8ALAAAAAAyAC0A
AAj/AP8JHEiwoMGDCBMqXMiwocOH/5QFu1KFCpUpvIDJg8ixYLIcMFqQGBGCw4YMGlL86thx2RIm
WJyUIFlhgoQGDCz4YgnxWIti+tLZ+FBzwgMGSFHwfEjMxbB86GpUoGAU6YIDB5Y6HMYCB5QfHCpU
kGDVgFmtDYWZIOmhqAMGV80aQMtyFwYGCswWEEDXYC8dLVywWBtCbIUISPMaIBAgQLtas2DJuobW
iowYLFisIFG4KFIGchsHYDcrVitWmrppVTKDxYkTI0XUlPCWAQKzAkSvc3U6EiRKS6XEcCF4JFGx
R22bHSA6gTpWkyA5YpTIHc8mmAePGPGBggQIOBfo/83d2IgzSZEaKUpESBrPG4JXbP/QdgJOBgfM
ig6g4hwnSOolkocdpfC0wgprjdDWVDQEQUQPEPIwxIS6NJMKgIroUccccoTCU2YjdbYBEshgw82J
3GyjTTbZUJPJdIloOMcaaoDC0wuEHRfFNLjYcsuPtES2yioAMpKhHXXQqMYnPO1Ak1g+MJPLj0DG
Assqm6SniCKE4CEHjWl8QQpPT3A3WxHV+Fglb9GpZ0gedbyhhhphdiEOT8aAcNwDSHxTy5qttMkl
kkqS8UUXY2gFxFgSPHDEN7fUQotpqkTyiHqE1JHknGR00YUWp6AlRAcXXJAEObVYOaQkjyCCSCF0
0PsRBxtonAEGGGJ00hdB5szySiubsGrJrhCV4worqkDyiCKIXIJJJYMMIkggxCIUDiuQKKuIIUjK
4cYffXQhRrUHhcNqI4twWwcca4jyjjdteEGuQeA4ot4hcMIxpzX91APIuPMWNMohhNghx5xqlMFH
NKZwAU3ABnlyx8FqmEHGFllkEcbDEBs0Dip7nOFFF2D48UzHKKes8soN4XPPy/fYI7M9ML8M8T4x
z6zzzjzjs6vLOtMj9NBEEy3zyzSjBXTMQttDzzzxxAPP1PBEPQ89TmNNc9JaAT1z0WAPPXPM9/TF
Dz5o86z2zGjjw0/AbcctN9os12333QoFBAA7

"""

python_j = """\
/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAkGBwgHBgkIBwgKCgkLDRYPDQwMDRsUFRAWIB0iIiAd
Hx8kKDQsJCYxJx8fLT0tMTU3Ojo6Iys/RD84QzQ5Ojf/2wBDAQoKCg0MDRoPDxo3JR8lNzc3Nzc3
Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzf/wAARCAAyADIDASIA
AhEBAxEB/8QAGwAAAgIDAQAAAAAAAAAAAAAAAAYDBAEFBwL/xAAxEAACAQMCBAQEBQUAAAAAAAAB
AgMABBEFEgYhMVETQXGBImGRoQcUM0LBMjRSYsL/xAAZAQADAQEBAAAAAAAAAAAAAAAEBQYCAQP/
xAAlEQACAgIBAwMFAAAAAAAAAAABAgADBBESITFBBTNRBhMyNIH/2gAMAwEAAhEDEQA/AOw4pX43
vrm0FlDb3RtlnZ90inaRjHn251NrnFkGl3Jt44DcSr/WA+0L74NKevcR22t+B+ZsJl8Hdt8K5AB3
Y65Q/wCP3oqmh+h1Bbbk0QDK3FdnBYXqpbXxug67mLSBmU8upH19K0i3EsLB4ZXRlOQVbaQfWrMk
2mlW2Wt0HxyJu0IB742dK1zt26Cjk6LxMBbvsTp/AOt3eqWtzFeyeI9sI9shGCwbdyJ88bevXvmm
vFc//C1wi6ofnF/3T3HcKzhCMZpJkZFVdxrJ0Y2pVmQGS4orPPtRWfupN8TOK3c5uJ5Jn+JpHZzu
58yc1VZs4Jx359qmu42t7iWFxhonKH5EHBps4B0u3nguL25hilKybIw6htpABY4PL9y8/kfd1lZK
Y9XPwImqqNj6iQ7Y75qIgsQFBJPTvXct5QbVYgDoAelQvPIOjtjz+IipxvqNfCxovp2+5i3wbpU+
k2U0lz8Ml1sbw8YKBc49c7vtW7Mm1wRnINeJH5cjzzUAJaRUU82OAKnL8psjJ5+Y3qoFdeoxbz3o
o8M0Ux52/EH6RV1/glNQvXubKcQvMxaRGyVJ8yB8/P3q7oOjyaDpzWskqyM8zPuUYwCqjH2pkxVT
UUcqjIMhc5xTb1F3fGKwSmpFfcou/MnO36cqicqRgzAZ/wBSaid8Ejn6Gi3nhjc+MM5HKpCobfiR
GxXQ3JobP81nwZlO3r8JHWrVppKwzLJK24qcgCs6LA8SSOylVfG0H3rZYqjxMGsqHI0YFZe2yAek
87T3P0or1RTPgvxBtt8zNY/Y1FFcv9szq9xF3Uv129P4rOkf3HtRRUgP2f7Gx9qMMf6i+n8Vmiiq
+r8RFTd4UUUV6TM//9k=

"""

if __name__ == '__main__':
    view(view)
