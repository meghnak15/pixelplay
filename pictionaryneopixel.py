#!/usr/bin/env python3
"""
Pictionary LED Matrix Game
===========================
Hardware:
  - Raspberry Pi
  - Adafruit RGB Matrix Bonnet (HUB75 protocol)
  - Two 64×64 RGB LED matrices chained side by side (128×64 total)
  - CY-822A USB Joystick Encoder board
      Joystick ABS_X / ABS_Y, center=127
        ABS_Y=255 → UP    ABS_Y=0 → DOWN
        ABS_X=255 → LEFT  ABS_X=0 → RIGHT
      BTN_CLEAR → Clear canvas
      BTN_COLOR → Cycle draw color

Run:
  sudo python3 pictionary_neopixel.py

Detect button codes with:
  sudo python3 -c "
  from inputs import get_gamepad
  while True:
      for e in get_gamepad():
          if e.ev_type not in ('Sync', 'Misc'):
              print(e.ev_type, e.code, e.state)"
"""

import time
import threading
from inputs import get_gamepad
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

# MATRIX CONFIG
# Two 64×64 panels chained → 128 wide, 64 tall

OPTIONS = RGBMatrixOptions()
OPTIONS.hardware_mapping         = 'adafruit-hat'
OPTIONS.rows                     = 63
OPTIONS.cols                     = 64        # width of ONE panel
OPTIONS.chain_length             = 2         # two panels chained
OPTIONS.parallel                 = 1
OPTIONS.gpio_slowdown            = 2
OPTIONS.led_rgb_sequence         = 'RGB'     # change to 'GRB' if colors look wrong
OPTIONS.brightness               = 80
OPTIONS.disable_hardware_pulsing = True

# add number of rows and columns as per daisy chain
CANVAS_WIDTH  = 128   # OPTIONS.cols * OPTIONS.chain_length
CANVAS_HEIGHT = 64

# JOYSTICK CONFIG
# Verified axis readings:
#   ABS_Y: 255=UP  127=CENTER  0=DOWN
#   ABS_X: 255=LEFT 127=CENTER  0=RIGHT

JOY_CENTER   = 127
JOY_DEADZONE = 40    # trigger movement outside 127±40 (i.e. <87 or >167)


# BUTTON CODES
# Update these after running the detection snippet above

BTN_CLEAR = "BTN_BASE4"   # ST button  — clears the canvas
BTN_COLOR = "BTN_BASE6"   # K12 button — cycles to next colour


# DRAWING CONFIG

CURSOR_SPEED = 1      # pixels moved per tick
MOVE_HZ      = 40     # movement ticks per second
CURSOR_BLINK = 0.3    # seconds per blink half-cycle


# COLOR PALETTE  (name, graphics.Color)

# Add RGB colour codes as desired
COLORS = [
    ("White",   graphics.Color(255, 255, 255)),
    ("Red",     graphics.Color(255,   0,   0)),
    ("Orange",  graphics.Color(255, 165,   0)),
    ("Yellow",  graphics.Color(255, 255,   0)),
    ("Green",   graphics.Color(  0, 255,   0)),
    ("Cyan",    graphics.Color(  0, 255, 255)),
    ("Blue",    graphics.Color(  0,   0, 255)),
    ("Magenta", graphics.Color(255,   0, 255)),
    ("Purple",  graphics.Color(128,   0, 128)),
    ("Pink",    graphics.Color(255, 105, 180)),
    ("Brown",   graphics.Color(139,  69,  19)),
]



# BRESENHAM LINE  (fills gaps when cursor moves diagonally fast)

def bresenham(x0, y0, x1, y1):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x1 > x0 else -1
    sy = 1 if y1 > y0 else -1
    err = dx - dy
    while True:
        yield x0, y0
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0  += sx
        if e2 < dx:
            err += dx
            y0  += sy



# GAME

class PictionaryGame:
    def __init__(self):
        self.matrix = RGBMatrix(options=OPTIONS)
        self.canvas = self.matrix.CreateFrameCanvas()

        # pixel buffer: (x, y) → graphics.Color
        self.buffer: dict = {}

        # cursor state — protected by self._lock
        self.cursor_x = CANVAS_WIDTH  // 2
        self.cursor_y = CANVAS_HEIGHT // 2
        self.cursor_visible = True

        self.color_index = 0
        self.running     = True

        # Raw joystick axis values (shared between threads)
        self._axis_x = JOY_CENTER
        self._axis_y = JOY_CENTER
        self._lock   = threading.Lock()

    # ── Helpers ───────────────────────────────────────────────────────────────

    @property
    def draw_color(self):
        return COLORS[self.color_index][1]

    def _clamp(self, val, lo, hi):
        return max(lo, min(hi, val))

    # ── Canvas operations ─────────────────────────────────────────────────────

    def paint_line(self, x0, y0, x1, y1):
        """Draw a Bresenham line into the pixel buffer using the current colour."""
        color = self.draw_color
        for x, y in bresenham(x0, y0, x1, y1):
            x = self._clamp(x, 0, CANVAS_WIDTH - 1)
            y = self._clamp(y, 0, CANVAS_HEIGHT - 1)
            self.buffer[(x, y)] = color

    def clear_canvas(self):
        """Erase all drawn pixels and refresh the display immediately."""
        self.buffer.clear()
        self.canvas.Clear()
        self.matrix.SwapOnVSync(self.canvas)
        print("[CLR]  Canvas cleared")

    # ── Rendering ─────────────────────────────────────────────────────────────

    def render(self):
        self.canvas.Clear()

        # --- drawn pixels ---
        for (x, y), color in self.buffer.items():
            self.canvas.SetPixel(x, y, color.red, color.green, color.blue)

        # --- blinking cursor ---
        if self.cursor_visible:
            with self._lock:
                cx, cy = self.cursor_x, self.cursor_y
            c = self.draw_color
            self.canvas.SetPixel(cx, cy, c.red, c.green, c.blue)

        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    # ── Button handlers ───────────────────────────────────────────────────────

    def handle_clear(self):
        self.clear_canvas()

    def handle_color(self):
        self.color_index = (self.color_index + 1) % len(COLORS)
        name = COLORS[self.color_index][0]
        print(f"[COL]  Color → {name}")

    # ── Joystick input thread ──────────────────────────────────────────────────

    def joystick_thread(self):
        """
        Reads raw events from the USB gamepad.
        Axis values are stored for use by the cursor loop.
        Button presses are handled immediately here.
        """
        print("[JOY]  Listening for joystick events…")
        while self.running:
            try:
                for event in get_gamepad():
                    if event.ev_type == "Absolute":
                        if event.code == "ABS_X":
                            with self._lock:
                                self._axis_x = event.state
                        elif event.code == "ABS_Y":
                            with self._lock:
                                self._axis_y = event.state

                    elif event.ev_type == "Key" and event.state == 1:  # press only
                        if event.code == BTN_CLEAR:
                            self.handle_clear()
                        elif event.code == BTN_COLOR:
                            self.handle_color()

            except Exception as exc:
                print(f"[JOY]  Error: {exc}")
                time.sleep(0.05)

    # ── Cursor / draw loop ────────────────────────────────────────────────────

    def cursor_loop(self):
        """
        Polls axis values at MOVE_HZ and moves the cursor accordingly.
        Only paints pixels when the joystick is deflected (not at rest).

        Axis mapping (verified):
          ABS_Y 255 → UP   (dy = -1)
          ABS_Y 0   → DOWN (dy = +1)
          ABS_X 255 → LEFT (dx = -1)
          ABS_X 0   → RIGHT(dx = +1)
        """
        interval = 1.0 / MOVE_HZ
        while self.running:
            with self._lock:
                ax = self._axis_x
                ay = self._axis_y

            dx = 0
            dy = 0

            # X axis: 255=LEFT → dx=-1,  0=RIGHT → dx=+1
            if ax < JOY_CENTER - JOY_DEADZONE:
                dx =  CURSOR_SPEED   # joystick right  (low value)
            elif ax > JOY_CENTER + JOY_DEADZONE:
                dx = -CURSOR_SPEED   # joystick left   (high value)

            # Y axis: 255=UP → dy=-1,  0=DOWN → dy=+1
            if ay < JOY_CENTER - JOY_DEADZONE:
                dy =  CURSOR_SPEED   # joystick down   (low value)
            elif ay > JOY_CENTER + JOY_DEADZONE:
                dy = -CURSOR_SPEED   # joystick up     (high value)

            if dx != 0 or dy != 0:
                with self._lock:
                    old_x = self.cursor_x
                    old_y = self.cursor_y
                    new_x = self._clamp(old_x + dx, 0, CANVAS_WIDTH  - 1)
                    new_y = self._clamp(old_y + dy, 0, CANVAS_HEIGHT - 1)
                    self.cursor_x = new_x
                    self.cursor_y = new_y

                # Paint only while moving
                self.paint_line(old_x, old_y, new_x, new_y)

            time.sleep(interval)

    # ── Main entry point ──────────────────────────────────────────────────────

    def run(self):
        print(f"[GAME] Pictionary  {CANVAS_WIDTH}×{CANVAS_HEIGHT}")
        print(f"[GAME] Clear={BTN_CLEAR}  Color={BTN_COLOR}")
        print(f"[GAME] {len(COLORS)} colours available  |  speed={CURSOR_SPEED}px @ {MOVE_HZ}Hz")
        self.clear_canvas()

        joy_t    = threading.Thread(target=self.joystick_thread, daemon=True)
        cursor_t = threading.Thread(target=self.cursor_loop,     daemon=True)
        joy_t.start()
        cursor_t.start()

        last_blink = time.time()
        try:
            while self.running:
                now = time.time()
                if now - last_blink >= CURSOR_BLINK:
                    self.cursor_visible = not self.cursor_visible
                    last_blink = now
                self.render()
                time.sleep(1 / 60)

        except KeyboardInterrupt:
            print("\n[GAME] Interrupted — shutting down")
        finally:
            self.running = False
            self.canvas.Clear()
            self.matrix.SwapOnVSync(self.canvas)
            print("[GAME] Display cleared. Goodbye!")



if __name__ == "__main__":
    game = PictionaryGame()
    game.run()
