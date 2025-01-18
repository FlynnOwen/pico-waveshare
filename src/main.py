from machine import Pin
import framebuf
import requests
import time
from gc import collect


from config import SSID, SSID_PASSWORD, RTT_URL, RTT_USER, RTT_PASSWORD
from train_image import TRAIN_IMAGE
from wifi import connect
from waveshare import EPD_WIDTH, EPD_HEIGHT, EPD_2in9, WHITE, BLACK
from render_utils import load_bitmap, LandscapeBuffer


class TrainInfo:
    def __init__(
        self,
        provider: str,
        platform: str,
        origin_time: str,
        origin_place: str,
        dest_time: str,
        dest_place: str,
    ) -> None:
        self.provider = f"{provider: <7}"
        self.origin_place = f"{origin_place: <12}"
        self.origin_time = f"{origin_time[:2]}:{origin_time[2:]}"
        self.platform = f"{platform: <7}"
        self.dest_place = f"{dest_place: <12}"
        self.dest_time = f"{dest_time[:2]}:{dest_time[2:]}"

    @classmethod
    def from_rtt_payload(cls, rtt_payload: dict):
        train = rtt_payload["locationDetail"]
        return cls(
            provider=rtt_payload["atocCode"],
            origin_place=train["origin"][0]["tiploc"],
            origin_time=train["origin"][0]["publicTime"],
            platform=train["platform"],
            dest_place=train["destination"][0]["tiploc"],
            dest_time=train["destination"][0]["publicTime"],
        )

    @property
    def first_line(self):
        return f" {self.provider}{self.origin_place}{self.origin_time}"

    @property
    def second_line(self):
        return f" {self.platform}{self.dest_place}{self.dest_time}"

    def __str__(self):
        return f"{self.first_line}\n{self.second_line}"


def render_trains(rtt_payload: list[dict]):
    """
    Render a collection of train timetable information
    to the epaper display.
    """
    idx = 0
    cnt = 0
    render_x = 90
    render_y = 8
    hline_len = 206
    landscape_buffer.hline(render_x, render_y - 4, hline_len, BLACK)
    while idx < len(rtt_payload) and cnt < 5:
        if rtt_payload[idx]["serviceType"] == "train":
            train_info = TrainInfo.from_rtt_payload(rtt_payload[idx])
            landscape_buffer.text(train_info.first_line, render_x, render_y, BLACK)
            landscape_buffer.text(
                train_info.second_line, render_x, render_y + 10, BLACK
            )
            landscape_buffer.hline(render_x, render_y + 20, hline_len, BLACK)
            cnt += 1
            render_y += 24
        idx += 1


def get_trains(timeout: int = 30):
    return requests.get(
        url=RTT_URL, auth=(RTT_USER, RTT_PASSWORD), timeout=timeout
    ).json()["services"]


def update(delay: float):
    """
    Request new trains, render to screen

    :param delay: How often to update with new information.
    """
    collect()
    rtt_payload = get_trains(timeout=30)
    landscape_buffer.fill(WHITE)

    render_trains(rtt_payload)

    landscape_inverted = landscape_buffer.invert_buffer()
    portrait_fb = framebuf.FrameBuffer(
        landscape_inverted, EPD_WIDTH, EPD_HEIGHT, framebuf.MONO_HLSB
    )

    load_bitmap(portrait_fb, TRAIN_IMAGE, 128, 90)
    epd.display(landscape_inverted)
    time.sleep(delay)


if __name__ == "__main__":
    epd = EPD_2in9()
    epd.init()
    pin = Pin("LED", Pin.OUT)
    ip = connect(pin=pin, ssid=SSID, ssid_password=SSID_PASSWORD)
    landscape_buffer = LandscapeBuffer(width=EPD_HEIGHT, height=EPD_WIDTH)

    try:
        while True:
            update(90)
    except Exception as e:  # noqa: E722
        print(e)
        pin.off()
