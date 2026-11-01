"""
MAZE SOLVER — Backtracking + Stack
Giao diện Pygame phong cách Dark Blue.

Cài đặt:
    pip install -r requirements.txt

Chạy:
    python main.py

Điều khiển:
    - Chạy: tự động mô phỏng
    - Bước tiếp: chạy đúng một thao tác thuật toán
    - Tạm dừng: dừng/chạy tiếp mô phỏng tự động
    - Mê cung mới: tạo mê cung ngẫu nhiên
    - Xóa đường: xóa tường bằng cách nhấp/ kéo chuột vào ô
    - Thêm tường: bật chế độ thêm tường rồi nhấp/ kéo chuột vào ô
    - -SIZE / +SIZE: thay đổi kích thước mê cung
    - HIỆN/ẨN NGÕ CỤT: hiện hoặc xóa các ô đã thăm nhưng bị bỏ (màu hồng)
"""

import random
import sys
import time
from collections import deque

import pygame


# =========================
# 1. CẤU HÌNH GIAO DIỆN
# =========================

pygame.init()
pygame.display.set_caption("MAZE SOLVER | Backtracking + Stack")

SCREEN_WIDTH = 1120
SCREEN_HEIGHT = 760
PANEL_WIDTH = 300
TOP_HEIGHT = 92
BOTTOM_HEIGHT = 54

COLORS = {
    "background": (10, 18, 35),
    "panel": (17, 29, 52),
    "panel_light": (25, 42, 70),
    "border": (43, 65, 98),
    "text": (231, 240, 255),
    "muted": (145, 165, 195),
    "accent": (58, 170, 230),
    "accent_hover": (83, 190, 245),
    "wall": (47, 66, 96),
    "floor": (222, 233, 247),
    "start": (42, 190, 135),
    "goal": (245, 157, 75),
    "visited": (100, 174, 220),
    "dead": (230, 179, 186),
    "current": (255, 211, 82),
    "solution": (44, 205, 145),
    "danger": (235, 95, 105),
    "white": (255, 255, 255),
}

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("segoeui", 17)
SMALL_FONT = pygame.font.SysFont("segoeui", 14)
TITLE_FONT = pygame.font.SysFont("segoeui", 27, bold=True)
BIG_FONT = pygame.font.SysFont("segoeui", 21, bold=True)


# =========================
# 2. HÀM TIỆN ÍCH GIAO DIỆN
# =========================

def draw_text(surface, text, x, y, color=None, font=None):
    """Vẽ văn bản tại tọa độ (x, y)."""
    if color is None:
        color = COLORS["text"]
    if font is None:
        font = FONT
    image = font.render(str(text), True, color)
    surface.blit(image, (x, y))


def draw_button(surface, rect, label, mouse_pos, active=False, disabled=False):
    """Vẽ nút giao diện."""
    if disabled:
        color = (35, 48, 69)
    elif active:
        color = COLORS["accent"]
    elif rect.collidepoint(mouse_pos):
        color = COLORS["accent_hover"]
    else:
        color = COLORS["panel_light"]

    pygame.draw.rect(surface, color, rect, border_radius=9)
    pygame.draw.rect(surface, COLORS["border"], rect, width=1, border_radius=9)
    text_color = COLORS["white"] if not disabled else COLORS["muted"]
    label_image = SMALL_FONT.render(label, True, text_color)
    surface.blit(label_image, label_image.get_rect(center=rect.center))


def draw_panel_card(surface, rect):
    pygame.draw.rect(surface, COLORS["panel"], rect, border_radius=12)
    pygame.draw.rect(surface, COLORS["border"], rect, width=1, border_radius=12)


# =========================
# 3. MÔ HÌNH MÊ CUNG
# =========================

class Maze:
    """Lưu mê cung dưới dạng ma trận: 0 là đường, 1 là tường."""

    def __init__(self, rows=17, cols=21):
        self.rows = rows
        self.cols = cols
        self.start = (0, 0)
        self.goal = (rows - 1, cols - 1)
        self.grid = []
        self.generate()

    def generate(self):
        """Tạo mê cung ngẫu nhiên có đường kết nối cơ bản từ S đến E."""
        self.start = (0, 0)
        self.goal = (self.rows - 1, self.cols - 1)
        self.grid = [
            [1 if random.random() < 0.27 else 0 for _ in range(self.cols)]
            for _ in range(self.rows)
        ]

        # Tạo một lối đi bảo đảm từ góc trên trái đến góc dưới phải.
        r, c = self.start
        self.grid[r][c] = 0
        while (r, c) != self.goal:
            choices = []
            if r < self.rows - 1:
                choices.append((r + 1, c))
            if c < self.cols - 1:
                choices.append((r, c + 1))
            r, c = random.choice(choices)
            self.grid[r][c] = 0

        self.grid[self.goal[0]][self.goal[1]] = 0

    def resize(self, rows, cols):
        """Thay đổi kích thước mê cung và tạo bản đồ mới."""
        self.rows = max(7, min(31, rows))
        self.cols = max(7, min(35, cols))
        self.generate()

    def toggle_wall(self, row, col, wall_value):
        """Thay đổi tường tại ô, không cho sửa điểm đầu/cuối."""
        if (row, col) not in (self.start, self.goal):
            self.grid[row][col] = 1 if wall_value else 0


# =========================
# 4. THUẬT TOÁN BACKTRACKING + STACK
# =========================

class MazeSolver:
    """
    Backtracking không đệ quy, sử dụng Stack tường minh.

    Mỗi phần tử Stack là [row, col, next_direction].
    next_direction ghi nhớ hướng tiếp theo cần thử tại ô đó.
    Nhờ vậy khi quay lại một ô, thuật toán không thử lại hướng cũ.
    """

    DIRECTIONS = [
        (-1, 0, "Lên"),
        (0, 1, "Phải"),
        (1, 0, "Xuống"),
        (0, -1, "Trái"),
    ]

    def __init__(self, maze):
        self.maze = maze
        self.visited = set()
        self.path = []
        self.stack = []
        self.finished = False
        self.found = False
        self.backtracks = 0
        self.visited_count = 0
        self.steps = 0
        self.message = "Sẵn sàng tìm đường"
        self.started_at = None
        self.elapsed = 0.0

        sr, sc = maze.start
        self.stack.append([sr, sc, 0])
        self.path.append((sr, sc))
        self.visited.add((sr, sc))
        self.visited_count = 1
        self.started_at = time.perf_counter()

    def step(self):
        """Thực hiện đúng một thao tác của thuật toán."""
        if self.finished:
            return

        self.steps += 1
        current = self.stack[-1]
        row, col, direction_index = current
        position = (row, col)

        if position == self.maze.goal:
            self.finished = True
            self.found = True
            self.message = "Đã tìm thấy lối thoát!"
            self.elapsed = time.perf_counter() - self.started_at
            return

        if direction_index >= len(self.DIRECTIONS):
            # Đã thử hết bốn hướng: quay lui.
            self.stack.pop()
            if self.path:
                self.path.pop()
            self.backtracks += 1

            if not self.stack:
                self.finished = True
                self.found = False
                self.message = "Không tìm thấy đường thoát."
                self.elapsed = time.perf_counter() - self.started_at
            else:
                self.message = "Ngõ cụt — quay lui"
            return

        # Ghi nhận hướng này đã được thử trước khi xét ô kế tiếp.
        dr, dc, direction_name = self.DIRECTIONS[direction_index]
        current[2] += 1

        next_row = row + dr
        next_col = col + dc
        next_position = (next_row, next_col)

        inside = (
            0 <= next_row < self.maze.rows
            and 0 <= next_col < self.maze.cols
        )

        if (
            inside
            and self.maze.grid[next_row][next_col] == 0
            and next_position not in self.visited
        ):
            self.visited.add(next_position)
            self.visited_count += 1
            self.stack.append([next_row, next_col, 0])
            self.path.append(next_position)
            self.message = f"Di chuyển: {direction_name}"
        else:
            self.message = f"Thử hướng {direction_name}: không hợp lệ"

    def run_to_end(self):
        """Chạy thuật toán đến khi kết thúc, có giới hạn an toàn."""
        safety_limit = self.maze.rows * self.maze.cols * 8
        count = 0
        while not self.finished and count < safety_limit:
            self.step()
            count += 1

    def stack_positions(self):
        """Trả về danh sách tọa độ hiện có trong Stack."""
        return [(item[0], item[1]) for item in self.stack]


# =========================
# 5. VẼ MÊ CUNG VÀ TRẠNG THÁI
# =========================

def get_maze_rect(maze):
    available_width = SCREEN_WIDTH - PANEL_WIDTH - 70
    available_height = SCREEN_HEIGHT - TOP_HEIGHT - BOTTOM_HEIGHT - 55
    cell_size = min(
        available_width // maze.cols,
        available_height // maze.rows,
        34
    )
    cell_size = max(12, cell_size)
    width = cell_size * maze.cols
    height = cell_size * maze.rows
    x = 35 + max(0, (available_width - width) // 2)
    y = TOP_HEIGHT + 25 + max(0, (available_height - height) // 2)
    return pygame.Rect(x, y, width, height), cell_size


def draw_maze(surface, maze, solver, mouse_pos, wall_mode, show_dead=True):
    maze_rect, cell_size = get_maze_rect(maze)
    path_set = set(solver.path) if solver else set()

    for row in range(maze.rows):
        for col in range(maze.cols):
            cell_rect = pygame.Rect(
                maze_rect.x + col * cell_size,
                maze_rect.y + row * cell_size,
                cell_size - 2,
                cell_size - 2,
            )
            position = (row, col)

            if maze.grid[row][col] == 1:
                color = COLORS["wall"]
            elif solver and position in path_set:
                color = COLORS["visited"]
            elif solver and show_dead and position in solver.visited:
                # Ô đã thăm nhưng đã bị bỏ (ngõ cụt / bước trùng)
                color = COLORS["dead"]
            else:
                color = COLORS["floor"]

            if solver and solver.found and position in path_set:
                color = COLORS["solution"]

            if solver and solver.stack and position == tuple(solver.stack[-1][:2]):
                color = COLORS["current"]

            if position == maze.start:
                color = COLORS["start"]
            elif position == maze.goal:
                color = COLORS["goal"]

            pygame.draw.rect(surface, color, cell_rect, border_radius=3)

            if cell_size >= 23:
                if position == maze.start:
                    draw_text(surface, "S", cell_rect.x + 5, cell_rect.y + 2,
                              COLORS["white"], SMALL_FONT)
                elif position == maze.goal:
                    draw_text(surface, "E", cell_rect.x + 5, cell_rect.y + 2,
                              COLORS["white"], SMALL_FONT)

    if wall_mode:
        pygame.draw.rect(surface, COLORS["accent"], maze_rect, width=2)


def draw_stack_panel(surface, solver, x, y, width, height):
    rect = pygame.Rect(x, y, width, height)
    draw_panel_card(surface, rect)
    draw_text(surface, "STACK  |  LIFO", x + 16, y + 13, COLORS["accent"], BIG_FONT)
    draw_text(surface, "Đỉnh Stack nằm ở trên cùng", x + 16, y + 42, COLORS["muted"], SMALL_FONT)

    if not solver:
        draw_text(surface, "Chưa khởi tạo", x + 16, y + 75, COLORS["muted"])
        return

    positions = solver.stack_positions()
    visible = positions[-3:]
    item_y = y + 75

    if not visible:
        draw_text(surface, "Stack rỗng", x + 16, item_y, COLORS["danger"])
        return

    for index, (row, col) in enumerate(reversed(visible)):
        item_rect = pygame.Rect(x + 16, item_y, width - 32, 27)
        is_top = index == 0
        color = COLORS["accent"] if is_top else COLORS["panel_light"]
        pygame.draw.rect(surface, color, item_rect, border_radius=6)
        label = f"({row}, {col})" + ("   ← TOP" if is_top else "")
        draw_text(surface, label, item_rect.x + 10, item_rect.y + 5,
                  COLORS["white"] if is_top else COLORS["muted"], SMALL_FONT)
        item_y += 32


# =========================
# 6. GIAO DIỆN CHÍNH
# =========================

def main():
    maze = Maze(17, 21)
    solver = None
    running_auto = False
    wall_mode = False
    show_dead = True
    auto_delay = 90
    last_auto_step = 0
    status_message = "Tạo mê cung hoặc nhấn CHẠY để bắt đầu."
    buttons = {}

    def reset_solver():
        nonlocal solver, running_auto, status_message
        solver = MazeSolver(maze)
        running_auto = False
        status_message = "Đã khởi tạo Stack tại điểm S."

    def new_maze():
        nonlocal solver, running_auto, status_message
        maze.generate()
        solver = None
        running_auto = False
        status_message = "Đã tạo mê cung mới."

    def build_buttons():
        buttons.clear()
        x = SCREEN_WIDTH - PANEL_WIDTH + 20
        y = 132
        w = 120
        h = 32
        gap = 7

        buttons["run"] = pygame.Rect(x, y, w, h)
        buttons["step"] = pygame.Rect(x + w + 10, y, w, h)
        y += h + gap
        buttons["pause"] = pygame.Rect(x, y, w, h)
        buttons["reset"] = pygame.Rect(x + w + 10, y, w, h)
        y += h + gap
        buttons["new"] = pygame.Rect(x, y, 250, h)
        y += h + gap
        buttons["minus"] = pygame.Rect(x, y, 72, h)
        buttons["plus"] = pygame.Rect(x + 80, y, 72, h)
        buttons["wall"] = pygame.Rect(x + 160, y, 90, h)
        y += h + gap
        buttons["slower"] = pygame.Rect(x, y, w, h)
        buttons["faster"] = pygame.Rect(x + w + 10, y, w, h)
        y += h + gap
        buttons["dead"] = pygame.Rect(x, y, 250, h)

    build_buttons()
    reset_solver()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(COLORS["background"])

        # Header
        pygame.draw.rect(screen, COLORS["panel"], (0, 0, SCREEN_WIDTH, TOP_HEIGHT))
        draw_text(screen, "MAZE SOLVER", 30, 17, COLORS["text"], TITLE_FONT)
        draw_text(screen, "BACKTRACKING  +  STACK", 32, 54, COLORS["accent"], SMALL_FONT)
        draw_text(screen, "MÔ PHỎNG THUẬT TOÁN TÌM ĐƯỜNG", 560, 35,
                  COLORS["muted"], FONT)

        # Maze area
        maze_area = pygame.Rect(18, TOP_HEIGHT + 10,
                                SCREEN_WIDTH - PANEL_WIDTH - 25,
                                SCREEN_HEIGHT - TOP_HEIGHT - BOTTOM_HEIGHT - 15)
        pygame.draw.rect(screen, (13, 24, 44), maze_area, border_radius=14)
        draw_maze(screen, maze, solver, mouse_pos, wall_mode, show_dead)

        # Side panel
        panel_x = SCREEN_WIDTH - PANEL_WIDTH
        pygame.draw.rect(screen, COLORS["panel"], (panel_x, TOP_HEIGHT,
                                                   PANEL_WIDTH, SCREEN_HEIGHT - TOP_HEIGHT))
        draw_text(screen, "ĐIỀU KHIỂN", panel_x + 20, TOP_HEIGHT + 12,
                  COLORS["text"], BIG_FONT)

        labels = {
            "run": "CHẠY",
            "step": "BƯỚC TIẾP",
            "pause": "TẠM DỪNG",
            "reset": "ĐẶT LẠI",
            "new": "MÊ CUNG MỚI",
            "minus": "-SIZE",
            "plus": "+SIZE",
            "wall": "THÊM TƯỜNG" if not wall_mode else "ĐANG VẼ",
            "dead": "ẨN NGÕ CỤT" if show_dead else "HIỆN NGÕ CỤT",
            "slower": "CHẬM HƠN",
            "faster": "NHANH HƠN",
        }

        for key, rect in buttons.items():
            active = ((key == "wall" and wall_mode) or (key == "pause" and running_auto)
                      or (key == "dead" and show_dead))
            draw_button(screen, rect, labels[key], mouse_pos, active=active)

        draw_text(screen, f"Kích thước: {maze.rows} x {maze.cols}",
                  panel_x + 20, 367, COLORS["muted"], SMALL_FONT)
        draw_text(screen, f"Tốc độ: {1000 / auto_delay:.1f} bước/giây",
                  panel_x + 20, 386, COLORS["muted"], SMALL_FONT)

        # Statistics
        stats_y = 410
        stats_rect = pygame.Rect(panel_x + 15, stats_y, PANEL_WIDTH - 30, 100)
        draw_panel_card(screen, stats_rect)
        draw_text(screen, "THỐNG KÊ", stats_rect.x + 14, stats_rect.y + 10,
                  COLORS["accent"], BIG_FONT)

        if solver:
            draw_text(screen, f"Ô đã thăm: {solver.visited_count}",
                      stats_rect.x + 14, stats_rect.y + 38, COLORS["text"], SMALL_FONT)
            draw_text(screen, f"Số lần quay lui: {solver.backtracks}",
                      stats_rect.x + 14, stats_rect.y + 58, COLORS["text"], SMALL_FONT)
            draw_text(screen, f"Độ dài đường hiện tại: {len(solver.path)}",
                      stats_rect.x + 14, stats_rect.y + 78, COLORS["text"], SMALL_FONT)
        else:
            draw_text(screen, "Chưa chạy thuật toán", stats_rect.x + 14,
                      stats_rect.y + 45, COLORS["muted"], SMALL_FONT)

        stack_y = stats_y + 108
        draw_stack_panel(screen, solver, panel_x + 15, stack_y,
                         PANEL_WIDTH - 30, 172)

        # Footer/status
        pygame.draw.rect(screen, COLORS["panel"], (0, SCREEN_HEIGHT - BOTTOM_HEIGHT,
                                                   SCREEN_WIDTH, BOTTOM_HEIGHT))
        draw_text(screen, status_message, 25, SCREEN_HEIGHT - 37,
                  COLORS["text"], SMALL_FONT)
        if solver and solver.finished:
            result = "THÀNH CÔNG" if solver.found else "THẤT BẠI"
            draw_text(screen, f"{result} | {solver.elapsed:.4f}s",
                      SCREEN_WIDTH - 245, SCREEN_HEIGHT - 37,
                      COLORS["solution"] if solver.found else COLORS["danger"],
                      SMALL_FONT)

        pygame.display.flip()

        # Automatic animation
        now = pygame.time.get_ticks()
        if running_auto and solver and not solver.finished:
            if now - last_auto_step >= auto_delay:
                solver.step()
                last_auto_step = now
                status_message = solver.message
                if solver.finished:
                    running_auto = False
                    status_message = solver.message

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked_button = False
                for key, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        clicked_button = True

                        if key == "run":
                            if solver is None or solver.finished:
                                reset_solver()
                            running_auto = True
                            last_auto_step = 0
                            status_message = "Đang chạy thuật toán..."
                        elif key == "step":
                            if solver is None or solver.finished:
                                reset_solver()
                            running_auto = False
                            solver.step()
                            status_message = solver.message
                        elif key == "pause":
                            running_auto = not running_auto
                            status_message = "Đang chạy..." if running_auto else "Đã tạm dừng."
                        elif key == "reset":
                            reset_solver()
                        elif key == "new":
                            new_maze()
                        elif key == "minus":
                            maze.resize(maze.rows - 2, maze.cols - 2)
                            reset_solver()
                        elif key == "plus":
                            maze.resize(maze.rows + 2, maze.cols + 2)
                            reset_solver()
                        elif key == "wall":
                            wall_mode = not wall_mode
                            running_auto = False
                        elif key == "dead":
                            show_dead = not show_dead
                            status_message = ("Đang hiện các ô ngõ cụt (màu hồng)."
                                              if show_dead else "Đã ẩn các ô ngõ cụt.")
                        elif key == "slower":
                            auto_delay = min(500, auto_delay + 20)
                        elif key == "faster":
                            auto_delay = max(15, auto_delay - 20)
                        break

                if not clicked_button:
                    maze_rect, cell_size = get_maze_rect(maze)
                    if maze_rect.collidepoint(event.pos):
                        col = (event.pos[0] - maze_rect.x) // cell_size
                        row = (event.pos[1] - maze_rect.y) // cell_size
                        if 0 <= row < maze.rows and 0 <= col < maze.cols:
                            if wall_mode:
                                maze.toggle_wall(row, col, 1)
                            else:
                                maze.toggle_wall(row, col, 0)
                            solver = None
                            running_auto = False
                            status_message = "Đã chỉnh sửa mê cung. Nhấn ĐẶT LẠI để tìm đường."

            if event.type == pygame.MOUSEMOTION and event.buttons[0]:
                maze_rect, cell_size = get_maze_rect(maze)
                if maze_rect.collidepoint(event.pos):
                    col = (event.pos[0] - maze_rect.x) // cell_size
                    row = (event.pos[1] - maze_rect.y) // cell_size
                    if 0 <= row < maze.rows and 0 <= col < maze.cols:
                        if wall_mode:
                            maze.toggle_wall(row, col, 1)
                        else:
                            maze.toggle_wall(row, col, 0)
                        solver = None
                        running_auto = False

        clock.tick(60)


if __name__ == "__main__":
    main()
