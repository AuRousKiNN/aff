from aff import *

def test_aff_objects():
    # 1. Header
    header = AffHeader(audio_offset=10, timing_point_density_factor=1.5)
    print(f"Header: {header}")

    # 3. Timing
    timing = Timing(time=0, bpm=180.0, beats=4.0)
    print(f"Timing: {timing}")

    # 4. Tap
    tap = Tap(time=1000, lane=1)
    print(f"Tap: {tap}")

    # Hold
    hold = Hold(start_time=1000, end_time=2000, lane=2)
    print(f"Hold: {hold}")

    # 5. Arc & Arctap
    arctap1 = Arctap(time=1200)
    arctap2 = Arctap(time=1400)
    arc = Arc(
        start_time=1000, end_time=2000,
        start_x=0.0, end_x=1.0,
        easing="s",
        start_y=1.0, end_y=0.0,
        color=0,
        hitsound="none",
        arctype="false",
        smoothness=None,
        arctaps=[arctap1, arctap2]
    )
    print(f"Arc: {arc}")

    # 6. Camera
    camera = Camera(
        time=500,
        trans_x=0, trans_y=0, trans_z=0,
        angle_xoz=0, angle_yoz=0, angle_xoy=0,
        easing="l", duration=1000
    )
    print(f"Camera: {camera}")

    # 7. SceneControl
    sc = SceneControl(time=3000, type="trackhide")
    print(f"SceneControl: {sc}")

    # 9. Flick
    flick = Flick(time=4000, x=0.5, y=0.5, vx=1.0, vy=0.0)
    print(f"Flick: {flick}")

    # 8. TimingGroup
    tg = TimingGroup(
        options=["noinput"],
        notes=[tap, hold]
    )
    print(f"TimingGroup: {tg}")

    # 10. Test parsing and saving
    chart_data = """AudioOffset:0
TimingPointDensityFactor:1.0
-
timing(0,180.00,4.00);
(1000,2.00);
hold(2000,3000,3.00);
"""
    with open("test.aff", "w", encoding="utf-8") as f:
        f.write(chart_data)

    chart = AffChart.from_file("test.aff")
    print("\nParsed Chart from test.aff:")
    print(f"Header: {chart.header}")
    print(f"Total notes: {len(chart.notes)}")
    for note in chart.notes:
        print(f"  {note}")

    print("\nAll objects verified successfully.")

if __name__ == "__main__":
    test_aff_objects()
