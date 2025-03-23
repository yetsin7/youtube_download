import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from threading import Thread
import webbrowser

class ModernYouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("Descargador de YouTube Pro")
        
        # Aumentar el tamaño de la ventana y hacerla más flexible
        self.root.geometry("1000x650")  # Ancho más grande, altura ajustada
        self.root.resizable(True, True)
        self.root.minsize(950, 600)  # Tamaño mínimo más generoso
        
        # Configurar estilo
        self.configure_styles()
        
        # Variable para almacenar la ruta de descarga
        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        
        # Crear y configurar el marco principal con más padding
        self.main_frame = ttk.Frame(root, padding="15")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Panel superior: Logo y título
        top_frame = ttk.Frame(self.main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Logo y título en línea
        logo_canvas = tk.Canvas(top_frame, width=50, height=50, bg="#FF0000", highlightthickness=0)
        logo_canvas.create_polygon(15, 10, 15, 40, 40, 25, fill="white")
        logo_canvas.pack(side=tk.LEFT, padx=(0, 15))
        
        title_label = ttk.Label(top_frame, text="YouTube Downloader Pro", font=("Helvetica", 18, "bold"))
        title_label.pack(side=tk.LEFT, expand=True)
        
        version_label = ttk.Label(top_frame, text="v1.2.1", font=("Helvetica", 10))
        version_label.pack(side=tk.RIGHT, padx=5)
        
        # Divisor principal con más espacio
        main_paned = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Panel izquierdo: URL y ruta de descarga
        left_frame = ttk.Frame(main_paned, padding=10)
        main_paned.add(left_frame, weight=1)
        
        # Marco para la URL con más espacio
        url_frame = ttk.LabelFrame(left_frame, text="URL del video", padding=10)
        url_frame.pack(fill=tk.X, pady=(0, 10))
        
        url_entry_frame = ttk.Frame(url_frame)
        url_entry_frame.pack(fill=tk.X)
        
        self.url_entry = ttk.Entry(url_entry_frame, font=("Helvetica", 11))
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Botones de URL más espaciados
        url_button_frame = ttk.Frame(url_entry_frame)
        url_button_frame.pack(side=tk.RIGHT)
        
        paste_button = ttk.Button(url_button_frame, text="Pegar", width=8, command=self.paste_url)
        paste_button.pack(side=tk.LEFT, padx=5)
        
        clear_button = ttk.Button(url_button_frame, text="Limpiar", width=8, command=self.clear_url)
        clear_button.pack(side=tk.LEFT)
        
        # Marco para la ruta de descarga
        path_frame = ttk.LabelFrame(left_frame, text="Ubicación de descarga", padding=10)
        path_frame.pack(fill=tk.X, pady=(0, 10))
        
        path_entry_frame = ttk.Frame(path_frame)
        path_entry_frame.pack(fill=tk.X)
        
        self.path_entry = ttk.Entry(path_entry_frame, font=("Helvetica", 11))
        self.path_entry.insert(0, self.download_path)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_button = ttk.Button(path_entry_frame, text="Examinar", width=10, command=self.browse_directory)
        browse_button.pack(side=tk.RIGHT)
        
        # Área de estado y progreso con más espacio
        status_frame = ttk.LabelFrame(left_frame, text="Estado", padding=10)
        status_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.status_var = tk.StringVar(value="Listo para descargar")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, anchor=tk.W, font=("Helvetica", 10))
        status_label.pack(fill=tk.X)
        
        progress_frame = ttk.Frame(status_frame)
        progress_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.progress = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(0, 5))
        
        # Etiqueta para mostrar el progreso
        self.progress_text = tk.StringVar(value="0%")
        progress_label = ttk.Label(progress_frame, textvariable=self.progress_text, font=("Helvetica", 9))
        progress_label.pack(anchor=tk.E)
        
        # Panel derecho: Opciones y botones
        right_frame = ttk.Frame(main_paned, padding=10)
        main_paned.add(right_frame, weight=1)
        
        # Marco para opciones de formato y calidad (horizontal)
        options_frame = ttk.Frame(right_frame)
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Panel izquierdo: opciones de calidad
        quality_frame = ttk.LabelFrame(options_frame, text="Calidad", padding=10)
        quality_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.quality_var = tk.StringVar(value="bestvideo[height<=1080]+bestaudio/best[height<=1080]")
        
        quality_options = [
            ("4K (2160p)", "bestvideo[height<=2160]+bestaudio/best[height<=2160]"),
            ("Full HD (1080p)", "bestvideo[height<=1080]+bestaudio/best[height<=1080]"),
            ("HD (720p)", "bestvideo[height<=720]+bestaudio/best[height<=720]"),
            ("SD (480p)", "bestvideo[height<=480]+bestaudio/best[height<=480]"),
            ("Baja (360p)", "bestvideo[height<=360]+bestaudio/best[height<=360]"),
            ("Mejor calidad", "best")
        ]
        
        for text, value in quality_options:
            radio = ttk.Radiobutton(quality_frame, text=text, value=value, variable=self.quality_var)
            radio.pack(anchor=tk.W, pady=3)
        
        # Panel derecho: opciones adicionales
        format_frame = ttk.LabelFrame(options_frame, text="Formato", padding=10)
        format_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.format_var = tk.StringVar(value="video")
        
        # Opciones de formato
        video_radio = ttk.Radiobutton(format_frame, text="Video", value="video", 
                                     variable=self.format_var, command=self.update_format_options)
        video_radio.pack(anchor=tk.W, pady=3)
        
        audio_radio = ttk.Radiobutton(format_frame, text="Audio (MP3)", value="audio", 
                                     variable=self.format_var, command=self.update_format_options)
        audio_radio.pack(anchor=tk.W, pady=3)
        
        # Marco para opciones adicionales
        options_extra_frame = ttk.LabelFrame(right_frame, text="Opciones adicionales", padding=10)
        options_extra_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Opciones adicionales en una fila más espaciada
        options_row = ttk.Frame(options_extra_frame)
        options_row.pack(fill=tk.X)
        
        # Opciones adicionales con más espacio
        self.keep_original_files = tk.BooleanVar(value=False)
        keep_files_check = ttk.Checkbutton(options_row, text="Mantener archivos originales", 
                                          variable=self.keep_original_files)
        keep_files_check.pack(side=tk.LEFT, padx=(0, 15))
        
        self.add_metadata = tk.BooleanVar(value=True)
        metadata_check = ttk.Checkbutton(options_row, text="Incluir metadatos", 
                                        variable=self.add_metadata)
        metadata_check.pack(side=tk.LEFT, padx=(0, 15))
        
        self.create_playlist = tk.BooleanVar(value=False)
        playlist_check = ttk.Checkbutton(options_row, text="Procesar toda la playlist", 
                                       variable=self.create_playlist)
        playlist_check.pack(side=tk.LEFT)
        
        # Botones de acción con más espacio
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Botón de descargar grande y centrado con colores fuertes
        self.download_button = tk.Button(button_frame, text="DESCARGAR", 
                                        command=self.start_download, 
                                        font=("Helvetica", 14, "bold"),
                                        bg="#4CAF50", fg="white",
                                        activebackground="#45a049",
                                        activeforeground="white",
                                        relief=tk.RAISED,
                                        borderwidth=3,
                                        padx=20, pady=10)
        self.download_button.pack(fill=tk.X, pady=10)
        
        # Fila de botones secundarios con más espacio
        button_row = ttk.Frame(button_frame)
        button_row.pack(fill=tk.X, pady=(0, 10))
        
        self.cancel_button = ttk.Button(button_row, text="Cancelar", 
                                      command=self.cancel_download, state=tk.DISABLED)
        self.cancel_button.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        help_button = ttk.Button(button_row, text="Ayuda", command=self.show_help)
        help_button.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # Enlace a GitHub en el pie
        footer_frame = ttk.Frame(self.main_frame)
        footer_frame.pack(fill=tk.X, pady=(10, 0))
        
        link_label = ttk.Label(footer_frame, text="github.com/tu-usuario/youtube-downloader", 
                              font=("Helvetica", 9), foreground="blue", cursor="hand2")
        link_label.pack(side=tk.RIGHT)
        link_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/"))
        
        # Variable para el proceso de descarga
        self.download_process = None
        self.downloading = False
        
        # Verificar si yt-dlp está instalado
        self.check_yt_dlp()

    # Resto del código permanece igual que en la versión anterior
    def configure_styles(self):
        """Configura los estilos personalizados para la interfaz"""
        style = ttk.Style()
        
        # Configurar tema
        if "clam" in style.theme_names():
            style.theme_use("clam")
        
        # Estilos personalizados
        style.configure("TLabel", font=("Helvetica", 10))
        style.configure("TButton", font=("Helvetica", 10))
        style.configure("TCheckbutton", font=("Helvetica", 10))
        style.configure("TRadiobutton", font=("Helvetica", 10))
        
        # Estilo para la LabelFrame con menos espacio
        style.configure("TLabelframe", font=("Helvetica", 10))
        style.configure("TLabelframe.Label", font=("Helvetica", 10, "bold"))

    # (Resto de los métodos permanecen igual que en la versión anterior)
    def update_format_options(self):
        """Actualiza las opciones disponibles según el formato seleccionado"""
        format_option = self.format_var.get()
        if format_option == "audio":
            self.quality_var.set("bestaudio")
        else:
            self.quality_var.set("bestvideo[height<=1080]+bestaudio/best[height<=1080]")

    def paste_url(self):
        """Pega el contenido del portapapeles en el campo de URL"""
        try:
            clipboard_content = self.root.clipboard_get()
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, clipboard_content)
        except tk.TclError:
            pass

    def clear_url(self):
        """Limpia el campo de URL"""
        self.url_entry.delete(0, tk.END)

    def browse_directory(self):
        """Abre un diálogo para seleccionar el directorio de descarga"""
        directory = filedialog.askdirectory(initialdir=self.download_path)
        if directory:
            self.download_path = directory
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, self.download_path)

    def check_yt_dlp(self):
        """Verifica si yt-dlp está instalado en el sistema y obtiene su ubicación exacta"""
        try:
            # Intentar obtener la ruta completa de yt-dlp
            if os.name == 'nt':  # Windows
                # En Windows, verificar si está en PATH usando where
                result = subprocess.run(
                    ["where", "yt-dlp"], 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, 
                    text=True, 
                    check=False
                )
                if result.returncode == 0:
                    yt_dlp_path = result.stdout.strip().split('\n')[0]
                    self.status_var.set(f"yt-dlp detectado: Listo para descargar")
                    return yt_dlp_path
                else:
                    # Intentar verificar si existe en ubicaciones comunes
                    potential_paths = [
                        os.path.join(sys.exec_prefix, 'Scripts', 'yt-dlp.exe'),
                        os.path.join(os.environ.get('APPDATA', ''), 'Python', 'Scripts', 'yt-dlp.exe'),
                        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'Python', 'Scripts', 'yt-dlp.exe')
                    ]
                    
                    for path in potential_paths:
                        if os.path.exists(path):
                            self.status_var.set("yt-dlp detectado: Listo para descargar")
                            return path
            else:
                # En Unix/Linux/Mac
                result = subprocess.run(
                    ["which", "yt-dlp"], 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, 
                    text=True, 
                    check=False
                )
                
                if result.returncode == 0:
                    yt_dlp_path = result.stdout.strip()
                    self.status_var.set("yt-dlp detectado: Listo para descargar")
                    return yt_dlp_path
            
            # Si llegamos aquí, no se encontró yt-dlp
            self.status_var.set("ERROR: yt-dlp no encontrado")
            messagebox.showerror("Error", "yt-dlp no está instalado.\n\nPuede instalarlo con:\npip install yt-dlp\n\nLuego, reinicie la aplicación.")
            return None
            
        except Exception as e:
            self.status_var.set(f"Error al verificar yt-dlp: {str(e)}")
            messagebox.showerror("Error", f"Error al verificar yt-dlp: {str(e)}")
            return None

    def update_status(self, message):
        """Actualiza el mensaje de estado"""
        self.status_var.set(message)
        self.root.update_idletasks()
        
        # Extraer el porcentaje de progreso si está presente en el mensaje
        if "%" in message and "[download]" in message:
            try:
                # Intentar extraer el porcentaje
                percent_str = message.split("%")[0].split(" ")[-1]
                if percent_str.replace('.', '', 1).isdigit():
                    percent = float(percent_str)
                    self.progress_text.set(f"{percent:.1f}%")
                    
                    # Si estamos en modo indeterminado, cambiar a determinado
                    if self.progress["mode"] == "indeterminate":
                        self.progress.stop()
                        self.progress["mode"] = "determinate"
                    
                    # Actualizar el valor de la barra de progreso
                    self.progress["value"] = percent
            except (ValueError, IndexError):
                pass

    def build_command(self):
        """Construye el comando de yt-dlp basado en las opciones seleccionadas"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Por favor, introduzca una URL válida.")
            return None
        
        # Obtener la ruta de yt-dlp
        yt_dlp_path = self.check_yt_dlp()
        if not yt_dlp_path:
            return None
            
        # Comando base - usar la ruta completa en lugar de confiar en PATH
        if os.name == 'nt' and os.path.exists(yt_dlp_path):  # Windows
            command = [yt_dlp_path]
        else:
            command = ["yt-dlp"]
        
        # Opciones de formato
        if self.format_var.get() == "audio":
            command.extend(["-x", "--audio-format", "mp3", "--audio-quality", "0"])
            if self.add_metadata.get():
                command.extend(["--embed-thumbnail", "--add-metadata"])
        else:
            format_option = self.quality_var.get()
            command.extend(["-f", format_option])
            if self.add_metadata.get():
                command.append("--add-metadata")
        
        # Opciones adicionales
        if self.keep_original_files.get():
            command.append("-k")
        
        # Opción de playlist
        if not self.create_playlist.get() and "playlist" in url:
            command.append("--no-playlist")
        
        # Directorio de salida
        output_path = self.path_entry.get().strip() or self.download_path
        # Asegurarse de que el directorio exista
        if not os.path.exists(output_path):
            try:
                os.makedirs(output_path)
                self.update_status(f"Creado directorio: {output_path}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo crear el directorio: {str(e)}")
                return None
        
        # Formato de salida más organizado
        if self.format_var.get() == "audio":
            output_template = "%(title)s.%(ext)s"
        else:
            output_template = "%(title)s.%(ext)s"
        
        command.extend(["--no-mtime", "-o", os.path.join(output_path, output_template)])
        
        # Agregar progreso para poder actualizarlo
        command.append("--newline")
        
        # URL del vídeo
        command.append(url)
        
        return command

    def start_download(self):
        """Inicia el proceso de descarga en un hilo separado"""
        command = self.build_command()
        if not command:
            return
        
        self.downloading = True
        self.download_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)
        
        # Iniciar progreso indeterminado
        self.progress["mode"] = "indeterminate"
        self.progress.start(10)
        self.progress_text.set("Preparando...")
        
        # Iniciar el proceso en un hilo separado
        download_thread = Thread(target=self.download_video, args=(command,))
        download_thread.daemon = True
        download_thread.start()

    def download_video(self, command):
        """Ejecuta el comando de descarga y actualiza el estado"""
        self.update_status("Iniciando descarga...")
        
        try:
            # Mostrar el comando que se está ejecutando (versión simplificada)
            self.update_status("Conectando con YouTube...")
            
            # Obtener el directorio para verificar posteriormente
            output_dir = self.path_entry.get().strip() or self.download_path
            files_before = set(os.listdir(output_dir)) if os.path.exists(output_dir) else set()
            
            # Iniciar el proceso
            if os.name == 'nt':  # Windows
                # Creamos el proceso con argumentos como lista sin usar shell
                self.download_process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                # En otros sistemas, la lista funciona mejor
                self.download_process = subprocess.Popen(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
            
            # Leer y actualizar el estado con la última línea
            for line in self.download_process.stdout:
                if not self.downloading:
                    break
                self.update_status(line.strip())
            
            # Esperar a que el proceso termine
            self.download_process.wait()
            
            if self.downloading:
                if self.download_process.returncode == 0:
                    # Verificar qué archivos nuevos se crearon
                    files_after = set(os.listdir(output_dir)) if os.path.exists(output_dir) else set()
                    new_files = files_after - files_before
                    
                    # Configurar la barra de progreso a 100%
                    self.progress["mode"] = "determinate"
                    self.progress["value"] = 100
                    self.progress_text.set("100%")
                    
                    success_message = "¡Descarga completada con éxito!"
                    self.update_status(success_message)
                    
                    # Mensaje detallado con los archivos
                    detail_message = ""
                    if new_files:
                        files_list = list(new_files)
                        files_str = "\n".join(files_list[:5])
                        if len(files_list) > 5:
                            files_str += f"\n... y {len(files_list)-5} archivos más"
                        
                        detail_message = f"Se han descargado {len(files_list)} archivo(s):\n\n{files_str}\n\nUbicación: {output_dir}"
                    
                    messagebox.showinfo("Descarga Exitosa", f"{success_message}\n\n{detail_message}")
                else:
                    error_msg = f"Error en la descarga (código: {self.download_process.returncode})."
                    self.update_status(error_msg)
                    messagebox.showerror("Error", error_msg)
        
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.update_status(error_msg)
            messagebox.showerror("Error", error_msg)
        
        finally:
            self.downloading = False
            self.download_process = None
            self.download_button.config(state=tk.NORMAL)
            self.cancel_button.config(state=tk.DISABLED)
            
            # Resetear progreso
            self.progress.stop()
            self.progress["value"] = 0
            self.progress_text.set("0%")

    def cancel_download(self):
        """Cancela el proceso de descarga en curso"""
        if self.download_process and self.downloading:
            self.downloading = False
            self.download_process.terminate()
            self.update_status("Descarga cancelada por el usuario.")
            self.download_button.config(state=tk.NORMAL)
            self.cancel_button.config(state=tk.DISABLED)
            self.progress.stop()
            self.progress["value"] = 0
            self.progress_text.set("0%")

    def show_help(self):
        """Muestra un diálogo de ayuda"""
        help_text = """
        📥 YouTube Downloader Pro - Ayuda 📥
        
        Esta aplicación permite descargar videos y audio de YouTube de manera fácil y eficiente.
        
        ► Cómo usar:
        1. Pegue la URL del video o playlist de YouTube en el campo superior
        2. Seleccione la ubicación donde desea guardar los archivos
        3. Elija la calidad y formato deseados
        4. Haga clic en el botón DESCARGAR
        
        ► Opciones de formato:
        • Video + Audio: Descarga el video con su audio original
        • Solo Audio (MP3): Extrae únicamente el audio en formato MP3
        
        ► Opciones adicionales:
        • Mantener archivos originales: Guarda los archivos sin procesar
        • Incluir metadatos: Agrega información como título, artista, etc.
        • Procesar toda la playlist: Descarga todos los videos de una playlist
        
        ► Requisitos del sistema:
        • Es necesario tener instalado yt-dlp (pip install yt-dlp)
        • FFmpeg es recomendado para conversiones de formato avanzadas
        
        Para más información y soporte, visite: 
        github.com/tu-usuario/youtube-downloader
        """
        messagebox.showinfo("Ayuda de YouTube Downloader Pro", help_text)

def main():
    # Configurar la aplicación
    root = tk.Tk()
    root.title("YouTube Downloader Pro")
    
    # Configurar el icono si está disponible
    try:
        root.iconbitmap("youtube.ico")
    except:
        pass  # Si no hay icono, continuar sin él
    
    # Configurar tema oscuro si está disponible
    try:
        # Intentar configurar tema oscuro
        root.tk.call("source", "azure-dark.tcl")
        root.tk.call("set_theme", "dark")
    except:
        pass  # Si no está disponible, usar el tema predeterminado
    
    # Centrar la ventana horizontal y verticalmente
    window_width = 1000
    window_height = 650
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Crear la aplicación
    app = ModernYouTubeDownloader(root)
    
    # Si hay argumentos en la línea de comandos, usarlos como URL
    if len(sys.argv) > 1:
        app.url_entry.delete(0, tk.END)
        app.url_entry.insert(0, sys.argv[1])
    
    # Iniciar el bucle principal
    root.mainloop()

if __name__ == "__main__":
    main()