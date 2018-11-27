import re
str = "#360 of 9,887 Restaurants in Hong Kong"

print(re.findall(r"#(.+?) of", str)[0])

