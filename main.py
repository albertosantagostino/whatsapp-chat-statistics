#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import pandas as pd
import pickle
import re

from pathlib import Path

from core import WhatsAppChat
from chat_analysis import create_wordcloud
import ipdb


def parse_chat_df(filepath):
    chat = open(filepath, 'r')
    latest_valid_header_idx = 0
    msgs = {}
    print("Start parsing...")
    for idx, line, in enumerate(chat):
        regex_exp = r'^([0-9]{1,2}\/[0-9]{1,2}\/[0-9]{2}),\s([0-9]{2}:[0-9]{2})\s-\s(.*?):\s(.*)$'
        matches = re.findall(regex_exp, line)
        # Create header for each valid message and add it to msgs

        if matches:
            try:
                date, time, author, message = matches[0]
                latest_valid_header_idx = idx
                msgs[latest_valid_header_idx] = [pd.Timestamp(f'{date}T{time}'), author, message.strip()]
            except IndexError:
                raise IndexError(f"Unexpected parsing in line {line}")
        # Handle lines without header (newlines in the original message) appending them to the latest valid message
        else:
            msgs[latest_valid_header_idx][-1] += f" {line.strip()}"
    df = pd.DataFrame.from_dict(msgs, columns=['datetime', 'author', 'message'], orient='index')
    df.reset_index(drop=True, inplace=True)
    # Set flag to identify media messages
    df['is_media'] = df['message'] == "<Media omitted>"
    print(f"Done!\n{idx} raw rows, {len(df)} message header parsed")
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-input_file", help="Chat filename (in folder chat_data/)")
    params = parser.parse_args()
    filepath_pickled = Path(f'chat_data/{params.input_file}').with_suffix('.pickle')
    # Check if chat is already parsed and stored in chat_data/
    if not filepath_pickled.exists():
        print("Chat is not parsed yet...")
        filepath_input = Path(f'chat_data/{params.input_file}').with_suffix('.txt')
        if not filepath_input.exists():
            raise FileNotFoundError(f"No file with name {params.input_file}")
            # Parse .txt chat file and pickle it as DataFrame
        df = parse_chat_df(Path(f'chat_data/{params.input_file}').with_suffix('.txt'))
        chat = WhatsAppChat(name=filepath_input.stem, df=df)
        pickle.dump(chat, filepath_pickled.open(mode='wb'))
    # Load the already pickled DataFrame representing the chat
    else:
        chat = pickle.load(filepath_pickled.open(mode='rb'))

    for author in chat.authors:
        create_wordcloud(chat, author)

    #ipdb.set_trace()
