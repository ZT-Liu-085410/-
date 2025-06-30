import os
import sounddevice as sd
import soundfile as sf
from vad import vad_segment
from preprocessor import preprocess
from mfcc import compute_mfcc
from recognizer import transcribe
from translator import baidu_translate
from synthesizer import synthesize_by_voice, synthesize_by_rate, synthesize_combined
from utils import plot_multiple_waveforms, plot_multiple_spectrograms

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)
RECORD_SECONDS = 5
SAMPLE_RATE = 16000

try:
    print("Step 1: 正在录音...")
    audio = sd.rec(int(RECORD_SECONDS * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()
    raw_path = os.path.join(OUTPUT_DIR, "raw.wav")
    sf.write(raw_path, audio, SAMPLE_RATE)
    print("录音完成，已保存到 raw.wav")

    print("Step 2: 端点检测中...")
    vad_audio = vad_segment(raw_path)
    vad_path = os.path.join(OUTPUT_DIR, "vad.wav")
    sf.write(vad_path, vad_audio, SAMPLE_RATE)
    print("端点检测完成，已保存到 vad.wav")

    print("Step 3: 预处理语音...")
    frames = preprocess(vad_audio.flatten(), SAMPLE_RATE)
    print("预处理完成，帧数：", frames.shape)

    print("Step 4: 提取 MFCC 特征...")
    mfcc_feat = compute_mfcc(frames, SAMPLE_RATE)
    print("MFCC 提取完成，特征维度：", mfcc_feat.shape)

    print("Step 5: 中文语音识别中...")
    text = transcribe(vad_path)
    print("识别结果：", text)

    print("Step 6: 中文→英文翻译中...")
    translated = baidu_translate(text)
    print("翻译结果：", translated)

    print("Step 7: 英文语音合成中...")

    synthesize_by_voice(translated, OUTPUT_DIR)
    print("完成：只变音色合成")

    synthesize_by_rate(translated, OUTPUT_DIR)
    print("完成：只变语速合成")

    synthesize_combined(translated, OUTPUT_DIR)
    print("完成：音色和语速全组合合成")

    print("合成全部完成")

    print("Step 8: 合成音频波形和频谱图差异比较中...")

    # 根据你合成的文件名规则，加载文件路径和标签

    # 只变音色的文件
    voices = [
        "en-US-JennyNeural",
        "en-US-GuyNeural",
        "en-GB-RyanNeural",
        "en-US-AriaNeural",
        "en-GB-SoniaNeural"
    ]
    wave_files_voice = [os.path.join(OUTPUT_DIR, f"{v}_default.wav") for v in voices]

    # 只变语速的文件
    rates = ["-20%", "+0%", "+20%"]
    wave_files_rate = [os.path.join(OUTPUT_DIR, f"en-US-JennyNeural_{r.replace('%', 'pct')}.wav") for r in rates]

    # 音色×语速组合里的部分示例（这里取每个音色的默认语速做对比）
    wave_files_combined = [os.path.join(OUTPUT_DIR, f"{v}_default.wav") for v in voices]

    # 画图保存路径
    waveform_save_path = os.path.join(OUTPUT_DIR, "compare_waveforms.png")
    spectrogram_save_path = os.path.join(OUTPUT_DIR, "compare_spectrograms.png")

    # 绘制只变音色波形图
    plot_multiple_waveforms(wave_files_voice, voices, os.path.join(OUTPUT_DIR, "waveform_by_voice.png"))

    # 绘制只变音色频谱图
    plot_multiple_spectrograms(wave_files_voice, voices, os.path.join(OUTPUT_DIR, "spectrogram_by_voice.png"))

    # 绘制只变语速波形图
    plot_multiple_waveforms(wave_files_rate, rates, os.path.join(OUTPUT_DIR, "waveform_by_rate.png"))

    # 绘制只变语速频谱图
    plot_multiple_spectrograms(wave_files_rate, rates, os.path.join(OUTPUT_DIR, "spectrogram_by_rate.png"))

    # 你也可以绘制音色×语速组合中几个典型文件对比（这里示范默认语速音色比较）
    plot_multiple_waveforms(wave_files_combined, voices, os.path.join(OUTPUT_DIR, "waveform_combined_default_rate.png"))
    plot_multiple_spectrograms(wave_files_combined, voices,
                               os.path.join(OUTPUT_DIR, "spectrogram_combined_default_rate.png"))

    print("图像保存完成，路径：", OUTPUT_DIR)

except Exception as e:
    print("❌ 程序出错：", e)
