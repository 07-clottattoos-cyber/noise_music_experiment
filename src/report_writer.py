from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def _markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return ""
    columns = [str(column) for column in df.columns]
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for _, row in df.iterrows():
        values = [str(row[column]) for column in df.columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def _file_list(output_dir: Path) -> list[str]:
    files = []
    for path in sorted(output_dir.rglob("*")):
        if path.is_file():
            files.append(str(path.relative_to(output_dir.parent)))
    return files


def write_report(
    output_dir: Path,
    analyses: dict[str, dict[str, Any]],
    motif_info: dict[str, Any],
    exported_files: dict[str, dict[str, Path]],
) -> Path:
    report_path = output_dir / "report" / "experiment_report.md"
    summary_path = output_dir / "stats" / "summary_stats.csv"
    summary_md = ""
    if summary_path.exists():
        summary_md = _markdown_table(pd.read_csv(summary_path))

    files_md = "\n".join(f"- `{path}`" for path in _file_list(output_dir))
    motif_md = "\n".join(
        f"- {label}: 第 {info.start_measure}-{info.end_measure} 小节；音高 MIDI {info.pitches}；时值 {info.durations}；{info.reason}"
        for label, info in motif_info.items()
    )

    content = f"""# 噪声音乐·随机旋律的发展实验报告

## 实验目的

本实验通过程序生成粉色随机音乐和棕色随机音乐，比较两种随机过程在旋律轮廓、节奏分布、音程分布和听觉印象上的差异，并从随机结果中提取主题片段进行音乐化发展。

## 使用软件与工具

- Python 3.10+
- music21：生成 MusicXML 和 MIDI
- numpy：随机序列与数值处理
- pandas / openpyxl：统计表格与 Excel 输出
- matplotlib：统计图表
- MuseScore：如本机可用，用于 PDF 和音频导出

## 粉色音乐生成方法

粉色音乐使用 Voss-McCartney 近似算法生成 1/f 特征的数值序列，再映射到 C4-C6 的 C 大调音阶。节奏在二分音符、四分音符、八分音符和十六分音符中随机选择，并保证每小节正好 4 拍。

## 棕色音乐生成方法

棕色音乐使用有边界反弹的随机游走。相邻音以级进和小幅移动为主，偶尔出现较大移动；音高同样映射到 C4-C6 的 C 大调音阶。

## 粉色音乐听觉感受

草稿：粉色旋律跳进更明显，局部节奏更密集，整体呈现较活跃、跳跃的随机感。此描述需要用户最终聆听音频或 MIDI 后修订。

## 棕色音乐听觉感受

草稿：棕色旋律线条更连贯，邻近移动较多，听感更像缓慢游移的旋律。此描述需要用户最终聆听音频或 MIDI 后修订。

## 两段随机音乐的统计结果

{summary_md}

## 统计分析

粉色音乐的音程分布通常更分散，说明跳进与方向变化较多；棕色音乐的相邻音程更集中在小音程，符合随机游走的生成逻辑。两段旋律都被强制检查两八度音域、四类时值和小节完整性。

## 有趣片段的选择

{motif_md}

## 粉色主题发展曲说明

粉色主题发展曲采用 A-B-A' 结构。A 段呈示与重复主题，B 段使用移调、倒影和节奏压缩，A' 段再现主题并扩展到较高音区，最后稳定结束。

## 棕色主题发展曲说明

棕色主题发展曲采用 A-A1-B-Coda 结构。A 段保留原型，A1 段做模进与微变形，B 段逐步扩大音区，Coda 回到 C 大调稳定音结束。

## 创作意图与手法

创作意图是让两类随机过程不仅作为声音材料存在，也能成为可发展的主题来源。粉色主题强调对比、倒影和节奏密度；棕色主题强调平滑线条、模进和渐进式音区扩展。

## 对听者聆听体验的影响

粉色材料可能带来更强的不可预测性和紧张感；棕色材料可能带来更连续、更平稳的方向感。发展曲通过重复和变形让随机片段获得更清楚的结构线索。

## 输出文件清单

{files_md}

## 参考文献

- OpenAI Codex CLI 文档，占位待补充。
- music21 文档，占位待补充。
- MuseScore 文件导出文档，占位待补充。
"""
    report_path.write_text(content, encoding="utf-8")
    return report_path
