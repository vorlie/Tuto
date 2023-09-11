import config
import json

# LOAD JSON FILES, LANGUAGES AND CONFIGS
with open(config.english, 'r', encoding='utf-8') as file:
        en_language = json.load(file)
        
with open(config.polish, 'r', encoding='utf-8') as file:
        pl_language = json.load(file)

with open(config.languages_servers, 'r') as file:
        server_languages = json.load(file)

with open(config.languages_users, 'r') as file:
        user_languages = json.load(file)

# SERVER SETTINGS
def get_server_language(server_id):
    return server_languages['server_list'].get(str(server_id), 'en')

def set_server_language(server_id, language):
    if language.lower() in ['en', 'pl']:
        server_languages['server_list'][str(server_id)] = language.lower()
        with open(config.languages_servers, 'w') as file:
            json.dump(server_languages, file)
        return True
    return False

# USER SETTINGS
def get_user_language(user_id):
    return user_languages['user_list'].get(str(user_id), 'en')

def set_user_language(user_id, language):
    if language.lower() in ['en', 'pl']:
        user_languages['user_list'][str(user_id)] = language.lower()
        with open(config.languages_users, 'w') as file:
            json.dump(user_languages, file)
        return True
    return False

def clear_user_language(user_id):
    if 'user_list' in user_languages and str(user_id) in user_languages['user_list']:
        del user_languages['user_list'][str(user_id)]
        with open(config.languages_users, 'w') as file:
            json.dump(user_languages, file)

# Function to retrieve translations
def translate(key, lang='en'):
        if lang == 'en':
                return en_language.get(key, key)  
        elif lang == 'pl':
                return pl_language.get(key, key)
        else:
                return key  # Return the key itself if translation not found