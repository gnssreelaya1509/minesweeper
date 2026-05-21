import flet as ft
from core.engine import MinesweeperEngine


def main(page: ft.Page):
    page.title = "Flet Minesweeper"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#263238"

    engine = MinesweeperEngine()

    # Text widget centered
    status = ft.Text("Find the Mines!", size=20, color="#FFFFFF", text_align=ft.TextAlign.CENTER)

    def get_color_for_number(num):
        # Each number gets a distinct color (Hex codes)
        colors = {
            1: "#2196F3", 2: "#4CAF50", 3: "#F44336", 4: "#9C27B0",
            5: "#FF9800", 6: "#00BCD4", 7: "#795548", 8: "#607D8B"
        }
        return colors.get(num, "#000000")

    def update_ui(e=None):
        if engine.game_over:
            status.value, status.color = "💥 BOOM! Game Over!", "#FF5252"
        elif engine.win:
            status.value, status.color = "🎉 YOU WIN!", "#66BB6A"
        else:
            status.value, status.color = "Find the Mines!", "#FFFFFF"

        for r in range(engine.rows):
            for c in range(engine.cols):
                tile = board_ui.controls[r].controls[c].content
                if engine.visible[r][c]:
                    tile.bgcolor = "#CFD8DC"
                    if engine.board[r][c] == -1:
                        tile.content.value = "💣"
                    elif engine.board[r][c] > 0:
                        tile.content.value = str(engine.board[r][c])
                        tile.content.color = get_color_for_number(engine.board[r][c])
                    else:
                        tile.content.value = ""
                else:
                    tile.bgcolor = "#455A64"
                    tile.content.value = "🚩" if engine.flags[r][c] else ""
        page.update()

    # Board container
    board_ui = ft.Column(spacing=2, alignment=ft.MainAxisAlignment.CENTER)
    for r in range(engine.rows):
        row = ft.Row(spacing=2, alignment=ft.MainAxisAlignment.CENTER)
        for c in range(engine.cols):
            row.controls.append(ft.GestureDetector(
                on_tap=lambda _, r=r, c=c: (engine.reveal(r, c), update_ui()),
                on_secondary_tap=lambda _, r=r, c=c: (engine.toggle_flag(r, c), update_ui()),
                content=ft.Container(width=35, height=35, bgcolor="#455A64", border_radius=4,
                                     alignment=ft.alignment.center, content=ft.Text("", weight="bold", size=18))
            ))
        board_ui.controls.append(row)

    # Adding everything to the page with center alignment
    page.add(
        ft.Column([
            status,
            board_ui,
            ft.ElevatedButton("Restart Game", on_click=lambda _: (engine.reset(), update_ui()))
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
    update_ui()


if __name__ == "__main__":
    ft.app(target=main)