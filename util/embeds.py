import random
import disnake

SUCCESS = 0x10D21B
ALERT = 0xCD0B00

def embed_neutral(desc, color = None):
    return disnake.Embed(description = str(desc), color = color)

def embed_success(desc):
    return disnake.Embed(description = str(desc), color = SUCCESS)

def embed_alert(desc):
    return disnake.Embed(description = str(desc), color = ALERT)