import re

str=['10.0.1.2/24', '10.0.1.13/24']

for s in str:
    print(re.findall('(.*)/', s))