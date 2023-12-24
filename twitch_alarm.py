import asyncio
import sys
from dataclasses import dataclass, field
from typing import List

import yt_dlp
from pydub import AudioSegment
from pydub.playback import play
from yaml import safe_load

TWITCH_BASE_URL = "https://www.twitch.tv"


def main():
    try:
        config = _read_config()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(_check_loop(config))
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        sys.exit(1)


@dataclass
class Config:
    twitch_watched_channels: List[str]
    interval_seconds: int = field(default=60)
    alarm_filepath: str = field(default="res/ドラえもんの目覚まし時計の歌 covered by 息根とめる.wav")

    def __init__(self, local_config: dict):
        self.twitch_watched_channels = local_config["twitch"]["watched_channels"]

        if "interval_seconds" in local_config.keys():
            if local_config["interval_seconds"]:
                self.interval_seconds = local_config["interval_seconds"]

        if "alarm_filepath" in local_config.keys():
            if local_config["alarm_filepath"]:
                self.alarm_filepath = local_config["alarm_filepath"]


def _read_config():
    with open("config.yaml", "r", encoding="utf-8") as s:
        return Config(safe_load(s))


async def _check_loop(config: Config):
    tasks = []
    for channel in config.twitch_watched_channels:
        tasks.append(_check_loop_child(channel, config))
    await asyncio.gather(*tasks)


async def _check_loop_child(channel: str, config: Config):
    waiting_msg = f'Waiting for "{channel}" to start a stream...'
    start_msg = f'The channel "{channel}" started a stream!'
    end_msg = f'The channel "{channel}" ended a stream.'

    print(waiting_msg)
    currently_streaming = False
    while True:
        try:
            if (is_live := _is_live(channel)) and not currently_streaming:
                print(start_msg)
                _alarm(config.alarm_filepath)
                currently_streaming = True
            elif not is_live and currently_streaming:
                print(end_msg)
                currently_streaming = False
                print(waiting_msg)
            else:
                pass
            await asyncio.sleep(config.interval_seconds)
        except Exception as err:
            print(err)
            await asyncio.sleep(config.interval_seconds)


# 配信開始してない時に出る邪魔なエラーログを出したくなくて定義している
class LoggerOutputs:
    def error(msg):
        pass

    def debug(msg):
        pass


def _is_live(channel: str, ydl_opts: dict = {"quiet": True, "logger": LoggerOutputs}):
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(_get_url(channel), download=False)
        return True
    except yt_dlp.utils.DownloadError:
        return False


def _alarm(alarm_filepath: str):
    play(AudioSegment.from_wav(alarm_filepath))


def _get_url(channel: str):
    return f"{TWITCH_BASE_URL}/{channel}"


if __name__ == "__main__":
    exit(main())
