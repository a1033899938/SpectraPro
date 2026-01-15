"""
Author: Junjie-Xie
Updated: 2025/07/18
Functions: 将MP4视频文件转换为GIF动图（支持指定时间段、帧率调整、分辨率缩放，优化内存占用）
"""

from moviepy.editor import VideoFileClip, ImageSequenceClip

def mp4_to_gif(input_path, output_path, start_time=0, end_time=None, fps=10, scale=0.5):
    """优化内存占用的MP4转GIF脚本"""
    try:
        with VideoFileClip(input_path) as clip:
            if end_time is None:
                end_time = clip.duration
            clip = clip.subclip(start_time, end_time)

            # 大幅降低分辨率（关键优化点）
            width = int(clip.size[0] * scale)
            height = int(clip.size[1] * scale)
            clip = clip.resize((width, height))

            # 直接获取帧（无需重复转换为np.array）
            frames = [frame for frame in clip.iter_frames(fps=fps)]
            ImageSequenceClip(frames, fps=fps).write_gif(output_path)

        print(f"成功转换：{output_path}，尺寸={width}x{height}")

    except MemoryError:
        print("错误：内存不足！请进一步降低分辨率或缩短时长。")
        raise
    except Exception as e:
        print(f"转换失败：{str(e)}")
        raise


def m1v_to_gif(input_path, output_path, start_time=0, end_time=None, fps=10, scale=0.5):
    """
    将M1V格式视频转换为GIF，优化内存占用

    参数:
        input_path: M1V文件路径（如 "video.m1v"）
        output_path: 输出GIF路径（如 "output.gif"）
        start_time: 起始时间（秒，默认0）
        end_time: 结束时间（秒，默认视频时长）
        fps: GIF帧率（默认10，降低可减少内存占用）
        scale: 分辨率缩放比例（默认0.5，0.1-1.0之间，越小内存占用越低）
    """
    try:
        # 读取M1V文件（moviepy支持解析MPEG-1流）
        with VideoFileClip(input_path) as clip:
            # 截取视频片段（若未指定结束时间则取完整视频）
            if end_time is None:
                end_time = clip.duration
            # 确保时间范围有效
            if start_time < 0 or end_time > clip.duration or start_time >= end_time:
                raise ValueError("无效的时间范围！请检查start_time和end_time。")
            clip = clip.subclip(start_time, end_time)

            # 降低分辨率（关键优化：减少内存占用）
            width = int(clip.size[0] * scale)
            height = int(clip.size[1] * scale)
            # 若缩放后尺寸过小，设置最小尺寸避免错误
            width = max(width, 16)
            height = max(height, 16)
            clip = clip.resize((width, height))

            # 逐帧提取并生成GIF（直接迭代帧，减少中间转换）
            frames = [frame for frame in clip.iter_frames(fps=fps)]
            # 用提取的帧生成GIF
            ImageSequenceClip(frames, fps=fps).write_gif(
                output_path,
                program='ffmpeg',  # 优先用ffmpeg加速处理
                # optimize=True  # 优化GIF大小
            )

        print(f"成功转换：{output_path}，尺寸={width}x{height}，帧率={fps}")

    except MemoryError:
        print("错误：内存不足！请尝试降低scale（如0.3）或fps（如5）。")
        raise
    except Exception as e:
        print(f"转换失败：{str(e)}")
        raise

# 示例用法
if __name__ == "__main__":
    import os
    path = r"D:\FDTDSimFile\movie"
    all_files = []
    # 遍历文件夹及其子文件夹
    for root, dirs, files in os.walk(path):
        for file in files:
            # 拼接文件的完整路径
            file_path = os.path.join(root, file)
            all_files.append(file_path)
            output_gif = os.path.join(root, file.replace(".m1v", ".gif"))

            m1v_to_gif(
                file_path, output_gif,
                scale=0.3,  # 重要：缩小至30%
                fps=10,  # 降低帧率
                start_time=0  # 缩短时长
            )