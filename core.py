#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class WhatsAppChat():
    """
    Represent a WhatsApp conversation, enriched with additional information upon initialization
    Args:
        name          String that identifies the conversation
        df            DataFrame containing the messages
    Attributes:
        name          String that identifies the conversation
        df            DataFrame containing the messages
        authors       Authors in the conversation
        date_range    Min and maximum datetime of the conversation
        message_count Amount of messages (with valid headers) exchanged
    """

    def __init__(self, name, df):
        self.name = name
        self.df = df
        self.authors = [*df.author.unique()]
        self.date_range = (df.datetime.min(), df.datetime.max())
        self.message_count = len(df)

    def __repr__(self):
        return f"WhatsAppChat('{self.name}')"

    def __str__(self):
        ret = f"{70*'-'}\n"
        ret += f"WhatsAppChat\nName:\t\t{self.name:20}\n"
        ret += f"Authors:\t{', '.join(map(str, [xx for xx in self.authors]))}\n"
        ret += f"Date range:\t{self.date_range[0].isoformat()}, {self.date_range[1].isoformat()}\n"
        ret += f"Message count:\t{self.message_count}\n"
        ret += f"{70*'-'}"
        return ret

    def get_squashed_messages(self, author):
        """Return the messages of a specified author all together, in a single string"""
        df_author = self.df[(self.df['author'] == author) & (self.df['is_media'] == False)]
        return df_author['message'].str.cat(sep=' ')