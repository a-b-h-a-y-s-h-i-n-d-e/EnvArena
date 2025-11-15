from rich.layout import Layout
from rich.panel import Panel
from rich.console import Console
from rich.live import Live
from rich.align import Align


class Dashboard:
    def __init__(self):
        self.console = Console()
        self.layout = Layout()
        self.layout.split_row(
            Layout(name="game"),
            Layout(name="agent")
        )
        self.MAX_LINES = 15

        # initial state
        self.update_game_state("Game not started")
        self.update_agent_state("Waiting for input...")

        # Live instance
        self.live = Live(
            self.layout,
            console=self.console,
            refresh_per_second=8,
            screen=True
        )

    def start(self):
        """Start live rendering."""
        self.live.start()

    def stop(self):
        """Stop live rendering."""
        self.live.stop()

    def update_game_state(self, state: str):
        self.layout["game"].update(Panel(state, title="Game", border_style="green"))

    def update_agent_state(self, state: str):
        lines = state.splitlines()
        clipped = "\n".join(lines[-self.MAX_LINES:])
        self.layout["agent"].update(
            Panel(clipped, title="Agent", border_style="yellow")
        )
    
    def win(self):
        message = " WIN! "
        style = "bold green"


        self.layout = Layout()
        centered_msg = Align.center(message, vertical="middle")  
        self.layout.update(Panel(centered_msg, title="Result", border_style=style))
        self.live.update(self.layout)

    def complete(self):
        message = " Env run completed! "
        style = "bold green"

        self.layout = Layout()
        centered_msg = Align.center(message, vertical="middle")  
        self.layout.update(Panel(centered_msg, title="Result", border_style=style))
        self.live.update(self.layout)