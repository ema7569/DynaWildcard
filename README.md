# DynaWildcard
A simplified dynamic prompt pour a1111


**DynaWildcardScript** is a script for the Automatic1111 WebUI that allows generating dynamic and varied prompts for Stable Diffusion. 

- **Nested random blocks** `{A|B|{C|D}}`
- **Internal word weights** `{{A|B:2}|{C|D}:2}` to control frequency  
- **Internal block weights** `{{A|B}:1|{C|D}:2}` to control frequency  
- **Optional blocks** `{A|B}?0.25` probability to remove a block (e.g., `?0.25`)  

---

## Installation

1. Place `DynaWildcardScript.py` in: extensions/dynawildcard/scripts/


---

## Prompt Syntax (default weight=1)

### 1. Simple random block

- A {cat|dog}

### 2. Block with internal weights

- A {red:3|green|blue} car

- red → 3/5 = 60% chance
- green → 1/5 = 20% chance
- red → 1/5 = 20% chance


### 3. Optional block

- A {red|green}?0.25 car
- 25% chance the block disappears → “A car”

### 4. Nested block

- A {small|{medium|large:3}} cat

- Outer block draw: `small` or inner block `{medium|large:3}`  
- Inner block draw: `medium` 25%, `large` 75%  

## Notes

- **Weights are local to the block**, no multiplication by parent.  
- **Optional blocks** use `?probability` (0–1), default 0.5 if omitted.  


⚠️ Important: The execution order of script callbacks in A1111 can affect results.
Make sure the Dynamic Wildcards script runs before prompt-merging extensions (such as embedding merge) but after file-based wildcards if you use both.
You can adjust this order in Settings → Script order.







