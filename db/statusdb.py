import discord
from utils.core import configData
from pymongo import MongoClient
import random

cluster = MongoClient(configData['MONGODB'])
db = cluster['BotWuWa']
membstat = db['StatusInfos']

def CreateProfile(user: discord.Member, astrite, lustrous, radiant, resona):
    insert = {
        '_id': user.id,
        'astrite': astrite,
        'lustrous': lustrous,
        'radiant': radiant,
        'forging': 0,
        'daily': 0,
        'fight': 0,

        'hp': 100,
        'atk': 15,
        'energy': 15,
        'rate': 10,
        'dmg': 10,

        'unionlvl': 1,
        'unionxp': 0,
        'unionreq': 400,


        'pity4perlim': 0,
        'pity5perlim': 0,
        'pity4armlim': 0,
        'pity5armlim': 0,
        'pity4perilim': 0,
        'pity5perilim': 0,
        'pity4armilim': 0,
        'pity5armilim': 0,

        'garantido': 'nao',
        'Inventário': '-'
    }
    membstat.insert_one(insert)

def EraseProfile(user: discord.Member):
    membstat.delete_one(
        {
            '_id': user.id,
        }
    )
    
def AddSaldo(user: discord.Member, sinal, item, valor: int):
    if sinal == '-':
        valor = -valor
    membstat.update_one(
        {
            '_id': user.id
        },
        {
            '$inc':{
                item: valor
            }
        }
    )
    
def ConvenePerLim(user: discord.Member, banner):
    def Pity():
        itens = {
            "5 estrelas": {
                "personagens": ["[⭐] Encore", "[⭐] Verina", "[⭐] Calcharo", "[⭐] Lingyang", "[⭐] Jianxin"],
                "url_imagem": "https://media.discordapp.net/attachments/1211401681690951820/1246357519186530355/IMG_3315.gif?ex=665cc124&is=665b6fa4&hm=abe6d4b055e32a22d92a4c65d590d6be19412ce5622f81406d34a140c82c13bd&="
            },
            "4 estrelas": {
                "personagens": ["[🟣] Chixia", "[🟣] Mortefi", "[🟣] Danjin", "[🟣] Yangyang", "[🟣] Baizhi", "[🟣] Aalto", "[🟣] Taoqi", "[🟣] Sanhua", "[🟣] Yuanwu"],
                "url_imagem": "https://media.discordapp.net/attachments/1211401681690951820/1246357453789200384/IMG_3313.gif?ex=665cc115&is=665b6f95&hm=487d1c62bba0c8b10e177900ef156ce7de0eeb423b06a908065feb01682ad798&="
            },
            "3 estrelas": {
                "personagens": ["[🔷] demais armas"],
                "url_imagem": "https://cdn.discordapp.com/attachments/1211401681690951820/1246357485846007828/IMG_3314.gif?ex=665cc11c&is=665b6f9c&hm=54a3e32cfdab29465194ba01124fccf13ef435e1e75216dc223119dca614f64d&"
            }
        }

        chance = random.uniform(0, 100)
        categoria = ""
        pity4 = membstat.find_one({"_id": user.id})['pity4perlim']
        pity5 = membstat.find_one({"_id": user.id})['pity5perlim']
        garantido = membstat.find_one({"_id": user.id})['garantido']
        if banner == 'perlim1':
            resultados = ''
            url_imagem10 = ''
            if pity5 == 79:
                categoria = "5 estrelas"
                if garantido == 'sim':
                    result = '[⭐] Jiyan'
                    url_imagem = itens[categoria]["url_imagem"]
                    membstat.update_one(
                {
                    '_id': user.id
                },
                {
                    '$set':{
                        'pity5perlim': 0,
                        'garantido': 'nao'
                    },
                    '$inc':{
                        'pity4perlim': 1
                    }
                })
                else:
                    result = "[⭐] Jiyan" if random.uniform(0, 100) < 50 else random.choice(itens[categoria]["personagens"])
                    url_imagem = itens[categoria]["url_imagem"]
                    if result == '[⭐] Jiyan':
                        membstat.update_one(
                    {
                        '_id': user.id
                    },
                    {
                        '$set':{
                            'pity5perlim': 0,
                            'garantido': 'nao'
                        },
                        '$inc':{
                            'pity4perlim': 1
                        }
                    })
                    else:
                        membstat.update_one(
                    {
                        '_id': user.id
                    },
                    {
                        '$set':{
                            'pity5perlim': 0,
                            'garantido': 'sim'
                        },
                        '$inc':{
                            'pity4perlim': 1
                        }
                    })
            elif pity4 == 9:
                categoria = "4 estrelas"
                result = random.choice(itens[categoria]["personagens"])
                url_imagem = itens[categoria]["url_imagem"]
                membstat.update_one(
            {
                '_id': user.id
            },
            {
                '$set':{
                    'pity4perlim': 0
                },
                '$inc':{
                    'pity5perlim': 1
                }
            })
            elif chance < 0.8:
                categoria = "5 estrelas"
                categoria = "5 estrelas"
                if garantido == 'sim':
                    result = '[⭐] Jiyan'
                    url_imagem = itens[categoria]["url_imagem"]
                    membstat.update_one(
                {
                    '_id': user.id
                },
                {
                    '$set':{
                        'pity5perlim': 0,
                        'garantido': 'nao'
                    },
                    '$inc':{
                        'pity4perlim': 1
                    }
                })
                else:
                    result = "[⭐] Jiyan" if random.uniform(0, 100) < 50 else random.choice(itens[categoria]["personagens"])
                    url_imagem = itens[categoria]["url_imagem"]
                    if result == '[⭐] Jiyan':
                        membstat.update_one(
                    {
                        '_id': user.id
                    },
                    {
                        '$set':{
                            'pity5perlim': 0,
                            'garantido': 'nao'
                        },
                        '$inc':{
                            'pity4perlim': 1
                        }
                    })
                    else:
                        membstat.update_one(
                    {
                        '_id': user.id
                    },
                    {
                        '$set':{
                            'pity5perlim': 0,
                            'garantido': 'sim'
                        },
                        '$inc':{
                            'pity4perlim': 1
                        }
                    })
            elif chance < 6.0:
                categoria = "4 estrelas"
                result = random.choice(itens[categoria]["personagens"])
                url_imagem = itens[categoria]["url_imagem"]
                membstat.update_one(
            {
                '_id': user.id
            },
            {
                '$set':{
                    'pity4perlim': 0
                },
                '$inc':{
                    'pity5perlim': 1
                }
            })
            else:
                categoria = "3 estrelas"
                result = random.choice(itens[categoria]["personagens"])
                url_imagem = itens[categoria]["url_imagem"]
                membstat.update_one(
            {
                '_id': user.id
            },
            {
                '$inc':{
                    'pity4perlim': 1,
                    'pity5perlim': 1
                }
            }
            )
                
        elif banner == 'perlim10':
            resultados = {}
            maior = {}
            maior[f"maior1"] = 0
            for i in range (1,11):
                chance = random.uniform(0, 100)
                apity4 = membstat.find_one({"_id": user.id})['pity4perlim']
                apity5 = membstat.find_one({"_id": user.id})['pity5perlim']
                garantido = membstat.find_one({"_id": user.id})['garantido']
                if apity5 == 79:
                    categoria = "5 estrelas"
                    if garantido == 'sim':
                        result = '[⭐] Jiyan'
                        url_imagem = itens[categoria]["url_imagem"]
                        membstat.update_one(
                    {
                        '_id': user.id
                    },
                    {
                        '$set':{
                            'pity5perlim': 0,
                            'garantido': 'nao'
                        },
                        '$inc':{
                            'pity4perlim': 1
                        }
                    })
                    else:
                        result = "[⭐] Jiyan" if random.uniform(0, 100) < 50 else random.choice(itens[categoria]["personagens"])
                        url_imagem = itens[categoria]["url_imagem"]
                        if result == '[⭐] Jiyan':
                            membstat.update_one(
                        {
                            '_id': user.id
                        },
                        {
                            '$set':{
                                'pity5perlim': 0,
                                'garantido': 'nao'
                            },
                            '$inc':{
                                'pity4perlim': 1
                            }
                        })
                        else:
                            membstat.update_one(
                        {
                            '_id': user.id
                        },
                        {
                            '$set':{
                                'pity5perlim': 0,
                                'garantido': 'sim'
                            },
                            '$inc':{
                                'pity4perlim': 1
                            }
                        })
                elif apity4 == 9:
                    categoria = "4 estrelas"
                    result = random.choice(itens[categoria]["personagens"])
                    url_imagem = itens[categoria]["url_imagem"]
                    membstat.update_one(
                {
                    '_id': user.id
                },
                {
                    '$set':{
                        'pity4perlim': 0
                    },
                    '$inc':{
                        'pity5perlim': 1
                    }
                })
                elif chance < 0.8:
                    categoria = "5 estrelas"
                    categoria = "5 estrelas"
                    if garantido == 'sim':
                        result = '[⭐] Jiyan'
                        url_imagem = itens[categoria]["url_imagem"]
                        membstat.update_one(
                    {
                        '_id': user.id
                    },
                    {
                        '$set':{
                            'pity5perlim': 0,
                            'garantido': 'nao'
                        },
                        '$inc':{
                            'pity4perlim': 1
                        }
                    })
                    else:
                        result = "[⭐] Jiyan" if random.uniform(0, 100) < 50 else random.choice(itens[categoria]["personagens"])
                        url_imagem = itens[categoria]["url_imagem"]
                        if result == '[⭐] Jiyan':
                            membstat.update_one(
                        {
                            '_id': user.id
                        },
                        {
                            '$set':{
                                'pity5perlim': 0,
                                'garantido': 'nao'
                            },
                            '$inc':{
                                'pity4perlim': 1
                            }
                        })
                        else:
                            membstat.update_one(
                        {
                            '_id': user.id
                        },
                        {
                            '$set':{
                                'pity5perlim': 0,
                                'garantido': 'sim'
                            },
                            '$inc':{
                                'pity4perlim': 1
                            }
                        })
                elif chance < 6.0:
                    categoria = "4 estrelas"
                    result = random.choice(itens[categoria]["personagens"])
                    url_imagem = itens[categoria]["url_imagem"]
                    membstat.update_one(
                {
                    '_id': user.id
                },
                {
                    '$set':{
                        'pity4perlim': 0
                    },
                    '$inc':{
                        'pity5perlim': 1
                    }
                })
                else:
                    categoria = "3 estrelas"
                    result = random.choice(itens[categoria]["personagens"])
                    url_imagem = itens[categoria]["url_imagem"]
                    membstat.update_one(
                {
                    '_id': user.id
                },
                {
                    '$inc':{
                        'pity4perlim': 1,
                        'pity5perlim': 1
                    }
                }
                )
                resultados[f"tiro{i}"] = result
                
                if categoria == "5 estrelas":
                    maior[f"maior1"] = 1
                elif categoria == '4 estrelas':
                    maior[f'maior2'] = 2
            if maior['maior1'] == 1:
                url_imagem10 = 'https://media.discordapp.net/attachments/1211401681690951820/1246357519186530355/IMG_3315.gif?ex=665cc124&is=665b6fa4&hm=abe6d4b055e32a22d92a4c65d590d6be19412ce5622f81406d34a140c82c13bd&='
            elif maior['maior2'] == 2 and maior['maior1'] == 0:
                url_imagem10 = 'https://media.discordapp.net/attachments/1211401681690951820/1246357453789200384/IMG_3313.gif?ex=665cc115&is=665b6f95&hm=487d1c62bba0c8b10e177900ef156ce7de0eeb423b06a908065feb01682ad798&='
                    
            result = ''
            categoria = ''

        return result, resultados, categoria, url_imagem, url_imagem10
        
        
    result, resultados, categoria, url_imagem, url_imagem10 = Pity()
    return result, resultados, categoria, url_imagem, url_imagem10
    
def ConvenePerIlim(user: discord.Member, banner):
    def Pity1():
        itens = {
            "5 estrelas": {
                "personagens": ["[⭐] Encore", "[⭐] Verina", "[⭐] Calcharo", "[⭐] Lingyang", "[⭐] Jianxin"],
                "url_imagem": "https://media.discordapp.net/attachments/1211401681690951820/1246357519186530355/IMG_3315.gif?ex=665cc124&is=665b6fa4&hm=abe6d4b055e32a22d92a4c65d590d6be19412ce5622f81406d34a140c82c13bd&="
            },
            "4 estrelas": {
                "personagens": ["[🟣] Chixia", "[🟣] Mortefi", "[🟣] Danjin", "[🟣] Yangyang", "[🟣] Baizhi", "[🟣] Aalto", "[🟣] Taoqi", "[🟣] Sanhua", "[🟣] Yuanwu"],
                "url_imagem": "https://media.discordapp.net/attachments/1211401681690951820/1246357453789200384/IMG_3313.gif?ex=665cc115&is=665b6f95&hm=487d1c62bba0c8b10e177900ef156ce7de0eeb423b06a908065feb01682ad798&="
            },
            "3 estrelas": {
                "personagens": ["[🔷] demais armas"],
                "url_imagem": "https://cdn.discordapp.com/attachments/1211401681690951820/1246357485846007828/IMG_3314.gif?ex=665cc11c&is=665b6f9c&hm=54a3e32cfdab29465194ba01124fccf13ef435e1e75216dc223119dca614f64d&"
            }
        }

        chance = random.uniform(0, 100)
        categoria = ""
        pity4 = membstat.find_one({"_id": user.id})['pity4perilim']
        pity5 = membstat.find_one({"_id": user.id})['pity5perilim']
        if banner == 'perlim1':
            resultados = ''
            url_imagem10 = ''
            if pity4 == 9:
                categoria = "4 estrelas"
                result = random.choice(itens[categoria]["personagens"])
                url_imagem = itens[categoria]["url_imagem"]
                membstat.update_one(
            {
                '_id': user.id
            },
            {
                '$set':{
                    'pity4': 0
                },
                '$inc':{
                    'pity5': 1
                }
            })
            elif pity5 == 79:
                categoria = "5 estrelas"
                result = random.choice(itens[categoria]["personagens"])
                url_imagem = itens[categoria]["url_imagem"]
                membstat.update_one(
            {
                '_id': user.id
            },
            {
                '$set':{
                    'pity5perilim': 0
                },
                '$inc':{
                    'pity4perilim': 1
                }
            })
            elif chance < 0.8:
                categoria = "5 estrelas"
                result = random.choice(itens[categoria]["personagens"])
                url_imagem = itens[categoria]["url_imagem"]
                membstat.update_one(
            {
                '_id': user.id
            },
            {
                '$set':{
                    'pity5perilim': 0
                },
                '$inc':{
                    'pity4perilim': 1
                }
            })
            elif chance < 6.0:
                categoria = "4 estrelas"
                result = random.choice(itens[categoria]["personagens"])
                url_imagem = itens[categoria]["url_imagem"]
                membstat.update_one(
            {
                '_id': user.id
            },
            {
                '$set':{
                    'pity4perilim': 0
                },
                '$inc':{
                    'pity5perilim': 1
                }
            })
            else:
                categoria = "3 estrelas"
                result = random.choice(itens[categoria]["personagens"])
                url_imagem = itens[categoria]["url_imagem"]
                membstat.update_one(
            {
                '_id': user.id
            },
            {
                '$inc':{
                    'pity4perilim': 1,
                    'pity5perilim': 1
                }
            }
            )
                
        elif banner == 'perlim10':
            resultados = {}
            maior = {}
            maior[f"maior1"] = 0
            for i in range (1,11):
                chance = random.uniform(0, 100)
                apity4 = membstat.find_one({"_id": user.id})['pity4perilim']
                apity5 = membstat.find_one({"_id": user.id})['pity5perilim']
                if apity5 == 79:
                    categoria = "5 estrelas"
                    result = random.choice(itens[categoria]["personagens"])
                    url_imagem = itens[categoria]["url_imagem"]
                    membstat.update_one(
                {
                    '_id': user.id
                },
                {
                    '$set':{
                        'pity5perilim': 0,
                        'pity4perilim': 0
                    }
                })
                elif apity4 == 9:
                    categoria = "4 estrelas"
                    result = random.choice(itens[categoria]["personagens"])
                    url_imagem = itens[categoria]["url_imagem"]
                    membstat.update_one(
                {
                    '_id': user.id
                },
                {
                    '$set':{
                        'pity4perilim': 0
                    },
                    '$inc':{
                        'pity5perilim': 1
                    }
                })
                elif chance < 1.8:
                    categoria = "5 estrelas"
                    result = random.choice(itens[categoria]["personagens"])
                    url_imagem = itens[categoria]["url_imagem"]
                    membstat.update_one(
                {
                    '_id': user.id
                },
                {
                    '$set':{
                        'pity5perilim': 0
                    },
                    '$inc':{
                        'pity4perilim': 1
                    }
                })
                elif chance < 12.0:
                    categoria = "4 estrelas"
                    result = random.choice(itens[categoria]["personagens"])
                    url_imagem = itens[categoria]["url_imagem"]
                    membstat.update_one(
                {
                    '_id': user.id
                },
                {
                    '$set':{
                        'pity4perilim': 0
                    },
                    '$inc':{
                        'pity5perilim': 1
                    }
                })
                else:
                    categoria = "3 estrelas"
                    result = random.choice(itens[categoria]["personagens"])
                    url_imagem = itens[categoria]["url_imagem"]
                    membstat.update_one(
                {
                    '_id': user.id
                },
                {
                    '$inc':{
                        'pity4perilim': 1,
                        'pity5perilim': 1
                    }
                }
                )
                resultados[f"tiro{i}"] = result
                
                if categoria == "5 estrelas":
                    maior[f"maior1"] = 1
                elif categoria == '4 estrelas':
                    maior[f'maior2'] = 2
            if maior['maior1'] == 1:
                url_imagem10 = 'https://media.discordapp.net/attachments/1211401681690951820/1246357519186530355/IMG_3315.gif?ex=665cc124&is=665b6fa4&hm=abe6d4b055e32a22d92a4c65d590d6be19412ce5622f81406d34a140c82c13bd&='
            elif maior['maior2'] == 2 and maior['maior1'] == 0:
                url_imagem10 = 'https://media.discordapp.net/attachments/1211401681690951820/1246357453789200384/IMG_3313.gif?ex=665cc115&is=665b6f95&hm=487d1c62bba0c8b10e177900ef156ce7de0eeb423b06a908065feb01682ad798&='
                    
            result = ''
            categoria = ''

        return result, resultados, categoria, url_imagem, url_imagem10
        
        
    result, resultados, categoria, url_imagem, url_imagem10 = Pity1()
    return result, resultados, categoria, url_imagem, url_imagem10

def ConveneArmLim(user: discord.Member, banner):
    def Pity():
        itens = {
            "5 estrelas": {
                "personagens": ["[⭐] Encore", "[⭐] Verina", "[⭐] Calcharo", "[⭐] Lingyang", "[⭐] Jianxin"],
                "url_imagem": "https://media.discordapp.net/attachments/1211401681690951820/1246357519186530355/IMG_3315.gif?ex=665cc124&is=665b6fa4&hm=abe6d4b055e32a22d92a4c65d590d6be19412ce5622f81406d34a140c82c13bd&="
            },
            "4 estrelas": {
                "personagens": ["[🟣] Chixia", "[🟣] Mortefi", "[🟣] Danjin", "[🟣] Yangyang", "[🟣] Baizhi", "[🟣] Aalto", "[🟣] Taoqi", "[🟣] Sanhua", "[🟣] Yuanwu"],
                "url_imagem": "https://media.discordapp.net/attachments/1211401681690951820/1246357453789200384/IMG_3313.gif?ex=665cc115&is=665b6f95&hm=487d1c62bba0c8b10e177900ef156ce7de0eeb423b06a908065feb01682ad798&="
            },
            "3 estrelas": {
                "personagens": ["[🔷] demais armas"],
                "url_imagem": "https://cdn.discordapp.com/attachments/1211401681690951820/1246357485846007828/IMG_3314.gif?ex=665cc11c&is=665b6f9c&hm=54a3e32cfdab29465194ba01124fccf13ef435e1e75216dc223119dca614f64d&"
            }
        }

        chance = random.uniform(0, 100)
        categoria = ""
        pity4 = membstat.find_one({"_id": user.id})['pity4perlim']
        pity5 = membstat.find_one({"_id": user.id})['pity5perlim']
        garantido = membstat.find_one({"_id": user.id})['garantido']
        if banner == 'perlim1':
            resultados = ''
            url_imagem10 = ''
            if pity5 == 79:
                categoria = "5 estrelas"
                if garantido == 'sim':
                    result = '[⭐] Jiyan'
                    url_imagem = itens[categoria]["url_imagem"]
                    membstat.update_one(
                {
                    '_id': user.id
                },
                {
                    '$set':{
                        'pity5perlim': 0,
                        'garantido': 'nao'
                    },
                    '$inc':{
                        'pity4perlim': 1
                    }
                })
                else:
                    result = "[⭐] Jiyan" if random.uniform(0, 100) < 50 else random.choice(itens[categoria]["personagens"])
                    url_imagem = itens[categoria]["url_imagem"]
                    if result == '[⭐] Jiyan':
                        membstat.update_one(
                    {
                        '_id': user.id
                    },
                    {
                        '$set':{
                            'pity5perlim': 0,
                            'garantido': 'nao'
                        },
                        '$inc':{
                            'pity4perlim': 1
                        }
                    })
                    else:
                        membstat.update_one(
                    {
                        '_id': user.id
                    },
                    {
                        '$set':{
                            'pity5perlim': 0,
                            'garantido': 'sim'
                        },
                        '$inc':{
                            'pity4perlim': 1
                        }
                    })
            elif pity4 == 9:
                categoria = "4 estrelas"
                result = random.choice(itens[categoria]["personagens"])
                url_imagem = itens[categoria]["url_imagem"]
                membstat.update_one(
            {
                '_id': user.id
            },
            {
                '$set':{
                    'pity4': 0
                },
                '$inc':{
                    'pity5': 1
                }
            })
            elif chance < 0.8:
                categoria = "5 estrelas"
                categoria = "5 estrelas"
                if garantido == 'sim':
                    result = '[⭐] Jiyan'
                    url_imagem = itens[categoria]["url_imagem"]
                    membstat.update_one(
                {
                    '_id': user.id
                },
                {
                    '$set':{
                        'pity5perlim': 0,
                        'garantido': 'nao'
                    },
                    '$inc':{
                        'pity4perlim': 1
                    }
                })
                else:
                    result = "[⭐] Jiyan" if random.uniform(0, 100) < 50 else random.choice(itens[categoria]["personagens"])
                    url_imagem = itens[categoria]["url_imagem"]
                    if result == '[⭐] Jiyan':
                        membstat.update_one(
                    {
                        '_id': user.id
                    },
                    {
                        '$set':{
                            'pity5perlim': 0,
                            'garantido': 'nao'
                        },
                        '$inc':{
                            'pity4perlim': 1
                        }
                    })
                    else:
                        membstat.update_one(
                    {
                        '_id': user.id
                    },
                    {
                        '$set':{
                            'pity5perlim': 0,
                            'garantido': 'sim'
                        },
                        '$inc':{
                            'pity4perlim': 1
                        }
                    })
            elif chance < 6.0:
                categoria = "4 estrelas"
                result = random.choice(itens[categoria]["personagens"])
                url_imagem = itens[categoria]["url_imagem"]
                membstat.update_one(
            {
                '_id': user.id
            },
            {
                '$set':{
                    'pity4perlim': 0
                },
                '$inc':{
                    'pity5perlim': 1
                }
            })
            else:
                categoria = "3 estrelas"
                result = random.choice(itens[categoria]["personagens"])
                url_imagem = itens[categoria]["url_imagem"]
                membstat.update_one(
            {
                '_id': user.id
            },
            {
                '$inc':{
                    'pity4perlim': 1,
                    'pity5perlim': 1
                }
            }
            )
                
        elif banner == 'perlim10':
            resultados = {}
            maior = {}
            maior[f"maior1"] = 0
            for i in range (1,11):
                chance = random.uniform(0, 100)
                apity4 = membstat.find_one({"_id": user.id})['pity4perlim']
                apity5 = membstat.find_one({"_id": user.id})['pity5perlim']
                garantido = membstat.find_one({"_id": user.id})['garantido']
                if apity5 == 79:
                    categoria = "5 estrelas"
                    if garantido == 'sim':
                        result = '[⭐] Jiyan'
                        url_imagem = itens[categoria]["url_imagem"]
                        membstat.update_one(
                    {
                        '_id': user.id
                    },
                    {
                        '$set':{
                            'pity5perlim': 0,
                            'garantido': 'nao'
                        },
                        '$inc':{
                            'pity4perlim': 1
                        }
                    })
                    else:
                        result = "[⭐] Jiyan" if random.uniform(0, 100) < 50 else random.choice(itens[categoria]["personagens"])
                        url_imagem = itens[categoria]["url_imagem"]
                        if result == '[⭐] Jiyan':
                            membstat.update_one(
                        {
                            '_id': user.id
                        },
                        {
                            '$set':{
                                'pity5perlim': 0,
                                'garantido': 'nao'
                            },
                            '$inc':{
                                'pity4perlim': 1
                            }
                        })
                        else:
                            membstat.update_one(
                        {
                            '_id': user.id
                        },
                        {
                            '$set':{
                                'pity5perlim': 0,
                                'garantido': 'sim'
                            },
                            '$inc':{
                                'pity4perlim': 1
                            }
                        })
                elif apity4 == 9:
                    categoria = "4 estrelas"
                    result = random.choice(itens[categoria]["personagens"])
                    url_imagem = itens[categoria]["url_imagem"]
                    membstat.update_one(
                {
                    '_id': user.id
                },
                {
                    '$set':{
                        'pity4perlim': 0
                    },
                    '$inc':{
                        'pity5perlim': 1
                    }
                })
                elif chance < 0.8:
                    categoria = "5 estrelas"
                    categoria = "5 estrelas"
                    if garantido == 'sim':
                        result = '[⭐] Jiyan'
                        url_imagem = itens[categoria]["url_imagem"]
                        membstat.update_one(
                    {
                        '_id': user.id
                    },
                    {
                        '$set':{
                            'pity5perlim': 0,
                            'garantido': 'nao'
                        },
                        '$inc':{
                            'pity4perlim': 1
                        }
                    })
                    else:
                        result = "[⭐] Jiyan" if random.uniform(0, 100) < 50 else random.choice(itens[categoria]["personagens"])
                        url_imagem = itens[categoria]["url_imagem"]
                        if result == '[⭐] Jiyan':
                            membstat.update_one(
                        {
                            '_id': user.id
                        },
                        {
                            '$set':{
                                'pity5perlim': 0,
                                'garantido': 'nao'
                            },
                            '$inc':{
                                'pity4perlim': 1
                            }
                        })
                        else:
                            membstat.update_one(
                        {
                            '_id': user.id
                        },
                        {
                            '$set':{
                                'pity5perlim': 0,
                                'garantido': 'sim'
                            },
                            '$inc':{
                                'pity4perlim': 1
                            }
                        })
                elif chance < 6.0:
                    categoria = "4 estrelas"
                    result = random.choice(itens[categoria]["personagens"])
                    url_imagem = itens[categoria]["url_imagem"]
                    membstat.update_one(
                {
                    '_id': user.id
                },
                {
                    '$set':{
                        'pity4perlim': 0
                    },
                    '$inc':{
                        'pity5perlim': 1
                    }
                })
                else:
                    categoria = "3 estrelas"
                    result = random.choice(itens[categoria]["personagens"])
                    url_imagem = itens[categoria]["url_imagem"]
                    membstat.update_one(
                {
                    '_id': user.id
                },
                {
                    '$inc':{
                        'pity4perlim': 1,
                        'pity5perlim': 1
                    }
                }
                )
                resultados[f"tiro{i}"] = result
                
                if categoria == "5 estrelas":
                    maior[f"maior1"] = 1
                elif categoria == '4 estrelas':
                    maior[f'maior2'] = 2
            if maior['maior1'] == 1:
                url_imagem10 = 'https://media.discordapp.net/attachments/1211401681690951820/1246357519186530355/IMG_3315.gif?ex=665cc124&is=665b6fa4&hm=abe6d4b055e32a22d92a4c65d590d6be19412ce5622f81406d34a140c82c13bd&='
            elif maior['maior2'] == 2 and maior['maior1'] == 0:
                url_imagem10 = 'https://media.discordapp.net/attachments/1211401681690951820/1246357453789200384/IMG_3313.gif?ex=665cc115&is=665b6f95&hm=487d1c62bba0c8b10e177900ef156ce7de0eeb423b06a908065feb01682ad798&='
                    
            result = ''
            categoria = ''

        return result, resultados, categoria, url_imagem, url_imagem10
        
        
    result, resultados, categoria, url_imagem, url_imagem10 = Pity()
    return result, resultados, categoria, url_imagem, url_imagem10

def AddInv(user: discord.Member, result, banner):
    membstat.update_one(
        {'_id': user.id},
        {'$inc': {result: 1}},
        upsert=True
    )

def AddXP(user: discord.Member, xp):
    checkxp = membstat.find_one({"_id": user.id})['unionxp']
    checkunion = membstat.find_one({"_id": user.id})['unionlvl']
    unionreq = membstat.find_one({"_id": user.id})['unionreq']
    if checkxp + xp >= unionreq:
        newxp = checkxp + xp - unionreq
        newunionreq = unionreq + 150
        membstat.update_one({'_id': user.id},{'$inc':{'unionlvl': 1}, '$set':{'unionxp': newxp, 'unionreq': newunionreq}})
        checkunion1 = membstat.find_one({"_id": user.id})['unionlvl']
        msg = f'__***NOVO UNION LEVEL: {checkunion} > {checkunion1}***__'
    else:
        membstat.update_one({'_id': user.id},{'$inc':{'unionxp': xp}})
        msg = None
    return msg
