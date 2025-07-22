"""
Quick demo script to test the Modern Auto-Dock UI
"""

import sys
import time
from pathlib import Path

# Add the Auto-Dock path to Python path  
autodock_path = Path("C:/Auto-Dock-")
sys.path.insert(0, str(autodock_path))

from cli.modern_ui import AutoDockUI
from rich.console import Console

def demo_ui():
    """Demo the Auto-Dock UI features"""
    console = Console()
    
    console.print("\n🎭 [bold cyan]Auto-Dock Modern UI Demo[/bold cyan]")
    console.print("This demonstrates the MetaChain-inspired interface\n")
    
    # Create UI instance
    app = AutoDockUI()
    
    # Show individual components
    console.print("🎨 [bold yellow]Component Demo:[/bold yellow]")
    
    # Show header art
    console.print("1. Header Art:")
    print(app.get_header_art())
    
    time.sleep(2)
    
    # Test AI query processing
    console.print("\n2. AI Query Processing:")
    app.process_ai_query("How do I deploy a Flask app with Docker?")
    
    time.sleep(2)
    
    # Show configuration
    console.print("\n3. AI Configuration Status:")
    try:
        from backend.llm.llm_wrapper import get_ai_status
        status = get_ai_status()
        console.print(f"Current AI Mode: [green]{status['mode']}[/green]")
        console.print(f"Gemini API: {'✅' if status['gemini_configured'] else '❌'}")
        console.print(f"OpenAI API: {'✅' if status['openai_configured'] else '❌'}")
    except Exception as e:
        console.print(f"[yellow]AI status: {e}[/yellow]")
    
    console.print("\n✅ [bold green]Demo complete! Launch with: python cli/modern_ui.py[/bold green]")

if __name__ == "__main__":
    demo_ui()
