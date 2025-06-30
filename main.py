import os
import tkinter as tk
from tkinter import messagebox
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
RECORD_SECONDS = 10
SAMPLE_RATE = 16000

# 创建主窗口
root = tk.Tk()
root.title("实时语音翻译系统")
root.geometry("600x400")

# 控制流程的状态变量
raw_path = os.path.join(OUTPUT_DIR, "raw.wav")
vad_path = os.path.join(OUTPUT_DIR, "vad.wav")
final_text = ""
translated_text = ""


def step1_record():
    try:
        status_label.config(text="Step 1: 正在录音...")
        audio = sd.rec(int(RECORD_SECONDS * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
        sd.wait()
        sf.write(raw_path, audio, SAMPLE_RATE)
        status_label.config(text="录音完成，已保存 raw.wav")
    except Exception as e:
        messagebox.showerror("错误", f"录音失败：{e}")


def step2_vad():
    try:
        status_label.config(text="Step 2: 端点检测中...")
        vad_audio = vad_segment(raw_path)
        sf.write(vad_path, vad_audio, SAMPLE_RATE)
        status_label.config(text="端点检测完成，已保存 vad.wav")
    except Exception as e:
        messagebox.showerror("错误", f"端点检测失败：{e}")


def step3_preprocess():
    try:
        status_label.config(text="Step 3: 预处理语音...")
        audio, _ = sf.read(vad_path)
        frames = preprocess(audio.flatten(), SAMPLE_RATE)
        status_label.config(text=f"预处理完成，帧数：{frames.shape}")
    except Exception as e:
        messagebox.showerror("错误", f"预处理失败：{e}")


def step4_mfcc():
    try:
        status_label.config(text="Step 4: 提取 MFCC 特征...")
        audio, _ = sf.read(vad_path)
        frames = preprocess(audio.flatten(), SAMPLE_RATE)
        mfcc_feat = compute_mfcc(frames, SAMPLE_RATE)
        status_label.config(text=f"MFCC 提取完成，维度：{mfcc_feat.shape}")
    except Exception as e:
        messagebox.showerror("错误", f"MFCC 提取失败：{e}")


def step5_recognize():
    global final_text
    try:
        status_label.config(text="Step 5: 中文语音识别中...")
        text = transcribe(vad_path)
        final_text = text
        status_label.config(text=f"识别结果：{text}")
    except Exception as e:
        messagebox.showerror("错误", f"语音识别失败：{e}")


def step6_translate():
    global translated_text
    try:
        status_label.config(text="Step 6: 中文→英文翻译中...")
        translated = baidu_translate(final_text)
        translated_text = translated
        status_label.config(text=f"翻译结果：{translated}")
    except Exception as e:
        messagebox.showerror("错误", f"翻译失败：{e}")


def step7_synthesize():
    try:
        status_label.config(text="Step 7: 英文语音合成中...")
        synthesize_by_voice(translated_text, OUTPUT_DIR)
        synthesize_by_rate(translated_text, OUTPUT_DIR)
        synthesize_combined(translated_text, OUTPUT_DIR)
        status_label.config(text="音频合成完成")
    except Exception as e:
        messagebox.showerror("错误", f"合成失败：{e}")


def step8_visualize():
    try:
        status_label.config(text="Step 8: 绘制波形和频谱图...")

        voices = [
            "en-US-JennyNeural",
            "en-US-GuyNeural",
            "en-GB-RyanNeural",
            "en-US-AriaNeural",
            "en-GB-SoniaNeural"
        ]
        wave_files_voice = [os.path.join(OUTPUT_DIR, f"{v}_default.wav") for v in voices]

        rates = ["-20%", "+0%", "+20%"]
        wave_files_rate = [os.path.join(OUTPUT_DIR, f"en-US-JennyNeural_{r.replace('%', 'pct')}.wav") for r in rates]

        # 默认速率下的组合比较
        wave_files_combined = [os.path.join(OUTPUT_DIR, f"{v}_default.wav") for v in voices]

        plot_multiple_waveforms(wave_files_voice, voices, os.path.join(OUTPUT_DIR, "waveform_by_voice.png"))
        plot_multiple_spectrograms(wave_files_voice, voices, os.path.join(OUTPUT_DIR, "spectrogram_by_voice.png"))

        plot_multiple_waveforms(wave_files_rate, rates, os.path.join(OUTPUT_DIR, "waveform_by_rate.png"))
        plot_multiple_spectrograms(wave_files_rate, rates, os.path.join(OUTPUT_DIR, "spectrogram_by_rate.png"))

        plot_multiple_waveforms(wave_files_combined, voices, os.path.join(OUTPUT_DIR, "waveform_combined_default_rate.png"))
        plot_multiple_spectrograms(wave_files_combined, voices,
                                   os.path.join(OUTPUT_DIR, "spectrogram_combined_default_rate.png"))

        status_label.config(text="图像绘制完成，保存在 outputs 文件夹")
    except Exception as e:
        messagebox.showerror("错误", f"可视化失败：{e}")


# 布局界面按钮
btns = [
    ("Step 1: 录音", step1_record),
    ("Step 2: 端点检测", step2_vad),
    ("Step 3: 预处理", step3_preprocess),
    ("Step 4: MFCC 特征", step4_mfcc),
    ("Step 5: 语音识别", step5_recognize),
    ("Step 6: 翻译", step6_translate),
    ("Step 7: 合成", step7_synthesize),
    ("Step 8: 可视化", step8_visualize),
]

for idx, (label, cmd) in enumerate(btns):
    b = tk.Button(root, text=label, width=25, height=2, command=cmd)
    b.grid(row=idx // 2, column=idx % 2, padx=10, pady=5)

# 状态栏
status_label = tk.Label(root, text="欢迎使用语音处理工具", bg="lightgray", anchor="w")
status_label.grid(row=5, column=0, columnspan=2, sticky="we", pady=10)

# 运行界面
root.mainloop()
