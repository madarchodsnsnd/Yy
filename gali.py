from telethon import TelegramClient, events
import random
import asyncio
import os
import time

# Config
api_id = 27494996
api_hash = '791274de917e999ebab112e60f3a163e'
session_name = 'my_account'
admin_id = 7681062358  # Your Telegram ID

# Files
caption_file = 'caption.txt'
targets_file = 'targets.txt'
delay_file = 'delay.txt'
approved_users_file = 'approved_users.txt'  # New file for approved users

# Enhanced Speed presets (messages per second)
SPEED_PRESETS = {
    'low': 20,
    'medium': 50,
    'high': 100,
    'ultra': 250,
    'ultra++': 2000,
    'superultra': 5000,
    'ultra+++': 10000,
    'extreme': 20000
}

# Default settings
DEFAULT_DELAY = 1  # 1 second between messages
MAX_MESSAGES = 50000  # Increased default max messages

# Emojis for extra style
EMOJIS = ["💣", "🔥", "⚡", "🎯", "👊", "💢", "🤬", "🚀", "💥", "🔪", "🖕", "🍆", "💦", "👅", "🤡"]

# Enhanced Vulgar word banks
VULGAR_NOUNS = ["maa", "behen", "bhosda", "lund", "chut", "gaand", "randi", "kutta", "madarchod", "harami", "gandu", "chutmarike", "bhenchod"]
VULGAR_VERBS = ["chod", "pel", "mara", "nanga", "chusa", "kaata", "phoda", "daba", "ghusa", "latka", "jhuka", "nacha", "dala"]
VULGAR_ADJECTIVES = ["sasti", "gandi", "kamina", "besharam", "nalayak", "chutiya", "bhadwa", "lulli", "jhaant", "randi", "kamine", "bewakoof"]

# Text Styles
STYLES = [
    lambda t: f"**{t}**",      # Bold
    lambda t: f"__{t}__",      # Underline
    lambda t: f"~~{t}~~",      # Strikethrough
    lambda t: f"`{t}`",        # Monospace
    lambda t: f"🔥 {t} 🔥",   # Emoji wrapped
    lambda t: f"⚡ {t} ⚡",    # Flashy
    lambda t: f"💢 {t} 💢",   # Angry
    lambda t: f"||{t}||",      # Spoiler
    lambda t: f"😈 {t} 😈",   # Devilish
]

# Global variables
is_sending = False
current_delay = DEFAULT_DELAY
message_count = 0
max_messages = MAX_MESSAGES

# Helper functions
def generate_vulgar_caption():
    """Generate random vulgar captions with more combinations"""
    patterns = [
        f"{random.choice(VULGAR_NOUNS)} ki {random.choice(VULGAR_NOUNS)}",
        f"{random.choice(VULGAR_ADJECTIVES)} {random.choice(VULGAR_NOUNS)}",
        f"{random.choice(VULGAR_VERBS)} diya {random.choice(VULGAR_NOUNS)} ko",
        f"{random.choice(VULGAR_NOUNS)} {random.choice(VULGAR_VERBS)}ne wala",
        f"{random.choice(VULGAR_NOUNS)} {random.choice(VULGAR_VERBS)} ke chod",
        f"{random.choice(VULGAR_NOUNS)} {random.choice(VULGAR_VERBS)} {random.choice(VULGAR_NOUNS)}",
        f"{random.choice(VULGAR_NOUNS)} ke {random.choice(VULGAR_NOUNS)} mein {random.choice(VULGAR_VERBS)}",
        f"{random.choice(VULGAR_ADJECTIVES)} {random.choice(VULGAR_NOUNS)} ka {random.choice(VULGAR_NOUNS)}"
    ]
    return random.choice(patterns)

def save_to_file(filename, text):
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(f"{text}\n")
        return True
    except Exception as e:
        print(f"Error saving to file: {e}")
        return False

def read_file(filename):
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def clear_file(filename):
    try:
        open(filename, 'w').close()
        return True
    except Exception as e:
        print(f"Error clearing file: {e}")
        return False

def remove_line(filename, text):
    try:
        lines = read_file(filename)
        if text in lines:
            lines.remove(text)
            if clear_file(filename):
                for line in lines:
                    save_to_file(filename, line)
                return True
        return False
    except Exception as e:
        print(f"Error removing line: {e}")
        return False

def random_style(text):
    words = text.split()
    styled = []
    for word in words:
        style = random.choice(STYLES)
        styled.append(style(word))
    return ' '.join(styled)

def get_delay():
    if os.path.exists(delay_file):
        try:
            with open(delay_file, 'r') as f:
                content = f.read().strip()
                return float(content) if content else DEFAULT_DELAY
        except:
            return DEFAULT_DELAY
    return DEFAULT_DELAY

def set_delay(seconds):
    try:
        with open(delay_file, 'w') as f:
            f.write(str(seconds))
        return True
    except Exception as e:
        print(f"Error setting delay: {e}")
        return False

def is_user_approved(user_id):
    """Check if user is approved"""
    approved_users = read_file(approved_users_file)
    return str(user_id) in approved_users

# Telegram Client
client = TelegramClient(session_name, api_id, api_hash)

# User Management Commands
@client.on(events.NewMessage(pattern='/approve'))
async def approve_user(event):
    """Approve a user to use spam commands"""
    if event.sender_id != admin_id:
        await event.reply("🚫 **Only Admin can approve users!**")
        return
    
    user_to_approve = event.raw_text.replace('/approve', '').strip()
    if not user_to_approve.isdigit():
        await event.reply("⚠️ **Invalid User ID!** Example: `/approve 123456789`")
        return
    
    if save_to_file(approved_users_file, user_to_approve):
        await event.reply(f"✅ **User Approved!**\nID: `{user_to_approve}`\n\nNow they can use /madarchod, /chodo, etc.")
    else:
        await event.reply("⚠️ **Failed to approve user!**")

@client.on(events.NewMessage(pattern='/disapprove'))
async def disapprove_user(event):
    """Remove user from approved list"""
    if event.sender_id != admin_id:
        await event.reply("🚫 **Only Admin can disapprove users!**")
        return
    
    user_to_remove = event.raw_text.replace('/disapprove', '').strip()
    if not user_to_remove.isdigit():
        await event.reply("⚠️ **Invalid User ID!** Example: `/disapprove 123456789`")
        return
    
    if remove_line(approved_users_file, user_to_remove):
        await event.reply(f"❌ **User Disapproved!**\nID: `{user_to_remove}`\n\nThey can no longer use spam commands.")
    else:
        await event.reply("⚠️ **User not found or already disapproved!**")

@client.on(events.NewMessage(pattern='/approved_list'))
async def list_approved_users(event):
    """Show all approved users"""
    if event.sender_id != admin_id:
        await event.reply("🚫 **Only Admin can view approved users!**")
        return
    
    approved_users = read_file(approved_users_file)
    if not approved_users:
        await event.reply("📭 **No approved users yet!**")
        return
    
    reply = "✅ **APPROVED USERS LIST:**\n\n"
    for i, user_id in enumerate(approved_users, 1):
        reply += f"{i}. `{user_id}`\n"
    
    await event.reply(reply)

# Spam Commands (Restricted to Approved Users)
@client.on(events.NewMessage(pattern='/chodo'))
async def chodo(event):
    """Start bombing"""
    if event.sender_id != admin_id and not is_user_approved(event.sender_id):
        await event.reply("🚫 **You are not approved to spam!**")
        return
    
    global is_sending, current_delay, message_count, max_messages
    is_sending = True
    message_count = 0
    current_delay = get_delay()
    await event.reply(f"**💣 BOMBING STARTED! 💣**\n__Speed:__ `{1/current_delay:.1f} msg/s`\n__Max:__ `{max_messages}`\n__Mode:__ `ULTRA SPAM`")
    
    while is_sending and message_count < max_messages:
        captions = read_file(caption_file)
        targets = read_file(targets_file)
        
        if not captions:
            caption = generate_vulgar_caption()
        else:
            caption = random.choice(captions)
        
        if not targets:
            await event.reply("⚠️ **No targets!** Use `/madarchod`")
            is_sending = False
            return
        
        target = random.choice(targets)
        emoji = random.choice(EMOJIS)
        styled_caption = random_style(caption)
        final_msg = f"__{target}__\n\n{emoji} {styled_caption} {emoji}"
        
        try:
            await event.respond(final_msg)
            message_count += 1
            if current_delay > 0:
                await asyncio.sleep(current_delay)
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds)  # Wait the required time
            continue  # Try again after waiting
        except Exception as e:
            is_sending = False
            try:
                await event.reply(f"⚠️ **Error:** `{str(e)}`")
            except:
                pass  # Avoid recursive errors
            return
    
    is_sending = False
    await event.reply(f"✅ **BOMBING COMPLETE!**\n__Messages sent:__ `{message_count}`\n__Rate:__ `{message_count/(message_count*current_delay):.1f} msg/s`")
    
@client.on(events.NewMessage(pattern='/ruko'))
async def ruko(event):
    """Stop spam"""
    if event.sender_id != admin_id and not is_user_approved(event.sender_id):
        await event.reply("🚫 **You are not approved to use this command!**")
        return
    
    global is_sending
    is_sending = False
    await event.reply(f"🛑 **SPAM STOPPED!**\n__Messages sent:__ `{message_count}`")

@client.on(events.NewMessage(pattern='/ac'))
async def ac(event):
    """Add caption"""
    if event.sender_id != admin_id and not is_user_approved(event.sender_id):
        await event.reply("🚫 **You are not approved to use this command!**")
        return
    
    text = event.raw_text.replace('/ac', '').strip()
    if not text:
        await event.reply("⚠️ **Please provide caption text!** Example: `/ac YourCaptionHere`")
        return
    
    if save_to_file(caption_file, text):
        styled_example = random_style(text)
        await event.reply(f"✅ **Caption Added!**\nExample:\n`{styled_example}`")
    else:
        await event.reply("⚠️ **Failed to add caption!**")

@client.on(events.NewMessage(pattern='/dc'))
async def dc(event):
    """Delete caption"""
    if event.sender_id != admin_id and not is_user_approved(event.sender_id):
        await event.reply("🚫 **You are not approved to use this command!**")
        return
    
    text = event.raw_text.replace('/dc', '').strip()
    if not text:
        await event.reply("⚠️ **Please provide caption to delete!** Example: `/dc YourCaptionHere`")
        return
    
    if remove_line(caption_file, text):
        await event.reply(f"❌ **Caption Deleted:**\n`{text}`")
    else:
        await event.reply("⚠️ **Caption not found or couldn't be deleted!**")

@client.on(events.NewMessage(pattern='/cc'))
async def cc(event):
    """Clear captions"""
    if event.sender_id != admin_id and not is_user_approved(event.sender_id):
        await event.reply("🚫 **You are not approved to use this command!**")
        return
    
    if clear_file(caption_file):
        await event.reply("🧹 **All captions cleared!**")
    else:
        await event.reply("⚠️ **Failed to clear captions!**")

@client.on(events.NewMessage(pattern='/viewcaptions'))
async def view_captions(event):
    """View saved captions"""
    if event.sender_id != admin_id and not is_user_approved(event.sender_id):
        await event.reply("🚫 **You are not approved to use this command!**")
        return
    
    captions = read_file(caption_file)
    if not captions:
        await event.reply("📭 **No captions saved!**")
        return
    
    reply = "📜 **SAVED CAPTIONS:**\n\n"
    for i, cap in enumerate(captions, 1):
        reply += f"{i}. `{cap}`\n"
    
    await event.reply(reply)

@client.on(events.NewMessage(pattern='/madarchod'))
async def madharchod(event):
    """Add target"""
    if event.sender_id != admin_id and not is_user_approved(event.sender_id):
        await event.reply("🚫 **You are not approved to use this command!**")
        return
    
    target = event.raw_text.replace('/madarchod', '').strip()
    if not target:
        await event.reply("⚠️ **Please provide target!** Example: `/madarchod username`")
        return
    
    if not target.startswith('@'):
        target = f"@{target}"
    
    if save_to_file(targets_file, target):
        await event.reply(f"🎯 **Target Added:** `{target}`")
    else:
        await event.reply("⚠️ **Failed to add target!**")

@client.on(events.NewMessage(pattern='/nikal'))
async def nikal(event):
    """Remove target"""
    if event.sender_id != admin_id and not is_user_approved(event.sender_id):
        await event.reply("🚫 **You are not approved to use this command!**")
        return
    
    target = event.raw_text.replace('/nikal', '').strip()
    if not target:
        await event.reply("⚠️ **Please provide target to remove!** Example: `/nikal username`")
        return
    
    if not target.startswith('@'):
        target = f"@{target}"
    
    if remove_line(targets_file, target):
        await event.reply(f"❌ **Target Removed:** `{target}`")
    else:
        await event.reply("⚠️ **Target not found or couldn't be removed!**")

@client.on(events.NewMessage(pattern='/saaf'))
async def saaf(event):
    """Clear targets"""
    if event.sender_id != admin_id and not is_user_approved(event.sender_id):
        await event.reply("🚫 **You are not approved to use this command!**")
        return
    
    if clear_file(targets_file):
        await event.reply("🧹 **All targets cleared!**")
    else:
        await event.reply("⚠️ **Failed to clear targets!**")

@client.on(events.NewMessage(pattern='/list'))
async def list_targets(event):
    """List targets"""
    if event.sender_id != admin_id and not is_user_approved(event.sender_id):
        await event.reply("🚫 **You are not approved to use this command!**")
        return
    
    targets = read_file(targets_file)
    if not targets:
        await event.reply("🎯 **No targets saved!**")
        return
    
    reply = "🎯 **SAVED TARGETS:**\n\n"
    for i, target in enumerate(targets, 1):
        reply += f"{i}. `{target}`\n"
    
    await event.reply(reply)

@client.on(events.NewMessage(pattern='/speed'))
async def speed(event):
    """Set speed"""
    if event.sender_id != admin_id and not is_user_approved(event.sender_id):
        await event.reply("🚫 **You are not approved to use this command!**")
        return
    
    args = event.raw_text.replace('/speed', '').strip().split()
    if not args:
        await event.reply("""
⚠️ **Please specify speed!** 
Options: 
`low` (20 msg/s), 
`medium` (50 msg/s), 
`high` (100 msg/s), 
`ultra` (250 msg/s), 
`ultra++` (2000 msg/s),
`superultra` (5000 msg/s),
`ultra+++` (10000 msg/s),
`extreme` (20000 msg/s)
Or custom delay (e.g. `/speed 0.01` for 100 msg/s)
        """)
        return
    
    global current_delay, max_messages
    
    if args[0].lower() in SPEED_PRESETS:
        speed = args[0].lower()
        msg_per_sec = SPEED_PRESETS[speed]
        current_delay = 1/msg_per_sec
        set_delay(current_delay)
        
        if speed == 'extreme':
            max_messages = 100000
        elif speed == 'ultra+++':
            max_messages = 50000
        elif speed == 'superultra':
            max_messages = 25000
        elif speed == 'ultra++':
            max_messages = 10000
        elif speed == 'ultra':
            max_messages = 5000
        else:
            max_messages = 2000
            
        await event.reply(f"⚡ **Speed set to {speed.upper()}!**\n__Rate:__ `{msg_per_sec} msg/s`\n__Max:__ `{max_messages}`")
        return
    
    try:
        delay = float(args[0])
        if delay <= 0:
            await event.reply("⚠️ **Delay must be >0 second!**")
            return
        
        current_delay = delay
        set_delay(delay)
        
        if delay <= 0.0005:
            max_messages = 100000
        elif delay <= 0.001:
            max_messages = 50000
        elif delay <= 0.002:
            max_messages = 25000
        elif delay <= 0.005:
            max_messages = 10000
        elif delay <= 0.01:
            max_messages = 5000
        else:
            max_messages = 2000
            
        await event.reply(f"⏱ **Delay set to:** `{delay:.5f}s`\n__Rate:__ `{1/delay:.1f} msg/s`\n__Max:__ `{max_messages}`")
    except:
        await event.reply("⚠️ **Invalid speed!** Use presets or custom delay")

@client.on(events.NewMessage(pattern='/setmax'))
async def set_max_messages(event):
    """Set max messages"""
    if event.sender_id != admin_id and not is_user_approved(event.sender_id):
        await event.reply("🚫 **You are not approved to use this command!**")
        return
    
    global max_messages
    try:
        new_max = int(event.raw_text.replace('/setmax', '').strip())
        if new_max < 1:
            await event.reply("⚠️ **Must be at least 1 message!**")
            return
        
        max_messages = new_max
        await event.reply(f"🔢 **Max messages set to:** `{max_messages}`")
    except:
        await event.reply("⚠️ **Invalid number!** Example: `/setmax 50000`")

@client.on(events.NewMessage(pattern='/status'))
async def show_status(event):
    """Show status"""
    if event.sender_id != admin_id and not is_user_approved(event.sender_id):
        await event.reply("🚫 **You are not approved to use this command!**")
        return
    
    status = "🟢 RUNNING" if is_sending else "🔴 STOPPED"
    reply = (
        f"⚡ **ULTRA SPAM BOT STATUS** ⚡\n\n"
        f"__Status:__ {status}\n"
        f"__Messages sent:__ `{message_count}`\n"
        f"__Current speed:__ `{1/current_delay:.1f} msg/s`\n"
        f"__Current delay:__ `{current_delay:.5f}s`\n"
        f"__Max messages:__ `{max_messages}`\n"
        f"__Captions loaded:__ `{len(read_file(caption_file))}`\n"
        f"__Targets loaded:__ `{len(read_file(targets_file))}`\n"
        f"__Approved users:__ `{len(read_file(approved_users_file))}`"
    )
    await event.reply(reply)
    
@client.on(events.NewMessage(pattern='/keepadmins'))
async def keep_only_admins(event):
    """Remove all non-admin members from current group (keep only admins)"""
    if event.sender_id != admin_id:  # Only main admin can use this
        await event.reply("🚫 **Only the bot owner can use this command!**")
        return
    
    if not event.is_group:
        await event.reply("⚠️ **This command only works in groups!**")
        return
    
    try:
        # Get the chat entity
        chat = await event.get_chat()
        
        # Check if we're admin in this group
        if not (await event.client.get_permissions(chat, event.sender_id)).is_admin:
            await event.reply("⚠️ **You need to be admin in this group to use this command!**")
            return
            
        # Get all participants
        participants = await event.client.get_participants(chat)
        
        removed_count = 0
        failed_count = 0
        
        # Process each participant
        for user in participants:
            # Skip ourselves and bots
            if user.id == event.sender_id or user.bot:
                continue
                
            # Check if user is NOT admin
            if not (await event.client.get_permissions(chat, user.id)).is_admin:
                try:
                    await event.client.kick_participant(chat, user.id)
                    removed_count += 1
                    await asyncio.sleep(1)  # Avoid flood
                except Exception as e:
                    print(f"Failed to remove user {user.id}: {e}")
                    failed_count += 1
        
        await event.reply(
            f"✅ **Group Cleaned!**\n"
            f"__Removed non-admins:__ `{removed_count}`\n"
            f"__Failed attempts:__ `{failed_count}`\n"
            f"__Only admins remain in the group.__"
        )
        
    except Exception as e:
        await event.reply(f"⚠️ **Error:** `{str(e)}`")

@client.on(events.NewMessage(pattern='/help'))
async def show_help(event):
    """Show help (admin only)"""
    # Check if the sender is an admin
    if not event.sender_id == admin_id:  # Replace ADMIN_ID with your actual admin ID
        return
    
    help_text = """
    💣 **ULTRA SPAM BOT v3.0 HELP** 💣

    👑 **ADMIN COMMANDS:**
    `/approve [user_id]` - Approve a user
    `/disapprove [user_id]` - Remove user approval
    `/approved_list` - List approved users

    🎯 **APPROVED USER COMMANDS:**
    `/madarchod [@user]` - Add target
    `/nikal [@user]` - Remove target
    `/saaf` - Clear all targets
    `/list` - View targets
    `/chodo` - Start bombing
    `/ruko` - Stop spam

    📜 **CAPTION MANAGEMENT:**
    `/ac [text]` - Add caption
    `/dc [text]` - Delete caption
    `/cc` - Clear all captions
    `/viewcaptions` - View captions

    ⚡ **SPEED CONTROL:**
    `/speed [preset]` - Set speed preset
    `/speed [seconds]` - Set custom delay
    `/setmax [number]` - Set max messages
    `/status` - Show bot status

    🔥 **Auto-Generates:** Strong vulgar abuse
    """
    await event.reply(help_text)

async def main():
    # Create files if they don't exist
    for file in [caption_file, targets_file, delay_file, approved_users_file]:
        if not os.path.exists(file):
            open(file, 'w').close()
    
    print("💣 **ULTRA SPAM BOT v3.0 STARTED!**")
    await client.start()
    print(f"Logged in as: {await client.get_me()}")
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())