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


# 示例用法
if __name__ == "__main__":
    input_mp4 = r"D:\ExpData\temp20250516\Automation\video\server.mp4"
    output_gif = r"D:\ExpData\temp20250516\Automation\video\server.gif"

    mp4_to_gif(
        input_mp4, output_gif,
        scale=0.3,  # 重要：缩小至30%
        fps=8,  # 降低帧率
        end_time=6  # 缩短时长
    )