import os


cache = {}
TARGET_DIRS = ("Audios", "Transcripts")


def search_target_dirs(path, level=1, max_level=4):
    assert level != max_level
    print(
        f"level: {level}",
        f"Content: {os.listdir(path)}",
        f"basename: {os.path.basename(path)}",
    )
    content = os.listdir(path)
    basename = os.path.basename(path)
    cache[basename] = []
    while content:
        temp_dir = content.pop(-1)
        temp_path = os.path.join(path, temp_dir)
        if (os.path.isdir(temp_path) and
                temp_dir not in TARGET_DIRS and os.listdir(temp_path)):
            cache[basename].append(
                search_target_dirs(path=temp_path, level=level + 1)
            )
    return basename


def get_speakers(speakers_dirs_path):
    search_target_dirs(path=speakers_dirs_path)
    target_dirs = []
    for speaker in cache[os.path.basename(speakers_dirs_path)]:
        if not cache[speaker]:
            cur_path = os.path.join(speakers_dirs_path, speaker)
            target_dirs.append((cur_path, speaker))
        else:
            cur_path = os.path.join(speakers_dirs_path, speaker)
            cur_paths = []
            for sub in cache[speaker]:
                cur_paths.append(
                    (os.path.join(cur_path, sub), f"{speaker}_{sub}")
                )
            target_dirs.extend(cur_paths)
    return target_dirs
