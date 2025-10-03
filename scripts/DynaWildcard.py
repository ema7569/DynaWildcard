import random
import re
from modules import scripts, shared

class DynaWildcardScript(scripts.Script):
    def title(self):
        return "DynaWildcardScript: {option1|option2|...} with weights, nested braces, optional blocks"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def replace_brace_options_in_text(self, text, gen):
        """
        Remplace récursivement les {option1|option2:poids|...} avec :
        - support des accolades imbriquées
        - poids internes
        - blocs optionnels avec ?probabilité
        """
        # Cherche le dernier bloc {...} pour gérer l'imbrication
        pattern = r"\{([^{}]+)\}(\?\d*\.?\d+)?"

        while True:
            match = re.search(pattern, text)
            if not match:
                break

            inner = match.group(1)
            optional = match.group(2)

            # Tirage pour bloc optionnel
            if optional:
                prob = float(optional[1:]) if len(optional) > 1 else 0.5  # ?0.25 → 0.25, ? → 0.5
                if gen.random() < prob:
                    # Le bloc disparaît
                    text = text[:match.start()] + "" + text[match.end():]
                    continue

            # Séparer options par | et strip
            options = [o.strip() for o in re.split(r'\|', inner)]

            # Remplacer récursivement les options contenant des {...}
            for i, opt in enumerate(options):
                if '{' in opt:
                    options[i] = self.replace_brace_options_in_text(opt, gen)

            # Tirage pondéré
            choices = []
            weights = []
            for opt in options:
                if ':' in opt:
                    val, weight = opt.rsplit(":", 1)
                    choices.append(val.strip())
                    try:
                        weights.append(float(weight))
                    except ValueError:
                        weights.append(1.0)
                else:
                    choices.append(opt.strip())
                    weights.append(1.0)

            replacement = gen.choices(choices, weights=weights, k=1)[0]

            # Remplacer le motif complet
            text = text[:match.start()] + replacement + text[match.end():]

        return text

    def replace_prompts(self, prompts, seeds):
        res = []
        for i, text in enumerate(prompts):
            gen = random.Random()
            gen.seed(seeds[i if not shared.opts.wildcards_same_seed else 0])
            res.append(self.replace_brace_options_in_text(text, gen))
        return res

    def apply_wildcards(self, p, attr):
        if all_prompts := getattr(p, attr, None):
            setattr(p, attr, self.replace_prompts(all_prompts, p.all_seeds))

    def process(self, p, *args):
        for attr in ['all_prompts', 'all_negative_prompts', 'all_hr_prompts', 'all_hr_negative_prompts']:
            self.apply_wildcards(p, attr)
