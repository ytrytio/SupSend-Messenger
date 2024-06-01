import eel
import eel.browsers

eel.init('web')
eel.browsers.set_path('electron', 'node_modules/electron/dist/electron')
eel.start('main.html', mode='electron')
