import psutil
import pygetwindow as gw

list_game_name = [{'process_name':'StarRail.exe', 'window_title': 'Honkai: Star Rail'},
                  {'process_name':'GenshinImpact.exe','window_title':'Genshin Impact'},
                  {'process_name':'ZenlessZoneZero.exe','window_title':'Zenless Zone Zero'},
                  {'process_name':'VALORANT-Win64-Shipping.exe','window_title':'VALORANT'},
                  {'process_name':'LeagueClient.exe','window_title':'League of Legends'},
                  {'process_name':'LeagueClientUx.exe','window_title':'League of Legends'},
                  {'process_name':'BH3.exe','window_title':'Honkai Impact 3rd'},
                  ]


def get_running_processes() -> list:
    process_list = []
    for proc in psutil.process_iter(['pid', 'name']):
        process_list.append(proc.info)

    return process_list

def write_processes_to_file(process_list, file_name):
    with open(file_name, 'w') as file:
        file.write(f"{'PID':<10}{'Name':<30}{'Status':<15}\n")
        file.write("="*55 + "\n")
        for process in process_list:
            pid = str(process['pid'])
            name = process['name']
            file.write(f"{pid:<10}{name:<30}\n")

def detect_game_active(process_list, game_names) -> list:
    games_active = []
    for process in process_list:
        for game in game_names:
            if game['process_name'].lower() == process['name'].lower():
                games_active.append(game)

    return games_active
            
def get_last_window_active(last_game_title_display: str) -> str:
    game_actives = detect_game_active(get_running_processes(),list_game_name)
    if len(game_actives) == 0:
        return ''
    elif len(game_actives) == 1:
        return game_actives[0]['window_title']
    else:
        last_window_active_title = str(gw.getActiveWindow())

        if last_window_active_title in [game ['window_title'] for game in game_actives]:
            last_game_title_display = last_window_active_title
        return last_game_title_display
                
