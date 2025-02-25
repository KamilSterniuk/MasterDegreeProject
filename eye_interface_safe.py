from eyex.api import EyeXInterface

class EyeXInterfaceSafe(EyeXInterface):
    def __init__(self, *args, **kwargs):
        try:
            super().__init__(*args, **kwargs)
        except Exception as e:
            print("Error during EyeX initialization:", e)
            self.context = None  # Zapewniamy, że context jest zdefiniowany

    def __del__(self):
        # Wyłącz połączenie tylko, jeśli context istnieje
        if hasattr(self, "context") and self.context is not None:
            try:
                self.eyex_dll.txDisableConnection(self.context)
            except Exception as e:
                print("Error during EyeX shutdown:", e)
