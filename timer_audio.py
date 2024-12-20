from pydub import AudioSegment
import os


def create_interval_timer(total_duration_minutes, interval_minutes=5, output_filename="timer.mp3", bell_duration_seconds=5):
    """
    Create an MP3 file with interval sounds every X minutes and a final sound.
    Uses progress.wav for interval bells and final.wav for start/end bells.
    """
    # Load bell sounds
    progress_sound = AudioSegment.from_file("progress.wav")
    final_sound = AudioSegment.from_file("final.wav")

    # Create pure digital silence segment
    one_sec_silence = AudioSegment.silent(duration=1000)

    # Calculate positions in milliseconds
    total_duration_ms = total_duration_minutes * 60 * 1000
    interval_ms = interval_minutes * 60 * 1000
    bell_duration_ms = bell_duration_seconds * 1000

    # Create list of bell positions and their sounds
    bell_positions = [(0, final_sound)]  # Opening bell

    # Add interval bells
    current_time = interval_ms
    while current_time < total_duration_ms:
        bell_position = current_time - bell_duration_ms
        bell_positions.append((bell_position, progress_sound))
        current_time += interval_ms

    # Add final bell
    final_position = total_duration_ms - bell_duration_ms
    bell_positions.append((final_position, final_sound))

    # Build audio file
    result = one_sec_silence
    last_end = 0

    # Add each bell with minimal silence between
    for position, bell in bell_positions:
        if position > last_end:
            silence_needed = position - last_end
            num_chunks = (silence_needed // 1000) + 1
            result += one_sec_silence * num_chunks

        result += bell
        last_end = position + len(bell)

    # Add final silence if needed
    if total_duration_ms > last_end:
        final_silence = total_duration_ms - last_end
        num_chunks = (final_silence // 1000) + 1
        result += one_sec_silence * num_chunks

    # Export with settings optimized for silence
    result.export(
        output_filename,
        format="mp3",
        parameters=[
            "-compression_level",
            "9",
            "-b:a",
            "8k",  # Very low bitrate since it's mostly silence
            "-map_metadata",
            "-1",  # Remove metadata
            "-joint_stereo",
            "1",  # Use joint stereo encoding
            "-abr",
            "1",  # Use ABR (average bitrate) encoding
        ],
    )
    print(f"Created timer audio file: {output_filename}")


if __name__ == "__main__":
    create_interval_timer(total_duration_minutes=15, interval_minutes=5, output_filename="15min_timer.mp3")
