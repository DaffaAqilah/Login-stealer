import os
import pickle
import discord
import requests
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN    = os.getenv('DISCORD_TOKEN')
BASE_URL = os.getenv('FLASK_URL')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


# ── Helper: load/save session admin ──────────────────────
def save_session(session):
    with open('admin_session.pkl', 'wb') as f:
        pickle.dump(session.cookies, f)

def load_session():
    session = requests.Session()
    with open('admin_session.pkl', 'rb') as f:
        session.cookies.update(pickle.load(f))
    return session

def get_base_url():
    load_dotenv(override=True)
    return os.getenv('FLASK_URL')


# ── Sync slash commands saat bot ready ───────────────────
@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f'✅ Bot online sebagai {bot.user}')
        print(f'✅ {len(synced)} slash command tersinkron')
    except Exception as e:
        print(f'❌ Gagal sync commands: {e}')


# ── /submit ───────────────────────────────────────────────
@bot.tree.command(name='submit', description='Kirim data email dan password ke database')
@app_commands.describe(
    email    = 'Email yang ingin didaftarkan',
    password = 'Password akun',
    box_id   = 'Nomor box yang dipilih (default: 1)'
)
async def submit(interaction: discord.Interaction, email: str, password: str, box_id: int = 1):
    await interaction.response.defer()

    try:
        res = requests.post(f'{get_base_url()}/api/submit', json={
            'email'   : email,
            'password': password,
            'box_id'  : box_id
        })
        data = res.json()

        if res.status_code == 201:
            embed = discord.Embed(title='✅ Data Berhasil Disimpan', color=0x7c6af7)
            embed.add_field(name='Email',    value=email,              inline=True)
            embed.add_field(name='Password', value=f'||{password}||',  inline=True)
            embed.add_field(name='Box',      value=f'Box {box_id}',    inline=True)
            embed.add_field(name='ID',       value=str(data.get('id')), inline=True)
            embed.set_footer(text='Password disembunyikan — klik untuk reveal')
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(f'❌ Gagal: {data.get("message")}')

    except Exception as e:
        await interaction.followup.send(f'❌ Error koneksi ke server: `{e}`')


# ── /adminlogin ───────────────────────────────────────────
@bot.tree.command(name='adminlogin', description='Login sebagai admin panel')
@app_commands.describe(
    username = 'Username admin',
    password = 'Password admin'
)
async def adminlogin(interaction: discord.Interaction, username: str, password: str):
    await interaction.response.defer(ephemeral=True)

    try:
        session = requests.Session()
        res = session.post(
            f'{get_base_url()}/api/admin/login',
            json    = {'username': username, 'password': password},
            headers = {'Content-Type': 'application/json'},
            allow_redirects = False
        )

        if not res.text.strip():
            await interaction.followup.send('❌ Server response kosong.', ephemeral=True)
            return

        data = res.json()

        if res.status_code == 200:
            save_session(session)
            await interaction.followup.send('✅ Login berhasil!', ephemeral=True)
        else:
            await interaction.followup.send(f'❌ {data.get("message", "Login gagal.")}', ephemeral=True)

    except Exception as e:
        await interaction.followup.send(f'❌ Error: `{e}`', ephemeral=True)


# ── /users ────────────────────────────────────────────────
@bot.tree.command(name='users', description='Lihat semua data user yang masuk (perlu login admin)')
async def users(interaction: discord.Interaction):
    await interaction.response.defer()

    try:
        session = load_session()
    except FileNotFoundError:
        await interaction.followup.send('❌ Belum login admin! Gunakan `/adminlogin` dulu.')
        return

    try:
        res  = session.get(f'{get_base_url()}/api/admin/users')
        data = res.json()

        if res.status_code == 200:
            user_list = data.get('data', [])

            if not user_list:
                await interaction.followup.send('📭 Belum ada data.')
                return

            embed = discord.Embed(
                title = f'📊 Data User — {len(user_list)} total',
                color = 0x7c6af7
            )
            for u in user_list[:10]:
                embed.add_field(
                    name   = f'ID {u["id"]} — {u["email"]}',
                    value  = f'🔑 `{u["password"]}` | Box {u["box_id"]} | {u["created_at"]}',
                    inline = False
                )
            if len(user_list) > 10:
                embed.set_footer(text=f'Menampilkan 10 dari {len(user_list)} data')

            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send('❌ Sesi expired. Login ulang dengan `/adminlogin`.')

    except Exception as e:
        await interaction.followup.send(f'❌ Error: `{e}`')


# ── /delete ───────────────────────────────────────────────
@bot.tree.command(name='delete', description='Hapus data user berdasarkan ID (perlu login admin)')
@app_commands.describe(user_id='ID user yang ingin dihapus')
async def delete(interaction: discord.Interaction, user_id: int):
    await interaction.response.defer()

    try:
        session = load_session()
    except FileNotFoundError:
        await interaction.followup.send('❌ Belum login admin! Gunakan `/adminlogin` dulu.')
        return

    try:
        res  = session.delete(f'{get_base_url()}/api/admin/users/{user_id}')
        data = res.json()

        if res.status_code == 200:
            embed = discord.Embed(
                title       = '🗑️ Data Berhasil Dihapus',
                description = f'ID `{user_id}` sudah dihapus dari database.',
                color       = 0xe05a6b
            )
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(f'❌ Gagal: {data.get("message")}')

    except Exception as e:
        await interaction.followup.send(f'❌ Error: `{e}`')


# ── /menu ─────────────────────────────────────────────────
@bot.tree.command(name='menu', description='Lihat semua command yang tersedia')
async def menu(interaction: discord.Interaction):
    embed = discord.Embed(
        title       = '📖 Daftar Command',
        description = 'Semua slash command yang tersedia:',
        color       = 0x7c6af7
    )
    embed.add_field(
        name  = '`/submit`',
        value = 'Kirim email, password, dan box_id ke database',
        inline= False
    )
    embed.add_field(
        name  = '`/adminlogin`',
        value = 'Login sebagai admin — hanya terlihat oleh kamu',
        inline= False
    )
    embed.add_field(
        name  = '`/users`',
        value = 'Lihat semua data user yang masuk',
        inline= False
    )
    embed.add_field(
        name  = '`/delete`',
        value = 'Hapus data user by ID',
        inline= False
    )
    embed.set_footer(text='Perlu /adminlogin dulu untuk akses /users dan /delete')
    await interaction.response.send_message(embed=embed)


bot.run(TOKEN)
