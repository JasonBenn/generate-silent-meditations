from timer_audio import create_interval_timer
import os


def generate_timer_suite(output_dir="meditation_timers"):
    """
    Generate a suite of meditation timer audio files with different durations,
    both with and without interval reminders.

    Parameters:
    output_dir (str): Directory to store the generated files
    progress_sound_path (str): Path to the sound file for progress notifications
    final_sound_path (str): Path to the sound file for the final bell
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    for duration in [5, 10, 15, 20, 25, 30, 45, 60, 75, 90]:
        # Version with interval reminders
        reminder_filename = os.path.join(output_dir, f"{duration}min_with_reminders.mp3")
        create_interval_timer(
            total_duration_minutes=duration,
            interval_minutes=5,
            output_filename=reminder_filename,
        )

        # Version without interval reminders
        silent_filename = os.path.join(output_dir, f"{duration}min_silent.mp3")
        create_interval_timer(
            total_duration_minutes=duration,
            interval_minutes=duration + 1,
            output_filename=silent_filename,
        )

        print(f"Generated {duration}-minute timer files:")
        print(f"  - With reminders: {reminder_filename}")
        print(f"  - Without reminders: {silent_filename}")


if __name__ == "__main__":
    # Example usage:
    generate_timer_suite(output_dir="meditation_timers")

    # Or use with default beep sounds:
    # generate_timer_suite(output_dir="meditation_timers")
