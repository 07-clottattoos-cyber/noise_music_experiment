from __future__ import annotations

from pathlib import Path

import yaml

from .development import MotifMaterial, build_brown_development, build_pink_development
from .melody_builder import build_brown_melody, build_pink_melody
from .motif_selector import select_motif
from .report_writer import write_report
from .score_exporter import ensure_output_dirs, export_score, find_musescore
from .statistics import analyze_score, write_statistics


ROOT = Path(__file__).resolve().parents[1]


def load_config() -> dict:
    with (ROOT / "config.yaml").open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main() -> None:
    config = load_config()
    output_dir = ROOT / str(config.get("output_dir", "output"))
    ensure_output_dirs(output_dir)
    musescore = find_musescore()
    if not musescore:
        print("未检测到 MuseScore，已跳过 PDF 和音频导出，可手动用 MuseScore 打开 MusicXML 后导出。")

    exported: dict[str, dict[str, Path]] = {}
    pink = build_pink_melody(config)
    brown = build_brown_melody(config)
    exported["pink_music"] = export_score(pink.score, "pink_music", output_dir, musescore)
    exported["brown_music"] = export_score(brown.score, "brown_music", output_dir, musescore)

    analyses = {
        "pink": analyze_score(pink.score, "pink"),
        "brown": analyze_score(brown.score, "brown"),
    }
    write_statistics(analyses, output_dir)

    pink_motif = select_motif(pink.score, "pink")
    brown_motif = select_motif(brown.score, "brown")
    motif_info = {"pink": pink_motif, "brown": brown_motif}
    print(f"粉色主题：第 {pink_motif.start_measure}-{pink_motif.end_measure} 小节，音高 {pink_motif.pitches}，时值 {pink_motif.durations}。{pink_motif.reason}")
    print(f"棕色主题：第 {brown_motif.start_measure}-{brown_motif.end_measure} 小节，音高 {brown_motif.pitches}，时值 {brown_motif.durations}。{brown_motif.reason}")

    exported["pink_motif"] = export_score(pink_motif.score, "pink_motif", output_dir, musescore)
    exported["brown_motif"] = export_score(brown_motif.score, "brown_motif", output_dir, musescore)

    pink_dev = build_pink_development(
        MotifMaterial(pink_motif.pitches, pink_motif.durations),
        int(config["measures"]["pink_development"]),
        int(config["tempo"]["pink_development"]),
    )
    brown_dev = build_brown_development(
        MotifMaterial(brown_motif.pitches, brown_motif.durations),
        int(config["measures"]["brown_development"]),
        int(config["tempo"]["brown_development"]),
    )
    exported["pink_theme_development"] = export_score(pink_dev, "pink_theme_development", output_dir, musescore)
    exported["brown_theme_development"] = export_score(brown_dev, "brown_theme_development", output_dir, musescore)

    write_report(output_dir, analyses, motif_info, exported)

    print("最终输出文件清单：")
    for path in sorted(output_dir.rglob("*")):
        if path.is_file():
            print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
