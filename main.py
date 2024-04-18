from tkinter import *
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from PIL import Image, ImageTk
from io import BytesIO
from datetime import datetime
from tkinter import ttk, messagebox
import requests
import pytz
import pycountry

root = Tk()
root.geometry("900x500")
root.resizable(False,False)
root.title("Weather Report")
root.configure(bg="#16394C")
root.iconbitmap("images/favicon.ico")

# background color,text color for for all
bg_color = "#16394C"
fg_color = "white"

def Go():
    global photo, show_img,pre_img
    
    # user_agent = the username in openweather website
    city = location.get()
    geolocator = Nominatim(user_agent="No-one")
    loc = geolocator.geocode(city)
    obj = TimezoneFinder()
    result = obj.timezone_at(lng=loc.longitude, lat=loc.latitude)

    # converting the time to utc
    home = pytz.timezone(result)
    local_time = datetime.now(home)
    current_time = local_time.strftime("%I:%M %p")

    # api key for weather api(openweather)
    api_key = "Your_api_key"
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&APPID={api_key}"

    response = requests.get(weather_url)
    weather_data = response.json()

    # getting icon(img) for weather
    icon_code = weather_data['weather'][0]['icon']
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
    icon = requests.get(icon_url)

    # converting byte image and resizing(enlarging)
    image = Image.open(BytesIO(icon.content))
    photo = ImageTk.PhotoImage(image.resize((200, 200),  Image.Resampling.LANCZOS))

    # converting country code to country name
    country_code = weather_data['sys']['country']
    country = pycountry.countries.get(alpha_2=country_code)
    country = country.name


    if weather_data.get('cod') == 200:
        weather_main = weather_data['main']
        wind_info = weather_data['wind']
        weather_desc = weather_data['weather'][0]['description']
        wind['text'] = f"{wind_info['speed']} m/s"
        humid['text'] = f"{weather_main['humidity']} %"
        desc['text'] = weather_desc.title()
        press['text'] = f"{weather_main['pressure']} hPa"
        img_label = weather_data['weather'][0]['main']
        temp = (weather_main['temp'] - 32)/1.8
        temp = str("{:.2f}".format(temp))

    
        display = Label(text="Currently: "+temp+"deg",font="bold 18",bg=bg_color,fg=fg_color)
        search_info = Label(root,text=weather_data['name']+" ,"+country,font=26,bg=bg_color,fg=fg_color)

        # converting the img bg and resizing 
        bg_image = Image.new("RGB", (200, 200), bg_color)
        bg_image_resized = bg_image.resize(image.size)
        
        combined_image = Image.alpha_composite(bg_image_resized.convert("RGBA"), image.convert("RGBA"))
        combined_image_resized = combined_image.resize((200, 200), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(combined_image_resized)

        show_img = Label(root, bg=bg_color)
        show_img.place(relx=0.3, rely=0.5, anchor=CENTER)
        show_img.config(image=photo)
        show_img.image = photo
        l5 = Label(root,text=img_label+" | "+current_time ,font="14",bg=bg_color,fg=fg_color)

        # removing the display image
        pre_img.destroy()
        # placing the wigids 
        press.place(relx=0.65,rely=0.6)
        desc.place(relx=0.68,rely=0.55)
        humid.place(relx=0.65,rely=0.5)
        wind.place(relx=0.68,rely=0.45)
        l1.place(relx=0.55,rely=0.45)
        l2.place(relx=0.55,rely=0.5)
        l3.place(relx=0.55,rely=0.55)
        l4.place(relx=0.55,rely=0.6)
        l5.place(relx=0.2,rely=0.65)
        display.place(relx=0.55,rely=0.38)
        search_info.place(relx=0.42, rely=0.18)  
        
    else:
        messagebox.showerror("Error", f"City {city} not found!")

# defining the wigids
location = Entry(root,font="bold 16",relief=FLAT,border=0)
location.place(relx=0.3,rely=0.08)
location.focus_set()
search = Button(root,text="Search",command=Go,relief="raised",width=15).place(relx=0.6,rely=0.08)

image = PhotoImage(file="images/weather_bg.png")
pre_img = Label(image=image,bg=bg_color)
pre_img.place(relx=0.2,rely=0.3)

l1 = Label(root,text= "Wind Speed: ",font="bold 14",bg=bg_color,fg=fg_color)
l2 = Label(root,text= "Humidity: ",font="bold 14",bg=bg_color,fg=fg_color)
l3 = Label(root,text= "Description: ",font="bold 14",bg=bg_color,fg=fg_color)
l4 = Label(root,text= "Pressure: ",font="bold 14",bg=bg_color,fg=fg_color)

wind = Label(font="bold 14",bg=bg_color,fg=fg_color)
humid = Label(font="bold 14",bg=bg_color,fg=fg_color)
desc = Label(font="bold 14",bg=bg_color,fg=fg_color)
press = Label(font="bold 14",bg=bg_color,fg=fg_color)

# on enter run go()
root.bind('<Return>', lambda e: Go())
root.mainloop()
