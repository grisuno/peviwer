# root

*Community 0 | 4 files | cohesion 1.00*

## Definition

This community groups 4 file(s) rooted at `root` with dominant language py (cohesion 1.00). Central symbols: `add_dict_to_tree`, `add_list_to_tree`, `visualize_pe_json`. Core file: `viewerpe.py` (3 symbols). Documented purpose: Autor: Gris Iscomeback Correo electrónico: grisiscomeback[at]gmail[dot]com Fecha de creación: xx/xx/xxxx Licencia: GPL v3  Descripción:.

## Files

| File | Language | Layer | Symbols | Doc |
|------|----------|-------|---------|-----|
| `app.py` | py | utility | 0 | yes |
| `install.sh` | sh | utility | 0 | no |
| `pe_gui_viewer.py` | py | presentation | 0 | no |
| `viewerpe.py` | py | presentation | 3 | yes |

## Key Symbols

- `add_dict_to_tree` (function, `viewerpe.py:9`) `def add_dict_to_tree(parent_node, d, prefix)` - Agrega recursivamente un dict al árbol de rich.
- `add_list_to_tree` (function, `viewerpe.py:21`) `def add_list_to_tree(parent_node, lst)` - Agrega una lista al árbol: si son dicts, los expande; si no, los muestra como items.
- `visualize_pe_json` (function, `viewerpe.py:36`) `def visualize_pe_json(data)`

## Internal vs External Edges

- Internal resolved imports (EXTRACTED): 0
- Cross-boundary resolved imports (EXTRACTED): 0

## Connections

- No cross-community bridges recorded. This community is self-contained.

## Risks

- No scoped security, taint, cycle, or layer risks.

## Open Questions

- Why do 2 file(s) lack file-level docs (e.g. `install.sh`)? What purpose do they serve?
- What would break if the most connected file in root changed?
- Should root be split, given cohesion 1.00?

## Sources

- `app.py`
- `install.sh`
- `pe_gui_viewer.py`
- `viewerpe.py`
