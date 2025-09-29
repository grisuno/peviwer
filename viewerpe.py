# viewerpe.py
import json
import sys
from rich import print
from rich.tree import Tree
from rich.panel import Panel
from rich.text import Text

def add_dict_to_tree(parent_node, d, prefix=""):
    """Agrega recursivamente un dict al árbol de rich."""
    for key, value in d.items():
        if isinstance(value, dict):
            node = parent_node.add(f"[cyan]{prefix}{key}[/cyan]")
            add_dict_to_tree(node, value)
        elif isinstance(value, list):
            node = parent_node.add(f"[cyan]{prefix}{key}[/cyan] ([yellow]{len(value)} items[/yellow])")
            add_list_to_tree(node, value)
        else:
            parent_node.add(f"[cyan]{prefix}{key}:[/cyan] [yellow]{value}[/yellow]")

def add_list_to_tree(parent_node, lst):
    """Agrega una lista al árbol: si son dicts, los expande; si no, los muestra como items."""
    for i, item in enumerate(lst):
        if isinstance(item, dict):
            # Caso especial: si la lista contiene dicts con una sola clave (como en Data Directories),
            # usamos esa clave como nombre
            if len(item) == 1:
                subkey, subval = next(iter(item.items()))
                node = parent_node.add(f"[green]• {subkey}[/green]: [yellow]{subval}[/yellow]")
            else:
                node = parent_node.add(f"[green]• Item {i}[/green]")
                add_dict_to_tree(node, item)
        else:
            parent_node.add(f"[green]•[/green] [yellow]{item}[/yellow]")

def visualize_pe_json(data):
    print(Panel("[bold blue]PE File Structure[/bold blue]", expand=False))
    tree = Tree("📄 PE File")

    for section_name, content in data.items():
        section_node = tree.add(f"[bold green]{section_name}[/bold green]")
        if isinstance(content, dict):
            add_dict_to_tree(section_node, content)
        elif isinstance(content, list):
            add_list_to_tree(section_node, content)
        else:
            section_node.add(f"[yellow]{content}[/yellow]")

    print(tree)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 viewerpe.py <archivo.json>")
        sys.exit(1)

    try:
        with open(sys.argv[1], 'r') as f:
            data = json.load(f)
        visualize_pe_json(data)
    except Exception as e:
        print(f"[red]Error:[/red] {e}")
        sys.exit(1)