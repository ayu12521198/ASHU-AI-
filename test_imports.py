try:
    from Ashu_prompts import behavior_prompts, Reply_prompts
    print("Ashu_prompts imported successfully")
except Exception as e:
    print(f"Error importing Ashu_prompts: {e}")

try:
    from Ashu_google_search import google_search, get_current_datetime
    print("Ashu_google_search imported successfully")
except Exception as e:
    print(f"Error importing Ashu_google_search: {e}")

try:
    from Ashu_get_whether import get_weather
    print("Ashu_get_whether imported successfully")
except Exception as e:
    print(f"Error importing Ashu_get_whether: {e}")

try:
    from Ashu_window_CTRL import open, close, folder_file
    print("Ashu_window_CTRL imported successfully")
except Exception as e:
    print(f"Error importing Ashu_window_CTRL: {e}")

try:
    from Ashu_file_opner import Play_file
    print("Ashu_file_opner imported successfully")
except Exception as e:
    print(f"Error importing Ashu_file_opner: {e}")

try:
    from keyboard_mouse_CTRL import move_cursor_tool, mouse_click_tool, scroll_cursor_tool, type_text_tool, press_key_tool, swipe_gesture_tool, press_hotkey_tool, control_volume_tool
    print("keyboard_mouse_CTRL imported successfully")
except Exception as e:
    print(f"Error importing keyboard_mouse_CTRL: {e}")

print("All imports checked.")