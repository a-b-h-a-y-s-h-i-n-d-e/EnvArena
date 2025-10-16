<p align="center">
  <img src="./static/logo.png" height="200" width="65%" alt="accessibility text">
</p>
<div align="center">
  <h2 style="border-bottom: none;">A collection of interactive environments with UI for LLMs</h2>
</div>


<div align="center">
<h3>
<a href="">Website </a> |
<a href="">Docs</a> |

</h3>
</div>

### 🧩 Installation
```bash
pip install envarena
```


### ⚡ Quick Start

```python
from envarena import Simulator
from envarena.envs import GuessTheNumber
from envarena.wrappers import OllamaWrapper


simulator = Simulator(
    env=GuessTheNumber(),
    model=OllamaWrapper("deepseek-r1:1.5b")
)

simulator.run()
```
