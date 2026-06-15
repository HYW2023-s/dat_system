#!/usr/bin/env python3
"""DAT System CLI - Command-line interface for the DAT system."""

import os
import sys
import subprocess
import csv
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

app = typer.Typer(
    name="dat",
    help="DAT System - Divergent Association Task CLI",
    add_completion=False,
)
console = Console()


@app.command()
def start(
    port: int = typer.Option(8000, "--port", "-p", help="Port to listen on"),
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host to bind to"),
):
    """Start the DAT web service."""
    console.print(Panel.fit(
        f"[bold blue]DAT System[/bold blue]\n"
        f"Starting web service at [bold]http://{host}:{port}[/bold]",
        border_style="blue",
    ))
    console.print(f"Press [bold red]Ctrl+C[/bold red] to stop the service.\n")

    uvicorn_path = subprocess.run(
        [sys.executable, "-c", "import uvicorn; print(uvicorn.__file__)"],
        capture_output=True, text=True
    )

    os.system(
        f"{sys.executable} -m uvicorn backend.main:app "
        f"--host {host} --port {port} "
        f"--log-level info"
    )


@app.command()
def export(
    format: str = typer.Option("csv", "--format", "-f", help="Export format: csv or xlsx"),
    output: str = typer.Option("./export", "--output", "-o", help="Output directory"),
):
    """Export experimental data (DAT test records)."""
    console.print("[bold]Exporting experimental data...[/bold]")

    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)

    # Import sync database and models
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from backend.config import DATABASE_SYNC_URL
    from backend.models import DatTest

    engine = create_engine(DATABASE_SYNC_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        records = session.query(DatTest).all()

        if not records:
            console.print("[yellow]No data to export.[/yellow]")
            return

        timestamp = __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S")

        if format == "xlsx":
            import openpyxl
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "DAT Results"

            headers = ["ID", "Username", "Create Time", "Word1", "Word2", "Word3",
                       "Word4", "Word5", "Word6", "Word7", "Word8", "Word9", "Word10",
                       "DAT Score", "Effective Words", "Spend Time", "Limited Time"]
            ws.append(headers)

            for r in records:
                ws.append([
                    r.id, r.username, str(r.create_time) if r.create_time else "",
                    r.word1, r.word2, r.word3, r.word4, r.word5,
                    r.word6, r.word7, r.word8, r.word9, r.word10,
                    r.dat_score, r.effective_num, r.spend_time, r.limited_time,
                ])

            filepath = output_path / f"dat_export_{timestamp}.xlsx"
            wb.save(filepath)

        else:  # csv
            filepath = output_path / f"dat_export_{timestamp}.csv"
            with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "ID", "Username", "Create Time",
                    "Word1", "Word2", "Word3", "Word4", "Word5",
                    "Word6", "Word7", "Word8", "Word9", "Word10",
                    "DAT Score", "Effective Words", "Spend Time", "Limited Time",
                ])
                for r in records:
                    writer.writerow([
                        r.id, r.username, str(r.create_time) if r.create_time else "",
                        r.word1, r.word2, r.word3, r.word4, r.word5,
                        r.word6, r.word7, r.word8, r.word9, r.word10,
                        r.dat_score, r.effective_num, r.spend_time, r.limited_time,
                    ])

        console.print(f"[green]Exported {len(records)} records to [bold]{filepath}[/bold][/green]")

    finally:
        session.close()


@app.command()
def deploy(
    port: int = typer.Option(80, "--port", "-p", help="Port to listen on"),
    host: str = typer.Option("0.0.0.0", "--host", "-h", help="Host to bind to"),
):
    """Deploy the DAT service to a specified port (production mode)."""
    console.print(Panel.fit(
        f"[bold green]DAT System - Production Mode[/bold green]\n"
        f"Deploying service at [bold]http://{host}:{port}[/bold]",
        border_style="green",
    ))

    os.system(
        f"{sys.executable} -m uvicorn backend.main:app "
        f"--host {host} --port {port} "
        f"--log-level warning --no-access-log"
    )


# Admin subcommands
admin_app = typer.Typer(help="Admin management commands")
app.add_typer(admin_app, name="admin")


@admin_app.command("reset-password")
def admin_reset_password(
    password: str = typer.Option("123456", "--password", "-p", help="New password"),
    username: str = typer.Option("admin", "--username", "-u", help="Target username"),
):
    """Reset admin (or any user) password."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from backend.config import DATABASE_SYNC_URL
    from backend.models import User

    engine = create_engine(DATABASE_SYNC_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        user = session.query(User).filter(User.username == username).first()
        if not user:
            console.print(f"[red]User '{username}' not found.[/red]")
            return

        from passlib.hash import bcrypt
        user.password_hash = bcrypt.hash(password)
        session.commit()
        console.print(f"[green]Password for user '[bold]{username}[/bold]' has been reset to '[bold]{password}[/bold]'.[/green]")
    finally:
        session.close()


def main():
    """CLI entry point."""
    app()


if __name__ == "__main__":
    main()
