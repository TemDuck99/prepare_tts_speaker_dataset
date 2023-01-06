import os

import pandas as pd
import librosa
import ndjson
from loguru import logger


logger.add("logs/error.log", format="{time}{level}{message}")


def get_transcribe(audio_filepath, text_path):
    filename = os.path.basename(audio_filepath).replace(".wav", ".txt")
    filepath = os.path.join(text_path, filename)
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            text = file.readline()
        return text
    else:
        logger.info(f"file not founded: {filename}")
        return None


def get_duration(audio_filepath):
    duration = librosa.core.get_duration(filename=audio_filepath, sr=22050)
    return duration


def create_df(audios_path, texts_path):
    audio_filepaths = pd.Series(
        os.path.join(audios_path, file) for file in os.listdir(audios_path)
    )
    df = pd.DataFrame(audio_filepaths, columns=["audio_filepath"])
    df["text"] = df["audio_filepath"].apply(
        lambda x: get_transcribe(x, text_path=texts_path)
    )
    df["duration"] = df["audio_filepath"].apply(lambda x: get_duration(x))
    df["audio_filepath"] = df["audio_filepath"].apply(
        lambda x: os.path.join(*x.split("/")[-4:]))
    return df


def save_result(df, out_json):
    with open(out_json, "w") as file:
        dict_records = df.to_dict(orient="records")
        ndjson.dump(dict_records, file, ensure_ascii=False)
