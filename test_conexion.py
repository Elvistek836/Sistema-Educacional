from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        ruta_brave = "/mnt/c/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
        # Esta carpeta guardará temporalmente tu sesión en Ubuntu
        user_data = "/tmp/playwright_brave_profile"
        
        print("Iniciando Brave con contexto persistente...")
        
        # Cambiamos launch por launch_persistent_context
        context = p.chromium.launch_persistent_context(
            user_data_dir=user_data,
            executable_path=ruta_brave,
            headless=False,
            args=["--no-sandbox"]
        )
        
        # Con este comando no necesitas hacer context.new_page(), 
        # porque ya se abre una por defecto.
        page = context.pages[0]
        
        try:
            page.goto("http://127.0.0.1:8000")
            print(f"Título: {page.title()}")
            page.wait_for_timeout(5000)
        finally:
            context.close()

if __name__ == "__main__":
    run()