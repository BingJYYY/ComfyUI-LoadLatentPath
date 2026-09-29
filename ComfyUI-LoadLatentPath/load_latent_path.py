"""
LoadLatentPath - Load a .latent file from a plain string path.

Same loading logic as the core LoadLatent node, but the path is a normal
STRING input instead of a combo dropdown, and there is deliberately no
VALIDATE_INPUTS. That makes it safe to feed the path through a link
(core LoadLatent crashes at validation time when its latent input is
linked, because validation cannot resolve linked values yet).

Supports ComfyUI path annotations like "xxx.latent [output]".
"""

import folder_paths
import safetensors.torch


class LoadLatentPath:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "path": (
                    "STRING",
                    {
                        "default": "",
                        "multiline": False,
                        "tooltip": "Path to a .latent file. Supports [output] / [input] / [temp] annotations, e.g. latents/xxx.latent [output]",
                    },
                )
            }
        }

    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("LATENT",)
    FUNCTION = "load"
    CATEGORY = "model/latent"
    DESCRIPTION = "Loads a .latent file from a plain path string (supports [output] annotations). Safe for linked inputs."

    def load(self, path):
        latent_path = folder_paths.get_annotated_filepath(path)
        latent = safetensors.torch.load_file(latent_path, device="cpu")
        multiplier = 1.0
        if "latent_format_version_0" not in latent:
            multiplier = 1.0 / 0.18215
        samples = {"samples": latent["latent_tensor"].float() * multiplier}
        return (samples,)


NODE_CLASS_MAPPINGS = {"LoadLatentPath": LoadLatentPath}
NODE_DISPLAY_NAME_MAPPINGS = {"LoadLatentPath": "Load Latent from Path"}
