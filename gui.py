import tkinter as tk
from tkinter import ttk, StringVar, DoubleVar, IntVar, BooleanVar
from utils import settings
from config import SCREEN_WIDTH, SCREEN_HEIGHT, TARGET_FPS

# GUI переменные для статусов
status_vars = {}
gui_vars = {}


def update_gui_status():
    """Обновление статусов в GUI"""
    if status_vars:
        status_vars["auto_aim"].set("🎯 ON" if settings.auto_aim_mode else "🎯 OFF")
        status_vars["auto_shoot"].set("🔫 ON" if settings.auto_shoot_mode else "🔫 OFF")
        status_vars["recoil_comp"].set("↗️ ON" if settings.recoil_compensation_enabled else "↗️ OFF")
        status_vars["instant_snap"].set("⚡ ON" if settings.instant_snap_mode else "⚡ OFF")


def update_settings_from_gui():
    """Обновление настроек из GUI"""
    if gui_vars:
        # Обновляем настройки аима
        settings.smoothing_factor = gui_vars["smoothing_factor"].get()
        settings.snap_sensitivity = gui_vars["snap_sensitivity"].get()
        settings.center_bias_x = gui_vars["center_bias_x"].get()
        settings.center_bias_y = gui_vars["center_bias_y"].get()

        # Обновляем настройки отдачи
        settings.recoil_vertical = gui_vars["recoil_vertical"].get()
        settings.recoil_horizontal = gui_vars["recoil_horizontal"].get()

        # Обновляем настройки детекции
        settings.min_area = int(gui_vars["min_area"].get())
        settings.fill_strength = gui_vars["fill_strength"].get()
        settings.pixel_expansion = gui_vars["pixel_expansion"].get()
        settings.contour_fill_aggressive = gui_vars["contour_fill_aggressive"].get()

        # Обновляем зону захвата
        settings.capture_zone_size = gui_vars["capture_zone_size"].get()
        settings.update_capture_zone()

        # Обновляем радиусы
        settings.radius_settings["auto_shoot_horizontal_radius"] = int(gui_vars["shoot_h_radius"].get())
        settings.radius_settings["auto_shoot_vertical_radius"] = int(gui_vars["shoot_v_radius"].get())
        settings.radius_settings["auto_aim_horizontal_radius"] = int(gui_vars["aim_h_radius"].get())
        settings.radius_settings["auto_aim_vertical_radius"] = int(gui_vars["aim_v_radius"].get())

        settings.shoot_delay = int(gui_vars["shoot_delay"].get())


def toggle_auto_aim():
    settings.auto_aim_mode = not settings.auto_aim_mode
    print(f"🎯 Auto-aim mode {'enabled' if settings.auto_aim_mode else 'disabled'}")
    update_gui_status()


def toggle_auto_shoot():
    settings.auto_shoot_mode = not settings.auto_shoot_mode
    print(f"🔫 Auto-shoot mode {'enabled' if settings.auto_shoot_mode else 'disabled'}")
    update_gui_status()


def toggle_recoil_compensation():
    settings.recoil_compensation_enabled = not settings.recoil_compensation_enabled
    print(f"↗️ Recoil compensation {'enabled' if settings.recoil_compensation_enabled else 'disabled'}")
    update_gui_status()


def toggle_instant_snap_mode():
    settings.instant_snap_mode = not settings.instant_snap_mode
    print(f"⚡ Instant snap mode {'enabled' if settings.instant_snap_mode else 'disabled'}")
    update_gui_status()


def save_all_settings():
    """Сохранение всех настроек"""
    update_settings_from_gui()
    settings.save_settings()
    print("💾 Настройки сохранены!")


def reset_to_defaults():
    """Сброс к настройкам по умолчанию"""
    from config import DEFAULT_SETTINGS, DEFAULT_RADIUS_SETTINGS

    for key, value in DEFAULT_SETTINGS.items():
        setattr(settings, key, value)

    settings.radius_settings.update(DEFAULT_RADIUS_SETTINGS)
    update_gui_from_settings()
    print("🔄 Настройки сброшены к значениям по умолчанию!")


def update_gui_from_settings():
    """Обновление GUI из настроек"""
    if gui_vars:
        gui_vars["smoothing_factor"].set(settings.smoothing_factor)
        gui_vars["snap_sensitivity"].set(settings.snap_sensitivity)
        gui_vars["center_bias_x"].set(settings.center_bias_x)
        gui_vars["center_bias_y"].set(settings.center_bias_y)

        gui_vars["recoil_vertical"].set(settings.recoil_vertical)
        gui_vars["recoil_horizontal"].set(settings.recoil_horizontal)

        gui_vars["min_area"].set(settings.min_area)
        gui_vars["fill_strength"].set(settings.fill_strength)
        gui_vars["pixel_expansion"].set(settings.pixel_expansion)
        gui_vars["contour_fill_aggressive"].set(settings.contour_fill_aggressive)

        gui_vars["capture_zone_size"].set(settings.capture_zone_size)

        gui_vars["shoot_h_radius"].set(settings.radius_settings["auto_shoot_horizontal_radius"])
        gui_vars["shoot_v_radius"].set(settings.radius_settings["auto_shoot_vertical_radius"])
        gui_vars["aim_h_radius"].set(settings.radius_settings["auto_aim_horizontal_radius"])
        gui_vars["aim_v_radius"].set(settings.radius_settings["auto_aim_vertical_radius"])

        gui_vars["shoot_delay"].set(settings.shoot_delay)


def create_enhanced_interface():
    """Создание интерфейса с вкладками"""
    global status_vars, gui_vars

    gui_root = tk.Tk()
    gui_root.title(f"⚡ Enhanced ⚡")
    gui_root.geometry("800x700")
    gui_root.configure(bg='#1a1a1a')
    gui_root.resizable(True, True)

    # Настройка стилей
    style = ttk.Style()
    style.theme_use('clam')

    # Темные стили
    style.configure('Dark.TNotebook', background='#2d2d2d', foreground='#ffffff')
    style.configure('Dark.TNotebook.Tab', background='#404040', foreground='#ffffff', padding=[10, 4])
    style.map('Dark.TNotebook.Tab', background=[('selected', '#00ff88'), ('active', '#555555')])

    style.configure('Dark.TLabelframe', background='#2d2d2d', foreground='#ffffff')
    style.configure('Dark.TLabelframe.Label', background='#2d2d2d', foreground='#00ff88')
    style.configure('Dark.TLabel', background='#2d2d2d', foreground='#ffffff')
    style.configure('Dark.TButton', background='#404040', foreground='#ffffff')
    style.map('Dark.TButton', background=[('active', '#555555')])

    # ВАЖНО: Инициализация переменных GUI ДО создания вкладок
    init_gui_vars()

    # Заголовок
    title_frame = tk.Frame(gui_root, bg='#1a1a1a')
    title_frame.pack(pady=10, fill='x')

    tk.Label(title_frame, text="⚡ Enhanced ⚡",
             font=("Arial", 18, "bold"), fg="#ff0066", bg='#1a1a1a').pack()
    tk.Label(title_frame, text="VISION ZONE",
             font=("Arial", 12, "bold"), fg="#00ff88", bg='#1a1a1a').pack()
    tk.Label(title_frame, text=f"Resolution: {SCREEN_WIDTH}x{SCREEN_HEIGHT} | FPS: {TARGET_FPS}",
             font=("Arial", 9), fg="#888888", bg='#1a1a1a').pack()

    # Создание вкладок (теперь gui_vars уже инициализирован)
    notebook = ttk.Notebook(gui_root, style='Dark.TNotebook')
    notebook.pack(fill='both', expand=True, padx=10, pady=5)

    # Вкладка 1: Главная / Статус
    tab_main = create_main_tab(notebook)
    notebook.add(tab_main, text="📊 Главная")

    # Вкладка 2: Настройки аима
    tab_aim = create_aim_tab(notebook)
    notebook.add(tab_aim, text="🎯 Аим")

    # Вкладка 3: Настройки отдачи
    tab_recoil = create_recoil_tab(notebook)
    notebook.add(tab_recoil, text="↗️ Отдача")

    # Вкладка 4: Детекция
    tab_detection = create_detection_tab(notebook)
    notebook.add(tab_detection, text="👁️ Детекция")

    # Вкладка 5: Зона видимости
    tab_vision = create_vision_tab(notebook)
    notebook.add(tab_vision, text="📹 Зона")

    # Вкладка 6: Горячие клавиши
    tab_hotkeys = create_hotkeys_tab(notebook)
    notebook.add(tab_hotkeys, text="⌨️ Клавиши")

    # Нижняя панель с кнопками
    bottom_frame = tk.Frame(gui_root, bg='#1a1a1a')
    bottom_frame.pack(fill='x', padx=10, pady=5)

    button_frame = tk.Frame(bottom_frame, bg='#1a1a1a')
    button_frame.pack(side='right')

    ttk.Button(button_frame, text="💾 Сохранить", command=save_all_settings,
               style='Dark.TButton').pack(side='left', padx=5)
    ttk.Button(button_frame, text="🔄 Сброс", command=reset_to_defaults,
               style='Dark.TButton').pack(side='left', padx=5)
    ttk.Button(button_frame, text="❌ Выход", command=gui_root.quit,
               style='Dark.TButton').pack(side='left', padx=5)

    # Обновление GUI значениями (после инициализации)
    update_gui_from_settings()
    update_gui_status()

    def on_closing():
        settings.running = False
        gui_root.quit()
        gui_root.destroy()

    gui_root.protocol("WM_DELETE_WINDOW", on_closing)
    gui_root.mainloop()


def init_gui_vars():
    """Инициализация переменных GUI"""
    global gui_vars

    # Загружаем настройки из settings перед инициализацией
    settings.load_settings()

    gui_vars = {
        "smoothing_factor": DoubleVar(value=settings.smoothing_factor),
        "snap_sensitivity": DoubleVar(value=settings.snap_sensitivity),
        "center_bias_x": DoubleVar(value=settings.center_bias_x),
        "center_bias_y": DoubleVar(value=settings.center_bias_y),

        "recoil_vertical": DoubleVar(value=settings.recoil_vertical),
        "recoil_horizontal": DoubleVar(value=settings.recoil_horizontal),

        "min_area": IntVar(value=settings.min_area),
        "fill_strength": DoubleVar(value=settings.fill_strength),
        "pixel_expansion": DoubleVar(value=settings.pixel_expansion),
        "contour_fill_aggressive": DoubleVar(value=settings.contour_fill_aggressive),

        "capture_zone_size": DoubleVar(value=settings.capture_zone_size),

        "shoot_h_radius": IntVar(value=settings.radius_settings["auto_shoot_horizontal_radius"]),
        "shoot_v_radius": IntVar(value=settings.radius_settings["auto_shoot_vertical_radius"]),
        "aim_h_radius": IntVar(value=settings.radius_settings["auto_aim_horizontal_radius"]),
        "aim_v_radius": IntVar(value=settings.radius_settings["auto_aim_vertical_radius"]),

        "shoot_delay": IntVar(value=settings.shoot_delay)
    }

    print("✅ GUI переменные инициализированы:", list(gui_vars.keys()))


def create_main_tab(notebook):
    """Создание главной вкладки со статусом"""
    global status_vars

    tab = tk.Frame(notebook, bg='#2d2d2d')

    # Статусная панель
    status_frame = ttk.LabelFrame(tab, text="📊 Статус системы",
                                  style='Dark.TLabelframe', padding=15)
    status_frame.pack(fill='x', padx=10, pady=10)

    status_vars["auto_aim"] = StringVar(value="🎯 OFF")
    status_vars["auto_shoot"] = StringVar(value="🔫 OFF")
    status_vars["recoil_comp"] = StringVar(value="↗️ OFF")
    status_vars["instant_snap"] = StringVar(value="⚡ OFF")

    status_grid = tk.Frame(status_frame, bg='#2d2d2d')
    status_grid.pack(fill='x')

    # Строка 1
    tk.Label(status_grid, textvariable=status_vars["auto_aim"], font=("Arial", 11, "bold"),
             fg="#00ff88", bg='#404040', relief='raised', padx=10, pady=5).grid(row=0, column=0, padx=5, pady=5,
                                                                                sticky='ew')
    tk.Label(status_grid, textvariable=status_vars["auto_shoot"], font=("Arial", 11, "bold"),
             fg="#00ff88", bg='#404040', relief='raised', padx=10, pady=5).grid(row=0, column=1, padx=5, pady=5,
                                                                                sticky='ew')

    # Строка 2
    tk.Label(status_grid, textvariable=status_vars["recoil_comp"], font=("Arial", 11, "bold"),
             fg="#00ff88", bg='#404040', relief='raised', padx=10, pady=5).grid(row=1, column=0, padx=5, pady=5,
                                                                                sticky='ew')
    tk.Label(status_grid, textvariable=status_vars["instant_snap"], font=("Arial", 11, "bold"),
             fg="#00ff88", bg='#404040', relief='raised', padx=10, pady=5).grid(row=1, column=1, padx=5, pady=5,
                                                                                sticky='ew')

    status_grid.columnconfigure(0, weight=1)
    status_grid.columnconfigure(1, weight=1)

    # Кнопки управления
    control_frame = ttk.LabelFrame(tab, text="🎮 Управление",
                                   style='Dark.TLabelframe', padding=15)
    control_frame.pack(fill='x', padx=10, pady=10)

    buttons_grid = tk.Frame(control_frame, bg='#2d2d2d')
    buttons_grid.pack(fill='x')

    ttk.Button(buttons_grid, text="🎯 Переключить аим", command=toggle_auto_aim,
               style='Dark.TButton').grid(row=0, column=0, padx=5, pady=5, sticky='ew')
    ttk.Button(buttons_grid, text="🔫 Переключить стрельбу", command=toggle_auto_shoot,
               style='Dark.TButton').grid(row=0, column=1, padx=5, pady=5, sticky='ew')

    ttk.Button(buttons_grid, text="↗️ Переключить отдачу", command=toggle_recoil_compensation,
               style='Dark.TButton').grid(row=1, column=0, padx=5, pady=5, sticky='ew')
    ttk.Button(buttons_grid, text="⚡ Переключить снап", command=toggle_instant_snap_mode,
               style='Dark.TButton').grid(row=1, column=1, padx=5, pady=5, sticky='ew')

    buttons_grid.columnconfigure(0, weight=1)
    buttons_grid.columnconfigure(1, weight=1)

    # Информация о системе
    info_frame = ttk.LabelFrame(tab, text="ℹ️ Информация о системе",
                                style='Dark.TLabelframe', padding=15)
    info_frame.pack(fill='both', expand=True, padx=10, pady=10)

    info_text = tk.Text(info_frame, bg='#1a1a1a', fg='#ffffff', font=("Consolas", 9),
                        wrap=tk.WORD, height=10)
    info_text.pack(fill='both', expand=True)

    system_info = f"""
🖥️ Разрешение экрана: {SCREEN_WIDTH} x {SCREEN_HEIGHT}
🎮 Целевой FPS: {TARGET_FPS}
📹 Текущая зона захвата: {settings.capture_zone_width} x {settings.capture_zone_height}
🎯 Центр прицела: ({SCREEN_WIDTH // 2}, {SCREEN_HEIGHT // 2})

⌨️ Горячие клавиши по умолчанию:
• 0 - Переключить авто-аим
• 8 - Переключить авто-стрельбу  
• 9 - Переключить компенсацию отдачи
• + - Увеличить силу отдачи
• - - Уменьшить силу отдачи

🎯 Описание функций:
• Auto-Aim: Автоматическое наведение на цели
• Auto-Shoot: Автоматическая стрельба при наведении
• Recoil Compensation: Компенсация отдачи оружия
• Instant Snap: Мгновенное наведение на цель

💡 Для лучшей работы системы настройте параметры в соответствующих вкладках.
    """

    info_text.insert(tk.END, system_info)
    info_text.config(state=tk.DISABLED)

    return tab


def create_aim_tab(notebook):
    """Создание вкладки настроек аима"""
    tab = tk.Frame(notebook, bg='#2d2d2d')

    # Основные настройки аима
    main_frame = ttk.LabelFrame(tab, text="🎯 Основные настройки аима",
                                style='Dark.TLabelframe', padding=15)
    main_frame.pack(fill='x', padx=10, pady=10)

    # Сглаживание - ИСПРАВЛЕНО: используем ttk.Label вместо tk.Label
    ttk.Label(main_frame, text="Сглаживание (0.1-1.0):", style='Dark.TLabel').grid(row=0, column=0, sticky='w', padx=5,
                                                                                   pady=5)
    ttk.Scale(main_frame, from_=0.1, to=1.0, variable=gui_vars["smoothing_factor"],
              orient='horizontal', length=200, command=lambda v: update_settings_from_gui()).grid(row=0, column=1,
                                                                                                  padx=5, pady=5)
    ttk.Label(main_frame, textvariable=gui_vars["smoothing_factor"], style='Dark.TLabel').grid(row=0, column=2, padx=5,
                                                                                               pady=5)

    # Чувствительность снапа
    ttk.Label(main_frame, text="Чувствительность снапа (0.1-2.0):", style='Dark.TLabel').grid(row=1, column=0,
                                                                                              sticky='w', padx=5,
                                                                                              pady=5)
    ttk.Scale(main_frame, from_=0.1, to=2.0, variable=gui_vars["snap_sensitivity"],
              orient='horizontal', length=200, command=lambda v: update_settings_from_gui()).grid(row=1, column=1,
                                                                                                  padx=5, pady=5)
    ttk.Label(main_frame, textvariable=gui_vars["snap_sensitivity"], style='Dark.TLabel').grid(row=1, column=2, padx=5,
                                                                                               pady=5)

    # Калибровка центра
    calib_frame = ttk.LabelFrame(tab, text="🎯 Калибровка центра",
                                 style='Dark.TLabelframe', padding=15)
    calib_frame.pack(fill='x', padx=10, pady=10)

    # Смещение по X
    ttk.Label(calib_frame, text="Смещение по X (-50 до 50):", style='Dark.TLabel').grid(row=0, column=0, sticky='w',
                                                                                        padx=5, pady=5)
    ttk.Scale(calib_frame, from_=-50, to=50, variable=gui_vars["center_bias_x"],
              orient='horizontal', length=200, command=lambda v: update_settings_from_gui()).grid(row=0, column=1,
                                                                                                  padx=5, pady=5)
    ttk.Label(calib_frame, textvariable=gui_vars["center_bias_x"], style='Dark.TLabel').grid(row=0, column=2, padx=5,
                                                                                             pady=5)

    # Смещение по Y
    ttk.Label(calib_frame, text="Смещение по Y (-50 до 50):", style='Dark.TLabel').grid(row=1, column=0, sticky='w',
                                                                                        padx=5, pady=5)
    ttk.Scale(calib_frame, from_=-50, to=50, variable=gui_vars["center_bias_y"],
              orient='horizontal', length=200, command=lambda v: update_settings_from_gui()).grid(row=1, column=1,
                                                                                                  padx=5, pady=5)
    ttk.Label(calib_frame, textvariable=gui_vars["center_bias_y"], style='Dark.TLabel').grid(row=1, column=2, padx=5,
                                                                                             pady=5)

    # Радиусы аима
    radius_frame = ttk.LabelFrame(tab, text="📐 Радиусы аима",
                                  style='Dark.TLabelframe', padding=15)
    radius_frame.pack(fill='x', padx=10, pady=10)

    # Горизонтальный радиус аима
    ttk.Label(radius_frame, text="Горизонтальный радиус аима:", style='Dark.TLabel').grid(row=0, column=0, sticky='w',
                                                                                          padx=5, pady=5)
    ttk.Scale(radius_frame, from_=50, to=800, variable=gui_vars["aim_h_radius"],
              orient='horizontal', length=200, command=lambda v: update_settings_from_gui()).grid(row=0, column=1,
                                                                                                  padx=5, pady=5)
    ttk.Label(radius_frame, textvariable=gui_vars["aim_h_radius"], style='Dark.TLabel').grid(row=0, column=2, padx=5,
                                                                                             pady=5)

    # Вертикальный радиус аима
    ttk.Label(radius_frame, text="Вертикальный радиус аима:", style='Dark.TLabel').grid(row=1, column=0, sticky='w',
                                                                                        padx=5, pady=5)
    ttk.Scale(radius_frame, from_=50, to=800, variable=gui_vars["aim_v_radius"],
              orient='horizontal', length=200, command=lambda v: update_settings_from_gui()).grid(row=1, column=1,
                                                                                                  padx=5, pady=5)
    ttk.Label(radius_frame, textvariable=gui_vars["aim_v_radius"], style='Dark.TLabel').grid(row=1, column=2, padx=5,
                                                                                             pady=5)

    return tab


def create_recoil_tab(notebook):
    """Создание вкладки настроек отдачи"""
    tab = tk.Frame(notebook, bg='#2d2d2d')

    # Основные настройки отдачи
    recoil_frame = ttk.LabelFrame(tab, text="↗️ Настройки компенсации отдачи",
                                  style='Dark.TLabelframe', padding=15)
    recoil_frame.pack(fill='x', padx=10, pady=10)

    # Вертикальная отдача
    ttk.Label(recoil_frame, text="Вертикальная отдача (-2.0 до 2.0):", style='Dark.TLabel').grid(row=0, column=0,
                                                                                                 sticky='w', padx=5,
                                                                                                 pady=5)
    ttk.Scale(recoil_frame, from_=-2.0, to=2.0, variable=gui_vars["recoil_vertical"],
              orient='horizontal', length=200, command=lambda v: update_settings_from_gui()).grid(row=0, column=1,
                                                                                                  padx=5, pady=5)
    ttk.Label(recoil_frame, textvariable=gui_vars["recoil_vertical"], style='Dark.TLabel').grid(row=0, column=2, padx=5,
                                                                                                pady=5)

    # Горизонтальная отдача
    ttk.Label(recoil_frame, text="Горизонтальная отдача (-2.0 до 2.0):", style='Dark.TLabel').grid(row=1, column=0,
                                                                                                   sticky='w', padx=5,
                                                                                                   pady=5)
    ttk.Scale(recoil_frame, from_=-2.0, to=2.0, variable=gui_vars["recoil_horizontal"],
              orient='horizontal', length=200, command=lambda v: update_settings_from_gui()).grid(row=1, column=1,
                                                                                                  padx=5, pady=5)
    ttk.Label(recoil_frame, textvariable=gui_vars["recoil_horizontal"], style='Dark.TLabel').grid(row=1, column=2,
                                                                                                  padx=5, pady=5)

    # Настройки стрельбы
    shoot_frame = ttk.LabelFrame(tab, text="🔫 Настройки стрельбы",
                                 style='Dark.TLabelframe', padding=15)
    shoot_frame.pack(fill='x', padx=10, pady=10)

    # Задержка стрельбы
    ttk.Label(shoot_frame, text="Задержка стрельбы (мс):", style='Dark.TLabel').grid(row=0, column=0, sticky='w',
                                                                                     padx=5, pady=5)
    ttk.Scale(shoot_frame, from_=0, to=100, variable=gui_vars["shoot_delay"],
              orient='horizontal', length=200, command=lambda v: update_settings_from_gui()).grid(row=0, column=1,
                                                                                                  padx=5, pady=5)
    ttk.Label(shoot_frame, textvariable=gui_vars["shoot_delay"], style='Dark.TLabel').grid(row=0, column=2, padx=5,
                                                                                           pady=5)

    # Радиусы стрельбы
    ttk.Label(shoot_frame, text="Горизонтальный радиус стрельбы:", style='Dark.TLabel').grid(row=1, column=0,
                                                                                             sticky='w', padx=5, pady=5)
    ttk.Scale(shoot_frame, from_=5, to=100, variable=gui_vars["shoot_h_radius"],
              orient='horizontal', length=200, command=lambda v: update_settings_from_gui()).grid(row=1, column=1,
                                                                                                  padx=5, pady=5)
    ttk.Label(shoot_frame, textvariable=gui_vars["shoot_h_radius"], style='Dark.TLabel').grid(row=1, column=2, padx=5,
                                                                                              pady=5)

    ttk.Label(shoot_frame, text="Вертикальный радиус стрельбы:", style='Dark.TLabel').grid(row=2, column=0, sticky='w',
                                                                                           padx=5, pady=5)
    ttk.Scale(shoot_frame, from_=5, to=100, variable=gui_vars["shoot_v_radius"],
              orient='horizontal', length=200, command=lambda v: update_settings_from_gui()).grid(row=2, column=1,
                                                                                                  padx=5, pady=5)
    ttk.Label(shoot_frame, textvariable=gui_vars["shoot_v_radius"], style='Dark.TLabel').grid(row=2, column=2, padx=5,
                                                                                              pady=5)

    # Информация о отдаче
    info_frame = ttk.LabelFrame(tab, text="ℹ️ Информация",
                                style='Dark.TLabelframe', padding=15)
    info_frame.pack(fill='both', expand=True, padx=10, pady=10)

    info_text = tk.Text(info_frame, bg='#1a1a1a', fg='#ffffff', font=("Consolas", 9),
                        wrap=tk.WORD, height=8)
    info_text.pack(fill='both', expand=True)

    recoil_info = """
↗️ Настройка компенсации отдачи:

• Вертикальная отдача: Положительные значения компенсируют подъем ствола вверх
• Горизонтальная отдача: Отрицательные значения компенсируют уход влево, положительные - вправо
• Задержка стрельбы: Пауза между выстрелами в миллисекундах
• Радиусы стрельбы: Зона вокруг прицела, в которой активируется автострельба

💡 Советы:
- Начните с малых значений и постепенно увеличивайте
- Тестируйте настройки на разном оружии
- Для точной стрельбы уменьшите радиусы стрельбы
    """

    info_text.insert(tk.END, recoil_info)
    info_text.config(state=tk.DISABLED)

    return tab


def create_detection_tab(notebook):
    """Создание вкладки настроек детекции"""
    tab = tk.Frame(notebook, bg='#2d2d2d')

    # Основные настройки детекции
    detection_frame = ttk.LabelFrame(tab, text="👁️ Основные настройки детекции",
                                     style='Dark.TLabelframe', padding=15)
    detection_frame.pack(fill='x', padx=10, pady=10)

    # Минимальная область
    ttk.Label(detection_frame, text="Минимальная область цели:", style='Dark.TLabel').grid(row=0, column=0, sticky='w',
                                                                                           padx=5, pady=5)
    ttk.Scale(detection_frame, from_=100, to=5000, variable=gui_vars["min_area"],
              orient='horizontal', length=200, command=lambda v: update_settings_from_gui()).grid(row=0, column=1,
                                                                                                  padx=5, pady=5)
    ttk.Label(detection_frame, textvariable=gui_vars["min_area"], style='Dark.TLabel').grid(row=0, column=2, padx=5,
                                                                                            pady=5)

    # Сила заливки
    ttk.Label(detection_frame, text="Сила заливки (0.1-2.0):", style='Dark.TLabel').grid(row=1, column=0, sticky='w',
                                                                                         padx=5, pady=5)
    ttk.Scale(detection_frame, from_=0.1, to=2.0, variable=gui_vars["fill_strength"],
              orient='horizontal', length=200, command=lambda v: update_settings_from_gui()).grid(row=1, column=1,
                                                                                                  padx=5, pady=5)
    ttk.Label(detection_frame, textvariable=gui_vars["fill_strength"], style='Dark.TLabel').grid(row=1, column=2,
                                                                                                 padx=5, pady=5)

    # Расширение пикселей
    ttk.Label(detection_frame, text="Расширение пикселей (0.5-3.0):", style='Dark.TLabel').grid(row=2, column=0,
                                                                                                sticky='w', padx=5,
                                                                                                pady=5)
    ttk.Scale(detection_frame, from_=0.5, to=3.0, variable=gui_vars["pixel_expansion"],
              orient='horizontal', length=200, command=lambda v: update_settings_from_gui()).grid(row=2, column=1,
                                                                                                  padx=5, pady=5)
    ttk.Label(detection_frame, textvariable=gui_vars["pixel_expansion"], style='Dark.TLabel').grid(row=2, column=2,
                                                                                                   padx=5, pady=5)

    # Агрессивность заливки контуров
    ttk.Label(detection_frame, text="Агрессивность заливки (0.5-3.0):", style='Dark.TLabel').grid(row=3, column=0,
                                                                                                  sticky='w', padx=5,
                                                                                                  pady=5)
    ttk.Scale(detection_frame, from_=0.5, to=3.0, variable=gui_vars["contour_fill_aggressive"],
              orient='horizontal', length=200, command=lambda v: update_settings_from_gui()).grid(row=3, column=1,
                                                                                                  padx=5, pady=5)
    ttk.Label(detection_frame, textvariable=gui_vars["contour_fill_aggressive"], style='Dark.TLabel').grid(row=3,
                                                                                                           column=2,
                                                                                                           padx=5,
                                                                                                           pady=5)

    return tab


def create_vision_tab(notebook):
    """Создание вкладки настроек зоны видимости"""
    tab = tk.Frame(notebook, bg='#2d2d2d')

    # Настройки зоны захвата
    vision_frame = ttk.LabelFrame(tab, text="📹 Зона захвата",
                                  style='Dark.TLabelframe', padding=15)
    vision_frame.pack(fill='x', padx=10, pady=10)

    # Размер зоны захвата
    ttk.Label(vision_frame, text="Размер зоны захвата (%):", style='Dark.TLabel').grid(row=0, column=0, sticky='w',
                                                                                       padx=5, pady=5)
    ttk.Scale(vision_frame, from_=10, to=100, variable=gui_vars["capture_zone_size"],
              orient='horizontal', length=200, command=lambda v: update_settings_from_gui()).grid(row=0, column=1,
                                                                                                  padx=5, pady=5)
    ttk.Label(vision_frame, textvariable=gui_vars["capture_zone_size"], style='Dark.TLabel').grid(row=0, column=2,
                                                                                                  padx=5, pady=5)

    # Информация о зоне
    info_frame = ttk.LabelFrame(tab, text="ℹ️ Информация о зоне видимости",
                                style='Dark.TLabelframe', padding=15)
    info_frame.pack(fill='both', expand=True, padx=10, pady=10)

    info_text = tk.Text(info_frame, bg='#1a1a1a', fg='#ffffff', font=("Consolas", 9),
                        wrap=tk.WORD, height=8)
    info_text.pack(fill='both', expand=True)

    vision_info = f"""
📹 Настройка зоны видимости:

🖥️ Полное разрешение экрана: {SCREEN_WIDTH} x {SCREEN_HEIGHT}
📹 Текущая зона захвата: {settings.capture_zone_width} x {settings.capture_zone_height}
📍 Смещение зоны: ({settings.capture_offset_x}, {settings.capture_offset_y})

• Размер зоны захвата определяет область экрана для анализа
• Меньшая зона = лучшая производительность
• Большая зона = больший охват целей
• Зона всегда центрируется на экране

💡 Рекомендации:
- Для быстрых игр: 50-70%
- Для точной стрельбы: 30-50%
- Для дальних дистанций: 80-100%
    """

    info_text.insert(tk.END, vision_info)
    info_text.config(state=tk.DISABLED)

    return tab


def create_hotkeys_tab(notebook: ttk.Notebook) -> tk.Frame:
    """
    Вкладка «Горячие клавиши»:
    • показывает текущие бинды
    • позволяет их изменить и сохранить
    """
    tab = tk.Frame(notebook, bg='#2d2d2d')

    # --- таблица биндов ----------------------------------------------------
    hotkeys_frame = ttk.LabelFrame(
        tab, text="⌨️ Горячие клавиши",
        style='Dark.TLabelframe', padding=15
    )
    hotkeys_frame.pack(fill='x', padx=10, pady=10)

    hotkeys_grid = tk.Frame(hotkeys_frame, bg='#2d2d2d')
    hotkeys_grid.pack(fill='x')

    # Заголовки
    ttk.Label(
        hotkeys_grid, text="Функция",
        style='Dark.TLabel', font=("Arial", 10, "bold")
    ).grid(row=0, column=0, padx=5, pady=5, sticky='w')

    ttk.Label(
        hotkeys_grid, text="Клавиша",
        style='Dark.TLabel', font=("Arial", 10, "bold")
    ).grid(row=0, column=1, padx=5, pady=5, sticky='w')

    # Доступные действия и описания
    hotkey_descriptions = {
        "toggle_auto_aim": "Переключить авто-аим",
        "toggle_auto_shoot": "Переключить авто-стрельбу",
        "toggle_recoil_compensation": "Переключить компенсацию отдачи",
        "increase_recoil_strength": "Увеличить силу отдачи",
        "decrease_recoil_strength": "Уменьшить силу отдачи",
    }

    # Динамически создаём строки
    entry_vars = {}     # для последующего сохранения
    row = 1
    for action, description in hotkey_descriptions.items():
        # Описание функции
        ttk.Label(
            hotkeys_grid, text=description,
            style='Dark.TLabel'
        ).grid(row=row, column=0, padx=5, pady=2, sticky='w')

        # Поле ввода клавиши
        var = tk.StringVar(value=settings.key_bindings.get(action, ""))
        entry = ttk.Entry(
            hotkeys_grid, textvariable=var,
            width=10, justify='center'
        )
        entry.grid(row=row, column=1, padx=5, pady=2, sticky='w')
        entry_vars[action] = var
        row += 1

    hotkeys_grid.columnconfigure(0, weight=1)

    # --- информационный блок ----------------------------------------------
    info_frame = ttk.LabelFrame(
        tab, text="ℹ️ Информация о горячих клавишах",
        style='Dark.TLabelframe', padding=15
    )
    info_frame.pack(fill='both', expand=True, padx=10, pady=10)

    info_text = tk.Text(
        info_frame, bg='#1a1a1a', fg='#ffffff',
        font=("Consolas", 9), wrap=tk.WORD, height=8
    )
    info_text.pack(fill='both', expand=True)

    info_text.insert(tk.END, """
⌨️  Как изменить клавишу:
  • щёлкните по полю, введите новую кнопку (символ или Key.*)
  • нажмите Enter → изменения сразу сохранятся

💾  Сохранение:
  • изменения записываются в settings.key_bindings
  • нажмите «Сохранить» в нижней панели для записи в файл
""")
    info_text.config(state=tk.DISABLED)

    # --- колбэк для мгновенного применения ---------------------------------
    def on_entry_validate(event=None):
        for act, var in entry_vars.items():
            settings.key_bindings[act] = var.get().strip()
        print("🔑 Горячие клавиши обновлены:", settings.key_bindings)

    # Привязываем Enter к каждому полю
    for child in hotkeys_grid.winfo_children():
        if isinstance(child, ttk.Entry):
            child.bind("<Return>", on_entry_validate)

    return tab
