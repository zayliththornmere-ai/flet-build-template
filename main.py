import flet as ft
import time

# 1. БАЗА ДАННЫХ ВОПРОСОВ
# В будущем мы можем подгружать это из твоего Excel-файла!
questions_db = [
    {
        "question": "Какой язык программирования мы учим?",
        "options": ["Java", "Python", "C++", "Pascal"],
        "correct": "Python"
    },
    {
        "question": "Что делает библиотека Pandas?",
        "options": ["Рисует 3D игры", "Взламывает Wi-Fi", "Работает с таблицами", "Пишет музыку"],
        "correct": "Работает с таблицами"
    },
    {
        "question": "Как называется 'мозг' компьютера?",
        "options": ["Видеокарта", "Жесткий диск", "Процессор", "Блок питания"],
        "correct": "Процессор"
    },
    {
        "question": "Сколько бит в одном байте?",
        "options": ["10", "8", "1024", "4"],
        "correct": "8"
    }
]

def main(page: ft.Page):
    # Настройки страницы
    page.title = "Python Quiz"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- Переменные состояния (память приложения) ---
    current_question_index = 0
    score = 0

    # --- Элементы интерфейса (Виджеты) ---
    
    # Текст вопроса
    text_question = ft.Text(
        value="", 
        size=24, 
        weight=ft.FontWeight.BOLD, 
        text_align=ft.TextAlign.CENTER
    )
    
    # Шкала прогресса
    progress_bar = ft.ProgressBar(width=300, value=0)
    
    # Контейнер для кнопок с ответами (мы будем их менять)
    options_column = ft.Column(spacing=10)
    
    # Текст результата (скрыт в начале)
    text_result = ft.Text(size=30, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN)
    
    # Кнопка перезапуска (скрыта в начале)
    btn_restart = ft.ElevatedButton("Начать заново", visible=False)

    # --- ЛОГИКА ---

    def check_answer(e):
        nonlocal current_question_index, score
        
        # e.control.text - это текст на кнопке, которую нажал пользователь
        selected_answer = e.control.text
        correct_answer = questions_db[current_question_index]["correct"]

        # Если ответ верный - красим кнопку в зеленый, иначе в красный (визуальный эффект)
        if selected_answer == correct_answer:
            score += 1
            e.control.bgcolor = ft.colors.GREEN
        else:
            e.control.bgcolor = ft.colors.RED
        
        # Обновляем страницу, чтобы показать цвет
        e.control.update()
        
        # Делаем маленькую паузу (0.5 сек), чтобы юзер увидел цвет, и идем дальше
        time.sleep(0.5) 
        
        # Переходим к следующему вопросу
        current_question_index += 1
        load_question()

    def load_question():
        # Очищаем старые кнопки
        options_column.controls.clear()
        
        # Проверяем, не закончились ли вопросы
        if current_question_index < len(questions_db):
            # Загружаем данные текущего вопроса
            q_data = questions_db[current_question_index]
            text_question.value = q_data["question"]
            
            # Обновляем прогресс бар
            progress_bar.value = (current_question_index) / len(questions_db)
            
            # Создаем кнопки для каждого варианта ответа
            for option in q_data["options"]:
                btn = ft.ElevatedButton(
                    text=option,
                    on_click=check_answer,
                    width=300,
                    height=50
                )
                options_column.controls.append(btn)
            
            # Показываем вопросы, скрываем результаты
            page.views[0].controls = [progress_bar, ft.Divider(height=20), text_question, ft.Divider(height=20), options_column]
            page.update()
            
        else:
            # Если вопросы кончились - показываем экран результата
            show_results()

    def show_results():
        page.clean() # Чистим экран полностью
        text_result.value = f"Вы набрали {score} из {len(questions_db)}!"
        
        # Логика оценки
        if score == len(questions_db):
            comment = "Ты программист! 🐍"
            img = ft.Icon(ft.icons.EMOJI_EVENTS, size=100, color=ft.colors.YELLOW)
        elif score > len(questions_db) / 2:
            comment = "Неплохо, но можно лучше."
            img = ft.Icon(ft.icons.THUMB_UP, size=100, color=ft.colors.BLUE)
        else:
            comment = "Иди учить Python!"
            img = ft.Icon(ft.icons.SENTIMENT_DISSATISFIED, size=100, color=ft.colors.RED)

        btn_restart.visible = True
        btn_restart.on_click = restart_game
        
        page.add(
            ft.Column(
                [img, text_result, ft.Text(comment), btn_restart],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

    def restart_game(e):
        nonlocal current_question_index, score
        current_question_index = 0
        score = 0
        load_question()

    # --- ЗАПУСК ---
    load_question()

ft.app(target=main)