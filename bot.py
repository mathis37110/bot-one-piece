import discord
from discord.ext import commands
import json
import random
import os
import asyncio
from datetime import datetime, timedelta

# ─── CONFIG ───────────────────────────────────────────────────────────────────
TOKEN = "TON_TOKEN_ICI"
PREFIX = "!"
DATA_FILE = "data.json"

# ─── FRUITS DU DEMON ──────────────────────────────────────────────────────────
FRUITS = {
    # ══ COMMUN (50%) ══
    "Gomu Gomu no Mi": {
        "type": "Paramecia", "rarity": "Commun", "emoji": "🟢",
        "desc": "Corps en caoutchouc, immunisé aux éclairs",
        "bonus_atk": 5, "bonus_hp": 10,
        "skill": "Gomu Gomu no Pistol", "skill_dmg": 20
    },
    "Bane Bane no Mi": {
        "type": "Paramecia", "rarity": "Commun", "emoji": "🟢",
        "desc": "Corps en ressort",
        "bonus_atk": 7, "bonus_hp": 5,
        "skill": "Bane Bane Slam", "skill_dmg": 18
    },
    "Kilo Kilo no Mi": {
        "type": "Paramecia", "rarity": "Commun", "emoji": "🟢",
        "desc": "Contrôle son poids de 1 à 10 000 kg",
        "bonus_atk": 6, "bonus_hp": 8,
        "skill": "Kilo Crush", "skill_dmg": 16
    },
    "Sube Sube no Mi": {
        "type": "Paramecia", "rarity": "Commun", "emoji": "🟢",
        "desc": "Peau glissante, les attaques glissent",
        "bonus_atk": 4, "bonus_hp": 12,
        "skill": "Slip Away", "skill_dmg": 14
    },

    # ══ RARE (30%) ══
    "Mera Mera no Mi": {
        "type": "Logia", "rarity": "Rare", "emoji": "🔵",
        "desc": "Contrôle le feu",
        "bonus_atk": 15, "bonus_hp": 15,
        "skill": "Hiken", "skill_dmg": 40
    },
    "Hie Hie no Mi": {
        "type": "Logia", "rarity": "Rare", "emoji": "🔵",
        "desc": "Contrôle la glace",
        "bonus_atk": 14, "bonus_hp": 18,
        "skill": "Ice Age", "skill_dmg": 38
    },
    "Suna Suna no Mi": {
        "type": "Logia", "rarity": "Rare", "emoji": "🔵",
        "desc": "Contrôle le sable",
        "bonus_atk": 16, "bonus_hp": 12,
        "skill": "Desert Spada", "skill_dmg": 42
    },
    "Neko Neko no Mi": {
        "type": "Zoan", "rarity": "Rare", "emoji": "🔵",
        "desc": "Transformation en léopard",
        "bonus_atk": 18, "bonus_hp": 20,
        "skill": "Leopard Fang", "skill_dmg": 35
    },

    # ══ EPIQUE (15%) ══
    "Gura Gura no Mi": {
        "type": "Paramecia", "rarity": "Épique", "emoji": "🟣",
        "desc": "Créer des tremblements de terre",
        "bonus_atk": 28, "bonus_hp": 25,
        "skill": "Gura Gura Tsunami", "skill_dmg": 65
    },
    "Ope Ope no Mi": {
        "type": "Paramecia", "rarity": "Épique", "emoji": "🟣",
        "desc": "Crée une salle opératoire, contrôle tout dedans",
        "bonus_atk": 25, "bonus_hp": 30,
        "skill": "ROOM - Shambles", "skill_dmg": 60
    },
    "Magu Magu no Mi": {
        "type": "Logia", "rarity": "Épique", "emoji": "🟣",
        "desc": "Contrôle le magma, plus puissant que le feu",
        "bonus_atk": 30, "bonus_hp": 20,
        "skill": "Ryusei Kazan", "skill_dmg": 70
    },
    "Uo Uo no Mi (Modèle: Seiryuu)": {
        "type": "Zoan Mythique", "rarity": "Épique", "emoji": "🟣",
        "desc": "Transformation en dragon céleste",
        "bonus_atk": 32, "bonus_hp": 28,
        "skill": "Boro Breath", "skill_dmg": 68
    },

    # ══ LEGENDAIRE (5%) ══
    "Yami Yami no Mi": {
        "type": "Logia", "rarity": "Légendaire", "emoji": "🟡",
        "desc": "Contrôle les ténèbres, attire et annule les pouvoirs",
        "bonus_atk": 45, "bonus_hp": 35,
        "skill": "Black Hole", "skill_dmg": 100
    },
    "Hito Hito no Mi (Modèle: Nika)": {
        "type": "Zoan Mythique", "rarity": "Légendaire", "emoji": "🟡",
        "desc": "Fruit le plus libre du monde, Gear 5",
        "bonus_atk": 50, "bonus_hp": 50,
        "skill": "Bajrang Gun", "skill_dmg": 120
    },
    "Tori Tori no Mi (Modèle: Phénix)": {
        "type": "Zoan Mythique", "rarity": "Légendaire", "emoji": "🟡",
        "desc": "Flammes de renaissance, régénération infinie",
        "bonus_atk": 40, "bonus_hp": 60,
        "skill": "Blue Fire", "skill_dmg": 95
    },
}

RARITY_WEIGHTS = {
    "Commun": 50,
    "Rare": 30,
    "Épique": 15,
    "Légendaire": 5
}

RARITY_COLORS = {
    "Commun": 0x2ecc71,
    "Rare": 0x3498db,
    "Épique": 0x9b59b6,
    "Légendaire": 0xf1c40f
}

# ─── MONSTRES PVE ─────────────────────────────────────────────────────────────
MONSTERS = [
    {"name": "Marine Rookie", "emoji": "👮", "hp": 40, "atk": 8, "xp": 15, "berry": 50},
    {"name": "Bandit des Mers", "emoji": "🏴‍☠️", "hp": 60, "atk": 12, "xp": 25, "berry": 80},
    {"name": "Marine Captain", "emoji": "⚓", "hp": 100, "atk": 20, "xp": 50, "berry": 150},
    {"name": "Corsaire Célèbre", "emoji": "🗡️", "hp": 150, "atk": 30, "xp": 80, "berry": 250},
    {"name": "Warlord", "emoji": "👑", "hp": 250, "atk": 45, "xp": 150, "berry": 500},
    {"name": "Amiral de la Marine", "emoji": "🌊", "hp": 400, "atk": 65, "xp": 250, "berry": 800},
    {"name": "Yonko", "emoji": "🔥", "hp": 700, "atk": 90, "xp": 500, "berry": 2000},
]

# ─── DATA MANAGER ─────────────────────────────────────────────────────────────
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_player(data, user_id):
    uid = str(user_id)
    if uid not in data:
        return None
    return data[uid]

def create_player(data, user_id, username):
    uid = str(user_id)
    data[uid] = {
        "username": username,
        "level": 1,
        "xp": 0,
        "xp_next": 100,
        "hp": 100,
        "max_hp": 100,
        "atk": 10,
        "berry": 500,
        "fruit": None,
        "wins": 0,
        "losses": 0,
        "last_heal": None,
        "last_fight": None,
        "last_gacha": None,
        "title": "Moussaillon"
    }
    save_data(data)
    return data[uid]

def get_title(level):
    if level < 5:   return "Moussaillon"
    if level < 10:  return "Pirate"
    if level < 20:  return "Capitaine Pirate"
    if level < 35:  return "Corsaire"
    if level < 50:  return "Supernova"
    if level < 75:  return "Commandant Yonko"
    return "Roi des Pirates 🏴‍☠️"

def xp_for_level(level):
    return int(100 * (level ** 1.5))

def add_xp(player, xp_gain):
    player["xp"] += xp_gain
    leveled = False
    while player["xp"] >= player["xp_next"]:
        player["xp"] -= player["xp_next"]
        player["level"] += 1
        player["xp_next"] = xp_for_level(player["level"])
        # Stats up on level
        player["max_hp"] += 15
        player["hp"] = player["max_hp"]
        player["atk"] += 3
        player["title"] = get_title(player["level"])
        leveled = True
    return leveled

def get_total_atk(player):
    base = player["atk"]
    if player["fruit"]:
        fruit_data = FRUITS.get(player["fruit"], {})
        base += fruit_data.get("bonus_atk", 0)
    return base

def get_total_hp(player):
    base = player["max_hp"]
    if player["fruit"]:
        fruit_data = FRUITS.get(player["fruit"], {})
        base += fruit_data.get("bonus_hp", 0)
    return base

def can_act(player, action_key, cooldown_seconds):
    last = player.get(action_key)
    if last is None:
        return True, 0
    elapsed = (datetime.now() - datetime.fromisoformat(last)).total_seconds()
    if elapsed >= cooldown_seconds:
        return True, 0
    return False, int(cooldown_seconds - elapsed)

# ─── BOT SETUP ────────────────────────────────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

# ─── EVENTS ───────────────────────────────────────────────────────────────────
@bot.event
async def on_ready():
    print(f"✅ {bot.user} est connecté et prêt !")
    await bot.change_presence(activity=discord.Game("One Piece RPG 🏴‍☠️"))

# ─── COMMANDES ────────────────────────────────────────────────────────────────

@bot.command(name="start", aliases=["debut", "jouer"])
async def start(ctx):
    """Crée ton personnage"""
    data = load_data()
    uid = str(ctx.author.id)

    if get_player(data, uid):
        embed = discord.Embed(
            title="⚠️ Déjà inscrit !",
            description="Tu as déjà un personnage. Utilise `!profil` pour le voir.",
            color=0xe74c3c
        )
        await ctx.send(embed=embed)
        return

    player = create_player(data, uid, ctx.author.display_name)
    embed = discord.Embed(
        title="🏴‍☠️ Bienvenue dans le Grand Siècle des Pirates !",
        description=(
            f"**{ctx.author.display_name}** commence son aventure en tant que **Moussaillon** !\n\n"
            f"❤️ HP : `100` | ⚔️ ATK : `10` | 🪙 Berry : `500`\n\n"
            f"**Commandes utiles :**\n"
            f"`!gacha` — Obtenir un Fruit du Démon\n"
            f"`!combat` — Affronter un monstre\n"
            f"`!pvp @joueur` — Défier un autre pirate\n"
            f"`!profil` — Voir tes stats\n"
            f"`!aide` — Toutes les commandes"
        ),
        color=0xf39c12
    )
    embed.set_thumbnail(url="https://i.imgur.com/3a3t7d2.png")
    await ctx.send(embed=embed)

@bot.command(name="profil", aliases=["stats", "moi"])
async def profil(ctx, member: discord.Member = None):
    """Affiche le profil d'un joueur"""
    data = load_data()
    target = member or ctx.author
    player = get_player(data, target.id)

    if not player:
        name = "Tu n'as" if target == ctx.author else f"{target.display_name} n'a"
        await ctx.send(f"❌ {name} pas encore de personnage. Utilise `!start` !")
        return

    fruit = player.get("fruit")
    fruit_data = FRUITS.get(fruit, {}) if fruit else {}
    total_atk = get_total_atk(player)
    total_hp = get_total_hp(player)
    hp_bar = "█" * int(player["hp"] / total_hp * 10) + "░" * (10 - int(player["hp"] / total_hp * 10))

    embed = discord.Embed(
        title=f"📜 Profil de {player['username']}",
        color=RARITY_COLORS.get(fruit_data.get("rarity", ""), 0x3498db)
    )
    embed.add_field(name="🏅 Titre", value=player["title"], inline=True)
    embed.add_field(name="⭐ Niveau", value=str(player["level"]), inline=True)
    embed.add_field(name="✨ XP", value=f"{player['xp']}/{player['xp_next']}", inline=True)
    embed.add_field(
        name=f"❤️ HP [{hp_bar}]",
        value=f"{player['hp']}/{total_hp}",
        inline=False
    )
    embed.add_field(name="⚔️ ATK", value=str(total_atk), inline=True)
    embed.add_field(name="🪙 Berry", value=f"{player['berry']:,}", inline=True)
    embed.add_field(name="🏆 Victoires / Défaites", value=f"{player['wins']}W / {player['losses']}L", inline=True)

    if fruit:
        rarity_emoji = fruit_data.get("emoji", "🍎")
        embed.add_field(
            name=f"🍎 Fruit du Démon",
            value=f"{rarity_emoji} **{fruit}** ({fruit_data.get('type')})\n_{fruit_data.get('desc')}_",
            inline=False
        )
    else:
        embed.add_field(name="🍎 Fruit du Démon", value="Aucun — Utilise `!gacha` !", inline=False)

    embed.set_footer(text=f"Demandé par {ctx.author.display_name}")
    await ctx.send(embed=embed)

@bot.command(name="gacha", aliases=["fruit", "invoquer"])
async def gacha(ctx):
    """Tente d'obtenir un Fruit du Démon (cooldown 1h)"""
    data = load_data()
    uid = str(ctx.author.id)
    player = get_player(data, uid)

    if not player:
        await ctx.send("❌ Utilise `!start` d'abord !")
        return

    can, remaining = can_act(player, "last_gacha", 3600)
    if not can:
        mins = remaining // 60
        secs = remaining % 60
        embed = discord.Embed(
            title="⏳ Cooldown Gacha",
            description=f"Prochain gacha dans **{mins}m {secs}s** !",
            color=0xe74c3c
        )
        await ctx.send(embed=embed)
        return

    if player["berry"] < 200:
        await ctx.send("❌ Il te faut **200 Berry** pour tenter le gacha !")
        return

    player["berry"] -= 200
    player["last_gacha"] = datetime.now().isoformat()

    # Tirage de rareté
    rarities = list(RARITY_WEIGHTS.keys())
    weights = list(RARITY_WEIGHTS.values())
    chosen_rarity = random.choices(rarities, weights=weights)[0]

    # Fruits de cette rareté
    fruits_of_rarity = [f for f, d in FRUITS.items() if d["rarity"] == chosen_rarity]
    chosen_fruit = random.choice(fruits_of_rarity)
    fruit_data = FRUITS[chosen_fruit]

    old_fruit = player.get("fruit")
    player["fruit"] = chosen_fruit
    save_data(data)

    embed = discord.Embed(
        title=f"🍎 Fruit du Démon obtenu !",
        description=(
            f"{fruit_data['emoji']} **{chosen_fruit}**\n"
            f"Type : `{fruit_data['type']}` | Rareté : `{fruit_data['rarity']}`\n\n"
            f"_{fruit_data['desc']}_\n\n"
            f"**Bonus :** +{fruit_data['bonus_atk']} ATK | +{fruit_data['bonus_hp']} HP\n"
            f"**Skill :** `{fruit_data['skill']}` ({fruit_data['skill_dmg']} dégâts)"
        ),
        color=RARITY_COLORS[chosen_rarity]
    )
    if old_fruit:
        embed.set_footer(text=f"Ancien fruit ({old_fruit}) remplacé ! | Coût : 200 Berry")
    else:
        embed.set_footer(text="Coût : 200 Berry | Prochain gacha dans 1h")
    await ctx.send(embed=embed)

@bot.command(name="combat", aliases=["fight", "attaque"])
async def combat(ctx):
    """Affronte un monstre (cooldown 30s)"""
    data = load_data()
    uid = str(ctx.author.id)
    player = get_player(data, uid)

    if not player:
        await ctx.send("❌ Utilise `!start` d'abord !")
        return

    can, remaining = can_act(player, "last_fight", 30)
    if not can:
        await ctx.send(f"⏳ Prochain combat dans **{remaining}s** !")
        return

    if player["hp"] <= 0:
        await ctx.send("💀 Tu es KO ! Utilise `!soin` pour récupérer !")
        return

    # Sélection monstre selon le level
    max_idx = min(player["level"] // 5, len(MONSTERS) - 1)
    monster = random.choice(MONSTERS[:max_idx + 1]).copy()

    total_atk = get_total_atk(player)
    total_hp = get_total_hp(player)
    fruit_data = FRUITS.get(player.get("fruit", ""), {})

    # Simulation du combat
    player_hp = player["hp"]
    monster_hp = monster["hp"]
    log = []
    round_num = 1

    while player_hp > 0 and monster_hp > 0 and round_num <= 10:
        # Attaque du joueur (chance d'utiliser skill)
        use_skill = fruit_data and random.random() < 0.3
        if use_skill:
            dmg = fruit_data["skill_dmg"] + random.randint(-5, 5)
            log.append(f"⚡ **{fruit_data['skill']}** ! Dégâts : **{dmg}**")
        else:
            dmg = total_atk + random.randint(-3, 3)
            log.append(f"⚔️ Tu attaques pour **{dmg}** dégâts")

        monster_hp -= dmg
        if monster_hp <= 0:
            break

        # Attaque du monstre
        mdmg = monster["atk"] + random.randint(-2, 2)
        player_hp -= mdmg
        log.append(f"💢 {monster['emoji']} attaque pour **{mdmg}** dégâts")
        round_num += 1

    player_hp = max(0, player_hp)
    player["hp"] = player_hp
    player["last_fight"] = datetime.now().isoformat()

    if monster_hp <= 0:
        # VICTOIRE
        xp_gain = monster["xp"] + random.randint(0, 10)
        berry_gain = monster["berry"] + random.randint(-20, 50)
        player["berry"] += berry_gain
        player["wins"] += 1
        leveled = add_xp(player, xp_gain)
        save_data(data)

        embed = discord.Embed(
            title=f"✅ Victoire contre {monster['emoji']} {monster['name']} !",
            color=0x2ecc71
        )
        embed.add_field(name="📜 Combat", value="\n".join(log[-4:]), inline=False)
        embed.add_field(name="🎁 Récompenses", value=f"+{xp_gain} XP | +{berry_gain} 🪙 Berry", inline=False)
        embed.add_field(name="❤️ HP restant", value=f"{player_hp}/{total_hp}", inline=True)
        if leveled:
            embed.add_field(name="🎉 LEVEL UP !", value=f"Niveau **{player['level']}** | {player['title']}", inline=False)
    else:
        # DEFAITE
        player["losses"] += 1
        player["hp"] = max(1, player["hp"])
        save_data(data)

        embed = discord.Embed(
            title=f"💀 Défaite contre {monster['emoji']} {monster['name']}...",
            color=0xe74c3c
        )
        embed.add_field(name="📜 Combat", value="\n".join(log[-4:]), inline=False)
        embed.add_field(name="❤️ HP restant", value=f"1/{total_hp} (KO !)", inline=True)
        embed.set_footer(text="Utilise !soin pour récupérer !")

    await ctx.send(embed=embed)

@bot.command(name="pvp", aliases=["duel", "defier"])
async def pvp(ctx, opponent: discord.Member):
    """Défie un autre joueur en duel"""
    data = load_data()
    uid = str(ctx.author.id)
    oid = str(opponent.id)

    if opponent == ctx.author:
        await ctx.send("❌ Tu ne peux pas te battre toi-même !")
        return

    player = get_player(data, uid)
    opp = get_player(data, oid)

    if not player:
        await ctx.send("❌ Utilise `!start` d'abord !")
        return
    if not opp:
        await ctx.send(f"❌ {opponent.display_name} n'a pas encore de personnage !")
        return
    if player["hp"] <= 0:
        await ctx.send("💀 Tu es KO ! Utilise `!soin` !")
        return
    if opp["hp"] <= 0:
        await ctx.send(f"💀 {opponent.display_name} est KO, ce serait une victoire trop facile !")
        return

    # Demande de confirmation
    embed = discord.Embed(
        title="⚔️ Défi PvP !",
        description=(
            f"**{ctx.author.display_name}** défie **{opponent.display_name}** en duel !\n\n"
            f"{opponent.mention}, acceptes-tu le défi ? Réponds **oui** dans les 30 secondes."
        ),
        color=0xe67e22
    )
    await ctx.send(embed=embed)

    def check(m):
        return m.author == opponent and m.channel == ctx.channel and m.content.lower() in ["oui", "non", "yes", "no"]

    try:
        msg = await bot.wait_for("message", check=check, timeout=30.0)
    except asyncio.TimeoutError:
        await ctx.send(f"⏰ {opponent.display_name} n'a pas répondu. Défi annulé.")
        return

    if msg.content.lower() in ["non", "no"]:
        await ctx.send(f"🏳️ {opponent.display_name} a refusé le défi !")
        return

    # COMBAT PVP
    p_hp = player["hp"]
    o_hp = opp["hp"]
    p_atk = get_total_atk(player)
    o_atk = get_total_atk(opp)
    p_fruit = FRUITS.get(player.get("fruit", ""), {})
    o_fruit = FRUITS.get(opp.get("fruit", ""), {})

    log = []
    round_num = 1

    while p_hp > 0 and o_hp > 0 and round_num <= 15:
        # Attaque joueur 1
        use_skill = p_fruit and random.random() < 0.25
        if use_skill:
            dmg = p_fruit["skill_dmg"] + random.randint(-5, 5)
            log.append(f"⚡ **{p_fruit['skill']}** → {dmg} dégâts à {opp['username']}")
        else:
            dmg = p_atk + random.randint(-3, 5)
            log.append(f"⚔️ {player['username']} → {dmg} dégâts à {opp['username']}")
        o_hp -= dmg
        if o_hp <= 0:
            break

        # Attaque joueur 2
        use_skill2 = o_fruit and random.random() < 0.25
        if use_skill2:
            dmg2 = o_fruit["skill_dmg"] + random.randint(-5, 5)
            log.append(f"⚡ **{o_fruit['skill']}** → {dmg2} dégâts à {player['username']}")
        else:
            dmg2 = o_atk + random.randint(-3, 5)
            log.append(f"⚔️ {opp['username']} → {dmg2} dégâts à {player['username']}")
        p_hp -= dmg2
        round_num += 1

    p_hp = max(0, p_hp)
    o_hp = max(0, o_hp)

    if p_hp > o_hp:
        winner, loser = player, opp
        winner_member, loser_member = ctx.author, opponent
    else:
        winner, loser = opp, player
        winner_member, loser_member = opponent, ctx.author

    # Récompenses
    xp_gain = 60 + (loser["level"] * 5)
    berry_gain = 300 + (loser["level"] * 20)
    winner["wins"] += 1
    loser["losses"] += 1
    winner["berry"] += berry_gain
    loser["hp"] = max(1, loser["hp"] // 2)
    leveled = add_xp(winner, xp_gain)

    save_data(data)

    embed = discord.Embed(
        title=f"🏆 {winner['username']} remporte le duel !",
        color=0xf1c40f
    )
    embed.add_field(name="📜 Derniers rounds", value="\n".join(log[-6:]), inline=False)
    embed.add_field(
        name="🎁 Récompenses (vainqueur)",
        value=f"+{xp_gain} XP | +{berry_gain} 🪙 Berry",
        inline=False
    )
    if leveled:
        embed.add_field(name="🎉 LEVEL UP !", value=f"Niveau **{winner['level']}** | {winner['title']}", inline=False)
    embed.set_footer(text=f"{loser['username']} perd 50% de ses HP !")
    await ctx.send(embed=embed)

@bot.command(name="soin", aliases=["heal", "repos"])
async def soin(ctx):
    """Régénère tes HP (cooldown 10 min)"""
    data = load_data()
    uid = str(ctx.author.id)
    player = get_player(data, uid)

    if not player:
        await ctx.send("❌ Utilise `!start` d'abord !")
        return

    can, remaining = can_act(player, "last_heal", 600)
    if not can:
        mins = remaining // 60
        secs = remaining % 60
        await ctx.send(f"⏳ Prochain soin dans **{mins}m {secs}s** !")
        return

    total_hp = get_total_hp(player)
    old_hp = player["hp"]
    heal_amount = int(total_hp * 0.5)
    player["hp"] = min(total_hp, player["hp"] + heal_amount)
    player["last_heal"] = datetime.now().isoformat()
    save_data(data)

    embed = discord.Embed(
        title="💊 Soin !",
        description=f"❤️ HP : `{old_hp}` → `{player['hp']}`/`{total_hp}` (+{player['hp'] - old_hp})",
        color=0x1abc9c
    )
    await ctx.send(embed=embed)

@bot.command(name="fruits", aliases=["liste_fruits", "bestiary"])
async def fruits_list(ctx):
    """Affiche la liste des Fruits du Démon disponibles"""
    embeds = []
    for rarity in ["Commun", "Rare", "Épique", "Légendaire"]:
        fruits_of_rarity = {f: d for f, d in FRUITS.items() if d["rarity"] == rarity}
        desc = "\n".join(
            f"{d['emoji']} **{name}** ({d['type']}) — {d['desc']}\n"
            f"  ⚔️+{d['bonus_atk']} ❤️+{d['bonus_hp']} | Skill: `{d['skill']}`"
            for name, d in fruits_of_rarity.items()
        )
        embed = discord.Embed(
            title=f"🍎 Fruits {rarity}s ({RARITY_WEIGHTS[rarity]}% de chance)",
            description=desc,
            color=RARITY_COLORS[rarity]
        )
        embeds.append(embed)

    for e in embeds:
        await ctx.send(embed=e)

@bot.command(name="classement", aliases=["top", "leaderboard"])
async def classement(ctx):
    """Affiche le classement des pirates"""
    data = load_data()
    if not data:
        await ctx.send("❌ Aucun joueur inscrit pour le moment !")
        return

    sorted_players = sorted(data.values(), key=lambda p: (p["level"], p["xp"]), reverse=True)[:10]

    desc = ""
    medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
    for i, p in enumerate(sorted_players):
        fruit_emoji = FRUITS[p["fruit"]]["emoji"] if p.get("fruit") else "❌"
        desc += f"{medals[i]} **{p['username']}** — Nv.{p['level']} {fruit_emoji} | {p['wins']}W/{p['losses']}L\n"

    embed = discord.Embed(
        title="🏴‍☠️ Classement des Pirates",
        description=desc,
        color=0xf39c12
    )
    await ctx.send(embed=embed)

@bot.command(name="aide", aliases=["help", "commandes"])
async def aide(ctx):
    """Liste toutes les commandes"""
    embed = discord.Embed(
        title="📖 Commandes du Bot One Piece RPG",
        color=0xe74c3c
    )
    commands_list = [
        ("!start", "Créer ton personnage"),
        ("!profil [@joueur]", "Voir les stats d'un joueur"),
        ("!gacha", "Obtenir un Fruit du Démon (200 Berry, 1h CD)"),
        ("!combat", "Affronter un monstre (30s CD)"),
        ("!pvp @joueur", "Défier un autre pirate en duel"),
        ("!soin", "Récupérer 50% de tes HP (10 min CD)"),
        ("!fruits", "Voir tous les Fruits du Démon"),
        ("!classement", "Top 10 des pirates"),
    ]
    for cmd, desc in commands_list:
        embed.add_field(name=f"`{cmd}`", value=desc, inline=False)
    embed.set_footer(text="Prefix : ! | Bonne aventure Moussaillon !")
    await ctx.send(embed=embed)

# ─── LAUNCH ───────────────────────────────────────────────────────────────────
bot.run(TOKEN)
