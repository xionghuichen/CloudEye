#!/usr/bin/env python
# coding=utf-8

# Author      :   Xionghui Chen
# Created     :   2017.3.20
# Modified    :   2017.3.20
# Version     :   1.0

from PIL import Image
im = Image.open(unicode('./missing_person/安琪儿/7.jpg','utf-8')).convert('L')
im.save('./missing_person/安琪儿/8.jpg')