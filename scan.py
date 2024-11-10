from scapy.all import *
import os
from colorama import Fore, Style, init
from rich.console import Console
from rich.table import Table
from rich.progress import track
from rich.align import Align
import time

# Inisialisasi Colorama untuk warna terminal
init(autoreset=True)
console = Console()

# ASCII art dan informasi developer
ascii_art = """
⠀⠀⠀⠀⠀⠀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣴⣿⣿⠿⣟⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢸⣏⡏⠀⠀⠀⢣⢻⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢸⣟⠧⠤⠤⠤⠋⠀⢿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣿⡆⠀⠀⠀⠀⠀⠸⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠘⣿⡀⢀⣶⠤⠒⠀⢻⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢹⣧⠀⠀⠀⠀⠀⠈⢿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣿⡆⠀⠀⠀⠀⠀⠈⢿⣆⣠⣤⣤⣤⣤⣴⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣾⢿⢿⠀⠀⠀⢀⣀⣀⠘⣿⠋⠁⠀⠙⢇⠀⠀⠙⢿⣦⡀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣾⢇⡞⠘⣧⠀⢖⡭⠞⢛⡄⠘⣆⠀⠀⠀⠈⢧⠀⠀⠀⠙⢿⣄⠀⠀⠀⠀
⠀⠀⣠⣿⣛⣥⠤⠤⢿⡄⠀⠀⠈⠉⠀⠀⠹⡄⠀⠀⠀⠈⢧⠀⠀⠀⠈⠻⣦⠀⠀⠀
⠀⣼⡟⡱⠛⠙⠀⠀⠘⢷⡀⠀⠀⠀⠀⠀⠀⠹⡀⠀⠀⠀⠈⣧⠀⠀⠀⠀⠹⣧⡀⠀
⢸⡏⢠⠃⠀⠀⠀⠀⠀⠀⢳⡀⠀⠀⠀⠀⠀⠀⢳⡀⠀⠀⠀⠘⣧⠀⠀⠀⠀⠸⣷⡀
⠸⣧⠘⡇⠀⠀⠀⠀⠀⠀⠀⢳⡀⠀⠀⠀⠀⠀⠀⢣⠀⠀⠀⠀⢹⡇⠀⠀⠀⠀⣿⠇
⠀⣿⡄⢳⠀⠀⠀⠀⠀⠀⠀⠈⣷⠀⠀⠀⠀⠀⠀⠈⠆⠀⠀⠀⠁⠀⠀⠀⠀⣼⡟⠀
⠀⢹⡇⠘⣇⠀⠀⠀⠀⠀⠀⠰⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⠀⣼⡟⠀⠀
⠀⢸⡇⠀⢹⡆⠀⠀⠀⠀⠀⠀⠙⠁⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⢳⣼⠟⠀⠀⠀
⠀⠸⣧⣀⠀⢳⡀⠀⠀⠀⠀⠀⠀⠀⡄⠀⠀⠀⠀⠀⠀⠀⢃⠀⢀⣴⡿⠁⠀⠀⠀⠀
⠀⠀⠈⠙⢷⣄⢳⡀⠀⠀⠀⠀⠀⠀⢳⡀⠀⠀⠀⠀⠀⣠⡿⠟⠛⠉⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠻⢿⣷⣦⣄⣀⣀⣠⣤⠾⠷⣦⣤⣤⡶⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

[ Developer ]
Name    : Cy57 And AI
Telegram: @bangcayy57
Team    : I AM ALONE
"""

def display_centered_text(text, style=""):
    """Menampilkan teks dengan animasi bergulir dan di tengah."""
    console.clear()
    console.print(Align.center(text, style=style))

def wifi_scan():
    # Tampilkan ASCII art dan informasi developer di tengah sekali
    display_centered_text(ascii_art, style="bold cyan")

    # Menu pilihan untuk scanning
    console.print(Align.center("[bold yellow]Pilih Menu:[/bold yellow]"))
    console.print(Align.center("[1] Scanning IP Address"))
    console.print(Align.center("[2] Scanning MAC Address"))
    console.print(Align.center("[3] Scanning Vendor"))

    # Ambil input dengan pembersihan layar setelahnya
    choice = input("Pilih Scanning (1/2/3): ")
    console.clear()

    # Menyiapkan mode monitor (Linux)
    os.system("sudo ip link set wlan0 down")
    os.system("sudo iw dev wlan0 set type monitor")
    os.system("sudo ip link set wlan0 up")

    networks = {}

    def packet_handler(packet):
        if packet.haslayer(Dot11Beacon) or packet.haslayer(Dot11ProbeResp):
            ssid = packet[Dot11Elt].info.decode(errors="ignore")
            bssid = packet[Dot11].addr2
            signal_strength = packet.dBm_AntSignal
            channel = int(ord(packet[Dot11Elt:3].info))

            if bssid not in networks:
                networks[bssid] = {
                    "SSID": ssid,
                    "Signal": signal_strength,
                    "Channel": channel,
                    "BSSID": bssid
                }

    display_centered_text("[bold cyan]Scanning Wi-Fi networks...[/bold cyan]")

    # Animasi progress
    for _ in track(range(10), description="Scanning...", transient=True):
        time.sleep(1)

    # Sniffing paket
    try:
        sniff(iface="wlan0", prn=packet_handler, timeout=10)
    except KeyboardInterrupt:
        pass

    # Tampilkan hasil dalam tabel dengan Rich
    table = Table(title="Wi-Fi Networks", box="ROUNDED")
    table.centered = True

    # Kondisi untuk menampilkan hasil berdasarkan pilihan menu
    if choice == "1":
        table.add_column("SSID", style="cyan", justify="center")
        table.add_column("IP Address", style="green", justify="center")
        for bssid in networks:
            ssid = networks[bssid]["SSID"]
            ip_address = "192.168.0.1"  # Placeholder
            table.add_row(ssid, ip_address)

    elif choice == "2":
        table.add_column("SSID", style="cyan", justify="center")
        table.add_column("MAC Address", style="magenta", justify="center")
        for bssid in networks:
            ssid = networks[bssid]["SSID"]
            mac_address = networks[bssid]["BSSID"]
            table.add_row(ssid, mac_address)

    elif choice == "3":
        table.add_column("SSID", style="cyan", justify="center")
        table.add_column("Vendor", style="yellow", justify="center")
        for bssid in networks:
            ssid = networks[bssid]["SSID"]
            vendor = "Unknown Vendor"  # Placeholder
            table.add_row(ssid, vendor)
    else:
        display_centered_text("[bold red]Pilihan tidak valid![/bold red]")
        return

    # Menampilkan tabel di tengah
    console.print(Align.center(table))

if __name__ == "__main__":
    wifi_scan()