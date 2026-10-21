import csv
import sys
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("Dependency missing. Run: python -m pip install -U yt-dlp")
    sys.exit(1)

PLAYLISTS = [
    {
        "playlist_id": "PLfqMhTWNBTe137I_EPQd34TsgV6IO55pt",
        "playlist_url": "https://www.youtube.com/playlist?list=PLfqMhTWNBTe137I_EPQd34TsgV6IO55pt",
        "playlist_name": "Complete C++ DSA Course",
    },
    {"playlist_id": "PLDzeHZWIZsTryvtXdMr6rPh4IDexB5NIA",
        "playlist_url": "https://www.youtube.com/playlist?list=PLDzeHZWIZsTryvtXdMr6rPh4IDexB5NIA",
        "playlist_name": "Complete C++ Placement DSA Course",
    },
    {
        "playlist_id": "PLgUwDviBIf0oF6QL8m22w1hIDC1vJ_BHz",
        "playlist_url": "https://www.youtube.com/playlist?list=PLgUwDviBIf0oF6QL8m22w1hIDC1vJ_BHz",
        "playlist_name": "Strivers A2Z DSA Course",
    },
]

OUTPUT_FILE = Path("dsa_mentor_800_video_dataset.csv")

FIELDS = [
    "video_id",
    "channel_id",
    "channel_name",
    "video_title",
    "video_url",
    "language",
    "transcript",
    "tags",
    "source",
    "source_playlist_id",
    "source_playlist_name",
    "playlist_position",
    "duration_seconds",
    "description",
    "label_verified",
]

def main():
    options = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": "in_playlist",
        "skip_download": True,
        "ignoreerrors": True,
    }

    all_rows = []
    seen_video_ids = set()
    playlist_counts = {}

    with yt_dlp.YoutubeDL(options) as ydl:
        for playlist in PLAYLISTS:
            print(f"Reading: {playlist['playlist_name']} ...")
            try:
                info = ydl.extract_info(
                    playlist["playlist_url"],
                    download=False
                )
            except Exception as exc:
                print(f"  Could not read this playlist: {exc}")
                playlist_counts[playlist["playlist_id"]] = 0
                continue

            if not info:
                print("  No playlist metadata returned.")
                playlist_counts[playlist["playlist_id"]] = 0
                continue

            count_before = len(all_rows)
            for position, entry in enumerate(info.get("entries") or [], start=1):
                if not entry:
                    continue

                video_id = entry.get("id")
                if not video_id or video_id in seen_video_ids:
                    continue

                seen_video_ids.add(video_id)
                url = entry.get("url") or ""
                if not url.startswith("http"):
                    url = f"https://www.youtube.com/watch?v={video_id}"

                all_rows.append({
                    "video_id": video_id,
                    "channel_id": entry.get("channel_id") or entry.get("uploader_id") or "",
                    "channel_name": entry.get("channel") or entry.get("uploader") or "",
                    "video_title": entry.get("title") or "",
                    "video_url": url,
                    "language": "",
                    "transcript": "",
                    "tags": "",
                    "source": "YouTube playlist",
                    "source_playlist_id": playlist["playlist_id"],
                    "source_playlist_name": playlist["playlist_name"],
                    "playlist_position": position,
                    "duration_seconds": entry.get("duration") or "",
                    "description": "",
                    "label_verified": "false",
                })

            added = len(all_rows) - count_before
            playlist_counts[playlist["playlist_id"]] = added
            print(f"  Added {added} unique videos.")

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(all_rows)

    print("\nDone.")
    print(f"Unique video rows: {len(all_rows)}")
    print(f"CSV saved to: {OUTPUT_FILE.resolve()}")
    print("Transcript, tags, and descriptions are blank where not reliably available.")
    print("Review video relevance and verify tags before using rows for model training.")
    if len(all_rows) < 800:
        print(f"These playlists returned fewer than 800 unique videos ({len(all_rows)}).")
        print("Add more public DSA playlists to reach the 800-video target.")

if __name__ == "__main__":
    main()