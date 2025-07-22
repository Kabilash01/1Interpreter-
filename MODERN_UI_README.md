# Auto-Dock Modern UI

A MetaChain-inspired terminal interface for Auto-Dock DevOps automation platform.

## 🚀 Quick Start

### Option 1: Double-click launcher
```
launch_modern_ui.bat    (Windows Batch)
launch_modern_ui.ps1    (PowerShell)
```

### Option 2: Command line
```bash
cd C:\Auto-Dock-
python cli/modern_ui.py
```

### Option 3: From notebook
Run the AI configuration cell in `numberplate.ipynb` and select "Launch Modern UI"

## 🎨 Interface Features

### Header Design
- ASCII art logo similar to MetaChain
- Version and author information
- Clean, professional appearance

### Important Notes Section
- Mode explanations
- Feature highlights
- Usage guidance

### Operation Modes

#### 🧑 User Mode
- General AI assistant for DevOps tasks
- Quick automation and troubleshooting
- Natural language queries

#### 🤖 Agent Mode  
- Create custom AI agents
- Specify purpose and programming language
- Save agent configurations

#### ⚡ Workflow Mode
- Build complete DevOps pipelines
- Step-by-step workflow creation
- Automated deployment chains

#### 🚪 Exit
- Clean application termination

## 🔧 Commands

| Command | Description |
|---------|-------------|
| `user` | Enter user assistant mode |
| `agent` | Create custom AI agent |
| `workflow` | Build DevOps workflow |
| `@agent_name` | Mention specific agent |
| `exit` | Quit application |

## 💬 User Mode Examples

- "How do I containerize my Flask app?"
- "Generate tests for my Python code"
- "Deploy my app to AWS"
- "Optimize my Docker image"
- "Create a CI/CD pipeline"

## 🤖 Agent Creation

1. Choose agent mode
2. Specify agent name and purpose
3. Select programming language
4. Agent files saved to `./agents/`

## ⚡ Workflow Building

1. Choose workflow mode
2. Name your workflow
3. Add steps one by one
4. Workflow saved to `./workflows/`

## 🎭 Demo

Run the demo to see all features:
```bash
python demo_ui.py
```

## 🔧 Configuration

The UI integrates with Auto-Dock's AI configuration:
- Cloud APIs (Gemini, OpenAI)
- Local models (Ollama, Hugging Face)
- Hybrid mode for best performance

## 📁 File Structure

```
cli/
├── modern_ui.py          # Main UI application
├── terminal_ui.py        # Legacy terminal UI
demo_ui.py                # Feature demonstration
launch_modern_ui.bat      # Windows launcher
launch_modern_ui.ps1      # PowerShell launcher
agents/                   # Generated agent configs
workflows/                # Generated workflow configs
```

## 🎨 Design Philosophy

Inspired by MetaChain's interface design:
- Clean ASCII art headers
- Structured information panels
- Intuitive mode selection
- Rich text formatting
- Interactive prompts with auto-completion

## 🔄 Integration

Works seamlessly with:
- Auto-Dock backend commands
- AI configuration system
- Jupyter notebook setup
- Docker automation
- Static analysis tools
- Test generation
- Code optimization

---

**Auto-Dock Team** | MIT License | v0.1.0
