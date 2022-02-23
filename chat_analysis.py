#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

import ipdb


def create_wordcloud(chat, author):
    messages_string = chat.get_squashed_messages(author)
    messages_string = re.sub(r'\b\w{1,6}\b', '', messages_string)
    wordcloud = WordCloud(width=1024, height=768).generate(messages_string)
    plt.figure(figsize=(20, 10))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(f'out/{author}_wordcloud.png')

    #ipdb.set_trace()