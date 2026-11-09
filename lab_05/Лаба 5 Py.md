ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ АВТОНОМНОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ ВЫСШЕГО ОБРАЗОВАНИЯ

  
«ОМСКИЙ ГОСУДАРСТВЕННЫЙ ТЕХНИЧЕСКИЙ УНИВЕРСИТЕТ»
  
Кафедра «Автоматизация и робототехника»
  
**ОТЧЕТ**
  
**по лабораторной работе № 5**
  
**Вариант №9**
  
Выполнил:
  
студент группы УТС-251т Доронин И.П.

  
(дата, подпись)
  
Проверил:
  
Доц., к.н. Ситников Д.В

  
(дата, подпись)
  
Омск 2026
  
**Цель работы**
  
Целью данной лабораторной работы является изучение основ объектно-ориентированного программирования в языке Python, освоение принципов инкапсуляции, наследования и полиморфизма. Получение практических навыков разработки приложений с графическим интерфейсом на библиотеке Tkinter на примере моделирования вертикального движения квадрокоптера.

  
**Теоретические сведения**
  
**Классы и объекты.** Класс представляет собой описание объекта, включающее его характеристики и методы управления ими. Объект является конкретным экземпляром класса. Метод \_\_init\_\_ используется для задания начальных параметров объекта, а self обеспечивает обращение к его атрибутам и методам.

  
**Инкапсуляция.** Представляет собой принцип сокрытия внутреннего состояния объекта и предоставления доступа к нему через специальные методы и свойства. В Python для контроля изменения атрибутов применяется декоратор @property, позволяющий проверять допустимость устанавливаемых значений.

  
**Наследование.** Позволяет создавать новые классы на основе уже существующих. Класс-потомок получает атрибуты и методы родительского класса, а при необходимости может дополнять или изменять их. Для обращения к функциональности родительского класса используется super().

  
**Полиморфизм.** Обеспечивает возможность использования одинаковых методов для объектов разных классов с различной реализацией. Например, расход энергии у обычного и грузового квадрокоптера может рассчитываться по-разному.

  
**Графический интерфейс Tkinter.** Библиотека Tkinter предназначена для создания оконных приложений на Python. Она позволяет использовать кнопки, текстовые поля, индикаторы состояния и графические области Canvas. Метод mainloop() запускает основной цикл обработки событий, а after() обеспечивает периодическое обновление состояния приложения без блокировки интерфейса.

  
**Индивидуальное задание и его выполнение**
  
**Суть задания:**
  
Разработать приложение для моделирования вертикального движения квадрокоптера. Создать базовый класс Drone, содержащий параметры высоты, скорости и заряда аккумулятора, а также производный класс CargoDrone, учитывающий снижение подъёмной скорости при наличии груза.

  
Графический интерфейс должен содержать кнопки «Взлёт», «Посадка» и «Удержание», отображение квадрокоптера сбоку, шкалу высоты и индикатор заряда аккумулятора. Необходимо предусмотреть ограничение максимальной высоты с использованием свойства класса.

  
**Код выполненного задания и пояснения к нему:**
  
import tkinter as tk  
from tkinter import ttk, messagebox  
  
  
\# 1. Базовый класс квадрокоптера  
class Drone:  
*"""Модель обычного квадрокоптера."""  
  
*def \_\_init\_\_(self, max\_height=100.0):  
self.max\_height = max\_height  
self.\_height = 0.0  
self.\_battery = 100.0  
self.\_speed = 5.0  
self.mode = "Удержание"  
  
@property  
def height(self):  
return self.\_height  
  
@height.setter  
def height(self, value):  
if not 0 <= value <= self.max\_height:  
raise ValueError("Высота вне допустимого диапазона!")  
self.\_height = value  
  
@property  
def battery(self):  
return self.\_battery  
def climb\_speed(self):  
*"""Скорость подъёма."""  
*return self.\_speed  
def takeoff(self):  
self.mode = "Взлёт"  
def land(self):  
self.mode = "Посадка"  
def hold(self):  
self.mode = "Удержание"  
def step(self, dt):  
*"""Один шаг моделирования."""  
*if self.\_battery <= 0:  
self.hold()  
return  
  
if self.mode == "Взлёт":  
self.\_height += self.climb\_speed() \* dt  
  
if self.\_height >= self.max\_height:  
self.\_height = self.max\_height  
self.hold()  
elif self.mode == "Посадка":  
self.\_height -= self.\_speed \* dt  
if self.\_height <= 0:  
self.\_height = 0  
self.hold()  
  
if self.mode != "Удержание":  
self.\_battery = max(  
0, self.\_battery - 0.15 \* dt  
)  
def \_\_str\_\_(self):  
return (  
f"Высота: {self.height:.1f} м | "  
f"Заряд: {self.battery:.1f}%"  
)  
\# 2. Класс грузового квадрокоптера  
class CargoDrone(Drone):  
*"""Квадрокоптер с дополнительной нагрузкой."""  
  
*def \_\_init\_\_(self, payload=0.0, max\_height=100.0):  
super().\_\_init\_\_(max\_height)  
self.payload = payload  
  
def climb\_speed(self):

  
*"""Скорость подъёма зависит от массы груза."""  
*return max(1.0, self.\_speed / (1 + 0.1 \* self.payload))  
\# 3. Класс графического приложения  
class DroneApp(tk.Tk):  
*"""Оконное приложение управления квадрокоптером."""  
*def \_\_init\_\_(self, drone):  
super().\_\_init\_\_()  
  
self.drone = drone  
self.dt = 0.1  
  
self.title("Управление квадрокоптером")  
self.geometry("620x480")  
self.resizable(False, False)  
  
self.\_build\_widgets()  
self.\_update\_display()  
  
self.after(100, self.\_tick)  
  
def \_build\_widgets(self):  
\# Область отображения  
self.canvas = tk.Canvas(  
self, width=350, height=420, bg="white"  
)  
self.canvas.pack(side="left", padx=10, pady=10)  
  
\# Панель управления  
panel = ttk.LabelFrame(self, text="Управление")  
panel.pack(side="right", fill="y", padx=10, pady=10)  
  
self.info = tk.StringVar()  
self.status = tk.StringVar(value="Удержание")  
  
ttk.Label(panel, text="Состояние:").pack(pady=5)  
ttk.Label(  
panel, textvariable=self.status  
).pack(pady=5)  
  
ttk.Button(  
panel, text="Взлёт",

  
command=self.\_takeoff  
).pack(fill="x", pady=5)  
  
ttk.Button(  
panel, text="Посадка",

  
command=self.\_land  
).pack(fill="x", pady=5)  
  
ttk.Button(  
panel, text="Удержание",  
command=self.\_hold  
).pack(fill="x", pady=5)  
  
ttk.Button(  
panel, text="Сброс",  
command=self.\_reset  
).pack(fill="x", pady=5)  
  
ttk.Separator(panel).pack(fill="x", pady=10)  
  
ttk.Label(panel, text="Масса груза, кг:").pack()  
  
self.payload\_var = tk.DoubleVar(value=0)  
  
ttk.Scale(  
panel,  
from\_=0,  
to=20,  
variable=self.payload\_var,  
command=self.\_set\_payload  
).pack(fill="x", pady=5)  
  
self.payload\_label = ttk.Label(  
panel, text="0.0 кг"  
)  
self.payload\_label.pack()  
  
ttk.Label(  
panel, text="Заряд аккумулятора:"  
).pack(pady=(15, 5))  
  
self.bar = ttk.Progressbar(  
panel, maximum=100, length=180  
)  
self.bar.pack()  
  
ttk.Label(  
panel, textvariable=self.info,  
wraplength=200  
).pack(pady=15)  
  
def \_takeoff(self):  
if self.drone.battery > 0:  
self.drone.takeoff()  
  
def \_land(self):  
self.drone.land()  
  
def \_hold(self):  
self.drone.hold()  
  
def \_reset(self):  
self.drone.height = 0  
self.drone.\_battery = 100

  
self.drone.hold()  
self.\_update\_display()  
  
def \_set\_payload(self, value):  
try:  
self.drone.payload = float(value)  
self.payload\_label.config(  
text=f"{float(value):.1f} кг"  
)  
except ValueError:  
messagebox.showerror(  
"Ошибка", "Некорректная масса груза"  
)  
  
def \_tick(self):  
self.drone.step(self.dt)  
self.\_update\_display()  
  
if self.drone.battery <= 0:

  
self.drone.hold()  
self.status.set("Аккумулятор разряжен")  
  
self.after(100, self.\_tick)  
def \_update\_display(self):  
d = self.drone  
  
self.status.set(d.mode)  
self.info.set(

  
f"Высота: {d.height:.1f} м\\n"  
f"Скорость подъёма: {d.climb\_speed():.1f} м/с\\n"  
f"Заряд: {d.battery:.1f}%"  
)  
  
self.bar\["value"\] = d.battery  
self.canvas.delete("all")  
  
\# Земля  
self.canvas.create\_line(  
20, 370, 330, 370, width=3  
)  
  
\# Шкала высоты  
for h in range(0, 101, 10):  
y = 370 - h \* 3  
self.canvas.create\_line(  
25, y, 40, y  
)  
self.canvas.create\_text(  
15, y, text=str(h), anchor="e"  
)  
  
self.canvas.create\_text(  
80, 30, text="Высота, м"  
)  
  
\# Положение квадрокоптера  
y = 370 - d.height \* 3  
  
self.canvas.create\_oval(  
150, y - 10, 190, y + 10,  
fill="orange", outline="black"  
)  
  
self.canvas.create\_line(  
145, y - 10, 195, y - 10, width=3  
)  
self.canvas.create\_line(  
145, y + 10, 195, y + 10, width=3  
)  
  
self.canvas.create\_text(  
170, y - 25,  
text=f"{d.height:.1f} м",  
fill="blue"  
)  
  
\# 4. Запуск программы  
def main():  
drone = CargoDrone(payload=0)  
app = DroneApp(drone)  
app.mainloop()  
  
if \_\_name\_\_ == "\_\_main\_\_":  
main()

  
**Пояснение к программе:**
  
Drone — основной класс, описывающий параметры и поведение квадрокоптера.

  
CargoDrone — производный класс, учитывающий влияние массы груза на скорость подъёма и расход аккумулятора.

  
DroneApp — класс графического интерфейса, обеспечивающий управление моделью.

  
height — свойство, ограничивающее максимальную высоту полёта.

  
battery — текущий уровень заряда аккумулятора.

  
takeoff() — переводит квадрокоптер в режим взлёта.

  
land() — активирует режим посадки.

  
hold() — включает режим удержания текущей высоты.

  
step() — выполняет один шаг моделирования движения.

  
energy\_rate() — определяет скорость расходования заряда аккумулятора.

  
climb\_speed() — рассчитывает скорость подъёма с учётом массы груза.

  
after() — обеспечивает регулярное обновление модели и графического интерфейса.

  
**Описание работы программы**
  
При запуске создаётся объект класса CargoDrone с заданной массой груза, максимальной высотой и скоростью движения.

  
Открывается графическое окно, в котором отображаются квадрокоптер, шкала высоты и уровень заряда аккумулятора.

  
При нажатии кнопки «Взлёт» квадрокоптер начинает постепенно набирать высоту.

  
Кнопка «Посадка» запускает снижение до нулевой высоты.

  
Кнопка «Удержание» прекращает изменение высоты и сохраняет текущее положение.

  
Во время полёта происходит постепенное уменьшение заряда аккумулятора.

  
При достижении максимальной высоты дальнейший подъём прекращается автоматически.

  
При разряде аккумулятора модель переходит в режим посадки.

  
**Результаты работы**
  
В результате выполнения программы было создано оконное приложение для моделирования вертикального движения квадрокоптера.

  
В ходе проверки реализованы следующие сценарии:
  
Запуск квадрокоптера и набор высоты.

  
Удержание заданного положения.

  
Снижение высоты при посадке.

  
Ограничение максимальной высоты полёта.

  
Изменение скорости подъёма в зависимости от массы груза.

  
Уменьшение заряда аккумулятора во время движения.

  
![](data:image/png;base64,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) ![](data:image/png;base64,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)

  
**Заключение и вывод**
  
В ходе лабораторной работы были изучены основные принципы объектно-ориентированного программирования на языке Python: создание классов и объектов, инкапсуляция, наследование и полиморфизм.

  
Была разработана программа моделирования вертикального движения квадрокоптера с использованием библиотеки Tkinter. Созданы базовый класс Drone и производный класс CargoDrone, позволяющий учитывать влияние дополнительной нагрузки на характеристики полёта.

  
Также был реализован графический интерфейс с кнопками управления, шкалой высоты и индикатором заряда аккумулятора. В процессе выполнения работы закреплены навыки создания классов, использования свойств, переопределения методов и обработки событий в оконных приложениях.