# 噪声音乐·随机旋律的发展实验报告

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

| label | lowest_pitch | highest_pitch | pitch_range_semitones | total_notes | total_measures | constraints_met |
| --- | --- | --- | --- | --- | --- | --- |
| pink | C4 | C6 | 24 | 116 | 20 | True |
| brown | C4 | C6 | 24 | 101 | 20 | True |

## 统计分析

粉色音乐的音程分布通常更分散，说明跳进与方向变化较多；棕色音乐的相邻音程更集中在小音程，符合随机游走的生成逻辑。两段旋律都被强制检查两八度音域、四类时值和小节完整性。

## 有趣片段的选择

- pink: 第 12-13 小节；音高 MIDI [84, 76, 72, 72, 65, 65, 83, 83, 79, 79, 67, 67, 69]；时值 [0.5, 0.5, 0.25, 2.0, 0.5, 0.25, 0.5, 0.5, 0.25, 1.0, 1.0, 0.25, 0.5]；含 6 个三度以上跳进，节奏种类 4，音程变化较丰富。
- brown: 第 15-15 小节；音高 MIDI [69, 67, 62, 60]；时值 [1.0, 1.0, 1.0, 1.0]；级进/同音比例 0.67，方向趋势评分 1.00，节奏较稳定。

## 粉色主题发展曲说明

粉色主题发展曲采用 A-B-A' 结构。A 段呈示与重复主题，B 段使用移调、倒影和节奏压缩，A' 段再现主题并扩展到较高音区，最后稳定结束。

## 棕色主题发展曲说明

棕色主题发展曲采用 A-A1-B-Coda 结构。A 段保留原型，A1 段做模进与微变形，B 段逐步扩大音区，Coda 回到 C 大调稳定音结束。

## 创作意图与手法

创作意图是让两类随机过程不仅作为声音材料存在，也能成为可发展的主题来源。粉色主题强调对比、倒影和节奏密度；棕色主题强调平滑线条、模进和渐进式音区扩展。

## 对听者聆听体验的影响

粉色材料可能带来更强的不可预测性和紧张感；棕色材料可能带来更连续、更平稳的方向感。发展曲通过重复和变形让随机片段获得更清楚的结构线索。

## 输出文件清单

- `output/audio/brown_motif.wav`
- `output/audio/brown_music.wav`
- `output/audio/brown_theme_development.wav`
- `output/audio/pink_motif.wav`
- `output/audio/pink_music.wav`
- `output/audio/pink_theme_development.wav`
- `output/charts/brown_duration_distribution.png`
- `output/charts/brown_interval_distribution.png`
- `output/charts/brown_pitch_distribution.png`
- `output/charts/pink_duration_distribution.png`
- `output/charts/pink_interval_distribution.png`
- `output/charts/pink_pitch_distribution.png`
- `output/midi/brown_motif.mid`
- `output/midi/brown_music.mid`
- `output/midi/brown_theme_development.mid`
- `output/midi/pink_motif.mid`
- `output/midi/pink_music.mid`
- `output/midi/pink_theme_development.mid`
- `output/musicxml/brown_motif.musicxml`
- `output/musicxml/brown_music.musicxml`
- `output/musicxml/brown_theme_development.musicxml`
- `output/musicxml/pink_motif.musicxml`
- `output/musicxml/pink_music.musicxml`
- `output/musicxml/pink_theme_development.musicxml`
- `output/report/experiment_report.md`
- `output/scores/brown_motif.pdf`
- `output/scores/brown_music.pdf`
- `output/scores/brown_theme_development.pdf`
- `output/scores/pink_and_brown_music.pdf`
- `output/scores/pink_motif.pdf`
- `output/scores/pink_music.pdf`
- `output/scores/pink_theme_development.pdf`
- `output/stats/brown_duration_stats.csv`
- `output/stats/brown_interval_stats.csv`
- `output/stats/brown_pitch_stats.csv`
- `output/stats/brown_zone_stats.csv`
- `output/stats/pink_duration_stats.csv`
- `output/stats/pink_interval_stats.csv`
- `output/stats/pink_pitch_stats.csv`
- `output/stats/pink_zone_stats.csv`
- `output/stats/summary_stats.csv`
- `output/stats/summary_stats.xlsx`

## 参考文献

- OpenAI Codex CLI 文档，占位待补充。
- music21 文档，占位待补充。
- MuseScore 文件导出文档，占位待补充。
