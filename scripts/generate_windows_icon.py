from __future__ import annotations

import struct
from pathlib import Path


ICON_SIZES = (16, 32, 48, 256)
SUPERSAMPLE = 4


def _in_rounded_rect(px: float, py: float, x: float, y: float, width: float, height: float, radius: float) -> bool:
    if px < x or py < y or px > x + width or py > y + height:
        return False
    nearest_x = min(max(px, x + radius), x + width - radius)
    nearest_y = min(max(py, y + radius), y + height - radius)
    return (px - nearest_x) ** 2 + (py - nearest_y) ** 2 <= radius**2


def _circle(px: float, py: float, cx: float, cy: float, radius: float) -> bool:
    return (px - cx) ** 2 + (py - cy) ** 2 <= radius**2


def _segment_distance(px: float, py: float, x1: float, y1: float, x2: float, y2: float) -> float:
    dx = x2 - x1
    dy = y2 - y1
    length_squared = dx * dx + dy * dy
    if length_squared == 0:
        return ((px - x1) ** 2 + (py - y1) ** 2) ** 0.5
    ratio = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / length_squared))
    nearest_x = x1 + ratio * dx
    nearest_y = y1 + ratio * dy
    return ((px - nearest_x) ** 2 + (py - nearest_y) ** 2) ** 0.5


def _smile_points() -> list[tuple[float, float]]:
    points: list[tuple[float, float]] = []
    for index in range(25):
        t = index / 24
        one = 1 - t
        x = one**3 * 46 + 3 * one**2 * t * 54 + 3 * one * t**2 * 74 + t**3 * 82
        y = one**3 * 78 + 3 * one**2 * t * 86 + 3 * one * t**2 * 86 + t**3 * 78
        points.append((x, y))
    return points


SMILE_POINTS = _smile_points()


def _lerp(start: int, end: int, ratio: float) -> int:
    return round(start + (end - start) * ratio)


def _pixel_color(px: float, py: float) -> tuple[int, int, int, int]:
    transparent = (0, 0, 0, 0)
    color = transparent

    if _in_rounded_rect(px, py, 16, 14, 96, 100, 24):
        color = (15, 23, 42, 255)

    if _in_rounded_rect(px, py, 24, 22, 80, 84, 18):
        ratio = max(0.0, min(1.0, ((px - 22) + (py - 18)) / ((106 - 22) + (110 - 18))))
        color = (_lerp(34, 37, ratio), _lerp(197, 99, ratio), _lerp(94, 235, ratio), 255)

    if _circle(px, py, 48, 54, 8) or _circle(px, py, 80, 54, 8):
        color = (248, 250, 252, 255)

    if 42 <= px <= 86 and 73 <= py <= 90:
        for start, end in zip(SMILE_POINTS, SMILE_POINTS[1:]):
            if _segment_distance(px, py, start[0], start[1], end[0], end[1]) <= 3.5:
                color = (248, 250, 252, 255)
                break

    if _segment_distance(px, py, 64, 14, 64, 4) <= 4:
        color = (34, 197, 94, 255)

    if _circle(px, py, 64, 4, 4):
        color = (34, 197, 94, 255)

    return color


def _render_rgba(size: int) -> list[tuple[int, int, int, int]]:
    high_size = size * SUPERSAMPLE
    high_pixels: list[tuple[int, int, int, int]] = []
    for y in range(high_size):
        source_y = (y + 0.5) * 128 / high_size
        for x in range(high_size):
            source_x = (x + 0.5) * 128 / high_size
            high_pixels.append(_pixel_color(source_x, source_y))

    pixels: list[tuple[int, int, int, int]] = []
    for y in range(size):
        for x in range(size):
            samples = [
                high_pixels[(y * SUPERSAMPLE + sy) * high_size + (x * SUPERSAMPLE + sx)]
                for sy in range(SUPERSAMPLE)
                for sx in range(SUPERSAMPLE)
            ]
            pixels.append(tuple(round(sum(sample[channel] for sample in samples) / len(samples)) for channel in range(4)))
    return pixels


def _dib_from_rgba(size: int, pixels: list[tuple[int, int, int, int]]) -> bytes:
    pixel_bytes = bytearray()
    for y in range(size - 1, -1, -1):
        for x in range(size):
            red, green, blue, alpha = pixels[y * size + x]
            pixel_bytes.extend((blue, green, red, alpha))

    mask_stride = ((size + 31) // 32) * 4
    mask_bytes = b"\x00" * (mask_stride * size)
    header = struct.pack(
        "<IiiHHIIiiII",
        40,
        size,
        size * 2,
        1,
        32,
        0,
        len(pixel_bytes),
        0,
        0,
        0,
        0,
    )
    return header + bytes(pixel_bytes) + mask_bytes


def build_icon() -> bytes:
    images = [(size, _dib_from_rgba(size, _render_rgba(size))) for size in ICON_SIZES]
    header = struct.pack("<HHH", 0, 1, len(images))
    directory = bytearray()
    offset = 6 + 16 * len(images)
    image_data = bytearray()
    for size, data in images:
        directory.extend(
            struct.pack(
                "<BBBBHHII",
                0 if size == 256 else size,
                0 if size == 256 else size,
                0,
                0,
                1,
                32,
                len(data),
                offset,
            )
        )
        image_data.extend(data)
        offset += len(data)
    return header + bytes(directory) + bytes(image_data)


def main() -> int:
    target = Path(__file__).resolve().parents[1] / "packaging" / "windows" / "JarvisLite.ico"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(build_icon())
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
