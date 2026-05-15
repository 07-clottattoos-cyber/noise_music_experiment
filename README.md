# 噪声音乐·随机旋律的发展

这个项目自动完成一组音乐实验：用 Python 生成粉色随机旋律和棕色随机旋律，导出 MusicXML/MIDI，统计谱面信息，生成图表，自动选择主题片段，并将片段发展成两首小曲。

## 安装

建议使用 Python 3.10+。

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 运行

```bash
python -m src.main
```

运行后会生成：

- `output/musicxml/`：随机旋律、主题片段、发展曲的 MusicXML
- `output/midi/`：对应 MIDI
- `output/stats/`：CSV 和 Excel 统计表
- `output/charts/`：音高、时值、音程分布图
- `output/report/experiment_report.md`：中文实验报告草稿
- `output/scores/`、`output/audio/`：如果检测到 MuseScore，会尝试导出 PDF 和 WAV

## MuseScore 导出

程序会自动检测 `mscore`、`musescore`、`musescore4`、`MuseScore4.exe`、`MuseScore.exe`，以及 macOS 常见应用路径。如果未检测到 MuseScore，MusicXML 和 MIDI 仍会正常生成，可手动用 MuseScore 打开 `output/musicxml/*.musicxml` 后导出 PDF 或音频。

## 测试

```bash
pytest
```

测试会检查小节数、每小节拍数、时值种类、音域跨度、导出文件、统计文件和发展曲长度。
