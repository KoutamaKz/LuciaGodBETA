import discord
from discord import app_commands
from discord.ui import Select, View
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import asyncio
import time
import random
from PIL import Image, ImageFont, ImageDraw, ImageOps
import io
from db.statusdb import membstat, CreateProfile, AddSaldo, ConvenePerLim, ConvenePerIlim, AddInv, AddXP

class Status(commands.Cog):
	def __init__(self, client):
		self.client = client

	@app_commands.command(name='registrar-se', description='Se registe para liberar sua conta!')
	async def register(self, interaction:discord.Interaction):
		check = membstat.find_one({'_id': interaction.user.id})
		if check is not None:
			await interaction.response.send_message(f'{interaction.user.display_name} já tem registro')
		CreateProfile(interaction.user, 0, 0, 0, 'Não há nada aqui!')
		await interaction.response.send_message(f'{interaction.user.display_name} se registrou!')

	@app_commands.command(name='saldo', description='Mostra seu saldo no Bot')
	async def balance(self, interaction:discord.Interaction, membro: discord.Member = None):
		if membro is None:
			membro = interaction.user
		check = membstat.find_one({'_id': membro.id})
		if check is None:
			await interaction.response.send_message(f'{membro.display_name} não tem registro')
		astrite = membstat.find_one({"_id": membro.id})['astrite']
		astriter = int(astrite)
		e = discord.Embed(title=f'Saldo de: {membro.display_name}')
		e.add_field(name='<:item_astrite:1251257679545110641> Astrites', value=astriter)
		e.add_field(name='<:item_lustrous:1251257743554248765> Lustrous Tide', value=membstat.find_one({"_id": membro.id})['lustrous'])
		e.add_field(name='<:item_radiant:1251257713363648653> Radiant Tide', value=membstat.find_one({"_id": membro.id})['radiant'])
		e.add_field(name='<:item_weapon:1251257727095668838> Forging Tide', value=membstat.find_one({"_id": membro.id})['forging'])
		await interaction.response.send_message(embed=e)

	@app_commands.command(name='editar_saldo', description='Adicione ou remova saldo da conta de um membro')
	@app_commands.choices(add_remove=[
		app_commands.Choice(name=f"[ ✅ ] Adicionar", value='+'),
		app_commands.Choice(name="[ ❌ ] Remover", value='-')
		])
	@app_commands.choices(item=[
		app_commands.Choice(name=f"[ ⚪ ] Astrite", value='astrite'),
		app_commands.Choice(name="[ 🔵 ] Lustrous Tide", value='lustrous'),
		app_commands.Choice(name="[ 🟡 ] Radiant Tide", value='radiant'),
		app_commands.Choice(name="[ ⚜️ ] Forging Tide", value='forging')
		])
	async def add_saldo(self, interaction:discord.Interaction, add_remove: app_commands.Choice[str], valor: int, item: app_commands.Choice[str], membro: discord.Member):
		allowed_users = [391625672050737163, 844272449168474193]
		if interaction.user.id in allowed_users:
			AddSaldo(membro, add_remove.value , item.value, valor)
			if item.value == 'astrite':
				item_name = '[ <:item_astrite:1251257679545110641> ] Astrite'
			elif item.value == 'lustrous':
				item_name = '[ <:item_lustrous:1251257743554248765> ] Lustrous Tide'
			elif item.value == 'radiant':
				item_name = '[ <:item_radiant:1251257713363648653> ] Radiant Tide'
			elif item.value == 'forging':
				item_name = '[ <:item_weapon:1251257727095668838> ] Forging Tide'
			await interaction.response.send_message(f'{item_name} {add_remove.value}{valor} para {membro.display_name}')

	@app_commands.command(name='convene', description='Visualize e atire no banner')
	async def convene(self, interaction: discord.Interaction):
		check = membstat.find_one({'_id': interaction.user.id})
		if check is None:
			await interaction.response.send_message(f'{interaction.user.display_name} não tem registro')
		author = interaction.user
		class Dropdown(discord.ui.Select):
			def __init__(self):
				options = [
			discord.SelectOption(label='Banner Personagem Limitado', value='https://i.ibb.co/ByVYZHS/174-Sem-T-tulo-20240601033931.png', description='Banner de personagem de evento limitado!', emoji='<:item_radiant:1251257713363648653>'),
			discord.SelectOption(label='Banner Arma Limitado', value='https://i.ibb.co/fn364QL/IMG-3326.jpg', description='Banner de arma de evento limitado!', emoji='<:item_weapon:1251257727095668838>'),
			discord.SelectOption(label='Banner Personagem Ilimitado', value='https://i.ibb.co/XXfdnQj/IMG-3327.jpg', description='Banner de personagem de evento ilimitado', emoji='<:item_lustrous:1251257743554248765>'),
			discord.SelectOption(label='Banner Arma Ilimitado', description='Banner de arma de evento ilimitado', emoji='<:item_lustrous:1251257743554248765>')
		]
				super().__init__(placeholder='Escolha o banner...', min_values=1, max_values=1, options=options)

			async def callback(self, interaction: discord.Interaction):
				authorcmd = author
				selected_value = self.values[0]
				selected_option = next(option for option in self.options if option.value == selected_value)
				label = selected_option.label
				value = selected_option.value
				emojis = selected_option.emoji
				class ConveneAction(discord.ui.View):
					def __init__(self):
						super().__init__()
					@discord.ui.button(label="1x  Convene x1", style=discord.ButtonStyle.blurple, emoji=emojis)
					async def convene_1(self, interaction: discord.Interaction, button: discord.ui.Button):
						banner = 'perlim1'
						if label == 'Banner Personagem Limitado':
							tiro = 'radiant'       
						elif label == 'Banner Arma Limitado':
							tiro = 'forging'
						elif label == 'Banner Personagem Ilimitado':
							tiro = 'lustrous'
						elif label == 'Banner Arma Ilimitado':
							tiro = 'lustrous'
						checkbal = membstat.find_one({"_id": interaction.user.id})[tiro]
						if interaction.user == author and checkbal >= 1:
							if tiro == 'radiant':
								conveneperlim = ConvenePerLim(interaction.user, banner)
								result, resultados, categoria, url_imagem, url_imagem10 = conveneperlim
							elif tiro == 'lustrous':
								conveneperilim = ConvenePerIlim(interaction.user, banner)
								result, resultados, categoria, url_imagem, url_imagem10 = conveneperilim
							membstat.update_one({'_id': interaction.user.id},{'$inc':{tiro: -1}})
							e = discord.Embed(title=f'__***{interaction.user.display_name} ATIROU 1x EM {label} !!!***__')
							e.set_image(url=url_imagem)
							
							await interaction.response.edit_message(embed=e, view=None)
							await asyncio.sleep(6)
							e = discord.Embed(title=interaction.user.display_name)
							e.add_field(name=f'1 - {result}', value='')
							await interaction.channel.send(embed=e)
							AddInv(interaction.user, result, banner)
						else:
							await interaction.response.send_message('Você não tem tiros o suficiente!', ephemeral=True)
							 
					@discord.ui.button(label="10x  Convene x10", style=discord.ButtonStyle.blurple, emoji=emojis)
					async def convene_10(self, interaction: discord.Interaction, button: discord.ui.Button):
						banner = 'perlim10'
						if label == 'Banner Personagem Limitado':
							tiro = 'radiant'
						elif label == 'Banner Arma Limitado':
							tiro = 'radiant'
						elif label == 'Banner Personagem Ilimitado':
							tiro = 'lustrous'
						elif label == 'Banner Arma Ilimitado':
							tiro = 'lustrous'
						class ConvenePull(discord.ui.View):
							def __init__(self):
								super().__init__()
							@discord.ui.button(label="", style=discord.ButtonStyle.gray, emoji='⏩')
							async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
								e.add_field(name=resultados[f'tiro{n+1}'])
								n = n+1

						checkbal = membstat.find_one({"_id": interaction.user.id})[tiro]
						if interaction.user == author and checkbal >= 10:
							if tiro == 'radiant':
								conveneperlim = ConvenePerLim(interaction.user, banner)
								result, resultados, categoria, url_imagem, url_imagem10 = conveneperlim
							elif tiro == 'lustrous':
								conveneperilim = ConvenePerIlim(interaction.user, banner)
								result, resultados, categoria, url_imagem, url_imagem10 = conveneperilim
							membstat.update_one({'_id': interaction.user.id},{'$inc':{tiro: -10}})
							e = discord.Embed(title=f'__***{interaction.user.display_name} ATIROU 10x EM {label} !!!***__')
							e.set_image(url=url_imagem10)
							await interaction.response.edit_message(embed=e, view=None)
							await asyncio.sleep(6)
							e = discord.Embed(title=f'***{interaction.user.display_name}***')
							for l in range(1,11):
								result = resultados[f'tiro{l}']
								AddInv(interaction.user, result, banner)
							tiroo = resultados[f'tiro1']
							e.add_field(name=f'1 - {tiroo}', value='')
							num = 2
							class ConvenePull(discord.ui.View):
								def __init__(self):
									super().__init__()
									self.num = 2
								@discord.ui.button(label="", style=discord.ButtonStyle.gray, emoji='▶️')
								async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
											if interaction.user == author:
												tironame = resultados[f'tiro{self.num}']
												e.add_field(name=f'{self.num} - {tironame}', value='')
												if self.num <= 9:
													await interaction.response.edit_message(embed=e)
													self.num = self.num+1
												else:
													await interaction.response.edit_message(embed=e, view=None)
									
								@discord.ui.button(label="SKIP", style=discord.ButtonStyle.gray, emoji='⏩')
								async def skip(self, interaction: discord.Interaction, button: discord.ui.Button):
									if interaction.user == author:
										for _ in range(self.num,11):
											tironamee = resultados[f'tiro{self.num}']
											e.add_field(name=f'{self.num} - {tironamee}', value='')
											result = resultados[f'tiro{self.num}']
											self.num = self.num+1
										await interaction.response.edit_message(embed=e, view=None)

							await interaction.channel.send(embed=e, view=ConvenePull())
						else:
							await interaction.response.send_message('Você não tem tiros o suficiente!', ephemeral=True)
					@discord.ui.button(label="Pity", style=discord.ButtonStyle.gray, emoji='❕')
					async def pity_view(self, interaction: discord.Interaction, button: discord.ui.Button):
						if label == 'Banner Personagem Limitado':
							rpity4 = 'pity4perlim'
							rpity5 = 'pity5perlim'
						elif label == 'Banner Arma Limitado':
							rpity4 = 'pity4armlim'
							rpity5 = 'pity5armlim'
						elif label == 'Banner Personagem Ilimitado':
							rpity4 = 'pity4perilim'
							rpity5 = 'pity5perilim'
						elif label == 'Banner Arma Ilimitado':
							rpity4 = 'pity4armilim'
							rpity5 = 'pity5armilim'
						pity4 = membstat.find_one({"_id": interaction.user.id})[rpity4]
						pity5 = membstat.find_one({"_id": interaction.user.id})[rpity5]
						e = discord.Embed(title=f'**Pity de:** __***{interaction.user.display_name}***__', description=f'Banner: ***{label}***')
						e.add_field(name='[⭐] 4 Estrelas: ', value=pity4)
						e.add_field(name='[⭐] 5 Estrelas: ', value=pity5)
						if label == 'Banner Personagem Limitado':
							garantido = membstat.find_one({"_id": interaction.user.id})['garantido']
							if garantido == 'nao':
								rgaran = '❌'
							else:
								rgaran = '✅'
							e.add_field(name='[⭐] Garantido: ', value=rgaran)
						await interaction.response.edit_message(embed=e, view=ConveneAction())
				if interaction.user == authorcmd:
					e = discord.Embed(title=f'__***{label}***__')
					e.set_image(url=value)
					await interaction.response.edit_message(embed=e, view=ConveneAction())

		class DropdownView(discord.ui.View):
			def __init__(self):
				super().__init__()

				self.add_item(Dropdown())
		await interaction.response.send_message('Selecione o banner que queira ver:', view=DropdownView())

	@app_commands.command(name='inventario', description='Veja seus personagens e armas')
	async def inventory(self, interaction:discord.Interaction, membro: discord.Member = None):
		if membro is None:
			membro = interaction.user
		check = membstat.find_one({'_id': membro.id})
		
		if check is None:
			await interaction.response.send_message(f'{membro.display_name} não tem registro')
		e = discord.Embed(title=f'Inventário de: {membro.display_name}')
		start_displaying = False
		for field, value in check.items():
			if field == 'Inventário':
				start_displaying = True
			if start_displaying and field != '_id':
				e.add_field(name=field, value=str(value), inline=False)
		if len(e.fields) == 0:
			await interaction.response.send_message('Não há itens para exibir.')
		else:
			await interaction.response.send_message(embed=e)

	@app_commands.command(name='daily', description='Pegue suas astrites diárias')
	async def daily(self, interaction:discord.Interaction):
		check = membstat.find_one({'_id': interaction.user.id})
		if check is None:
			await interaction.response.send_message(f'{interaction.user.display_name} não tem registro')
		result = random.randrange(50, 400)
		astrite = int(result)
		current_time = time.time()
		check = membstat.find_one({'_id': interaction.user.id})['daily']
		if current_time - check < 86400:
			remaining_time = 86400 - (current_time - check)
			await interaction.response.send_message(f'{interaction.user.display_name} já resgatou seu daily, tente novamente em {remaining_time / 3600:.1f} horas')
		else:
			membstat.update_one(
			{'_id': interaction.user.id},{'$set': {'daily': current_time}, '$inc': {'astrite': astrite}})
			if result < 40:
				message = f'Recebeu apenas [ <:item_astrite:1251257679545110641> ] +{result} de seu daily'
			elif result < 140:
				message = f'Recebeu [ <:item_astrite:1251257679545110641> ] +{result} de seu daily'
			else:
				message = f'Recebeu [ <:item_astrite:1251257679545110641> ] +{result} de seu daily, que sorte!'
			await interaction.response.send_message(f'{interaction.user.display_name} {message}')

	@app_commands.command(name='shop', description='Loja para comprar tiros e outros recursos')
	@app_commands.choices(item=[
		app_commands.Choice(name="[ 🔵 ] Lustrous Tide", value='lustrous'),
		app_commands.Choice(name="[ 🟡 ] Radiant Tide", value='radiant')
		])
	async def shop(self, interaction:discord.Interaction, item: app_commands.Choice[str] = None, valor: int = None):
		check = membstat.find_one({'_id': interaction.user.id})
		if check is None:
			await interaction.response.send_message(f'{interaction.user.display_name} não tem registro')
		if item == None and valor == None:
			e = discord.Embed(title=f'{interaction.user.display_name}', description='__***LOJINHA DA LUCIAGOD!***__\n[ ⚠️ ] **Para visualizar a loja, apenas use /shop, para comprar, use /shop - item - valor**')
			e.add_field(name='[ <:item_lustrous:1251257743554248765> ] Lustrous Tide', value='<:item_astrite:1251257679545110641> 160')
			e.add_field(name='[ <:item_radiant:1251257713363648653> ] Radiant Tide', value='<:item_astrite:1251257679545110641> 160')
			await interaction.response.send_message(embed=e)
		elif item == None or valor == None:
			await interaction.response.send_message('Comando inválido! certifique-se de que você definiu o item e o valor', ephemeral=True)
		else:
			check = membstat.find_one({'_id': interaction.user.id})['astrite']
			custo = 160 * valor
			if check >= custo:
				membstat.update_one(
				{'_id': interaction.user.id},{'$inc': {item.value: valor, 'astrite': -custo}})
				await interaction.response.send_message(f'**Compra de: {interaction.user.display_name}**: {item.name} +{valor}')
			else:
				await interaction.response.send_message('Você não tem astrites suficiente', ephemeral=True)

	@app_commands.command(name='bet', description='Aposte uma certa quantidade de astrite com algum membro')
	async def bet(self, interaction: discord.Interaction, valor: int):
		check = membstat.find_one({'_id': interaction.user.id})
		if check is None:
			await interaction.response.send_message(f'{interaction.user.display_name} não tem registro')
		class Bet(discord.ui.View):
			def __init__(self, user_id, interaction: discord.Interaction, valor):
				super().__init__(timeout=60)
				self.user_id = user_id
				self.interaction = interaction
				self.winner = None
				self.loser = None
				self.valor = valor
			@discord.ui.button(label="Participar", style=discord.ButtonStyle.green)
			async def bet(self, interaction: discord.Interaction, button: discord.ui.Button):
				if interaction.user.id != self.user_id:
					checkp = membstat.find_one({'_id': interaction.user.id})['astrite']
					if checkp >= self.valor:
						participants = [self.interaction.user, interaction.user]
						self.winner = random.choice(participants)
						participants.remove(self.winner)  # Remove o vencedor da lista de participantes
						self.loser = participants[0] if participants else None
						membstat.update_one({'_id': self.winner.id},{'$inc': {'astrite': valor}})
						membstat.update_one({'_id': self.loser.id},{'$inc': {'astrite': -valor}})
						await interaction.response.send_message(f'{self.winner.mention} ganhou a aposta, saindo com +{valor}!')
						self.stop()
					else:
						await interaction.response.send_message('Você não tem astrites o suficiente', ephemeral=True)
			async def on_timeout(self):
				for child in self.children:
					if isinstance(child, discord.ui.Button):
						child.disabled = True
					await self.interaction.edit_original_response(content="Ninguém clicou no botão a tempo!", view=None)
		check = membstat.find_one({'_id': interaction.user.id})['astrite']
		if check >= valor:
			await interaction.response.send_message(f'{interaction.user.display_name} está apostando: {valor}', view=Bet(interaction.user.id, interaction, valor))
		else:
			await interaction.response.send_message(f'Você não tem astrites o suficiente', ephemeral=True)

	@app_commands.command(name='fight', description='Lute contra echos')
	async def start_fight(self, interaction: discord.Interaction):
		check = membstat.find_one({'_id': interaction.user.id})
		if check is None:
			await interaction.response.send_message(f'{interaction.user.display_name} não tem registro')
		current_time = time.time()
		check = membstat.find_one({'_id': interaction.user.id})['fight']
		if current_time - check < 120:
			remaining_time = 120 - (current_time - check)
			await interaction.response.send_message(f'{interaction.user.display_name} já lutou com echo, tente novamente em {remaining_time / 60:.1f} minutos')
		else:
			membstat.update_one(
			{'_id': interaction.user.id},{'$set': {'fight': current_time}})
			enemy = {
				"Union 1 - 19": {
					"enemy": [{"name": ["1⭐ SabyrBoar", "1⭐ Hooscamp", "1⭐ Gulpuff"], "hp": 110, "dmg": 10, "xp": random.randint(80, 200), "stats": random.choice(('atk', 'hp'))},
				{"name": ["3⭐ Hoochief", "3⭐ Chaserazor", "3⭐ Roseshroom"], "hp": 130, "dmg": 15, "xp": random.randint(90, 200), "stats": random.choice(('energy', 'atk', 'hp'))},
				{"name": ["3⭐ Violet-Feathered Heron", "3⭐ Tambourinist", "3⭐ Spearback"], "hp": 160, "dmg": 20, "xp": random.randint(110, 220), "stats": random.choice(('energy', 'atk', 'hp'))},
				{"name": ["4⭐ Mech Abomination", "4⭐ Mourning Aix ", "4⭐ Lampylumen Myriad"], "hp": 190, "dmg": 30, "xp": random.randint(150, 300), "stats": random.choice(('dmg', 'rate'))}],
				},
				"Union 20 - 39": {
					"enemy": [{"name": ["1⭐ZigZag", "1⭐ TickTack", "1⭐ SnipSnap"], "hp": 360, "dmg": 35, "xp": random.randint(90, 220), "stats": random.choice(('atk', 'hp'))},
				{"name": ["3⭐ ChasmGuardian", "3⭐ GeohideSaurian", "3⭐ Rocksteady Guardian"], "hp": 390, "dmg": 50, "xp": random.randint(110, 230), "stats": random.choice(('energy', 'atk', 'hp'))},
				{"name": ["3⭐ Havoc Dreadmanen", "3⭐ Flautist", "3⭐ Autopuppet Scout"], "hp": 450, "dmg": 65, "xp": random.randint(110, 250), "stats": random.choice(('energy', 'atk', 'hp'))},
				{"name": ["4⭐ Mech Abomination", "4⭐ Mourning Aix ", "4⭐ Lampylumen Myriad"], "hp": 550, "dmg": 90, "xp": random.randint(140, 300), "stats": random.choice(('dmg', 'rate'))}],
				}
			}
			unionperso = membstat.find_one({"_id": interaction.user.id})['unionlvl']
			if unionperso <= 19:
				inimigos = enemy["Union 1 - 19"]["enemy"]
				inimigo_aleatorio = random.choice(inimigos)
				enemyname = random.choice(inimigo_aleatorio["name"])
				enemyhp = inimigo_aleatorio["hp"]
				enemyxp = inimigo_aleatorio["xp"]
				enemystat = inimigo_aleatorio["stats"]
				enemydmg = inimigo_aleatorio["dmg"]
			elif unionperso <= 39:
				inimigos = enemy["Union 20 - 39"]["enemy"]
				inimigo_aleatorio = random.choice(inimigos)
				enemyname = random.choice(inimigo_aleatorio["name"])
				enemyhp = inimigo_aleatorio["hp"]
				enemyxp = inimigo_aleatorio["xp"]
				enemystat = inimigo_aleatorio["stats"]
				enemydmg = inimigo_aleatorio["dmg"]

			persohp = membstat.find_one({"_id": interaction.user.id})['hp']
			persoatk = membstat.find_one({"_id": interaction.user.id})['atk']
			e = discord.Embed(title=f'FIGHT: {interaction.user.display_name}', description=f'**[ ⚠️ ] Cooldown de 30 minutos.\nConfira seus status**')
			e.add_field(name=f'[ ❤️ ] {interaction.user.display_name}', value=persohp, inline=True)
			e.add_field(name=f'[ ❤️ ] {enemyname}', value=f'{enemyhp}', inline=True)
			e.add_field(name='\u200b', value='\u200b', inline=True)
			e.add_field(name=f'[ ⚔️ ] {interaction.user.display_name}', value=persoatk, inline=True)
			e.add_field(name=f'[ ⚔️ ] {enemyname}', value=enemydmg, inline=True)
			e.add_field(name='\u200b', value='\u200b', inline=True)
			e.add_field(name=f'Status do Echo', value=enemystat, inline=False)
			class Fight(discord.ui.View):
				def __init__(self, interaction: discord.Interaction, persohp, persoatk, enemyname, enemyhp, enemydmg, enemystat, enemyxp):
					super().__init__()
					self.interaction = interaction
					self.persohp = persohp
					self.persoatk = persoatk
					self.persoenergy = membstat.find_one({"_id": interaction.user.id})['energy']
					self.energy = 0
					self.persorate = membstat.find_one({"_id": interaction.user.id})['rate']
					self.persodmg = membstat.find_one({"_id": interaction.user.id})['dmg']
					self.enemyname = enemyname
					self.enemyhp = enemyhp
					self.enemydmg = enemydmg
					self.enemystat = enemystat
					self.enemyxp = enemyxp
					self.message = None 
				@discord.ui.button(label="Attack", style=discord.ButtonStyle.red)
				async def attack(self, interaction: discord.Interaction, button: discord.ui.Button):
					if interaction.user == self.interaction.user:
						rate = random.uniform(0, 100)
						if rate <= self.persorate:
							msg = '**[ ⚔️ ] CRITICAL: **'
							damage = random.randint(10, self.persoatk) + self.persodmg
						else:
							damage = random.randint(0, self.persoatk)
							msg = '[ ⚔️ ] ATK: '
						self.enemyhp -= damage
						self.energy = self.energy + self.persoenergy
						await self.check_fight(interaction, damage, msg)

				@discord.ui.button(label="Resonance Lib.", style=discord.ButtonStyle.blurple)
				async def resonance(self, interaction: discord.Interaction, button: discord.ui.Button):
					if interaction.user == self.interaction.user and self.energy >= 100:
						rate = random.uniform(0, 100)
						if rate <= self.persorate:
							msg = '**[ 🌀 ] RESONANCE LIB. CRITICAL: **'
							damage = random.randint(self.persoatk-5, self.persoatk+20) + self.persodmg
						else:
							damage = random.randint(self.persoatk-10, self.persoatk+20)
							msg = '[ 🌀 ]RESONANCE LIB. ATK: '
						self.enemyhp -= damage
						self.energy -= 100
						await self.check_fight(interaction, damage, msg)
					elif interaction.user == self.interaction.user and self.energy < 100:
						await interaction.response.send_message('Você não tem energia suficiente', ephemeral=True)
				async def check_fight(self, interaction: discord.Interaction, damage, msg):
					if self.enemyhp <= 0:
						self.enemyhp = 0
						e = discord.Embed(title=f'Turno de {interaction.user.display_name}', description=f'{msg}{damage}')
						e.add_field(name=f'[ ❤️ ] {interaction.user.display_name}', value=self.persohp, inline=True)
						e.add_field(name=f'[ ❤️ ] {self.enemyname}', value=f'💥{self.enemyhp}', inline=True)
						e.add_field(name='\u200b', value='\u200b', inline=True)
						e.add_field(name=f'[ 🌀 ] {interaction.user.display_name}', value=self.energy, inline=True)
						await interaction.response.edit_message(embed=e, view=None)
						xp = self.enemyxp
						msg = AddXP(interaction.user, self.enemyxp)
						uxp = membstat.find_one({'_id': interaction.user.id})['unionxp']
						union = membstat.find_one({'_id': interaction.user.id})['unionlvl']
						userxp = membstat.find_one({'_id': interaction.user.id})['unionxp']
						unionreq = membstat.find_one({'_id': interaction.user.id})['unionreq']
						astritegain = random.randint(5,150)
						membstat.update_one({'_id': self.interaction.user.id},{'$inc':{'astrite': astritegain}})
						astrite = membstat.find_one({'_id': interaction.user.id})['astrite']
						userenergy = membstat.find_one({'_id': interaction.user.id})['energy']
						userrate = membstat.find_one({'_id': interaction.user.id})['rate']
						userdmg = membstat.find_one({'_id': interaction.user.id})['dmg']
						

						rate = random.uniform(0,100)
						if self.enemystat in ('hp', 'atk') and rate <= 50:
							gain = random.randint(1, 3)
							membstat.update_one({'_id': self.interaction.user.id},{'$inc':{self.enemystat: gain}})
							gainmsg = f'Echo absorb: **+{gain} {self.enemystat}**'
						elif self.enemystat in ('energy', 'rate', 'dmg') and rate <= 50:
							stat = membstat.find_one({'_id': interaction.user.id})[self.enemystat]
							if stat >= 30:
								gain = random.randint(2, 4)
								membstat.update_one({'_id': self.interaction.user.id},{'$inc':{self.enemystat: gain}})
								gainmsg = f'Echo absorb: **+{gain} {self.enemystat}**'
							elif stat >= 50:
								gain = random.randint(1, 2)
								membstat.update_one({'_id': self.interaction.user.id},{'$inc':{self.enemystat: gain}})
								gainmsg = f'Echo absorb: **+{gain} {self.enemystat}**'
							else:
								gain = random.randint(2, 5)
								membstat.update_one({'_id': self.interaction.user.id},{'$inc':{self.enemystat: gain}})
								gainmsg = f'Echo absorb: **+{gain} {self.enemystat}**'
						else:
							gainmsg = ''
						await interaction.channel.send(f'{interaction.user.display_name} derrotou {self.enemyname}\n[ ✨ ] +{xp}XP `{uxp}/{unionreq}xp - ⭐ Union Level: {union}`\n[ <:item_astrite:1251257679545110641> ] +{astritegain}\n{gainmsg}')
						if msg != None:
							await interaction.channel.send(msg)
						self.stop()
					else:
						e = discord.Embed(title=f'Turno de {interaction.user.display_name}', description=f'{msg}{damage}')
						e.add_field(name=f'[ ❤️ ] {interaction.user.display_name}', value=self.persohp, inline=True)
						e.add_field(name=f'[ ❤️ ] {self.enemyname}', value=f'💥{self.enemyhp}', inline=True)
						e.add_field(name='\u200b', value='\u200b', inline=True)
						e.add_field(name=f'[ 🌀 ] {interaction.user.display_name}', value=self.energy, inline=True)
						await interaction.response.edit_message(embed=e, view=None)
						await asyncio.sleep(3)
						damage = random.randint(0,self.enemydmg)
						self.persohp -= damage
						e = discord.Embed(title=f'Turno do Echo', description=f'ATK: {damage}')
						message = await interaction.edit_original_response()
						if self.persohp <= 0:
							self.persohp = 0
							e.add_field(name=f'[ ❤️ ] {interaction.user.display_name}', value=f'💥{self.persohp}', inline=True)
							e.add_field(name=f'[ ❤️ ] {self.enemyname}', value=self.enemyhp, inline=True)
							e.add_field(name='\u200b', value='\u200b', inline=True)
							e.add_field(name=f'[ 🌀 ] {interaction.user.display_name}', value=self.energy, inline=True)
							message = await interaction.edit_original_response()
							await message.edit(embed=e, view=None)
							await interaction.channel.send(f'O Echo derrotou {interaction.user.display_name}')
							self.stop()
						else:
							e.add_field(name=f'[ ❤️ ] {interaction.user.display_name}', value=f'💥{self.persohp}', inline=True)
							e.add_field(name=f'[ ❤️ ] {self.enemyname}', value=self.enemyhp, inline=True)
							e.add_field(name='\u200b', value='\u200b', inline=True)
							e.add_field(name=f'[ 🌀 ] {interaction.user.display_name}', value=self.energy, inline=True)
							await message.edit(embed=e, view=self)

			await interaction.response.send_message(embed=e, view=Fight(interaction, persohp, persoatk, enemyname, enemyhp, enemydmg, enemystat, enemyxp))

	@app_commands.command(name='status', description='veja seus status')
	async def status(self, interaction: discord.Interaction, membro: discord.Member = None):
		if membro is None:
			membro = interaction.user
		check = membstat.find_one({'_id': membro.id})
		if check is None:
			await interaction.response.send_message(f'{membro.display_name} não tem registro')
		e = discord.Embed(title=f'Status de: {membro.display_name}')
		e.add_field(name='❤️ HP', value=membstat.find_one({"_id": membro.id})['hp'])
		e.add_field(name='⚔️ ATK', value=membstat.find_one({"_id": membro.id})['atk'])
		e.add_field(name='🌀 Energy Regen', value=membstat.find_one({"_id": membro.id})['energy'])
		e.add_field(name='💢 Crit. Rate', value=membstat.find_one({"_id": membro.id})['rate'])
		e.add_field(name='💥 Crit. DMG', value=membstat.find_one({"_id": membro.id})['dmg'])
		e.add_field(name='⭐ Union Level', value=membstat.find_one({"_id": membro.id})['unionlvl'])
		unionxp = membstat.find_one({"_id": membro.id})['unionxp']
		unionreq = membstat.find_one({"_id": membro.id})['unionreq']
		e.add_field(name='🌠 Union XP', value=f'{unionreq}/{unionreq}')
		await interaction.response.send_message(embed=e)

	@app_commands.command(name='help', description='conheça o bot e seus comandos')
	async def help(self, interaction: discord.Interaction):
		e = discord.Embed(title='HELP LUCIAGOD', description='LuciaGOD é um bot brasileiro baseado no game: Wuthering Waves, atualmente está em BETA, sendo assim, tenha em mente que o bot está sujeito a falhas e erros, além de ter sido por uma pessoa apenas: ```Koutama Kazegashira#4130```\n**[ ⚠️ ] Lembre-se de se registrar antes de usar, todos os comandos são em slash ( / ) e alguns podem falhar caso não tenha feito o registro\n[ ⚠️ ] BANNER DE ARMAS AINDA EM DESENVOLVIMENTO!**')
		e.set_author(name='LuciaGOD', icon_url='https://cdn.discordapp.com/attachments/1241080711679836281/1252034110277554247/this-was-amazing-what-are-your-thoughts-are-the-recent-v0-844l4gvju9jc1.png?ex=6670bf21&is=666f6da1&hm=1ed7e24949fa5ff183e9b52c2818d54073affe5c252af5c2820d07e30064921&')
		e.add_field(name='registrar-se', value='Se registrar no bot para liberar os comandos')
		e.add_field(name='saldo', value='Ver o seu saldo no bot (ex: Lustrous Tides, Radiant Tides, etc.)')
		e.add_field(name='status', value='Ver o seus status no bot (ex: union, hp, atk, etc.)')
		e.add_field(name='inventario', value='Ver o seu inventário de personagens: (ps: sujeito a falhas)')
		e.add_field(name='convene', value='Atire nos banners (Banner de arma em desnvolvimento) é necessário usar tiros ao invés de astrites para atirar nos banners.')
		e.add_field(name='shop', value='Ver a loja da Lucia (/shop - item - valor para comprar item)')
		e.add_field(name='daily', value='Resgate suas astrites diárias')
		e.add_field(name='fight', value='Lute contra echos para ganhar xp, status e astrites')
		e.add_field(name='bet', value='Desafie membros apostando uma certa quantidade de astrites')
		e.set_footer(text=f"Comando por: {interaction.user.display_name}")
		await interaction.response.send_message(embed=e)


async def setup(client):
	await client.add_cog(Status(client))