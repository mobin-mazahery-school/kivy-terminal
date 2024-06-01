from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from remote_pdb import set_trace

class SocketListenerApp(App):
    def build(self):
        # Create an empty screen layout
        layout = BoxLayout(orientation='vertical')

        # Thread to handle socket communication in the background
        set_trace(host="0.0.0.0",port=8022)
        
        return layout

if __name__ == '__main__':
    SocketListenerApp().run()
