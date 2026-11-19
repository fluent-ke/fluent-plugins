# Setup: Android from Windows, macOS or Linux (mobile-mcp)

[mobile-mcp](https://github.com/mobile-next/mobile-mcp) drives an Android phone over adb, the Android debug bridge, from any of the three systems. It needs Node.js 20 or later.

## 1. Install adb

| System | Command |
|---|---|
| Windows | `winget install Google.PlatformTools` |
| macOS | `brew install --cask android-platform-tools` |
| Linux (Debian, Ubuntu) | `sudo apt install adb` |

Or download Platform Tools from [developer.android.com/tools/releases/platform-tools](https://developer.android.com/tools/releases/platform-tools). Open a new terminal afterwards and check that `adb version` answers. Wi-Fi pairing below needs version 30 or later; Linux distribution packages can be older, in which case use Google's download.

## 2. Allow the computer on the phone

The person does these on the phone:

1. Settings → About phone → tap **Build number** seven times to unlock Developer options. On some phones it sits under Software information.
2. Settings → Developer options → turn on **USB debugging**.
3. Connect the USB cable and tap **Allow** on the "Allow USB debugging?" prompt.

Without a cable, on Android 11 or later: Developer options → **Wireless debugging** → Pair device with pairing code, then on the computer `adb pair <ip>:<pair-port>`, enter the code, and `adb connect <ip>:<port>` with the port the Wireless debugging screen shows. Phone and computer must be on the same Wi-Fi.

`adb devices` lists the phone as `device` when it is ready. `unauthorized` means the prompt on the phone is still waiting.

## 3. Register the server

- Claude Code: `claude mcp add mobile-mcp -- npx -y @mobilenext/mobile-mcp@latest`
- Codex: `codex mcp add mobile-mcp -- npx -y @mobilenext/mobile-mcp@latest`
- Other agents: command `npx`, args `["-y", "@mobilenext/mobile-mcp@latest"]`.
- On native Windows, if the server fails to start, register it through the shell: `claude mcp add mobile-mcp -- cmd /c npx -y @mobilenext/mobile-mcp@latest`.

## Using it

- `mobile_list_available_devices` first, then `mobile_list_elements_on_screen` to read the screen. Android exposes its interface as elements, so this is usually more exact than reading text off pixels.
- `mobile_click_on_screen_at_coordinates`, `mobile_swipe_on_screen`, `mobile_type_keys`, and `mobile_press_button` for Back and Home. `mobile_launch_app` takes the package name; `mobile_list_apps` finds it.
- mobile-mcp has no list of blocked apps, so the consent rules in SKILL.md are the only guard. Tell the person before the first session that the agent can reach every app on the phone.
- `mobile_install_app`, `mobile_uninstall_app`, `mobile_clear_app_data` and `mobile_open_url` change the phone. Use them only when the person asked for that exact action.
- This route has been used less in the field than the iPhone route. Read the screen after every action, and save what you learn about each app in the project's notes.
